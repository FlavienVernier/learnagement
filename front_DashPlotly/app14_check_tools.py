from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()

def check_sequencage_vs_maquette(token):

    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url("/maquette_vs_sequencage/"),
        token=token)
    return df

def check_session_vs_maquette(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("maquette_vs_session"),
        token=token)
    return df

def check_module_without_learning_unit(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("module_sans_unite_d_enseignement"),
        token=token)
    return df

def check_module_without_apprentissage_critique(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/module_sans_apprentissage_critique/"),
        token=token)
    return df

def check_module_ects(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/module_detail_ects/"),
        token=token)
    return df

def check_enseignant_sans_cours(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/enseignant_sans_cours/"),
        token=token)
    return df

def check_session_sans_enseignant(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/session_sans_intervenant/"),
        token=token)
    return df

def check_session_corruption(token):
    """
    Vérifie la corruption de session via l'API FastAPI

    Args:
        token: Token d'authentification (JWT)

    Returns:
        DataFrame avec les résultats de la requête or empty dataframe if exception

    Raises:
        HTTPError: Si le token est invalide (401) ou accès refusé (403)
        RequestException: Pour les autres erreurs réseau
    """
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("session_reference_corruption"),
        token=token)
    return df

def get_access_auth(token)->pd.DataFrame:
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("access_auth/"),
        token=token)
    return df


def get_access_auth_tree_sqlglot(token)->dict:
    data = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("access_auth_tree_sqlglot/"),
        token=token)
    return data