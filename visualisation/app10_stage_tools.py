from dotenv import load_dotenv
import os
import mysql
import pandas as pd
import requests
import io

load_dotenv()

def get_etudiants_by_promo(cur, id_promo) : 
    cur.execute(f"SELECT id_etudiant, nom, prenom FROM LNM_etudiant as etu JOIN LNM_promo as promo ON etu.id_promo=promo.id_promo WHERE etu.id_promo = {id_promo};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["id_etudiant", "nom", "prenom"])
    return data

def get_etudiant_stage(cur, id_promo, noms_etudiant) : 
    cur.execute(f"SELECT etu.id_etudiant, nom, prenom, stage.id_stage FROM LNM_etudiant as etu JOIN LNM_promo as promo ON etu.id_promo=promo.id_promo JOIN LNM_stage as stage ON stage.id_etudiant=etu.id_etudiant WHERE etu.id_promo = {id_promo};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["id_etudiant", "nom", "prenom", "stage"])
    
    stages = []
    for nom in noms_etudiant:
        if nom in data['nom'].values:
            # Vérifier si l'étudiant a un stage
            stage_value = data.loc[data['nom'] == nom, 'stage'].values[0]
            stages.append(1 if pd.notna(stage_value) else 0)
        else:
            # Si l'étudiant n'est pas trouvé dans data, ajouter 0
            stages.append(0)
    
    return stages

def get_eleves_sans(stages, noms):
    eleves_sans=[]
    for i in range (0, len(noms)):
        if (stages[i] == 0):
            eleves_sans.append(noms[i])
    return eleves_sans

def get_stages():
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStages.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def get_stages_by_supervisorId(supervisorId):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStagesEnseignant.php'
    resp = requests.post(url, data={'id_enseignant':supervisorId}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_stages_by_studentId(studentId):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStagesEtudiant.php'
    resp = requests.post(url, data={'id_etudiant':studentId}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def get_stages_with_supervisorId():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStagesWithSupervisor.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_stages_without_supervisorId():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStagesWithOutSupervisor.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_students_without_stage():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStagesStudentsWithOutStage.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def add_stage(entreprise, sujet, mission, ville, start_date, end_date, id_etudiant, id_enseignant):
    print(id_etudiant, entreprise, sujet, mission, start_date, end_date, id_enseignant, flush=True)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/create/createStage.php'
    resp = requests.post(url, data={'entreprise':entreprise,
                                    'sujet':entreprise,
                                    'mission':entreprise,
                                    'ville':ville,
                                    'start_date':start_date,
                                    'end_date':end_date,
                                    'id_etudiant': id_etudiant,
                                    'id_enseignant':id_enseignant}, headers=headers)
    urlData = resp.content
    return urlData.decode('utf-8')