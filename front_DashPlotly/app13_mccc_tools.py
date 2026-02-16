from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

import app_tools

load_dotenv()

def get_list_enseignants_responsabilites(token):
    url = app_tools.get_python_backend_url("//enseignant_responsabilite/")
    df = app_tools.get_endpoint_data(url, token=token)
    return df


def get_list_modules_m2c3(token, id_filiere, id_statut):
    url = app_tools.get_python_backend_url("/m2c3/")
    df = app_tools.get_endpoint_data(
        url,
        data={'id_filiere': id_filiere,
              'id_statut': id_statut},
        token=token)
    return df


def set_modules_responsable(token, id_module, id_responsable):
    url = app_tools.get_python_backend_url(f"/module/{id_module}/")
    df = app_tools.patch_endpoint(
        url,
        data={'id_responsable':id_responsable},
        token=token)
    return df

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/update/setModuleResponsable.php'
    resp = requests.post(url, data={'id_module':id_module,
                                    'id_responsable':id_responsable},
                            headers=headers)
    urlData = resp.content
    return io.StringIO(urlData.decode('utf-8'))
