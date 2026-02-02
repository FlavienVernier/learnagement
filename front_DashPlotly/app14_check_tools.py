from dotenv import load_dotenv
import os
import pandas as pd
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import io
import json

load_dotenv()

def check_sequencage_vs_maquette():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleSequencageVsMaquette.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def check_module_without_learning_unit():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleWithOutLearningUnit.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def check_module_without_apprentissage_critique():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleWithOutApprentissageCritique.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def check_module_ects():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listModuleECTS.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def check_enseignant_sans_cours():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listEnseignantSansCours.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


def check_session_sans_enseignant():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/check/listSessionSansEnseignant.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def check_session_corruption(token):
    """
    Vérifie la corruption de session via l'API FastAPI

    Args:
        token: Token d'authentification (JWT)

    Returns:
        DataFrame avec les résultats de la requête

    Raises:
        HTTPError: Si le token est invalide (401) ou accès refusé (403)
        RequestException: Pour les autres erreurs réseau
    """
    #print(token, flush=True)
    url="URL not defined"
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {token}'
        }

        base_url = os.getenv("PYTHON_BACKEND_DOCKER_URL")
        port = os.getenv("PYTHON_BACKEND_DOCKER_PORT")
        url = f"{base_url}:{port}/session_reference_corruption/"

        # Appel au "endpoint" (pas besoin de body car tout est dans la dépendance)
        resp = requests.post(url, headers=headers, timeout=30)

        # Gérer les erreurs HTTP immédiatement après la requête
        if resp.status_code == 401:
            raise HTTPError("Token invalide ou expiré", response=resp)
        elif resp.status_code == 403:
            raise HTTPError("Accès refusé - L'utilisateur n'a pas le rôle 'administratif'", response=resp)

        # Gérer les erreurs HTTP
        resp.raise_for_status()

        # Parser la réponse en DataFrame
        json_string = resp.content.decode('utf-8')
        print(json_string, flush=True)
        if json_string != "[]":
            url_data = json.loads(json_string)
            print(url_data, flush=True)
            return pd.read_json(io.StringIO(url_data))
        else:
            return pd.DataFrame()

    except Timeout:
        print(f"Timeout lors de l'appel à {url}")
        raise

    except RequestException as e:
        print(f"Erreur de connexion: {e}")
        raise

    except ValueError as e:
        print(f"Erreur lors du parsing de la réponse JSON: {e}")
        raise

    except Exception as e:
        print(f"Erreur inattendue: {e}")
        raise