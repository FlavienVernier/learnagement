import getpass
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time
import chromedriver_autoinstaller
import csv

import lien_db

url='https://www.polytech.univ-smb.fr/intranet/accueil.html'

#Ouverture de la page web
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

driver.get(url)

html = driver.page_source

soup= bs(html, 'html.parser')

#Connexion
username=driver.find_element(By.ID,'user')
password=driver.find_element(By.NAME,'pass')

#Récuperation information 
# partie où on demande de rentrer son identifiant et son mot de passe
id=input("Entrez votre identifiant :")
mdp=getpass.getpass("Entrez votre mot de passe (l'affichage est caché): ")

# on envoie les identifiants et mots de passe dans la page
username.send_keys(id)
password.send_keys(mdp)

# on valide les informations rentrées
password.send_keys(Keys.RETURN)
time.sleep(2)

#Aller à la page programme
soup =bs(driver.page_source, "lxml")
lien=soup.find(title="Accéder aux programmes")["href"]
driver.get("https://www.polytech.univ-smb.fr"+lien)

soup= bs(driver.page_source, 'html.parser')

#Récupération des disciplines
recup_disciplines=soup.find('select',id="discipline")
disciplines=[]
for elt in (recup_disciplines):
    if elt!='\n':  #enlever les \n collés aux noms des disciplines
        if elt.get_text()!='---':  #e,elevr les premier elt qui n'est pas une discipline (ne peut pas être fait avec un if and)
            disciplines.append(elt.get_text())
            #Mettre cette ligne pour csv
            #disciplines.append([elt.get_text()])
            
driver.close()

# # Sauvegarde des données en csv
# with open("disciplines.csv", "wt+", newline="") as f:
#     writer = csv.writer(f,delimiter=',')
#     for row in disciplines:
#         writer.writerow(row)
        
#Sauvegarde des données dans la bd
bd=lien_db.get_db()
for elt in (disciplines):
    query= f"INSERT INTO MAQUETTE_discipline (nom) VALUES ('{elt}')"
    print(query)
    lien_db.execute_query(bd,query)

print(lien_db.get_data(bd,"MAQUETTE_discipline"))
lien_db.close_db(bd)
