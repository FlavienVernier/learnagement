# coding=utf-8
import glob
import os
import sys
import shutil
import subprocess
import time
import socket
import datetime
import dotenv
import re
import asyncio
#from dotenv import load_dotenv
from getpass import getpass
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from pathlib import Path


# Couleurs pour les messages (non directement nécessaires dans Python mais émulation via ANSI codes)
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW='\033[0;33m'
#Blue='\033[0;34m'
#Purple='\033[0;35m'
#Cyan='\033[0;36m'
#White='\033[0;37m'
NC = "\033[0m"  # No color

ENVIRONMENT= "dev"
#INSTANCE_NAME=None
#INSTANCE_NUMBER=None
#DOCKER_COMMAND=[]
#DOCKER_COMPOSE_COMMAND=[]

containers = ["docker", "backend_python", "webApp", "front_DashPlotly", "front_NextJS", ]


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

# def load_dotenv():
#     dotenv.load_dotenv()
#     global DOCKER_COMMAND
#     DOCKER_COMMAND=os.environ["DOCKER_COMMAND"].split(' ')
#     global DOCKER_COMPOSE_COMMAND
#     DOCKER_COMPOSE_COMMAND=os.environ["DOCKER_COMPOSE_COMMAND"].split(' ')

def update_env_variable(env_variables, key=None, value=None):
    updated = re.sub(
        rf'^{key}=.*$',
        f'{key}={value}',
        env_variables,
        flags=re.MULTILINE
    )
    return updated

# Generate default .env for dev environment
def __generate_env():
    if not os.path.exists(".env"):
        dotenv.load_dotenv("env_default.env")
        with open("env_skeleton.env", 'r') as f:
            content = f.read()

        # Instance

        instance_name = input("Give the intance name (lowercase): ").lower()
        content = update_env_variable(content, key="INSTANCE_NAME", value=instance_name)
        content = update_env_variable(content, key="COMPOSE_PROJECT_NAME", value=f"learnagement_{instance_name}")

        # Due to ports generation, and as ports 1XXXX are locked in some OS, instance number 1 cannot be used
        instance_number = "-1"
        while not instance_number in ["0", "2", "3", "4"]:
            try:
                instance_number = input("Give the instance number (0,2,3 or 4 -- not 1): ")
            except:
                instance_number = "-1"
        content=update_env_variable(content, key="INSTANCE_NUMBER", value=instance_number)

        # Compute ports
        backend_python_port  = int(instance_number) * 10000 + int(os.environ["BACKEND_PYTHON_DOCKER_PORT"])
        front_php_port = int(instance_number) * 10000 + int(os.environ["FRONT_PHP_DOCKER_PORT"])
        front_dash_port = int(instance_number) * 10000 + int(os.environ["FRONT_DASH_DOCKER_PORT"])
        front_nextauth_port = int(instance_number) * 10000 + int(os.environ["FRONT_NEXTAUTH_DOCKER_PORT"])
        instance_port = front_php_port

        content = update_env_variable(content, key="COMPOSE_PROJECT_NAME", value=f"learnagement_{instance_name}")

        content = update_env_variable(content, key="INSTANCE_SECRET", value=str(__generate_secret__().hex()))
        protocol="http"
        content = update_env_variable(content, key="FRONT_PHP_PROTOCOL", value =protocol)
        content = update_env_variable(content, key="INSTANCE_URL", value = protocol + "://" + socket.gethostname())
        content = update_env_variable(content, key="INSTANCE_PORT", value = str(instance_port))

        # MySQL
        content = update_env_variable(content, key="MYSQL_SERVER", value=f"learnagement_mysql_{instance_name}")
        content = update_env_variable(content, key="MYSQL_ROOT_PASSWORD", value=getpass("Give the MySQL Root password: "))
        content = update_env_variable(content, key="MYSQL_USER_PASSWORD", value=getpass("Give the MySQL User password: "))

        # Backend
        content = update_env_variable(content, key="BACKEND_PYTHON_DOCKER_URL", value=f"http://learnagement_backend_python_{instance_name}")
        content = update_env_variable(content, key="BACKEND_PYTHON_PORT", value=str(backend_python_port))

        # Fronts
        content = update_env_variable(content, key="FRONT_PHP_PORT", value=str(front_php_port))
        content = update_env_variable(content, key="FRONT_DASH_PORT", value=str(front_dash_port))
        content = update_env_variable(content, key="FRONT_NEXTAUTH_PORT", value=str(front_nextauth_port))

        with open(".env", 'w') as f:
            f.write(content)
    updateEnv()
    dotenv.load_dotenv()

