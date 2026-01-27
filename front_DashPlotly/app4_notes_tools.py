import sys

from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io
import math

load_dotenv()


def calcul_informations(notes_promo: pd.Series, note_eleve=None):
    # calcul des informations
    # on récupère seulement les notes :

    # notes_promo=[eleve['note'] for eleve in notes_promo]

    if note_eleve == None:
        note_eleve = notes_promo[0]


    #ordre_notes = [round(val, 2) for val in sorted(notes_promo, reverse=True)]
    ordre_notes = notes_promo.sort_values().round().reset_index(drop=True)
    classement = ordre_notes[ordre_notes == round(note_eleve)].index[0]

    #moyenne = statistics.mean(notes_promo)
    moyenne = notes_promo.mean()
    #mediane = statistics.median(notes_promo)
    mediane = notes_promo.median()

    #ecart_type = statistics.pstdev(notes_promo)
    ecart_type = notes_promo.std()

    print(moyenne, mediane, ecart_type, flush=True)

    print(type(notes_promo), flush=True)

    X_notes = list(range(21))  # liste qui va de 0 à 20
    #Y_notes = [0] * len(X_notes)  # initialisation de la liste
    Y_notes = notes_promo.round().to_list()



    # for note in notes_promo:
    #     note_arrondie = math.floor(note)
    #     Y_notes[note_arrondie] += 1

    couleur = ['#007bff' if math.floor(i) != math.floor(note_eleve) else '#D10065' if i < 10 else '#65D100' for i in
               X_notes]

    return classement, moyenne, mediane, ecart_type, X_notes, Y_notes, couleur

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
