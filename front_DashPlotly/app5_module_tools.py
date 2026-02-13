from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

import app_tools

load_dotenv()


def get_moduleByEnseignantId(id_enseignant):

    df1 = app_tools.get_endpoint_data(
        url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesResponsable.php',
        data = {'id_enseignant': id_enseignant}
    )
    # headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    # url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesResponsable.php'
    # resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    # urlData = resp.content
    # df2 = pd.read_json(io.StringIO(urlData.decode('utf-8')))
    #
    # print("df1 shape:", df1.shape)
    # print("df1 columns:", df1.columns)
    # print("df1 dtypes:\n", df1.dtypes)
    #
    # print("df2 shape:", df2.shape)
    # print("df2 columns:", df2.columns)
    # print("df2 dtypes:\n", df2.dtypes)

    return df1
    #return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_moduleByEtudiantId(id_etudiant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesEtudiant.php'
    resp = requests.post(url, data={'id_etudiant': id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_moduleByIntervenantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listSessionIntervenant.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_moduleSequencageByEnseignantId(id_enseignant):
    # return app_tools.get_endpoint(
    #     url=os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleSequencage.php',
    #     data={'id_enseignant': id_enseignant},
    # )
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleSequencage.php'
    resp = requests.post(
        url,
        data={'id_enseignant': id_enseignant},
        headers=headers
    )

    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def add_moduleSequencage(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/create/createSequencage.php'
    resp = requests.post(url, data=data, headers=headers)
    urlData = resp.content
    return io.StringIO(urlData.decode('utf-8'))

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


def check_moduleSequencage(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleSequencageVsMaquetteByIdResp.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    #print(urlData, flush=True)
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

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
