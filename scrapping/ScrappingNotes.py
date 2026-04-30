from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as bs

import json

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

driver.get("https://cas-uds.grenet.fr/login") #lien pour la connexion

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

login = open("learnagement_tests/login.txt").readlines() # va chercher le mot de passe dans un autre fichier

username.send_keys(login[0])
password.send_keys(login[1])

driver.find_element(By.XPATH,"//button[@type='submit']").click()

driver.get("https://rvn.grenet.fr/uds/") #lien pour accéder au relevé de notes
soup = bs(driver.page_source,"html.parser")

data = []
UE = {}
table_rows = soup.find("table",id="tableau").find_all("tr")
index = 1
while index < len(table_rows)-1:
    row = table_rows[index].find_all("td")

    epreuve = row[0].text.replace("\n								    ","")
    for i in range(1, len(row)):
        row[i] = row[i].text.replace(" ","")

    if row[0].find("b"):
        if index != 1 : data.append(UE)
        UE = {"Epreuve":epreuve, "Note_dividende":row[1], "Note_diviseur":row[2], "Pts jury":row[3], "Année":row[4], "Session":row[5], "Résultat":row[6], "Crédit":row[7], "Classement":row[8], "Matières":[]}
    
    else:
        UE["Matières"].append({"Epreuve":epreuve, "Note_dividende":row[1], "Note_diviseur":row[2], "Pts jury":row[3], "Année":row[4], "Session":row[5], "Résultat":row[6], "Crédit":row[7], "Classement":row[8]})
    
    index+=1
data.append(UE)

with open("notes.json", "wt+", newline="", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

driver.quit()