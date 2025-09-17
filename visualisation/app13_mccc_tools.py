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
    print(urlData, flush=True)
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))
