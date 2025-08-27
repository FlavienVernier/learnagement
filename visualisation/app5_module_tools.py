from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

load_dotenv()


def get_moduleByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesResponsable.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_moduleByIntervenantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listSessionIntervenant.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_moduleSequencageByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleSequencage.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def add_moduleSequencage(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/create/createSequencage.php'
    resp = requests.post(url, data=data, headers=headers)
    urlData = resp.content
    print(urlData, flush=True)
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
    print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))


def check_moduleSequencage(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleSequencageVsMaquette.php'
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
    print(urlData, flush=True)
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
    print(urlData, flush=True)
    return io.StringIO(urlData.decode('utf-8'))
#
# def headers(df : pd.DataFrame) -> list:
#     return [ft.DataColumn(ft.Text(header)) for header in df.columns]
#
# def rows(df : pd.DataFrame) -> list:
#     rows = []
#     for index, row in df.iterrows():
#         rows.append(ft.DataRow(cells = [ft.DataCell(ft.Text(row[header])) for header in df.columns]))
#     return rows