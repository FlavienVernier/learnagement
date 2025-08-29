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

INSTANCE_NAME=None
INSTANCE_NUMBER=None
DOCKER_COMMAND=[]
DOCKER_COMPOSE_COMMAND=[]

def load_dotenv():
    dotenv.load_dotenv()
    global DOCKER_COMMAND
    DOCKER_COMMAND=os.environ["DOCKER_COMMAND"].split(' ')
    global DOCKER_COMPOSE_COMMAND
    DOCKER_COMPOSE_COMMAND=os.environ["DOCKER_COMPOSE_COMMAND"].split(' ')

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

def __mainConfiguration__():
    """
    Ask the system administrator for configuration information if the configuration file does not exist and store these information into "config.py"
    """
    
    #if not os.path.exists("config.py") or not os.path.exists(".env"):
    if not os.path.exists(".env"):
        with open(".env", 'w') as file:
            file.write("#########################################################################" + "\n")
            file.write("# Edit only root .env, next propagate it with 'Learnagement -updateEnv' #" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")
            instance_name = input("Give the intance name (lowercase): ").lower()
            file.write("COMPOSE_PROJECT_NAME=learnagement_" + instance_name + "\n") # Define project name for docker
            file.write("SESSION_TIMEOUT=" + "900" + "\n")
            file.write("INSTANCE_NAME=" + instance_name + "\n")
            instance_number = 0
            while instance_number < 2 or instance_number > 4:
                try:
                    instance_number = int(input("Give the instance number (2..4): "))
                except:
                    instance_number = 0
            file.write("INSTANCE_NUMBER=" + str(instance_number) + "\n")
            file.write("INSTANCE_SECRET=" + __generate_secret__().hex() + "\n")
            file.write("INSTANCE_URL=" + socket.gethostname() + ":" + str(instance_number) + "0080" + "\n")

            file.write("" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")
            file.write("DOCKER_COMMAND=docker")
            file.write("DOCKER_COMPOSE_COMMAND=docker compose")

            file.write("" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")
            file.write("MYSQL_SERVER=learnagement_mysql_" + instance_name + "\n")
            file.write("MYSQL_PORT=3306" + "\n")
            file.write("MYSQL_DB=learnagement" + "\n")
            file.write("MYSQL_ROOT_PASSWORD=" + getpass("Give the MySQL Root password: ") + "\n")
            file.write("MYSQL_USER_LOGIN=learnagement" + "\n")
            file.write("MYSQL_USER_PASSWORD=" + getpass("Give the MySQL User password: ") + "\n")


            file.write("" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")

            # Refactor XXX_URL (not XXX_DOCKER_URL) must be XXX_PUBLIC_URL

            file.write("PHP_BACKEND_URL=http://localhost:" + str(instance_number) + "0081" + "\n")
            file.write("PHP_BACKEND_DOCKER_URL=http://learnagement_phpbackend_" + instance_name + "\n")

            file.write("" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")

            file.write("DASH_SERVER=learnagement_python_web_server_" + instance_name + "\n")
            file.write("DASH_PORT=" + str(instance_number) + "8050" + "\n")

            file.write("" + "\n")
            file.write("#########################################################################" + "\n")
            file.write("" + "\n")

            file.write("NEXTAUTH_URL=http://localhost:" + str(instance_number) + "3000" + "\n")
            file.write("NEXTAUTH_DOCKER_URL=http://learnagement_nextjs_" + instance_name + "\n")

        print(f".env générated")

        updateEnv()


    # Load environment variables from the .env file
    load_dotenv()
    return os.environ

def updateEnv():
    source_path = os.path.join("./", ".env")

    containers=["docker", "phpbackend", "webApp", "visualisation", "webappnext", ]

    for container in containers:
        target_path = os.path.join(container, ".env")
        shutil.copy(source_path, target_path)
        print(f"Copied: {source_path} -> {target_path}")

def __dbDataConfiguration__():

    ##########
    # Création du répertoire de données initiales
    print("##########")
    print("Configure the initial data folder")
    
    # Création du répertoire de données initiales s'il n'existe pas
    data_folder = "db/data"
    try:
        os.makedirs(data_folder, exist_ok=False) # if it exists, an exception is thrown
        # Dossiers source et cible
        free_data_folder = "db/freeData"

        # Vérifie si le dossier cible existe, sinon le crée
        os.makedirs(data_folder, exist_ok=True)

        input("If you want an initial data set, put it into 'db/data' folder with name matches with [0-9]*.sql, then press enter")
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

def __dockerConfiguration__():
    
    ##########
    # Docker configuration
    print("##########")
    print("Docker configuration")
    
    os.chdir("docker")
    
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.skeleton", "docker-compose.yml")
        __searchReplaceInFile__("docker-compose.yml", "${INSTANCE_NAME}", os.environ["INSTANCE_NAME"])
        __searchReplaceInFile__("docker-compose.yml", "${INSTANCE_NUMBER}", str(os.environ["INSTANCE_NUMBER"]))
        #searchReplaceInFile("docker-compose.yml", "MYSQL_ROOT_PASSWORD", os.environ["MYSQL_ROOT_PASSWORD"])
    elif(os.path.getmtime("docker-compose.yml.skeleton") > os.path.getmtime("docker-compose.yml")):
        print(f"{YELLOW}WARNING: docker-compose.yml.skeleton has been updated, your docker-compose.yml can be deprecated{NC}")
    
    os.chdir("..")



def __dockerRun__(docker_option):
    
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
        subprocess.run(DOCKER_COMPOSE_COMMAND + ["up"] + docker_option, check=True)

    # Pause pour laisser Docker démarrer
    time.sleep(5)

    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose ps'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker', 'compose', 'ps'])
        #prog.stdin.write(b'password')
        prog.communicate()
    else:            
        subprocess.run(DOCKER_COMPOSE_COMMAND + ["ps"], check=True)
        
    os.chdir("..")

    

def start(docker_option = []):
    __mainConfiguration__()

    __dbDataConfiguration__()
    __dockerConfiguration__()
    __dockerRun__(docker_option)
    
    print(f"{YELLOW}WWeb Apps will run on: {os.environ['INSTANCE_NUMBER']}0080{NC}")
    print(f"{YELLOW}WPHPMyAdmin will run on: http://127.0.0.1:{os.environ['INSTANCE_NUMBER']}8080{NC}")
    
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
    load_dotenv()
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
        cmd = DOCKER_COMMAND + ["exec", "-it", "learnagement_mysql_" + os.environ["INSTANCE_NAME"], "mysqld", "--version"]
        os.system(" ".join(cmd))
       
        # get Learnagement db schemas
        structureFile = os.path.join(backup_folder,"0_struct_" + now + ".sql")
        cmd = DOCKER_COMMAND + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-data", "--ignore-views", "--skip-triggers", "--skip-comments", "--skip-extended-insert", "learnagement", ">", structureFile]
        print(" ".join(cmd))
        print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement DB data
        dataFile = os.path.join(backup_folder,"5_data_" + now + ".sql")
        cmd = DOCKER_COMMAND + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--skip-triggers", "--skip-comments", "--skip-extended-insert", "learnagement", ">", dataFile]
        print(" ".join(cmd))
        print("Enter MySQL password:")
        os.system(" ".join(cmd))

        # get Learnagement db triggers
        triggerFile = os.path.join(backup_folder,"99_trigger_" + now + ".sql")
        cmd = DOCKER_COMMAND + ["exec", "-it", "learnagement_mysql_"+os.environ["INSTANCE_NAME"], "mysqldump", "-u", os.environ["MYSQL_USER_LOGIN"], "-p" + os.environ["MYSQL_USER_PASSWORD"], "--no-create-info", "--ignore-views", "--no-data", "--skip-comments", "--skip-extended-insert", "learnagement", ">", triggerFile]
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
    load_dotenv()
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

def importInstance(instanceArchive):
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
    load_dotenv()
    ##########
    # Stop App
    print("##########")
    print(f"{GREEN}Stop App{NC}")
    
    os.chdir("docker")
    
    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(DOCKER_COMPOSE_COMMAND + ['down'])
        prog.communicate()
    else:    
        subprocess.run(DOCKER_COMPOSE_COMMAND + ["down"], check=True)
    
    os.chdir("..")
    
def destroy():

    load_dotenv()

    ##########
    # Destroy App
    print("##########")
    print(f"{RED}Destroy App{NC}")
    

    if "YES" == input("Are you sure (YES/NO)? NO DATA CAN BE RECOVERED! ") and "YES" == input("Are you realy sure(YES/NO)? don't cry if you've lost your data! "):
    
        #stop()

        os.chdir("docker")

        try:
    
            if os.name == 'nt':
                #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
                #prog.stdin.write(b'password')
                prog = subprocess.Popen(['docker', 'volume', 'rm', 'docker_learnagement_persistent_db_'+os.environ["INSTANCE_NAME"]])
                prog.communicate()
                prog = subprocess.Popen(["rm ", "../db/sql/5_*"])
                prog.communicate()
            else:
                subprocess.run(DOCKER_COMMAND + ["volume", "rm", "docker_learnagement_persistent_db_"+os.environ["INSTANCE_NAME"]], check=True)
                subprocess.run(["sudo", "rm ", "../db/sql/5_*"], check=True)
            print(f"{RED}App destroyed{NC}")
            
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(f"{GREEN}App not destroyed{NC}")
              
        os.chdir("..")
    else:
        print(f"{GREEN}App not destroyed{NC}")

def fromscratch():

    load_dotenv()

    ##########
    # Clean up App from scratch
    print("##########")
    print(f"{RED}Clean up App from scratch{NC}")
    
    if "YES" == input("Are you sure (YES/NO)? NO INITIAL DATA OR CUSTOMIZED CONFIGURATION CAN BE RECOVERED! ") and "YES" == input("Are you realy sure(YES/NO)? don't cry if you've lost anything! "):
        shutil.rmtree("db/data", ignore_errors=True)
        for f in glob.glob("db/sql/5*"):
            os.remove(f)
        os.remove("docker/docker-compose.yml")
        #os.remove("docker/phpmyadmin/config.inc.php")
        os.remove("webApp/config.php")
        os.remove("config.py")
        
def help(argv):
    print("Usage: " + argv[0] + " [-start|-stop|-build|-backupDB|-destroy|-updateEnv|-exportInstance|-importInstance FILE_NAME|-help]")
            
def main(argv):
    # if script parameter is destroy
    if len(argv)==1 or (len(argv)==2 and argv[1] == "-start"):
        start()
    elif len(argv)==2 and argv[1] == "-backupDB":
        backupDB()
    elif len(argv)==2 and argv[1] == "-stop":
        stop()
    elif len(argv)==2 and argv[1] == "-build":
        start(docker_option = ["--build"])
    elif len(argv)==2 and argv[1] == "-destroy":
        destroy()
    elif len(argv)==2 and argv[1] == "-updateEnv":
        updateEnv()
    elif len(argv)==2 and argv[1] == "-exportInstance":
        exportInstance()
    elif len(argv)==3 and argv[1] == "-importInstance":
        importInstance(argv[2])
    else:
        help(argv)

if __name__ == "__main__":
    main(sys.argv)
