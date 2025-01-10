import getpass
import re
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from lien_db import get_db, execute_query, get_data, close_db

# Connexion à la base de données et initialisation de la requête
db=get_db()
query = ""

chromedriver_autoinstaller.install()

url=f"https://www.polytech.univ-smb.fr/intranet/accueil.html"
driver = webdriver.Chrome()

# Accéder à la page de connexion
driver.get(url)

username=driver.find_element(By.ID, "user")
password=driver.find_element(By.NAME, "pass")
# partie où on demande de rentrer son identifiant et son mot de passe
id=input("Entrez votre identifiant :")
mdp=getpass.getpass("Entrez votre mot de passe (l'affichage est caché): ")

# on envoie les identifiants et mots de passe dans la page
username.send_keys(id)
password.send_keys(mdp)

# on valide les informations rentrées
password.send_keys(Keys.RETURN)
time.sleep(2)
# Attendre un court instant pour permettre à la page de se charger
time.sleep(2)

explore_link = "/intranet/personnels-enseignants.html"
data_final = []

finished = False
while not finished :
    try:
        driver.get(f"https://www.polytech.univ-smb.fr{explore_link}")
    except WebDriverException:
        print("page down")

    data = []

    try:
        soup = bs(driver.page_source, "lxml")
        
        try:
            # Récupérer le lien de la page suivante pour continuer la récupération des données des enseignants
            explore_link =  soup.find("a",href=re.compile("nextPage"))["href"]
            if "https" in explore_link:
                explore_link = explore_link.replace("https://www.polytech.univ-smb.fr","")
        except:
            finished = True
            print("exception pas de page suivante")
        
        data = soup.find_all(class_="info")
        
        for personne in data:
            # Récupérer les informations de chaque personne
            nom_prenom = personne.find(class_="name").text         
            telephones = personne.find(class_="telephones").text
            bureaux = personne.find(class_="bureaux").text
            email = personne.find(class_="email").text

            nom = nom_prenom.split(" ")[0]
            prenom = nom_prenom.split(" ")[1]
            liste_bureaux = bureaux[6:].split("\n")
            email = email[6:]
            password='null'
            password_updated='null'
            statut='null'
            id_discipline='null'
            composante='null'
            service_statutaire='null'
            décharge='null'
            service_effectif='null'
            HCAutorisées='null'
            fullName='null'
            commentaire='null'

            # Ajouter les informations à la requête sql
            query += f"INSERT INTO LNM_enseignants (prenom, nom, mail, password, password_updated, statut, id_discipline, composante, service statutaire, décharge, service effectif, HCAutorisées, fullName, commentaire) VALUES ('{nom}', '{prenom}','{email}', '{password}', '{password_updated}', '{statut, id_discipline}', '{composante}', '{service_statutaire}', '{décharge}', '{service_effectif}', '{HCAutorisées}', '{fullName}', '{commentaire}');\n"

    except Exception as e:
        print(f"Une exception s'est produite : {e}")
        
# Fermer le navigateur
driver.quit()

# Execute la requête pour ajouter les données dans la base de données
for i in query.split("\n"):
    if i != "":
        print(i)
        print(execute_query(db, i))
close_db(db)

print("done")
