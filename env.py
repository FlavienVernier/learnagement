import logging
import os
import re
import shutil
from getpass import getpass

import dotenv
from dotenv import dotenv_values
from tools import get_local_ip_and_hostname, __generate_secret__
from config import GREEN, YELLOW, NC, containers, container_app_dirs, envs, RED

############################
# Manage existing env files
############################

def __scan_envs(directory="."):
    # Scan all spécific environments like dev, prod (that are defaults and already in envs) and add them in envs
    # A specific environment is defined by a .env file with a name like .env_xxxxx.env (ex .env_lnm.env)
    ## Each defined variable in specific environment will replace its default value in .env
    for filename in os.listdir(directory):
        match = re.match(r'^\.env_([a-z]+)\.env$', filename)
        if match:
            envs.add(match.group(1))

def __load_env_parts(directory=".", base=None) -> dict:
    """
    Charge tous les fichiers « parts » d'environnement d'un répertoire.

    Une part d'environnement est un fichier nommé `.env.<part>` (ex. `.env.git`).
    Les parts sont des COMPLÉMENTS au fichier `.env` de base : elles ne doivent
    jamais redéfinir une clé déjà définie. Toute redéfinition (entre parts, ou
    entre une part et la base) lève une EnvConflictError.

    Args:
        directory: Répertoire où chercher les fichiers `.env.<part>`.
        base:      Dictionnaire de la base `.env` déjà chargée (clés interdites
                   de redéfinition). Si None, aucune base n'est considérée.

    Returns:
        Dictionnaire {clé: valeur} contenant l'union de toutes les parts.

    Raises:
        EnvConflictError: si une clé est définie plusieurs fois.
    """
    base = base or {}
    env_vars = {}

    # Ordre déterministe, sinon la notion d'erreur serait instable
    for filename in sorted(os.listdir(directory)):
        match = re.match(r'^\.env\.([a-z]+)$', filename)
        if not match:
            continue

        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue

        part_vars = __load_env_file(filepath)
        for key, value in part_vars.items():
            if key in base:
                raise ValueError(
                    f"La clé '{key}' définie dans '{filename}' est déjà définie dans le fichier .env de base."
                )
            if key in env_vars:
                raise ValueError(
                    f"La clé '{key}' est définie plusieurs fois dans les parts d'environnement (au moins dans '{filename}')."
                )
            env_vars[key] = value

    return env_vars

def __load_all_env(directory=".") -> dict:
    """
    Charge la base `.env` puis les parts `.env.<part>` (compléments).
    Toute redéfinition entre les deux lève une EnvConflictError.
    """
    base_env = {}
    base_path = os.path.join(directory, ".env")
    if os.path.isfile(base_path):
        base_env = __load_env_file(base_path)

    parts_env = __load_env_parts(directory, base=base_env)

    return {**base_env, **parts_env}


def __load_env_file(filepath: str) -> dict:
    """
    Lit un fichier env et retourne son contenu sous forme de dictionnaire.
    Ignore les lignes vides et les commentaires (commençant par #).

    Args:
        filepath: Chemin vers le fichier .env

    Returns:
        Dictionnaire {clé: valeur} des variables d'environnement
    """
    env_vars = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        logging.info(f"load env {filepath}")
        for line in f:
            line = line.strip()

            # Ignorer les lignes vides et les commentaires
            if not line or line.startswith('#'):
                continue

            # Séparer sur le premier '=' uniquement
            if '=' not in line:
                continue

            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()

            # Supprimer les guillemets entourants si présents
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]

            env_vars[key] = value

    return env_vars


