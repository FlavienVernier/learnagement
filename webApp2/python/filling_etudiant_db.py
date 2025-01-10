import lien_db 
import csv
#http://gpu-epu.univ-savoie.fr:48080/
#creation de la table dans la base de données si elle n'existe pas déjà
query ="CREATE TABLE IF NOT EXISTS TEST_etudiant(id_etudiant INT NOT NULL AUTO_INCREMENT,nom VARCHAR(255),prenom VARCHAR(255),annee VARCHAR(255),filiere VARCHAR(12),PRIMARY KEY (id_etudiant))"
#voir avec les contraintes pour la suite

#TODO : code à reprendre entièrement => ne fonctionne pas avec la BDD

db = lien_db.get_db()
print(lien_db.execute_query(db,query))

# Ouvrir le fichier CSV en mode lecture
with open('liste_etudiants.csv', 'r') as fichier:
    # Créer un lecteur CSV à partir du fichier
    lecteur = csv.reader(fichier, delimiter=',')

    # Parcourir toutes les lignes du fichier CSV
    for ligne in lecteur:
        # Récupérer le nom et le prénom à partir de la ligne courante
        if ligne[0]=='FI1':
            annee = 1
        elif ligne[0]=='FI2':
            annee = 2
        elif ligne[0]=='FI3':
            annee = 3
        elif ligne[0]=='FI4' or ligne[0]=='M1':
            annee = 4
        elif ligne[0]=='FI5' or ligne[0]=='M2':
            annee = 5
        if ligne[1]=='PEIP-A2' or ligne[1]=='PEIP-A1':
            filiere = 'PEIP-A'
        elif ligne[1]=='MECA':
            filiere='MM'
        else : 
            filiere = ligne[1]
        nom = ligne[2]
        prenom = ligne[3]
        # Afficher le nom et le prénom
        print("annee :", annee)
        print("filiere :", filiere)
        #print("nom :", nom)
        #print("Prénom :", prenom)

         #insertion d'elt de la table 
         
        # Pour ajouter un étudiant : INSERT INTO LNM_etudiant ('nom', 'prenom', 'mail', 'pswd') VALUES ('{nom}','{prenom}',
        # il manque id_promo : id_filiere = SELECT id_filiere FROM LNM_filiere WHERE nom_filiere=filiere
        # puis SELECT id_promo FROM LNM_promo WHERE LNM_promo.id_filiere=id_filiere AND LNM_promo.annee=annee
        
        id_promo = f"SELECT id_promo FROM LNM_promo WHERE LNM_promo.id_filiere=(SELECT id_filiere FROM LNM_filiere WHERE nom_filiere='{filiere}') AND LNM_promo.annee='{annee}'"
        promo=lien_db.get_data(db,id_promo, "LNM_promo")
        print(promo)
        
        '''
        email=prenom+"."+nom+"@etu.univ-smb.fr"
        query = f"INSERT INTO LNM_etudiant(`nom`, `prenom`, `mail`, `password` , `id_promo`) VALUES ('{nom}','{prenom}', '{email}', null, '{promo}')"
        
        lien_db.execute_query(db,query)'''
        #print(lien_db.execute_query(db,query))
        
    print("fini")