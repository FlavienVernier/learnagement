import os
import glob

def main():
    # Dossier source contenant les fichiers .sql
    source_folder = "./data"
    # Dossier cible où les liens symboliques seront créés
    target_folder = os.path.join(os.getcwd(), "sql")

    # Crée le dossier cible s'il n'existe pas
    os.makedirs(target_folder, exist_ok=True)

    # Parcourt les fichiers correspondant au motif [0-9]*.sql
    for filepath in glob.glob(os.path.join(source_folder, "[0-9]*.sql")):
        # Obtient le nom de base du fichier
        basename = os.path.basename(filepath)
        # Construit le chemin cible avec le préfixe "5_"
        target_path = os.path.join(target_folder, f"5_{basename}")
        
        # Construit le chemin relatif du fichier source par rapport au dossier cible
        relative_path = os.path.relpath(filepath, start=target_folder)

        # Crée ou met à jour le lien symbolique
        try:
            if os.path.exists(target_path):  # Supprime le lien existant s'il est déjà présent
                os.remove(target_path)
            os.symlink(relative_path, target_path)
            print(f"Created symlink: {target_path} -> {relative_path}")
        except OSError as e:
            print(f"Error creating symlink for {filepath}: {e}")

if __name__ == "__main__":
    main()
