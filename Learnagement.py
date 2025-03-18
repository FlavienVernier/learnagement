# coding=utf-8

import os
import sys
import shutil
import subprocess
import time
from getpass import getpass

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

def mainConfiguration():
    """
    Ask the system administrator for configuration information if the configuration file does not exist and store these information into "config.py"
    """
    
    if not os.path.exists("config.py"):
        configurationSettings={}
        configurationSettings["INSTANCE_NAME"]=input("Give the intance name: ")
        configurationSettings["INSTANCE_NUMBER"]=int(input("Give the instance number (1..4): "))
        configurationSettings["INSTANCE_MYSQL_ROOT_PASSWORD"]=getpass("Give the MySQL Root password: ")
        configurationSettings["INSTANCE_MYSQL_USER_PASSWORD"]=getpass("Give the MySQL User password: ")
        with open("config.py", 'w') as file:
            file.write("configurationSettings=" + repr(configurationSettings))


    
def webAppConfiguration(configurationSettings):

    ##########
    # Initialisation de la configuration de l'application web
    print("##########")
    print("Initialisation de la configuration de l'application web")
    
    os.chdir("webApp")
    
    if not os.path.exists("config.php"):
        shutil.copy("config.php.skeleton", "config.php")
        searchReplaceInFile("config.php", "INSTANCE_NAME", configurationSettings["INSTANCE_NAME"])
        searchReplaceInFile("config.php", "INSTANCE_MYSQL_ROOT_PASSWORD", configurationSettings["INSTANCE_MYSQL_ROOT_PASSWORD"])
        searchReplaceInFile("config.php", "INSTANCE_MYSQL_USER_PASSWORD", configurationSettings["INSTANCE_MYSQL_USER_PASSWORD"])
    elif(os.path.getmtime("config.php.skeleton") > os.path.getmtime("config.php")):
        print(f"{YELLOW}WARNING: config.php.skeleton has been updated, your confing.php can be deprecated{NC}")
    
    os.chdir("..")

def dbDataConfiguration():

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

        if "y" == input("Do you want to start with free data (y/n)? "):
            # Parcourt tous les fichiers dans le dossier source
            for filename in os.listdir(free_data_folder):
                source_path = os.path.join(free_data_folder, filename)
                target_path = os.path.join(data_folder, filename)

                # Vérifie si l'élément est un fichier (et non un dossier)
                if os.path.isfile(source_path):
                    # Copie le fichier
                    shutil.copy(source_path, target_path)
                    print(f"Copied: {source_path} -> {target_path}")
            
    except OSError as error:
        print(f"{GREEN}Data already exist!{NC}")
        
    # Chemin vers le fichier db/data/README
    readme_path = os.path.join(data_folder, "README")
    # Texte à ajouter
    text_to_append = "This folder contains data inserted into DB when the system is launch at the first time.  If it doesn't exist it will contans free data"
    # Ouvrir le fichier en mode ajout et écrire le texte
    with open(readme_path, "a") as file:
        file.write(text_to_append)
        file.write("\n")  # Ajoute une nouvelle ligne, comme `echo` le ferait

    os.chdir("db")
    subprocess.run([sys.executable, "insertPrivateData.py"], check=True)
    os.chdir("..")

def dockerConfiguration(configurationSettings):
    
    ##########
    # Docker configuration
    print("##########")
    print("Docker configuration")
    
    os.chdir("docker")
    
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.skeleton", "docker-compose.yml")
        searchReplaceInFile("docker-compose.yml", "INSTANCE_NAME", configurationSettings["INSTANCE_NAME"])
        searchReplaceInFile("docker-compose.yml", "INSTANCE_NUMBER", str(configurationSettings["INSTANCE_NUMBER"]))
        searchReplaceInFile("docker-compose.yml", "INSTANCE_MYSQL_ROOT_PASSWORD", configurationSettings["INSTANCE_MYSQL_ROOT_PASSWORD"])
    elif(os.path.getmtime("docker-compose.yml.skeleton") > os.path.getmtime("docker-compose.yml")):
        print(f"{YELLOW}WARNING: docker-compose.yml.skeleton has been updated, your docker-compose.yml can be deprecated{NC}")
    
    os.chdir("..")



def dockerRun(configurationSettings):  
    
    ##########
    # Run Docker
    print("##########")
    print("Run Docker")
    
    os.chdir("docker")
    
    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker-compose', 'up'])
        prog.communicate()
    else:    
        subprocess.run(["sudo", "docker-compose", "up"], check=True)

    # Pause pour laisser Docker démarrer
    time.sleep(5)

    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose ps'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker-compose', 'ps'])
        #prog.stdin.write(b'password')
        prog.communicate()
    else:            
        subprocess.run(["sudo", "docker-compose", "ps"], check=True)
        
    os.chdir("..")

    

def run():
    mainConfiguration()
    from config import configurationSettings
    
    webAppConfiguration(configurationSettings)
    dbDataConfiguration()
    dockerConfiguration(configurationSettings)
    dockerRun(configurationSettings)
    
    # Population avec des données libres
    # subprocess.run(["sh", "populationScript.sh"], check=True)

    # Population via ADE
    # subprocess.run([sys.executable, "ade2sql.py"], check=True)

def filecmp(file1, file2):
    """Compare deux fichiers pour vérifier s'ils sont identiques."""
    with open(file1, "r") as f1, open(file2, "r") as f2:
        return f1.read() == f2.read()

def searchReplaceInFile(fileName, patern, value):
    # Read in the file
    with open(fileName, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(patern, value)
    
    # Write the file out again
    with open(fileName, 'w') as file:
        file.write(filedata)
        
def stop():
    ##########
    # Stop App
    print("##########")
    print(f"{GREEN}Stop App{NC}")
    
    os.chdir("docker")
    
    if os.name == 'nt':
        #prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose up'],stdin=subprocess.PIPE)
        #prog.stdin.write(b'password')
        prog = subprocess.Popen(['docker-compose', 'down'])
        prog.communicate()
    else:    
        subprocess.run(["sudo", "docker-compose", "down"], check=True)

    # sudo docker-compose down
    
    os.chdir("..")
    
def destroy():
    from config import configurationSettings 
    
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
                prog = subprocess.Popen(['docker', 'volume', 'rm', 'docker_learnagement_persistent_db_'+configurationSettings["INSTANCE_NAME"]])
                prog.communicate()
            else:    
                subprocess.run(["sudo", "docker", "volume", "rm", "docker_learnagement_persistent_db_"+configurationSettings["INSTANCE_NAME"]], check=True)
            print(f"{RED}App destroyed{NC}")
            
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(f"{GREEN}App not destroyed{NC}")
              
        os.chdir("..")
    else:
        print(f"{GREEN}App not destroyed{NC}")

def help(argv):
    print("Usage: " + argv[0] + " [-stop|-destroy|-help]")
            
def main(argv):
    # if script parameter is destroy
    if len(argv)==1:
        run()
    elif len(argv)==2 and argv[1] == "-stop":
        stop()
    elif len(argv)==2 and argv[1] == "-destroy":
        destroy()
    else:
        help(argv)

if __name__ == "__main__":
    main(sys.argv)
