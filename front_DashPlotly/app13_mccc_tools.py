from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()

def get_list_enseignants_responsabilites(token):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url("//enseignant_responsabilite/"),
        token=token)
    return df


def get_list_modules_m2c3(token, id_filiere, id_statut):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url("/m2c3/"),
        data={'id_filiere': id_filiere,
              'id_statut': id_statut},
        token=token)
    return df


def set_modules_responsable(token, id_module, id_responsable):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/module/{id_module}/"),
        data={'id_responsable':id_responsable},
        token=token)
    return df
