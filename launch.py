import os
import shutil
import subprocess

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
        print(f"{GREEN}Update docker/docker-compose.yml and webApp/config.php files with new password.{NC}")
        input("Then press any key to continue... ")
    
    if os.path.exists("config.php.example") and os.path.exists("config.php"):
        if filecmp("config.php.example", "config.php"):
            print(f"{RED}WARNING default password seems to be used !!!{NC}")
    
    os.chdir("..")

    ##########
    # Création des liens pour les données privées
    print("##########")
    print("Création des liens pour les données privées")
    
    # Création du répertoire de données privées s'il n'existe pas
    os.makedirs("db/data", exist_ok=True)
    os.chdir("db")
    subprocess.run(["python", "insertPrivateData.py"], check=True)
    os.chdir("..")

    ##########
    # Lancement de Docker
    print("##########")
    print("Lancement de Docker")
    
    os.chdir("docker")
    if not os.path.exists("docker-compose.yml"):
        shutil.copy("docker-compose.yml.example", "docker-compose.yml")
        print(f"{GREEN}Update docker/docker-compose.yml and webApp/config.php files with new password.{NC}")
        input("Then press any key to continue... ")

    if os.path.exists("docker-compose.yml.example") and os.path.exists("docker-compose.yml"):
        if filecmp("docker-compose.yml.example", "docker-compose.yml"):
            print(f"{RED}WARNING default password seems to be used !!!{NC}")

    
    if os.name == 'nt':
        prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose', 'up'],stdin=sp.PIPE)
        prog.stdin.write('password')
        prog.communicate()
    else:    
        subprocess.run(["sudo", "docker-compose", "up"], check=True)

    # Pause pour laisser Docker démarrer
    time.sleep(5)

    if os.name == 'nt':
        prog = subprocess.Popen(['runas', '/noprofile', '/user:Administrator', 'docker-compose', 'ps'],stdin=sp.PIPE)
        prog.stdin.write('password')
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
