#!/usr/bin/env python3
"""
Bootstrap script: Initialise un environnement Python isolé (venv) et lance l'application.

Ce script :
1. Crée un environnement virtuel (`.venv`) s'il n'existe pas.
2. Installe les dépendances depuis `requirements.txt`.
3. Lance l'application avec les arguments fournis.

Usage:
    python bootstrap.py [args...]
"""
import subprocess
import sys
import os
import venv

from git import install_hooks, write_commit_file

VENV_DIR = ".venv"
APP_MODULE = "Learnagement"
REQUIREMENTS = "requirements.txt"

def create_venv() -> None:
    """Crée l'environnement virtuel s'il n'existe pas."""
    if not os.path.exists(VENV_DIR):
        print(">> Création de l'environnement virtuel...")
        venv.create(VENV_DIR, with_pip=True)

def get_venv_executables() -> tuple[str, str]:
    """Retourne les chemins de pip et python du venv."""
    if os.name == "nt":
        pip = os.path.join(VENV_DIR, "Scripts", "pip.exe")
        python = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        pip = os.path.join(VENV_DIR, "bin", "pip")
        python = os.path.join(VENV_DIR, "bin", "python")
    return pip, python

def install_dependencies(pip: str) -> None:
    """Installe les dépendances depuis requirements.txt si présent."""
    if os.path.exists(REQUIREMENTS):
        print(">> Installation des dépendances...")
        subprocess.check_call([pip, "install", "-r", REQUIREMENTS])
    else:
        print(f"!! {REQUIREMENTS} introuvable, installation ignorée.")

def configure_git() -> None:
    """
    Met en place le suivi automatique du hash de commit :
    - installe les hooks Git (post-commit, post-merge, post-rewrite) ;
    - écrit immédiatement `.commit_id` pour la session en cours
      (utile si les hooks viennent d'être installés ou en cas de premier clone).
    """
    written = install_hooks(repo_dir=".", short=True)
    if written:
        print(f">> Hooks Git installés ({len(written)}) : {', '.join(h.name for h in written)}")
    else:
        print("!! Pas de dépôt Git détecté, hooks non installés.")

    commit = write_commit_file(short=True)
    if commit:
        print(f">> Commit courant : {commit}")
    else:
        print("!! Impossible de lire le hash de commit.")

def run_app(python: str, args: list[str]) -> None:
    """Lance l'application dans le venv avec les arguments fournis."""
    print(">> Lancement de l'application...")
    cmd = [python, "-m", APP_MODULE] + args
    try:
        print(f">> {cmd}")
        os.execv(python, cmd)
    except OSError:
        sys.exit(subprocess.call(cmd))

def main() -> None:
    args = sys.argv[1:]
    create_venv()
    pip, python = get_venv_executables()
    install_dependencies(pip)
    configure_git()
    run_app(python, args)

if __name__ == "__main__":
    main()