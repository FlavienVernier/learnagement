from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io
import plotly.express as px

load_dotenv()


def get_renduByEtudianttId(id_etudiant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listRenduEtudiant.php'
    resp = requests.post(url, data={'id_etudiant': id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))