from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io
import plotly.express as px

load_dotenv()

# Palette originale
original_palette = px.colors.qualitative.Alphabet

# Retirer une couleur (ex : '#FFB5E8')
custom_palette = [c for c in original_palette if c.lower() != '#85660d']

def get_chargeByEnseignantId(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesChargeEnseignant.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def get_chargeByEtudianttId(id_etudiant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesChargeEtudiant.php'
    resp = requests.post(url, data={'id_etudiant': id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))