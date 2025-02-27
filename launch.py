# coding=utf-8

import os
import shutil
import subprocess
import time

def main():
    # Couleurs pour les messages (non directement nécessaires dans Python mais émulation via ANSI codes)
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    NC = "\033[0m"  # No color

    ##########
    # Initialisation de la configuration de l'application web
    print("##########")
    print("Initialisation de la configuration de l'application web")
    
    os.chdir("webApp")
    if not os.path.exists("config.php"):
        shutil.copy("config.php.example", "config.php")
        print(f"{GREEN}Update webApp/config.php files with new password.{NC}")
        input("Then press any key to continue... ")
    
    if os.path.exists("config.php.example") and os.path.exists("config.php"):
        #ToDo implement a real ceck password
        if filecmp("config.php.example", "config.php"):
            print(f"{RED}WARNING default password seems to be used !!!{NC}")
    
    os.chdir("..")

    ##########
    # Création du répertoire de données initiales
    print("##########")
    print("Création du répertoire de données initiales")
    
    # Création du répertoire de données initiales s'il n'existe pas
    try:
        os.makedirs("db/data", exist_ok=False)
        # Dossiers source et cible
        source_folder = "db/freeData"
        target_folder = "db/data"

        # Vérifie si le dossier cible existe, sinon le crée
        os.makedirs(target_folder, exist_ok=True)

        # Parcourt tous les fichiers dans le dossier source
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)

            # Vérifie si l'élément est un fichier (et non un dossier)
            if os.path.isfile(source_path):
                # Copie le fichier
                shutil.copy(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path}")
            
    except OSError as error:
        print(f"{GREEN}Data already exist!{NC}")
        
    # Chemin vers le fichier db/data/README
    readme_path = "db/data/README"
    # Texte à ajouter
    text_to_append = "This folder contains data inserted into DB when the system is launch at the first time.  If it doesn't exist it will contans free data"
    # Ouvrir le fichier en mode ajout et écrire le texte
    with open(readme_path, "a") as file:
        file.write(text_to_append)
        file.write("\n")  # Ajoute une nouvelle ligne, comme `echo` le ferait

    os.chdir("db")
    subprocess.run(["python3", "insertPrivateData.py"], check=True)
    os.chdir("..")

    ##########
    # Run Docker
    print("##########")
    print("Lancement de Docker")
    
    os.chdir("docker")
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.example", "docker-compose-dev.yml")
        print(f"{GREEN}Update docker/docker-compose.yml files with new password.{NC}")
        input("Then press any key to continue... ")

    if os.path.exists("docker-compose.yml.example") and os.path.exists("docker-compose.yml"):
        #ToDo implement a real ceck password
        if filecmp("docker-compose.yml.example", "docker-compose.yml"):
            print(f"{RED}WARNING default password seems to be used !!!{NC}")

    
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

    # Population avec des données libres
    # subprocess.run(["sh", "populationScript.sh"], check=True)

    # Population via ADE
    # subprocess.run(["python3", "ade2sql.py"], check=True)

def filecmp(file1, file2):
    """Compare deux fichiers pour vérifier s'ils sont identiques."""
    with open(file1, "r") as f1, open(file2, "r") as f2:
        return f1.read() == f2.read()

if __name__ == "__main__":
    main()
