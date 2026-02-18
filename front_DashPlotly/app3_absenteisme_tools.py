from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

import app_tools

load_dotenv()

def get_absences(token, id_responsable=None, id_enseignant=None, id_etudiant=None):
    if id_enseignant:
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/absences/")
    else:
        url = app_tools.get_python_backend_url(f"/etudiants/absences/")
    df = app_tools.get_endpoint_data(
        url,
        data={'id_responsable': id_responsable,
              'id_enseignant': id_enseignant,
              'id_etudiant': id_etudiant},
        token=token)
    return df

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listAbsence.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_absenceByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listAbsenceByEnseignantId.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def get_absenceByResponsableId(id_responsable):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listAbsenceByResponsableId.php'
    resp = requests.post(url, data={'id_responsable': id_responsable}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def get_absenceByEtudiantId(id_etudiant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listAbsenceByEtudiantId.php'
    resp = requests.post(url, data={'id_etudiant': id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))