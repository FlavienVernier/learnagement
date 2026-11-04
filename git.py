#!/usr/bin/env python3
"""
git.py — Récupération automatique du hash de commit Git.

Deux modes d'utilisation :

1. En ligne de commande (appelé depuis les hooks Git) :
       python git.py [--short] [--out FILE]

2. En tant que module (depuis bootstrap.py ou l'application) :
       from git_config import get_commit_hash, write_commit_file
       h = get_commit_hash()

Le fichier généré par défaut est `.commit_id`, placé à la racine du dépôt.
Il est conçu pour être lu par l'application à l'exécution (version affichée).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Fichier où le hash est écrit (à la racine du dépôt, à côté de .git)
COMMIT_FILE = ".env.git"


def _run_git(args: list[str], cwd: Path | None = None) -> str | None:
    """Exécute une commande git et retourne sa sortie stdout nettoyée, ou None si échec."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_commit_hash(
    short: bool = False,
    repo_dir: Path | None = None,
    mark_dirty: bool = True,
    dirty_suffix: str = "-DIRTY",
) -> str | None:
    """
    Retourne le hash du commit HEAD courant.

    - short=True        -> hash abrégé (git rev-parse --short HEAD)
    - mark_dirty=True   -> si la copie de travail contient des modifications
                           non commitées, un suffixe est ajouté au hash
                           (par défaut "-DIRTY").
    - Retourne None si pas de dépôt Git ou pas de commit (dépôt vide).
    """
    args = ["rev-parse", "--short", "HEAD"] if short else ["rev-parse", "HEAD"]
    commit = _run_git(args, cwd=repo_dir)
    if commit is None:
        return None

    if not mark_dirty:
        return commit

    if _is_working_tree_dirty(repo_dir):
        return commit + dirty_suffix
    return commit


def _is_working_tree_dirty(repo_dir: Path | None = None) -> bool:
    """
    Indique si la copie de travail contient des modifications non commitées :
    fichiers modifiés suivis, fichiers non suivis, ou index en cours de modification.

    Retourne False en cas d'erreur (mieux vaut un ID sans marqueur qu'un faux positif).
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return bool(result.stdout.strip())


def get_branch(repo_dir: Path | None = None) -> str | None:
    """Retourne le nom de la branche courante (utile pour l'affichage de version)."""
    return _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir)


def write_commit_file(
    path: str | Path = COMMIT_FILE,
    short: bool = False,
    repo_dir: Path | None = None,
) -> str | None:
    """Écrit le hash courant dans `path`. Retourne le hash écrit, ou None si échec."""
    commit = get_commit_hash(short=short, repo_dir=repo_dir)
    if commit is None:
        return None
    out = Path(path)
    if repo_dir is not None:
        out = Path(repo_dir) / out
    out.write_text("GIT_COMMIT=" + commit + "\n", encoding="utf-8")
    return commit


# ---------------------------------------------------------------------------
# Installation des hooks Git
# ---------------------------------------------------------------------------

HOOK_TEMPLATE = """#!/bin/sh
# Hook {hook_name} généré par git.py
# Met à jour .commit_id après {trigger}.
python "{python}" "{script}" --out "{commit_file}" {short_flag}|| true
"""

HOOKS = {
    "post-commit": "un commit",
    "post-merge": "un pull/merge",
    "post-rewrite": "un rebase/amend",
}


def _hook_path(hook_name: str, repo_dir: Path) -> Path:
    """Retourne le chemin du hook, en respectant core.hooksPath si défini."""
    custom = _run_git(["config", "--get", "core.hooksPath"], cwd=repo_dir)
    hooks_dir = Path(custom) if custom else repo_dir / ".git" / "hooks"
    if not hooks_dir.is_absolute():
        hooks_dir = repo_dir / hooks_dir
    return hooks_dir / hook_name


def install_hooks(
    repo_dir: str | Path = ".",
    short: bool = True,
    python_exe: str | None = None,
) -> list[Path]:
    """
    Installe les hooks post-commit, post-merge et post-rewrite dans le dépôt.
    Retourne la liste des fichiers de hooks écrits.
    Si le dépôt n'est pas un dépôt Git, retourne une liste vide (sans planter).
    """
    repo = Path(repo_dir).resolve()
    if _run_git(["rev-parse", "--git-dir"], cwd=repo) is None:
        return []

    py = python_exe or sys.executable
    script = Path(__file__).resolve()
    commit_file = (repo / COMMIT_FILE).resolve()

    written: list[Path] = []
    for hook_name, trigger in HOOKS.items():
        hook_file = _hook_path(hook_name, repo)
        hook_file.parent.mkdir(parents=True, exist_ok=True)
        hook_file.write_text(
            HOOK_TEMPLATE.format(
                hook_name=hook_name,
                trigger=trigger,
                python=py,
                script=script,
                commit_file=commit_file,
                short_flag="--short" if short else "",
            ),
            encoding="utf-8",
        )
        # Rendre exécutable (sans effet visible sur Windows, mais inoffensif)
        hook_file.chmod(0o755)
        written.append(hook_file)

    return written


# ---------------------------------------------------------------------------
# Point d'entrée CLI (appelé par les hooks)
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Récupère et écrit le hash du commit Git courant.")
    parser.add_argument("--short", action="store_true", help="Hash abrégé")
    parser.add_argument("--out", default=COMMIT_FILE, help="Fichier de sortie")
    parser.add_argument(
        "--install-hooks",
        action="store_true",
        help="Installe les hooks Git (post-commit, post-merge, post-rewrite)",
    )
    parser.add_argument("--repo", default=".", help="Répertoire du dépôt Git")
    args = parser.parse_args(argv)

    if args.install_hooks:
        written = install_hooks(repo_dir=args.repo, short=args.short)
        if not written:
            print("!! Pas un dépôt Git, hooks non installés.", file=sys.stderr)
            return 1
        for f in written:
            print(f"✓ Hook installé : {f}")
        return 0

    commit = write_commit_file(path=args.out, short=args.short)
    if commit is None:
        print("!! Impossible de récupérer le hash (pas de dépôt Git ou pas de commit).", file=sys.stderr)
        return 1
    print(commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())


def __get_git_branch():
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return branch
    except Exception:
        return None
