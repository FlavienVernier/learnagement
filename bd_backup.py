# coding=utf-8
"""
Système de sauvegarde planifiée de la base de données Learnagement.

Variables d'environnement :
  BACKUP                    bool  : active le système (true/1/yes/on). Défaut : false
  BACKUP_AT                 "HH:MM" : heure de la sauvegarde quotidienne. Défaut : 00:00
  BACKUP_DIRECTORY          str   : répertoire local. Défaut : db/backup
  BACKUP_REMOTE_DIRECTORY   str   : si défini, répertoire distant monté temporairement
                                    (a priorité sur BACKUP_DIRECTORY). Formats reconnus :
                                      //serveur/partage          -> cifs (SMB)
                                      serveur:/chemin            -> nfs
                                      utilisateur@serveur:chemin -> sshfs
                                      \\\\serveur\\partage         -> Windows (net use)
  BACKUP_REMOTE_TYPE        str   : (optionnel) force cifs | nfs | sshfs
  BACKUP_REMOTE_USER        str   : (optionnel) utilisateur (cifs / Windows)
  BACKUP_REMOTE_PASSWORD    str   : (optionnel) mot de passe (cifs / Windows)
  BACKUP_REMOTE_OPTIONS     str   : (optionnel) options de montage supplémentaires (-o)
  BACKUP_REMOTE_SUDO        bool  : (optionnel, UNIX) préfixe mount/umount par `sudo -n`
  BACKUP_RETENTION_DAYS     int   : (optionnel) supprime les sauvegardes plus anciennes
"""
import asyncio
import datetime
import logging
import os
import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

import dotenv

from config import RED, GREEN, YELLOW, NC

# Racine du projet : indispensable car learnagement.py fait des os.chdir("docker")
# pendant que la tâche de sauvegarde tourne en parallèle.
ROOT = Path(__file__).resolve().parent

DEFAULT_BACKUP_DIRECTORY = os.path.join("db", "backup")
DEFAULT_BACKUP_AT = "00:00"
BACKUP_PREFIXES = ("0_struct_", "5_data_", "99_trigger_")

_backup_task: asyncio.Task | None = None


#############################################################
# Helpers

def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in ("1", "true", "yes", "y", "on", "oui")


def _parse_backup_at(value: str | None) -> datetime.time:
    value = (value or DEFAULT_BACKUP_AT).strip()
    match = re.fullmatch(r"([01]?\d|2[0-3])[:hH]([0-5]\d)", value)
    if not match:
        raise ValueError(f"BACKUP_AT invalide : '{value}' (format attendu HH:MM)")
    return datetime.time(int(match.group(1)), int(match.group(2)))


def _seconds_until(at: datetime.time) -> float:
    now = datetime.datetime.now()
    target = now.replace(hour=at.hour, minute=at.minute, second=0, microsecond=0)
    if target <= now:
        target += datetime.timedelta(days=1)
    return (target - now).total_seconds()


def _resolve(folder: str | os.PathLike) -> Path:
    path = Path(folder)
    return path if path.is_absolute() else ROOT / path


#############################################################
# Dump (ex-backupDB, refactorisé)

def _dump(target: Path, extra_args: list[str]) -> None:
    """Exécute mysqldump dans le conteneur MySQL et écrit le résultat dans `target`."""
    container = os.environ.get("MYSQL_SERVER") or "learnagement_mysql_" + os.environ["INSTANCE_NAME"]

    cmd = os.environ["DOCKER_COMMAND"].split(" ") + [
        "exec", "-i",                 # pas de -t : pas de TTY en tâche de fond
        "-e", "MYSQL_PWD",            # valeur transmise via l'env du process (pas dans la ligne de commande)
        container,
        "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"],
        *extra_args,
        "--skip-comments", "--skip-extended-insert", "--no-tablespaces",
        os.environ["MYSQL_DB"],
    ]
    env = {**os.environ, "MYSQL_PWD": os.environ["MYSQL_USER_PASSWORD"]}

    part = target.with_name(target.name + ".part")
    try:
        with open(part, "wb") as out:
            result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"mysqldump a échoué ({result.returncode}) : "
                               f"{result.stderr.decode(errors='replace').strip()}")
        os.replace(part, target)      # écriture atomique : pas de sauvegarde à moitié écrite
    finally:
        part.unlink(missing_ok=True)


