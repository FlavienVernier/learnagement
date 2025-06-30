from dotenv import load_dotenv
import os
import mysql
import pandas as pd
import requests
import io


load_dotenv()


def get_notes_eleves(id_etudiant):
    # cur.execute(f"SELECT evaluation, id_etudiant, module.nom  FROM ETU_classical_evaluation as eval JOIN MAQUETTE_module as module ON eval.id_module=module.id_module WHERE eval.id_etudiant={num_etu}")
    #
    # rows = cur.fetchall()
    #
    # # Récupération des données
    # data = pd.DataFrame(rows, columns=["evaluation", "id_etudiant", "nom_module"])
    # return data

    # id_etudiant not in the following result

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEvaluationEtudiant.php'
    resp = requests.post(url, data={'id_etudiant':id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_average_notes_promo(id_module):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEvaluationModuleAverage.php'
    resp = requests.post(url, data={'id_module':id_module}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_data_promo(id_matiere):
    # cur.execute(
    #     f"SELECT evaluation, id_etudiant, module.nom  FROM ETU_classical_evaluation as eval JOIN MAQUETTE_module as module ON eval.id_module=module.id_module WHERE eval.id_module={id_matiere}")
    #
    # rows = cur.fetchall()
    #
    # # Récupération des données
    # data = pd.DataFrame(rows, columns=["evaluation", "id_etudiant", "nom_module"])
    # return data

    # id_etudiant not in the following result due to anonymous raisons

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset':'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEvaluationModule.php'
    resp = requests.post(url, data={'id_module':id_matiere}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))


# use get_notes_eleves with matiere filter instead
# def get_data_etudiant(id_etudiant, id_matiere):
#     cur.execute(
#         f"SELECT evaluation, id_etudiant, module.nom  "
#         f"FROM ETU_classical_evaluation as eval "
#         f"JOIN MAQUETTE_module as module ON eval.id_module=module.id_module "
#         f"WHERE eval.id_etudiant={num_etu} and eval.id_module={id_matiere}")
#
#     rows = cur.fetchall()
#
#     # Récupération des données
#     data = pd.DataFrame(rows, columns=["evaluation", "id_etudiant", "nom_module"])
#     return data

def get_modules_byIdEtudiant(id_etudiant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listModulesEtudiant.php'
    resp = requests.post(url, data={'id_etudiant': id_etudiant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))

def get_data_prof(id_enseignant):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
    url = os.getenv("PHP_BACKEND_DOCKER_URL") + '/list/listEvaluationEnseignant.php'
    resp = requests.post(url, data={'id_enseignant': id_enseignant}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))
