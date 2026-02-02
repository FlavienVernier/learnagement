from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

load_dotenv()

def get_endpoint(url, data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    resp = requests.post(
        url,
        data=data,
        headers=headers
    )

    resp.raise_for_status()  # sécurité HTTP

    json_data = resp.json()  # ← parsing JSON propre

    # Cas [] ou null
    if not json_data:
        df = pd.DataFrame()
    else :
        #df = pd.DataFrame.from_records(json_data) # do not use int stay as str
        # conversion intelligente des types
        #df = df.convert_dtypes() # does not solve the problem
        df = pd.read_json(io.StringIO(resp.content.decode('utf-8')))


    # print("Status code:", resp.status_code)
    # print("Raw text:", repr(resp.text))
    # print("Parsed JSON:", resp.json())
    # print("Type:", type(resp.json()))
    #
    # print("url", url)
    # print("data", data)
    # print("json_data", json_data)
    # print("df", df, flush=True)
    return df

def get_list_enseignants():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEnseignant.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_list_filieres():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listAllFilieres.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_list_statuts():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listStatut.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_list_promo():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listPromo.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_explicit_keys(table):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/explicitSecondaryKeys.php'
    resp = requests.post(url, data={'table':table}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))
