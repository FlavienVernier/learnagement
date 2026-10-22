import logging
import os
import re
import shutil
from getpass import getpass

import dotenv
from tools import get_local_ip_and_hostname, __generate_secret__
from config import GREEN, YELLOW, NC, containers_system, containers_prod, containers_dev, envs


def __scan_envs(directory="."):
    for filename in os.listdir(directory):
        match = re.match(r'^\.env_(.+)\.env$', filename)
        if match:
            envs.add(match.group(1))


def update_env_variable(env_variables, key=None, value=None):
    updated = re.sub(
        rf'^{key}=.*$',
        f'{key}={value}',
        env_variables,
        flags=re.MULTILINE
    )
    return updated


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


def save_env_file(env_vars: dict, filepath: str) -> None:
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
    default_env_vars["MYSQL_SERVER"] = f"learnagement_mysql_{instance_name}"
    default_env_vars["MYSQL_ROOT_PASSWORD"] = getpass("Give the MySQL Root password: ")
    default_env_vars["MYSQL_USER_PASSWORD"] = getpass("Give the MySQL User password: ")
    default_env_vars["LEARNAGEMENT_ADMINISTRATOR_PASSWORD"] = getpass("Give the Learnagement Administrator password: ")

    #ToDo check if passwords are different if prod env
    # ...

    # Backend
    default_env_vars["BACKEND_PYTHON_DOCKER_URL"] = f"learnagement_backend_python_{instance_name}"

    return default_env_vars


def update_env_file_variable(env_file=".env", key=None, value=None):
    if key and value:
        with open(env_file, 'r') as f:
            content = f.read()

        updated = update_env_variable(content, key, value)

        with open(env_file, 'w') as f:
            f.write(updated)

        logging.warning(f"{YELLOW}Environment variables changed!{NC}")

    # Load environment variables from the .env file
    dotenv.load_dotenv()


def propagate_env():
    source_path = os.path.join("./", ".env")

    for container in containers_system + containers_dev + containers_prod:
        target_path = os.path.join(container, ".env")
        shutil.copy(source_path, target_path)
        logging.info(f"{GREEN}Copied: {source_path} -> {target_path}{NC}")
