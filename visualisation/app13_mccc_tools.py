from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

load_dotenv()

def get_list_enseignants_responsabilites():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEnseignantResponsabilite.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_list_modules_m2c3(id_filiere, id_statut):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/getModulesM2C3.php'
    resp = requests.post(url, data={'id_filiere':id_filiere,
                                    'id_statut':id_statut},
                            headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def set_modules_responsable(id_module, id_responsable):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/update/setModuleResponsable.php'
    resp = requests.post(url, data={'id_module':id_module,
                                    'id_responsable':id_responsable},
                            headers=headers)
    urlData = resp.content
    return io.StringIO(urlData.decode('utf-8'))