def save_env_file(env_vars: dict, filepath: str=".env") -> None:
    """
    Sauvegarde un dictionnaire sous forme de fichier .env.

    Args:
        env_vars: Dictionnaire {clé: valeur} des variables d'environnement
        filepath: Chemin vers le fichier .env à créer/écraser
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for key, value in env_vars.items():
            # Ajouter des guillemets si la valeur contient des espaces
            if ' ' in str(value):
                f.write(f'{key}="{value}"\n')
            else:
                f.write(f'{key}={value}\n')


def __set_env(env_vars: dict, filepath: str) -> dict:
    """
    Met à jour un dictionnaire de variables d'environnement avec les valeurs
    contenues dans un fichier .env. Seules les clés déjà présentes dans le
    dictionnaire sont mises à jour.

    Args:
        env_vars: Dictionnaire de référence {clé: valeur}
        filepath: Chemin vers le fichier .env source

    Returns:
        Nouveau dictionnaire avec les valeurs mises à jour
    """
    file_vars = __load_env_file(filepath)

    return {
        key: file_vars.get(key, value)
        for key, value in env_vars.items()
    }


def __generate_base_env():
    default_env_vars = __load_env_file("__env_skeleton.env")

    # Instance

    instance_name = input("Give the intance name (lowercase): ").lower()
    default_env_vars["INSTANCE_NAME"] = instance_name
    default_env_vars["COMPOSE_PROJECT_NAME"] = f"learnagement_{instance_name}"

    default_env_vars["COMPOSE_PROJECT_NAME"] = f"learnagement_{instance_name}"


    default_env_vars["CAS_SERVICE_TOKEN"] = str(__generate_secret__( info = "CAS Generated Encryption Key").hex())
    default_env_vars["JWT_SIGNING_KEY"] = str(__generate_secret__( info = "LNM Generated Encryption Key").hex())
    default_env_vars["NEXTAUTH_SECRET"] = str(__generate_secret__( info = "NextAuth.js Generated Encryption Key").hex())
    protocol = "http"
    default_env_vars["FRONT_PHP_PROTOCOL"] = protocol

    default_env_vars["INSTANCE_PROTOCOL"] = protocol
    default_env_vars["INSTANCE_IP"], default_env_vars["INSTANCE_URL"] = get_local_ip_and_hostname()

    # MySQL
    default_env_vars["MYSQL_SERVER"] = f"learnagement_data_mysql_{instance_name}"
    default_env_vars["MYSQL_ROOT_PASSWORD"] = getpass("Give the MySQL Root password: ")
    default_env_vars["MYSQL_USER_PASSWORD"] = getpass("Give the MySQL User password: ")
    default_env_vars["LEARNAGEMENT_ADMINISTRATOR_PASSWORD"] = getpass("Give the Learnagement Administrator password: ")

    #ToDo check if passwords are different if prod env
    # ...

    # Backend
    default_env_vars["BACKEND_PYTHON_DOCKER_URL"] = f"learnagement_backend_python_{instance_name}"

    save_env_file(default_env_vars, filepath=".env.default")

    if not os.path.exists(".env_dev.env"):
        shutil.copy("__env_default_dev.env", ".env_dev.env")
    if not os.path.exists(".env_prod.env"):
        shutil.copy("__env_default_prod.env", ".env_prod.env")

    return __load_env_parts()


# def update_env_file_variable(env_file=".env", key=None, value=None):
#     if key and value:
#         with open(env_file, 'r') as f:
#             content = f.read()
#
#         updated = __update_env_variable(content, key, value)
#
#         with open(env_file, 'w') as f:
#             f.write(updated)
#
#         logging.warning(f"{YELLOW}Environment variables changed!{NC}")
#
#     # Load environment variables from the .env file
#     dotenv.load_dotenv()


def propagate_env():
    source_path = os.path.join("./", ".env")
    dotenv.load_dotenv()

    for container in containers[os.environ["ENV"]]:
        if container_app_dirs[container]:
            target_path = os.path.join(container_app_dirs[container], ".env")
            shutil.copy(source_path, target_path)
            logging.info(f"{GREEN}Copied: {source_path} -> {target_path}{NC}")

def remove_env_file():
        for container in containers[os.environ["ENV"]]:
            if container_app_dirs[container]:
                try:
                    target_path = os.path.join(container_app_dirs[container], ".env")
                    os.remove(target_path)
                except FileNotFoundError as e:
                    logging.exception(e)

        try:
            os.remove(".env")
            os.remove(".env_dev.env")
            os.remove(".env_prod.env")
        except FileNotFoundError as e:
            logging.exception(e)


def load_env(env: str | None = None):
    if not os.path.exists(".env"):

        #logging.warning(f"{YELLOW}env file doesn't exist, generate it with '{env}' environnement {NC}")
        if not env:
            env = input(f"{YELLOW}env file doesn't exist and environment not specified, give the required environment (alpha lowercase): {NC}").lower()

        env_vars = __generate_base_env()

        if not os.path.exists(f".env_{env}.env"):
            logging.error(f"{RED}Specific env file '.env_{env}.env' doesn't exist{NC}")
            exit()
        env_vars = __set_env(env_vars, f".env_{env}.env")

        save_env_file(env_vars, ".env")
    else:
        logging.info("environment already exists")
    propagate_env()
    dotenv.load_dotenv()