def perform_backup(backup_folder: str | os.PathLike = DEFAULT_BACKUP_DIRECTORY) -> list[Path]:
    """
    Sauvegarde structure, données et triggers dans `backup_folder`.
    Utilisée par la commande CLI `backupDB` et par le système planifié.
    """
    dotenv.load_dotenv()
    folder = _resolve(backup_folder)
    folder.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    files = [
        (folder / f"0_struct_{now}.sql",
         ["--no-data", "--ignore-views", "--skip-triggers"]),
        (folder / f"5_data_{now}.sql",
         ["--no-create-info", "--ignore-views", "--skip-triggers"]),
        (folder / f"99_trigger_{now}.sql",
         ["--no-create-info", "--ignore-views", "--no-data"]),
    ]
    for target, args in files:
        _dump(target, args)

    logging.info(f"{GREEN}Backup DB done in {folder}{NC}")
    return [t for t, _ in files]


def _purge_old_backups(folder: Path) -> None:
    days = os.environ.get("BACKUP_RETENTION_DAYS", "").strip()
    if not days:
        return
    try:
        limit = datetime.datetime.now().timestamp() - int(days) * 86400
    except ValueError:
        logging.warning(f"{YELLOW}BACKUP_RETENTION_DAYS invalide : '{days}', purge ignorée{NC}")
        return
    for f in folder.glob("*.sql"):
        if f.name.startswith(BACKUP_PREFIXES) and f.stat().st_mtime < limit:
            f.unlink(missing_ok=True)
            logging.info(f"Old backup removed: {f.name}")


#############################################################
# Montage du répertoire distant

def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def _guess_remote_type(remote: str) -> str:
    forced = os.environ.get("BACKUP_REMOTE_TYPE", "").strip().lower()
    if forced:
        return forced
    if remote.startswith("//"):
        return "cifs"
    if re.match(r"^[^@/\s]+@[^:/\s]+:", remote):
        return "sshfs"
    if re.match(r"^[^/\s:]+:/", remote):
        return "nfs"
    raise ValueError(f"Format de BACKUP_REMOTE_DIRECTORY non reconnu : '{remote}' "
                     f"(utiliser BACKUP_REMOTE_TYPE pour le préciser)")


@contextmanager
def _mount_unix(remote: str):
    remote_type = _guess_remote_type(remote)
    user = os.environ.get("BACKUP_REMOTE_USER")
    password = os.environ.get("BACKUP_REMOTE_PASSWORD")
    extra_opts = os.environ.get("BACKUP_REMOTE_OPTIONS", "").strip()
    sudo = ["sudo", "-n"] if _env_bool("BACKUP_REMOTE_SUDO") and os.geteuid() != 0 else []

    mount_point = tempfile.mkdtemp(prefix="learnagement_backup_")
    cred_file = None
    mounted = False
    try:
        options = [extra_opts] if extra_opts else []
        if remote_type == "cifs":
            if user:
                # fichier de credentials (0600) : le mot de passe n'apparaît pas dans `ps`
                fd, cred_file = tempfile.mkstemp(prefix="learnagement_cred_")
                with os.fdopen(fd, "w") as f:
                    f.write(f"username={user}\npassword={password or ''}\n")
                options.insert(0, f"credentials={cred_file}")
            else:
                options.insert(0, "guest")
            cmd = sudo + ["mount", "-t", "cifs", remote, mount_point]
        elif remote_type == "nfs":
            cmd = sudo + ["mount", "-t", "nfs", remote, mount_point]
        elif remote_type == "sshfs":
            cmd = ["sshfs", remote, mount_point]
        else:
            raise ValueError(f"Type de montage non supporté : '{remote_type}'")

        if options:
            cmd += ["-o", ",".join(options)]

        result = _run(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"Montage de '{remote}' impossible : {result.stderr.strip()}")
        mounted = True
        logging.info(f"Remote directory mounted ({remote_type}) on {mount_point}")
        yield Path(mount_point)
    finally:
        if mounted:
            if remote_type == "sshfs":
                umount = ["fusermount", "-u", mount_point]
            else:
                umount = sudo + ["umount", mount_point]
            res = _run(umount)
            if res.returncode != 0:                       # démontage paresseux en dernier recours
                lazy = ["fusermount", "-uz", mount_point] if remote_type == "sshfs" \
                    else sudo + ["umount", "-l", mount_point]
                res = _run(lazy)
            if res.returncode != 0:
                logging.error(f"{RED}Démontage de {mount_point} impossible : {res.stderr.strip()}{NC}")
                mount_point = None  # ne pas tenter de supprimer un point de montage encore actif
            else:
                logging.info("Remote directory unmounted")
        if cred_file:
            Path(cred_file).unlink(missing_ok=True)
        if mount_point:
            try:
                os.rmdir(mount_point)
            except OSError:
                pass


