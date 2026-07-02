# coding=utf-8
import glob
import logging
import os
import sys
import shutil
import subprocess
import time
import socket
import datetime
from time import sleep

import dotenv
import re
import asyncio
import click
#from dotenv import load_dotenv
from getpass import getpass
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from pathlib import Path

from sqlalchemy import true

# Couleurs pour les messages (non directement nécessaires dans Python mais émulation via ANSI codes)
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW='\033[0;33m'
#Blue='\033[0;34m'
#Purple='\033[0;35m'
#Cyan='\033[0;36m'
#White='\033[0;37m'
NC = "\033[0m"  # No color

containers = ["docker", "backend_python", "front_PHP", "front_DashPlotly", "front_NextJS", ]
envs = {"dev", "prod"}

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

#############################################################
# Lernagement security

def __get_git_branch():
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return branch
    except Exception:
        return None

def __check_certificates():
    dotenv.load_dotenv()
    if os.environ["ENV"] != "prod" and (not os.path.exists(os.environ["SSL_DIR"] + "learnagement/cert.pem") or  not os.path.exists(os.environ["SSL_DIR"] + "learnagement/key.pem")):
        logging.error("Certificate not found. Please run learnagement.py first.")
        sys.exit(1)

def __security_check():
    dotenv.load_dotenv()
    git_branch = __get_git_branch()
    if git_branch == "main" :
        if os.environ["ENV"] !="prod" :
            logging.error(f"{RED}SECURITY ALERT: App run from main branch without 'ENV' environment variable set as 'prod'{NC}")
            exit(1)

    elif git_branch == "prerelease":
        if os.environ["ENV"] != "prod":
            logging.warning(f"{YELLOW}SECURITY WARNING: App run from prerelease branch without 'ENV' environment variable set as 'prod'{NC}")

    else:
        logging.info(f"{GREEN}App run from '{git_branch}' branch with '{os.environ['ENV']}' environment{NC}")

#def generate_nextauth_secret(base_secret: str) -> bytes:
def __generate_secret__() -> bytes:
    base_secret = os.urandom(32).hex()
    """
    Génère une clé dérivée compatible avec NextAuth à partir d'un secret de base.
    """
    info = "NextAuth.js Generated Encryption Key".encode('utf-8')
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 32 octets pour une clé symétrique
        salt=b"",    # pas de sel ici, mais peut être personnalisé
        info=info
    )
    derived_key = hkdf.derive(base_secret.encode('utf-8'))
    return derived_key


#############################################################
# Lernagement env management

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


# Generate default env variables

def __generate_base_env():
    default_env_vars = __load_env_file("__env_skeleton.env")

    # Instance

    instance_name = input("Give the intance name (lowercase): ").lower()
    default_env_vars["INSTANCE_NAME"] = instance_name
    default_env_vars["COMPOSE_PROJECT_NAME"] = f"learnagement_{instance_name}"

    default_env_vars["COMPOSE_PROJECT_NAME"] = f"learnagement_{instance_name}"

    default_env_vars["CAS_SERVICE_TOKEN"] = str(__generate_secret__().hex())

    default_env_vars["INSTANCE_SECRET"] = str(__generate_secret__().hex())
    protocol = "http"
    default_env_vars["FRONT_PHP_PROTOCOL"] = protocol

    default_env_vars["INSTANCE_PROTOCOL"] = protocol
    default_env_vars["INSTANCE_URL"] = socket.gethostname()

    # MySQL
    default_env_vars["MYSQL_SERVER"] = f"learnagement_mysql_{instance_name}"
    default_env_vars["MYSQL_ROOT_PASSWORD"] = getpass("Give the MySQL Root password: ")
    default_env_vars["MYSQL_USER_PASSWORD"] = getpass("Give the MySQL User password: ")

    # Backend
    default_env_vars["BACKEND_PYTHON_DOCKER_URL"] = f"http://learnagement_backend_python_{instance_name}"

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

    for container in containers:
        target_path = os.path.join(container, ".env")
        shutil.copy(source_path, target_path)
        logging.info(f"{GREEN}Copied: {source_path} -> {target_path}{NC}")



#############################################################
# Lernagement BD

