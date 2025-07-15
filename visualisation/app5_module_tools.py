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