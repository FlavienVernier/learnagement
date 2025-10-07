from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

load_dotenv()

def get_list_dependance_by_idModule(id_module):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleDependance.php'
    resp = requests.post(url, data={'id_module':id_module}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_list_sequence_dependance_by_idModule(id_module):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModuleSequenceDependance.php'
    resp = requests.post(url, data={'id_module':id_module}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))
