import os
import glob
import shutil

def main():
    # Couleurs pour les messages (non directement nécessaires dans Python mais émulation via ANSI codes)
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    NC = "\033[0m"  # No color

    # Dossier source contenant les fichiers .sql
    source_folder = os.path.join(os.getcwd(), "data")
    # Dossier cible où les liens symboliques seront créés
    target_folder = os.path.join(os.getcwd(), "sql")

    # Crée le dossier cible s'il n'existe pas
    os.makedirs(target_folder, exist_ok=True)

    print(f"link data from {source_folder} to {target_folder}")
    # Parcourt les fichiers correspondant au motif [0-9]*.sql
    for filepath in glob.glob(os.path.join(source_folder, "[0-9]*.sql")):
        print(f"link {filepath}")
        # Obtient le nom de base du fichier
        basename = os.path.basename(filepath)
        # Construit le chemin cible avec le préfixe "5_"
        target_path = os.path.join(target_folder, f"5_{basename}")
        
        # Construit le chemin relatif du fichier source par rapport au dossier cible
        relative_path = os.path.relpath(filepath, start=target_folder)
        source_path = os.path.join(source_folder , basename)
        
        # Crée ou met à jour le lien symbolique
        try:
            if os.path.exists(target_path):  # Supprime le lien existant s'il est déjà présent
                os.remove(target_path)
            if os.name == 'nt':
                shutil.copy(source_path, target_path)
            else:
                os.symlink(relative_path, target_path)
                
            print(f"{GREEN}Created symlink: {target_path} -> {source_path}{NC}")
        except OSError as e:
            print(f"{RED}Error creating symlink for {filepath}: {e}{NC}")

if __name__ == "__main__":
    main()
