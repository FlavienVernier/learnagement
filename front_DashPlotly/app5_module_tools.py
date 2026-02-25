from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

import app_tools

load_dotenv()


def get_moduleByEnseignantId(token, id_enseignant: int):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/modules/responsables/{id_enseignant}/"),
        data = {'id_intervenant': id_enseignant},
        token = token
    )
    return df

def get_moduleByEtudiantId(token, id_etudiant: int):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/modules/etudiants/{id_etudiant}/"),
        data = {'id_etudiant': id_etudiant},
        token = token
    )
    return df

def get_moduleByIntervenantId(token, id_enseignant: int):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/modules/intervenants/{id_enseignant}/"),
        data = {'id_intervenant': id_enseignant},
        token = token
    )
    return df

######################
# Sequencage

def get_moduleSequencageByEnseignantId(token, id_enseignant: int):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/modules/sequencages/{id_enseignant}/"),
        data = {'id_responsable': id_enseignant},
        token = token
    )
    return df

def add_moduleSequencage(token, data):
    df = app_tools.post_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{data['id_module']}/sequencage"),
        data = data,
        token = token
    )
    return df


    # headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    # url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/create/createSequencage.php'
    # resp = requests.post(url, data=data, headers=headers)
    # urlData = resp.content
    # return io.StringIO(urlData.decode('utf-8'))

def remove_moduleSequencage(id_sequencage):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/delete/deleteSequencage.php'
    resp = requests.post(url, data={'id_module_sequencage': id_sequencage}, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))

def set_intervenant_principal_sequencage(id_sequencage, id_intervenant_principal):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/update/setSequencageIntervenantPrincipal.php'
    resp = requests.post(url, data={'id_module_sequencage': id_sequencage, 'id_intervenant_principal': id_intervenant_principal }, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))


def check_moduleSequencage(token, id_enseignant):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/maquette_vs_sequencage/{id_enseignant}/"),
        data = {'id_responsable': id_enseignant},
        token=token
    )
    return df

######################
# Sequence

def get_moduleSequenceByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleSequence.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def set_intervenant_principal_sequence(id_sequence, id_intervenant_principal):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/update/setSequenceIntervenantPrincipal.php'
    resp = requests.post(url, data={'id_module_sequence': id_sequence, 'id_intervenant_principal': id_intervenant_principal }, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))

######################
# Session

def get_moduleSessionByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listSessionEnseignant.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def set_intervenant_session(id_session, id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/update/setSessionIntervenant.php'
    resp = requests.post(url, data={'id_session': id_session, 'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))
