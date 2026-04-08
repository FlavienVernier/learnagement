import logging
import sys

from dotenv import load_dotenv
import os
from warnings import deprecated
import pandas as pd
import requests
import io
import json

from requests import HTTPError, Timeout, RequestException

load_dotenv()

def get_python_backend_url(endpoint):
    base_url = os.getenv("PYTHON_BACKEND_DOCKER_URL")
    port = os.getenv("PYTHON_BACKEND_DOCKER_PORT")
    url = f"{base_url}:{port}/{endpoint}"
    return url

def get_endpoint(url, token, data=None):
    return python_endpoint('get', url, data, token)

def patch_endpoint(url, data, token):
    return python_endpoint('patch', url, data, token)

def post_endpoint(url, data, token):
    return python_endpoint('post', url, data, token)

def delete_endpoint(url, token):
    return python_endpoint('delete', url, None, token)

def python_endpoint(method, url, data, token):
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
        if data:
            logging.info(f"Calling {method} {url} {data}")
        else:
            logging.info(f"Calling {method} {url}")
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
        elif method == 'post':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            resp = requests.post(url, headers=headers, json=data, timeout=30)
        elif method == 'delete':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'
            }
            resp = requests.delete(url, headers=headers, timeout=30)
        else:
            raise Exception(f"Method {method} not supported")

        # Gérer les erreurs HTTP immédiatement après la requête
        if resp.status_code == 401:
            raise HTTPError("Token invalide ou expiré", response=resp)
        elif resp.status_code == 403:
            raise HTTPError("Accès refusé - L'utilisateur n'a pas le rôle requis", response=resp)

        # Gérer les erreurs HTTP
        resp.raise_for_status()

        # Parser la réponse received as string en DataFrame
        #json_string = resp.content.decode('utf-8')
        #print(json_string, flush=True)
        #f json_string != "[]":
        #    url_data = json.loads(json_string)
        #    return pd.read_json(io.StringIO(url_data))
        #else:
        #    return pd.DataFrame()

        # Parser la réponse JSON
        data = resp.json()

        if data:
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()


    except Timeout as e:
        logging.exception(f"Timeout lors de l'appel à {url}")
        #return pd.DataFrame()
        raise e

    except RequestException as e:
        logging.exception(f"Erreur de connexion: {e}")
        #return pd.DataFrame()
        raise e

    except ValueError as e:
        logging.exception(f"Erreur lors du parsing de la réponse JSON: {e}")
        #return pd.DataFrame()
        raise e

    except Exception as e:
        logging.exception(f"Erreur inattendue: {e}")
        #return pd.DataFrame()
        raise e


def get_enseignants(token):
    url = get_python_backend_url("/enseignants/")
    df = get_endpoint(url, token=token)
    return df

def get_etudiants(token):
    url = get_python_backend_url("/etudiants/")
    df = get_endpoint(url, token=token)
    return df

def get_filieres(token):
    url = get_python_backend_url("/filieres/")
    df = get_endpoint(url, token=token)
    return df

def get_statuts(token):
    url = get_python_backend_url("/statuts/")
    df = get_endpoint(url, token=token)
    return df

def get_promos(token):
    url = get_python_backend_url("/promos/")
    df = get_endpoint(url, token=token)
    return df

def get_groupe_types(token):
    url = get_python_backend_url("/groupe_types/")
    df = get_endpoint(url, token=token)
    return df

def get_seance_types(token):
    url = get_python_backend_url("/seance_types/")
    df = get_endpoint(url, token=token)
    return df