@contextmanager
def _mount_windows(remote: str):
    """
    Windows ne monte pas un partage dans un répertoire arbitraire avec `net use` :
    on utilise une lettre de lecteur libre (équivalent du répertoire temporaire).
    """
    if not remote.startswith("\\\\"):
        raise ValueError(f"Sous Windows, BACKUP_REMOTE_DIRECTORY doit être un chemin UNC "
                         f"(\\\\serveur\\partage), reçu : '{remote}'")
    letter = next((l for l in "ZYXWVUTSRQPONMLKJIHGFED" if not os.path.exists(f"{l}:\\")), None)
    if letter is None:
        raise RuntimeError("Aucune lettre de lecteur disponible")

    cmd = ["net", "use", f"{letter}:", remote, "/persistent:no"]
    user = os.environ.get("BACKUP_REMOTE_USER")
    if user:
        cmd.insert(4, os.environ.get("BACKUP_REMOTE_PASSWORD", ""))
        cmd.insert(5, f"/user:{user}")
    result = _run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Montage de '{remote}' impossible : {result.stderr.strip()}")
    logging.info(f"Remote directory mounted on {letter}:")
    try:
        yield Path(f"{letter}:\\")
    finally:
        res = _run(["net", "use", f"{letter}:", "/delete", "/y"])
        if res.returncode != 0:
            logging.error(f"{RED}Démontage de {letter}: impossible : {res.stderr.strip()}{NC}")
        else:
            logging.info("Remote directory unmounted")


@contextmanager
def _mounted_remote(remote: str):
    with (_mount_windows(remote) if os.name == "nt" else _mount_unix(remote)) as path:
        yield path


#############################################################
# Exécution d'une sauvegarde et planification

def run_backup_once() -> None:
    """Une sauvegarde complète : distante (montée puis démontée) ou locale."""
    dotenv.load_dotenv()
    remote = os.environ.get("BACKUP_REMOTE_DIRECTORY", "").strip()

    if remote:
        with _mounted_remote(remote) as mount_path:
            perform_backup(mount_path)
            _purge_old_backups(mount_path)
    else:
        local = os.environ.get("BACKUP_DIRECTORY", "").strip() or DEFAULT_BACKUP_DIRECTORY
        perform_backup(local)
        _purge_old_backups(_resolve(local))


async def _backup_loop(at: datetime.time) -> None:
    while True:
        delay = _seconds_until(at)
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        logging.info(f"{GREEN}Next DB backup: {next_run:%Y-%m-%d %H:%M}{NC}")
        await asyncio.sleep(delay)
        try:
            # thread séparé : subprocess et montages sont bloquants
            await asyncio.to_thread(run_backup_once)
        except asyncio.CancelledError:
            raise
        except Exception as e:           # une sauvegarde ratée ne doit jamais arrêter l'application
            logging.error(f"{RED}DB backup failed: {e}{NC}")


async def __launch_bd_backup_system() -> asyncio.Task | None:
    """
    Lance (en tâche de fond) le système de sauvegarde si BACKUP est vrai.
    Retourne immédiatement : ne bloque pas le démarrage.
    """
    global _backup_task
    dotenv.load_dotenv()

    if not _env_bool("BACKUP", False):
        logging.info("DB backup system disabled (BACKUP is not set to true)")
        return None

    try:
        at = _parse_backup_at(os.environ.get("BACKUP_AT"))
    except ValueError as e:
        logging.error(f"{RED}{e} — backup system not started{NC}")
        return None

    if _backup_task is not None and not _backup_task.done():
        return _backup_task

    # référence conservée pour éviter que la tâche soit garbage-collectée
    _backup_task = asyncio.create_task(_backup_loop(at), name="learnagement-db-backup")
    logging.info(f"{GREEN}DB backup system started (every day at {at:%H:%M}){NC}")
    return _backup_task