def update_env_file_variable(env_file=".env", key=None, value=None):
    if key and value:
        with open(env_file, 'r') as f:
            content = f.read()

        updated = update_env_variable(content, key, value)

        with open(env_file, 'w') as f:
            f.write(updated)

        print(f"{YELLOW}Warning: environment variables changed!{NC}")

    # Load environment variables from the .env file
    dotenv.load_dotenv()

def updateEnv():
    source_path = os.path.join("./", ".env")

    for container in containers:
        target_path = os.path.join(container, ".env")
        shutil.copy(source_path, target_path)
        print(f"Copied: {source_path} -> {target_path}")

        
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
        print(f"{GREEN}DB already exist initialized!{NC}")

def __dbData_configuration__():

    ##########
    # Création du répertoire de données initiales
    print("##########")
    print("Configure the initial data folder")
    
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
        print(f"{GREEN}Data already exist in 'db/data'!{NC}")
        
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

def __docker_configuration__():
    
    ##########
    # Docker configuration
    print("##########")
    print("Docker configuration")
    
    os.chdir("docker")
    
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.skeleton", "docker-compose.yml")
        __searchReplaceInFile__("docker-compose.yml", "${INSTANCE_NAME}", os.environ["INSTANCE_NAME"])
        __searchReplaceInFile__("docker-compose.yml", "${INSTANCE_NUMBER}", str(os.environ["INSTANCE_NUMBER"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_PHP_PORT}", str(os.environ["FRONT_PHP_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${FRONT_PHP_DOCKER_PORT}", str(os.environ["FRONT_PHP_DOCKER_PORT"]))
        __searchReplaceInFile__("docker-compose.yml", "${SSL_DIR}", str(os.environ["SSL_DIR"]))
        __searchReplaceInFile__("docker-compose.yml", "${DOCKER_SSL_DIR}", str(os.environ["DOCKER_SSL_DIR"]))
    elif(os.path.getmtime("docker-compose.yml.skeleton") > os.path.getmtime("docker-compose.yml")):
        print(f"{YELLOW}WARNING: docker-compose.yml.skeleton has been updated, your docker-compose.yml can be deprecated{NC}")
    
    os.chdir("..")



async def __docker_run__(docker_option):
    
    ##########
    # Run Docker
    print("##########")
    print("Run Docker")
    
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

    

async def start(docker_option = None):
    if not docker_option:
        docker_option = []
    #__mainConfiguration__()
    __generate_env()

    dotenv.load_dotenv()

    __dbConfiguration__()
    __dbData_configuration__()

    __docker_configuration__()
    __security_check()
    task = asyncio.create_task(__docker_run__(docker_option))
    
    print(f"{GREEN}Web Apps will run on: {os.environ['INSTANCE_URL']}{NC}")
    print(f"{GREEN}PHPMyAdmin will run on: http://127.0.0.1:{os.environ['INSTANCE_NUMBER']}8080{NC}")

    await task

    # Population avec des données libres
    # subprocess.run(["sh", "populationScript.sh"], check=True)

    # Population via ADE
    # subprocess.run([sys.executable, "ade2sql.py"], check=True)

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

def backupDB(backup_folder="db/backup"):

    """
SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = "learnagement" AND TABLE_TYPE = "BASE TABLE"
    """
    dotenv.load_dotenv()
    print(os.environ)

    ##########
    # Backup DB
    print("##########")
    print(f"{GREEN}BackUp DB{NC}")

    #f="listOfTable.txt"
    #cmd=["docker", "exec", "-it", "learnagement_mysql_"+configurationSettings["INSTANCE_NAME"], "mysql",  "-u",  "root", "-p"+configurationSettings["INSTANCE_MYSQL_ROOT_PASSWORD"], "-e", "'SELECT", "table_name", "FROM", "information_schema.tables", "WHERE", "TABLE_SCHEMA", "=", "\"learnagement\"", "AND", "TABLE_TYPE", "=", "\"BASE TABLE\"'", "> db/backup/"+f]
    #cmd=["docker", "exec", "-it", "learnagement_mysql_"+configurationSettings["INSTANCE_NAME"], "mysql",  "-u",  "root", "-p"+configurationSettings["INSTANCE_MYSQL_ROOT_PASSWORD"], "-e", "'SELECT", "table_name", "FROM", "information_schema.tables", "WHERE", "TABLE_SCHEMA", "=", "\"learnagement\"", "AND", "TABLE_TYPE", "=", "\"BASE TABLE\"'"]
    #cmd=["docker", "exec", "-it", "learnagement_mysql_"+configurationSettings["INSTANCE_NAME"], "mysql",  "-u",  "root", "-p", "-e", "'SELECT", "table_name", "FROM", "information_schema.tables", "WHERE", "TABLE_SCHEMA", "=", "\"learnagement\"", "AND", "TABLE_TYPE", "=", "\"BASE TABLE\"'"]

    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    
    if os.name == 'nt':
        print ("Not yet implemented for Windows.")
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
        print(" ".join(cmd))
        print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement DB data
        dataFile = os.path.join(backup_folder,"5_data_" + now + ".sql")
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--skip-triggers", "--skip-comments", "--skip-extended-insert", "--no-tablespaces", "learnagement", ">", dataFile]
        print(" ".join(cmd))
        print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement db triggers
        triggerFile = os.path.join(backup_folder,"99_trigger_" + now + ".sql")
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--no-data", "--skip-comments", "--skip-extended-insert", "--no-tablespaces", "learnagement", ">", triggerFile]
        print(" ".join(cmd))
        print("Enter MySQL password:")
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
        print(error)

def import_instance(instanceArchive):
    # Check if instance is not already running from .
    # ToDo
    # If no instance running
    import_dir_path = Path(instanceArchive).stem
    # Unarchive instance archive
    shutil.unpack_archive(instanceArchive)
    # Move .env from import directory to .
    shutil.copy(os.path.join(import_dir_path, "env"), ".env")
    updateEnv()
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

def stop():
    dotenv.load_dotenv()
    ##########
    # Stop App
    print("##########")
    print(f"{GREEN}Stop App{NC}")
    
    os.chdir("docker")
    
    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ['down'])
        prog.communicate()
    else:    
        subprocess.run(os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + ["down"], check=True)
    
    os.chdir("..")
    
def destroy():

    dotenv.load_dotenv()

    ##########
    # Destroy App
    print("##########")
    print(f"{RED}DEPRECATED (use from scratch): Destroy App{NC}")
    

    if "YES" == input("Are you sure (YES/NO)? NO DATA CAN BE RECOVERED! ") and "YES" == input("Are you realy sure(YES/NO)? don't cry if you've lost your data! "):
    
        #stop()

        try:
    
            if os.name == 'nt':
                prog = subprocess.Popen(['docker', 'volume', 'rm', os.environ["COMPOSE_PROJECT_NAME"] + '_learnagement_persistent_db_'+os.environ["INSTANCE_NAME"]])
                prog.communicate()
                prog = subprocess.Popen(["rm", "db/sql/5_*"])
                prog.communicate()
            else:
                subprocess.run(os.environ["DOCKER_COMMAND"].split(" ") + ["volume", "rm", os.environ["COMPOSE_PROJECT_NAME"] + "_learnagement_persistent_db_"+os.environ["INSTANCE_NAME"]], check=True)
                subprocess.run(["pwd"], check=True)
                subprocess.run(["rm", "db/sql/5_*"], check=True)
            print(f"{RED}App destroyed{NC}")
            
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(f"{GREEN}App not destroyed{NC}")
    else:
        print(f"{GREEN}App not destroyed{NC}")

def from_env(environment=None):
    if environment:
        global ENVIRONMENT
        ENVIRONMENT=environment

        # buils .env if not exist
        #__mainConfiguration__()
        __generate_env()

        # remove configuration files that depends on .env
        try:
            os.remove(os.path.join("docker", "docker-compose.yml"))
        except FileNotFoundError as e:
            print(e)

        # Reset environment variable according to dev or prod environment
        update_env_file_variable(key="ENV", value=environment)
        if environment == "prod":
            # ToDo refactor so that default parameters are in prod.env file
            port = 443
            update_env_file_variable(key="FRONT_PHP_PROTOCOL", value="https")
        else:
            port = 80
            update_env_file_variable(key="FRONT_PHP_PROTOCOL", value="http")

        update_env_file_variable(key="FRONT_PHP_DOCKER_PORT", value=port)
        update_env_file_variable(key="FRONT_PHP_PORT", value=int(os.environ["INSTANCE_NUMBER"]) * 10000 + port)

    # Update .env for each sub-app
    updateEnv()

def from_scratch():

    dotenv.load_dotenv()

    ##########
    # Clean up App from scratch
    print("##########")
    print(f"{RED}Clean up App from scratch{NC}")
    print(f"{RED}The application must be stopped{NC}")

    
    if "YES" == input("Are you sure (YES/NO)? NO INITIAL DATA OR CUSTOMIZED CONFIGURATION CAN BE RECOVERED! ") and "YES" == input("Are you realy sure(YES/NO)? don't cry if you've lost anything! "):
        try:
            if os.name == 'nt':
                prog = subprocess.Popen(os.environ["DOCKER_COMMAND"].split(" ") + ['volume', 'rm', os.environ["COMPOSE_PROJECT_NAME"] + '_learnagement_persistent_db_' + os.environ["INSTANCE_NAME"]])
                prog.communicate()
            else:
                subprocess.run(os.environ["DOCKER_COMMAND"].split(" ") + ["volume", "rm", os.environ["COMPOSE_PROJECT_NAME"] + "_learnagement_persistent_db_" + os.environ["INSTANCE_NAME"]], check=True)
        except subprocess.CalledProcessError as e:
            print(e.output)

        try:
            shutil.rmtree(os.path.join("db", "data"), ignore_errors=True)
            shutil.rmtree(os.path.join("db", "docker-entrypoint-initdb.d"), ignore_errors=True)
            os.remove(os.path.join("docker", "docker-compose.yml"))
        except FileNotFoundError as e:
            print(e)
        try:
            os.remove(".env")
        except FileNotFoundError as e:
            print(e)

        for container in containers:
            try:
                target_path = os.path.join(container, ".env")
                os.remove(target_path)
            except FileNotFoundError as e:
                print(e)

        print(f"{GREEN}The application was reset to its initial state.{NC}")



def __get_git_branch():
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return branch
    except Exception:
        return None

def __security_check():
    dotenv.load_dotenv()
    git_branch = __get_git_branch()
    if git_branch == "main" :
        if os.environ["ENV"] !="prod" :
            print(f"{RED}SECURITY ALERT: App run from main branch without 'ENV' environment variable set as 'prod'{NC}")
            exit(1)

    elif git_branch == "prerelease":
        if os.environ["ENV"] != "prod":
            print(f"{YELLOW}SECURITY WARNING: App run from prerelease branch without 'ENV' environment variable set as 'prod'{NC}")

    else:
        print(f"{GREEN}App run from '{git_branch}' branch with '{os.environ['ENV']}' environment{NC}")


def __help(argv):
    print(f"""
        {GREEN}Usage:{NC} {argv[0]} [OPTION]
        
        {GREEN}Options:{NC}
          -start                Start the application (default if no option given)
          -build                Start the application and rebuild Docker images
          -stop                 Stop the application
          -backupDB             Backup the database (structure, data and triggers)
          -fromEnv [dev|prod]   Reset the application to to use new .env , app must be stopped before. Without env it propagate root .env to all apps.
          -fromScratch          Reset the application to its initial state (IRREVERSIBLE), app must be stopped before
          -exportInstance       Export the current instance as a zip archive
          -importInstance FILE  Import an instance from a zip archive
          -help                 Show this help message
        
        {YELLOW}Examples:{NC}
          {argv[0]} -start
          {argv[0]} -stop
          {argv[0]} -importInstance Learnagement_myinstance_20240101.zip
        
        {RED}WARNING:{NC} -fromScratch will delete all data and configuration. Use with caution.
    """)

def main(argv):
    # if script parameter is destroy
    if len(argv)==1 or (len(argv)==2 and argv[1] == "-start"):
        asyncio.run(start())
    elif len(argv)==2 and argv[1] == "-backupDB":
        backupDB()
    elif len(argv)==2 and argv[1] == "-stop":
        stop()
    elif len(argv)==2 and argv[1] == "-build":
        asyncio.run(start(docker_option = ["--build"]))
    elif len(argv)==2 and argv[1] == "-fromScratch":
        from_scratch()
    elif len(argv) in [2, 3] and argv[1] == "-fromEnv":
        if len(argv)==2:
            from_env()
        elif argv[2] in ["dev","prod"]:
            from_env(argv[2])
    elif len(argv)==2 and argv[1] == "-exportInstance":
        exportInstance()
    elif len(argv)==3 and argv[1] == "-importInstance":
        import_instance(argv[2])
    elif len(argv) == 2 and argv[1] == "-help":
        __help(argv)
    else:
        __help(argv)

if __name__ == "__main__":
    main(sys.argv)
