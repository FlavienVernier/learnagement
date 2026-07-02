from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()


def get_moduleByEnseignantId(token, id_enseignant: int):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/responsables/{id_enseignant}/"),
        token = token
    )
    return df

def get_moduleByEtudiantId(token, id_etudiant: int):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/etudiants/{id_etudiant}/"),
        token = token
    )
    return df

def get_moduleByIntervenantId(token, id_enseignant: int):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/intervenants/{id_enseignant}/"),
        token = token
    )
    return df

######################
# Sequencage

def get_moduleSequencageByEnseignantId(token, id_enseignant: int):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/sequencages/{id_enseignant}/"),
        token = token
    )
    return df

def add_moduleSequencage(token, data):
    df = app_tools.post_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{data['id_module']}/sequencage"),
        data = data,
        token = token
    )
    return df



def remove_moduleSequencage(token, id_module: int, id_sequencage: int):
    df = app_tools.delete_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequencages/{id_sequencage}"),
        token = token
    )
    return df

def set_intervenant_principal_sequencage(token, id_module: int, id_sequencage: int, id_intervenant_principal: int):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequencages/{id_sequencage}/"),
        data = {'id_intervenant_principal': id_intervenant_principal},
        token = token
    )
    return df

def reset_intervenant_principal_sequencage(token, id_module: int, id_sequencage: int):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequencages/{id_sequencage}/"),
        data = {'id_intervenant_principal': None},
        token = token
    )
    return df

def check_moduleSequencage(token, id_enseignant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/maquette_vs_sequencage/{id_enseignant}/"),
        token=token
    )
    return df

######################
# Sequence

def get_moduleSequenceByEnseignantId(token, id_responsable):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/modules/sequences/{id_responsable}/"),
        token=token
    )
    return df

def set_intervenant_principal_sequence(token, id_module, id_sequence, id_intervenant_principal):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequences/{id_sequence}/"),
        data = {'id_intervenant_principal': id_intervenant_principal},
        token = token
    )
    return df


def reset_intervenant_principal_sequence(token, id_module, id_sequence):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequences/{id_sequence}/"),
        data = {'id_intervenant_principal': None},
        token = token
    )
    return df

######################
# Session

def get_moduleSessionByEnseignantId(token, id_responsable):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/modules/sessions/{id_responsable}/"),
        token=token
    )
    return df

def set_intervenant_session(token, id_module, id_session, id_intervenant):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sessions/{id_session}/"),
        data = {'id_enseignant': id_intervenant},
        token = token
    )
    return df

def reset_intervenant_session(token, id_module, id_session):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sessions/{id_session}/"),
        data = {'id_enseignant': None},
        token = token
    )
    return df