def __dbConfiguration__():

    init_db_folder = os.path.join("db", "docker-entrypoint-initdb.d")
    try:
        os.makedirs(init_db_folder, exist_ok=False) # if it exists, an exception is thrown

        sql_folder = os.path.join("db", "sql")
        for filename in os.listdir(sql_folder):
             source_path = os.path.join(sql_folder, filename)
             target_path = os.path.join(init_db_folder, filename)

             # Vérifie si l'élément est un fichier (et non un dossier)
             if os.path.isfile(source_path):
                 # Copie le fichier
                 shutil.copy(source_path, target_path)

    except OSError as error:
        logging.info(f"{GREEN}DB already exist initialized!{NC}")

def __dbData_configuration__():

    ##########
    # Création du répertoire de données initiales
    logging.info(f"{GREEN}Configure the initial data folder{NC}")
    
    # Création du répertoire de données initiales s'il n'existe pas
    data_folder = os.path.join("db", "data")
    try:
        os.makedirs(data_folder, exist_ok=False) # if it exists, an exception is thrown
        # Dossiers source et cible
        #free_data_folder = "db/freeData"

        # Vérifie si le dossier cible existe, sinon le crée
        #os.makedirs(data_folder, exist_ok=True)

        print("If you want an initial data set, put it into 'db/data' folder with name matches with [0-9]*.sql.")
        print("Free data samples are available at 'db/freeData' folder.")
        input("Then press enter")
        # if "y" == input("Do you want to start with free data (y/n)? "):
        #     # Parcourt tous les fichiers dans le dossier source
        #     for filename in os.listdir(free_data_folder):
        #         source_path = os.path.join(free_data_folder, filename)
        #         target_path = os.path.join(data_folder, filename)
        #
        #         # Vérifie si l'élément est un fichier (et non un dossier)
        #         if os.path.isfile(source_path):
        #             # Copie le fichier
        #             shutil.copy(source_path, target_path)
        #             print(f"Copied: {source_path} -> {target_path}")
            
    except OSError as error:
        logging.info(f"{GREEN}Data already exist in 'db/data'!{NC}")
        
    # # Chemin vers le fichier db/data/README
    # readme_path = os.path.join(data_folder, "README")
    # # Texte à ajouter
    # text_to_append = "This folder contains data inserted into DB when the system is launch at the first time.  If it doesn't exist it will contans free data"
    # # Ouvrir le fichier en mode ajout et écrire le texte
    # with open(readme_path, "a") as file:
    #     file.write(text_to_append)
    #     file.write("\n")  # Ajoute une nouvelle ligne, comme `echo` le ferait

    os.chdir("db")
    subprocess.run([sys.executable, "insertPrivateData.py"], check=True)
    os.chdir("..")



#############################################################
# Lernagement Dockers

