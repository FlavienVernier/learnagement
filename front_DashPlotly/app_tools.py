from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io
import json

from requests import HTTPError, Timeout, RequestException

load_dotenv()

def get_endpoint_data(url, data=None, token=None):
    if data is None:
        data = {}
    if token:
        return get_endpoint(url, data, token)
    else:
        return get_PHP_endpoint_data(url, data)

def get_python_backend_url(endpoint):
    base_url = os.getenv("PYTHON_BACKEND_DOCKER_URL")
    port = os.getenv("PYTHON_BACKEND_DOCKER_PORT")
    url = f"{base_url}:{port}/{endpoint}"
    return url

def get_endpoint(url, data, token):
    return get_python_endpoint_data('get', url, data, token)

def patch_endpoint(url, data, token):
    return get_python_endpoint_data('patch', url, data, token)

def get_python_endpoint_data(method, url, data, token):
    """
    Appel de l'API FastAPI

    Args:
        token: Token d'authentification (JWT)

    Returns:
        DataFrame avec les résultats de la requête

    Raises:
        HTTPError: Si le token est invalide (401) ou accès refusé (403)
        RequestException: Pour les autres erreurs réseau
    """

    try:


        # Appel au "endpoint" (pas besoin de body car tout est dans la dépendance)
        if method == 'get':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'
            }
            resp = requests.get(url, headers=headers, params=data, timeout=30)
        elif method == 'patch':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            resp = requests.patch(url, headers=headers, json=data, timeout=30)
        else:
            return pd.DataFrame()

        # Gérer les erreurs HTTP immédiatement après la requête
        if resp.status_code == 401:
            raise HTTPError("Token invalide ou expiré", response=resp)
        elif resp.status_code == 403:
            raise HTTPError("Accès refusé - L'utilisateur n'a pas le rôle requis", response=resp)

        # Gérer les erreurs HTTP
        resp.raise_for_status()

        # Parser la réponse en DataFrame
        json_string = resp.content.decode('utf-8')
        #print(json_string, flush=True)
        if json_string != "[]":
            url_data = json.loads(json_string)
            #print(url_data, flush=True)
            return pd.read_json(io.StringIO(url_data))
        else:
            return pd.DataFrame()

    except Timeout:
        print(f"Timeout lors de l'appel à {url}")
        return pd.DataFrame()
        raise

    except RequestException as e:
        print(f"Erreur de connexion: {e}")
        return pd.DataFrame()
        raise

    except ValueError as e:
        print(f"Erreur lors du parsing de la réponse JSON: {e}")
        return pd.DataFrame()
        raise

    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return pd.DataFrame()
        raise

def get_php_backend_url(endpoint):
    base_url_with_port = os.getenv("PHP_BACKEND_DOCKER_URL")
    url = f"{base_url_with_port}/{endpoint}"
    return url

def get_PHP_endpoint_data(url, data):
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
