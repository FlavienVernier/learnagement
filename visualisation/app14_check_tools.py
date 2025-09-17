from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

load_dotenv()

def check_sequencage_vs_maquette():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleSequencageVsMaquette.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    print(urlData, flush=True)
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def check_module_without_learning_unit():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleWithOutLearningUnit.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    print(urlData, flush=True)
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))