def __docker_configuration__():
    
    ##########
    # Docker configuration
    logging.info(f"{GREEN}Docker configuration{NC}")
    
    os.chdir("docker")
    
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.skeleton", "docker-compose.yml")
        __searchReplaceInFile__("docker-compose.yml", "${INSTANCE_NAME}", os.environ["INSTANCE_NAME"])
        __searchReplaceInFile__("docker-compose.yml", "${ENV}", str(os.environ["ENV"]))
        __searchReplaceInFile__("docker-compose.yml", "${PHPMYADMIN_PORT}", str(os.environ["PHPMYADMIN_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${PHPMYADMIN_DOCKER_PORT}", str(os.environ["PHPMYADMIN_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${BACKEND_PYTHON_PORT}", str(os.environ["BACKEND_PYTHON_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${BACKEND_PYTHON_DOCKER_PORT}", str(os.environ["BACKEND_PYTHON_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_PHP_PORT}", str(os.environ["FRONT_PHP_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_PHP_DOCKER_PORT}", str(os.environ["FRONT_PHP_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_DASH_PORT}", str(os.environ["FRONT_DASH_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_DASH_DOCKER_PORT}", str(os.environ["FRONT_DASH_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_NEXTAUTH_PORT}", str(os.environ["FRONT_NEXTAUTH_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_NEXTAUTH_DOCKER_PORT}", str(os.environ["FRONT_NEXTAUTH_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${SSL_DIR}", str(os.environ["SSL_DIR"]))
        __searchReplaceInFile__("docker-compose.yml", "${DOCKER_SSL_DIR}", str(os.environ["DOCKER_SSL_DIR"]))
    elif(os.path.getmtime("docker-compose.yml.skeleton") > os.path.getmtime("docker-compose.yml")):
        logging.warning(f"{YELLOW}docker-compose.yml.skeleton has been updated, your docker-compose.yml can be deprecated{NC}")
    
    os.chdir("..")



async def __run_dockers__(docker_option):
    
    ##########
    # Run Docker
    logging.info(f"{GREEN}Run Docker{NC}")
    
    os.chdir("docker")
    
    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker', 'compose', 'up'] + docker_option)
        prog.communicate()
    else:    
        subprocess.run(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ["up"] + docker_option, check=True)

    # Pause pour laisser Docker démarrer
    time.sleep(5)

    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose ps'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker', 'compose', 'ps'])
        #prog.stdin.write(b'password')
        prog.communicate()
    else:            
        subprocess.run(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ["ps"], check=True)
        
    os.chdir("..")
    return "done"


def __is_compose_running(project_name: str, docker_compose_command: str = "docker compose") -> bool:
    """
    Vérifie si un docker compose est en cours d'exécution.

    Args:
        project_name: Nom du projet docker compose (COMPOSE_PROJECT_NAME)
        docker_compose_command: Commande docker compose à utiliser

    Returns:
        True si au moins un container du projet est en cours d'exécution
    """
    try:
        result = subprocess.run(
            [*docker_compose_command.split(), "ls", "--filter", f"name={project_name}", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )

        import json
        projects = json.loads(result.stdout)

        return any(
            p["Name"] == project_name and p["Status"].startswith("running")
            for p in projects
        )

    except subprocess.CalledProcessError:
        return False

def __validate_env__(ctx, param, value):
    if not value in envs:
        logging.error(f"{RED}env must be :" + ", ".join(envs) + "{NC}")
        raise click.BadParameter("env must be :" + ", ".join(envs))
    return value


#############################################################
# Lernagement command options

def __generate_env__(env="dev"):
    if not os.path.exists(".env"):

        if not os.path.exists(".env_dev.env"):
            shutil.copy("__env_default_dev.env", ".env_dev.env")
        if not os.path.exists(".env_prod.env"):
            shutil.copy("__env_default_prod.env", ".env_prod.env")

        logging.warning(f"{YELLOW}env file doesn't exist, generate it with '{env}' environnement {NC}")

        env_vars = __generate_base_env()

        #env_vars = __set_env(env_vars, "env_default.env")

        # if(env == "dev"):
        #     env_vars = __set_env(env_vars, "env_dev.env")
        # elif(env == "prod"):
        #     env_vars = __set_env(env_vars, "env_prod.env")

        if not os.path.exists(f".env_{env}.env"):
            logging.error(f"{RED}Specific env file '.env_{env}.env' doesn't exist{NC}")
            exit()
        env_vars = __set_env(env_vars, f".env_{env}.env")

        save_env_file(env_vars, ".env")

    propagate_env()
    dotenv.load_dotenv()

def __from_env__(env=None):
    __generate_env__()
    if env:

        logging.info(f"{GREEN}Switch to env: {env}{NC}")

        # remove configuration files that depends on .env
        try:
            os.remove(os.path.join("docker", "docker-compose.yml"))
        except FileNotFoundError as e:
            logging.exception(e)

        env_vars = __load_env_file(".env")
        if env == "prod":
            env_vars = __set_env(env_vars, ".env_prod.env")

        else:
            env_vars = __set_env(env_vars, ".env_dev.env")

        save_env_file(env_vars, ".env")

    # Update .env for each sub-app
    propagate_env()

def __from_scratch__():
    dotenv.load_dotenv()

    if __is_compose_running(os.environ["COMPOSE_PROJECT_NAME"], os.environ["DOCKER_COMPOSE_COMMAND"]):
        logging.warning(f"{YELLOW}Instance running, it cannot be reset from scratch{NC}")
        return

    ##########
    # Clean up App from scratch
    logging.warning(f"{RED}Clean up App from scratch{NC}")
    logging.warning(f"{RED}The application must be stopped{NC}")

    # ToDo Check if app runs

    if "YES" == input(
            "Are you sure (YES/NO)? NO INITIAL DATA OR CUSTOMIZED CONFIGURATION CAN BE RECOVERED! ") and "YES" == input(
            "Are you realy sure(YES/NO)? don't cry if you've lost anything! "):
        try:
            if os.name == 'nt':
                prog = subprocess.Popen(os.environ["DOCKER_COMMAND"].split(" ") + ['volume', 'rm', os.environ[
                    "COMPOSE_PROJECT_NAME"] + '_learnagement_persistent_db_' + os.environ["INSTANCE_NAME"]])
                prog.communicate()
            else:
                subprocess.run(os.environ["DOCKER_COMMAND"].split(" ") + ["volume", "rm", os.environ[
                    "COMPOSE_PROJECT_NAME"] + "_learnagement_persistent_db_" + os.environ["INSTANCE_NAME"]], check=True)
        except subprocess.CalledProcessError as e:
            logging.exception(e.output)

        try:
            shutil.rmtree(os.path.join("db", "data"), ignore_errors=True)
            shutil.rmtree(os.path.join("db", "docker-entrypoint-initdb.d"), ignore_errors=True)
            os.remove(os.path.join("docker", "docker-compose.yml"))
        except FileNotFoundError as e:
            logging.exception(e)
        try:
            os.remove(".env")
            os.remove(".env_dev.env")
            os.remove(".env_prod.env")
        except FileNotFoundError as e:
            logging.exception(e)

        for container in containers:
            try:
                target_path = os.path.join(container, ".env")
                os.remove(target_path)
            except FileNotFoundError as e:
                logging.exception(e)

        logging.info(f"{GREEN}The application was reset to its initial state.{NC}")


async def __start__(docker_option=None):
    dotenv.load_dotenv()

    # Check if instance is not already running
    if "COMPOSE_PROJECT_NAME" in os.environ.keys() and __is_compose_running(os.environ["COMPOSE_PROJECT_NAME"],
                                                                            os.environ["DOCKER_COMPOSE_COMMAND"]):
        logging.warning(f"{YELLOW}Instance already running{NC}")
        return

    if not docker_option:
        docker_option = []
    # __mainConfiguration__()
    __generate_env__()

    dotenv.load_dotenv()

    __dbConfiguration__()
    __dbData_configuration__()

    __docker_configuration__()
    __security_check()
    task = asyncio.create_task(__run_dockers__(docker_option))

    logging.info(f"{GREEN}Web Apps will run on: {os.environ['INSTANCE_URL']}{NC}")
    logging.info(f"{GREEN}PHPMyAdmin will run on: http://127.0.0.1:{os.environ['PHPMYADMIN_PORT']}{NC}")

    await task

def __stop__():
    dotenv.load_dotenv()
    ##########
    # Stop App
    logging.info(f"{GREEN}Stop App{NC}")

    os.chdir("docker")

    if os.name == 'nt':
        # prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        # prog.stdin.write(b'password')
        prog = subprocess.Popen(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ['down'])
        prog.communicate()
    else:
        subprocess.run(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ["down"], check=True)

    os.chdir("..")

    logging.info(f"{GREEN}App stopped{NC}")

############################################
# Lernagement commands

@click.group()
def cli(): pass

# Generate default .env for dev environment
@cli.command(help="Generate environment without starting the application")
@click.option("--env", type=click.Choice(envs), default="dev", help="Environment to use: " + ", ".join(envs))
def generate_env(env="dev"):
    __generate_env__(env)


@cli.command(help="Start the application")
@click.option("--docker_option", default=None, help="See docker compose options")
@click.option("--restart", is_flag=True, help="Restart the application")
@click.option("--rebuild", is_flag=True, help="Rebuild Docker images")
@click.option("--test", is_flag=True, help="Test options without starting the application")
@click.option("--from_scratch", is_flag=True, help="Reset the application to its initial state (IRREVERSIBLE)")
@click.option("--env", type=click.Choice(envs), default=None, help="Environment to use, (use previously used if not set)")
def start(docker_option=None, restart:bool=False, rebuild:bool=False, test:bool=False, from_scratch:bool=False, env=None):

    logging.info(f"{GREEN}Starting application with: {locals()} {NC}" )

    if not docker_option:
        docker_option = []
    if restart:
        if test:
            logging.warning(f"{YELLOW}You cannot test restart.{NC}")
            return
        #ToDo check restart with switch env
        logging.warning(f"{YELLOW}Restart sometimes unstable.{NC}")
        __stop__()


    if from_scratch:
        __from_scratch__()

    if env:
        __from_env__(env)
        rebuild = True

    if rebuild and not test:
        asyncio.run(__start__(docker_option=["--build"] + docker_option))
        return
    if not test:
        asyncio.run(__start__(docker_option))


def __filecmp__(file1, file2):
    """Compare deux fichiers pour vérifier s'ils sont identiques."""
    with open(file1, "r") as f1, open(file2, "r") as f2:
        return f1.read() == f2.read()

def __searchReplaceInFile__(fileName, patern, value):
    # Read in the file
    with open(fileName, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(patern, value)
    
    # Write the file out again
    with open(fileName, 'w') as file:
        file.write(filedata)

@cli.command(help="Backup the database (structure, data and triggers)")
@click.option("--backup_folder")
def backupDB(backup_folder="db/backup"):

    """
SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = "learnagement" AND TABLE_TYPE = "BASE TABLE"
    """
    dotenv.load_dotenv()

    ##########
    # Backup DB
    logging.info(f"{GREEN}BackUp DB{NC}")

    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    
    if os.name == 'nt':
        logging.warning(f"{YELLOW}Not yet implemented for Windows.{NC}")
    else:
        # Création du répertoire de données initiales s'il n'existe pas
        #backup_folder = "db/backup"
        try:
            os.makedirs(backup_folder, exist_ok=False)  # if it exists, an exception is thrown
        except OSError as error:
            pass

        # display MySQL server version
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_" + os.environ["INSTANCE_NAME"], "mysqld", "--version"]
        os.system(" ".join(cmd))
       
        # get Learnagement db schemas
        structureFile = os.path.join(backup_folder,"0_struct_" + now + ".sql")
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-data", "--ignore-views", "--skip-triggers", "--skip-comments", "--skip-extended-insert", "--no-tablespaces", "learnagement", ">", structureFile]
        #print(" ".join(cmd))
        #print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement DB data
        dataFile = os.path.join(backup_folder,"5_data_" + now + ".sql")
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--skip-triggers", "--skip-comments", "--skip-extended-insert", "--no-tablespaces", "learnagement", ">", dataFile]
        #print(" ".join(cmd))
        #print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement db triggers
        triggerFile = os.path.join(backup_folder,"99_trigger_" + now + ".sql")
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--no-data", "--skip-comments", "--skip-extended-insert", "--no-tablespaces", "learnagement", ">", triggerFile]
        #print(" ".join(cmd))
        #print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # Bidouille
        with open(structureFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(structureFile, 'w') as fout:
            fout.writelines(data[1:])

        with open(dataFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(dataFile, 'w') as fout:
            fout.writelines(data[1:])

        with open(triggerFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(triggerFile, 'w') as fout:
            fout.writelines(data[1:])

@cli.command(help="Export the current instance as a zip archive")
def exportInstance():
    dotenv.load_dotenv()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    export_dir_path = 'Learnagement_'+ os.environ["INSTANCE_NAME"] + '_' + now

    try:
        # Build export directory
        os.mkdir(export_dir_path)
        # Export BD (backup struct, data and triggers) and move them into export directory
        export_dir_path_sql = os.path.join(export_dir_path, "sql")
        os.mkdir(export_dir_path_sql)
        backupDB(export_dir_path_sql)
        # Copi .env into export directory
        shutil.copy(os.path.join("docker", "docker-compose.yml"), export_dir_path)
        # Copy docker-compose into export directory
        shutil.copy(".env", os.path.join(export_dir_path, "env"))
        # Build archive from export directory
        archive_name = export_dir_path
        shutil.make_archive(archive_name, 'zip', '.', export_dir_path)
        # Remove export directory
        shutil.rmtree(export_dir_path)
    except OSError as error:
        logging.exception(error)

@cli.command(help="Import an instance from a zip archive")
@click.option("--file", required=True)
def import_instance(instanceArchive):

    dotenv.load_dotenv()

    # Check if instance is not already running
    if __is_compose_running(os.environ["COMPOSE_PROJECT_NAME"], os.environ["DOCKER_COMPOSE_COMMAND"]):
        logging.warning(f"{YELLOW}Instance running, you cannot import new instance{NC}")
        return

    # ToDo
    # If no instance running
    import_dir_path = Path(instanceArchive).stem
    # Unarchive instance archive
    shutil.unpack_archive(instanceArchive)
    # Move .env from import directory to .
    shutil.copy(os.path.join(import_dir_path, "env"), ".env")
    propagate_env()
    # Copy docker-compose to docker directory
    shutil.copy(os.path.join(import_dir_path, "docker-compose.yml"), "docker")
    # Move BD files into the appropriate directories
    os.mkdir(os.path.join("db","data")) # So that Learnagement does not ask for free data
    sql_instance_path = os.path.join("db", "sql")
    files = glob.glob(os.path.join(sql_instance_path,'*'))
    for f in files:
        os.remove(f)
    shutil.copytree(os.path.join(import_dir_path, "sql"), sql_instance_path, dirs_exist_ok=True)
    # Remove import directory
    shutil.rmtree(import_dir_path)
    # Run instance
    # ToDo

@cli.command(help="Stop application")
def stop():
    __stop__()

if __name__ == "__main__":
    cli()