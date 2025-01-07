# -*- coding: utf-8 -*-
"""
@author: Axelle ROY
"""

### import des bibliothèques ###
import csv
import getpass
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
import lien_db
import re

chromedriver_autoinstaller.install()
driver=webdriver.Chrome()

# définition de l'url à scrapper
url_connexion="https://www.polytech.univ-smb.fr/intranet/accueil.html"
driver.get(url_connexion)
html_connexion=driver.page_source
soup=bs(html_connexion, "lxml")

# connexion à la page :
username=driver.find_element(By.ID, "user")
password=driver.find_element(By.NAME, "pass")

# récupération de l'identifiant et du mot de passe
"""
# partie où l'identifiant et le mot de passe sont récupéré automatiquement depuis un fichier texte
login="logs.txt"
with open(login, 'r') as fichier :
    lines=fichier.readlines()
    id=lines[0]
    mdp=lines[1]
"""
# partie où on demande de rentrer son identifiant et son mot de passe
id=input("Entrez votre identifiant :")
mdp=getpass.getpass("Entrez votre mot de passe (l'affichage est caché): ")
email=input("Entrez votre email :")

# on envoie les identifiants et mots de passe dans la page
username.send_keys(id)
password.send_keys(mdp)

# on valide les informations rentrées
password.send_keys(Keys.RETURN)
time.sleep(2)

# on recharge la page espace-personnel :
url="https://www.polytech.univ-smb.fr/intranet/pages-speciales/espace-etudiants/espace-personnel.html"
driver.get(url)
html=driver.page_source
soup=bs(html, "lxml")
valeurs=soup.find_all('div', class_='value')

# scraping des polypoints
informations_polypoint=[]
for point in valeurs :
# grâce au print, on a vu que la class "value" contenait les polypoints et les stages effectués. 
# il faut donc générer une exception quand on a pas les intitulés de classes qu'on recherche 
    try :
        intitule=point.find('li', class_='intitule').text
        tache=point.find('li', class_='intitule_tache').text
        nb_points=point.find('li', class_='nb_points').text
        annee=point.find('li', class_='annee').text
        informations_polypoint.append([intitule, tache,  nb_points, annee, email])
    except:
        # quand on a pas les informations liées aux polypoints, on ne fait rien
        pass

# scraping des stages
informations_stage=[]
for point in valeurs :
# grâce au print, on a vu que la class "value" contenait les polypoints et les stages effectués. 
# il faut donc générer une exception quand on a pas les intitulés de classes qu'on recherche 
    try :
        #Le scrapping des stages ne fonctionne pas
        entreprise_temp=point.find('li', class_='entreprise').text
        entreprise=entreprise_temp.split(' - ')[0]
        ville=entreprise_temp.split(' - ')[1]
        date=point.find('li', class_='date').text
        # Expression régulière pour trouver les dates au format jj/mm/aaaa
        pattern = r'\d{2}/\d{2}/\d{4}'

        # Utilisation de findall pour extraire toutes les dates correspondant au pattern
        dates = re.findall(pattern, date)
        annee=dates[0].split('/')[2]
        mois=dates[0].split('/')[1]
        jour=dates[0].split('/')[0]
        date_debut=""+annee+"-"+mois+"-"+jour
        annee=dates[1].split('/')[2]
        mois=dates[1].split('/')[1]
        jour=dates[1].split('/')[0]
        date_fin=""+annee+"-"+mois+"-"+jour
        nature='null'
        mail=email
        id_enseignant=6   #id random (présent dans la liste)
        informations_stage.append([entreprise, ville, date_debut, date_fin, nature, mail, id_enseignant])
    except:
        # quand on a pas les informations liées aux polypoints, on ne fait rien
        pass
    
print(informations_stage)
    
driver.close()
# enregistrement des informations dans la base de donnée

bd=lien_db.get_db()
#enregistrement des polypoints
'''for info in informations_polypoint:
    intitule=info[0]
    tache=info[1]
    nb_points=info[2]
    annee=info[3]
    email=info[4]
    query= f"INSERT INTO ETU_polypoint (intitule, tache, nb_point, annee_universitaire, id_etudiant) SELECT '{intitule}', '{tache}', '{nb_points}', '{annee}', (SELECT id_etudiant FROM LNM_etudiant WHERE mail='{email}');"
    print(query)
    lien_db.execute_query(bd,query)

print(lien_db.get_data(bd,"ETU_polypoint"))'''

#enregistrement des stages
for info in informations_stage:
    entreprise=info[0]
    ville=info[1]
    date_debut=info[2]
    date_fin=info[3]
    nature=info[4]
    email=info[5]
    id_enseignant=info[6]

    query= f"INSERT INTO LNM_stage (entreprise, ville, date_debut, date_fin, nature, id_etudiant, id_enseignant) SELECT '{entreprise}', '{ville}', '{date_debut}', '{date_fin}', '{nature}', (SELECT id_etudiant FROM LNM_etudiant WHERE mail='{email}'), '{id_enseignant}';"
    print(query)
    print(lien_db.execute_query(bd,query))

print(lien_db.get_data(bd,"LNM_stage"))

lien_db.close_db(bd)