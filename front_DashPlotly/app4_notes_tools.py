from dotenv import load_dotenv
import pandas as pd
import math

import app_tools

load_dotenv()


def calcul_informations(notes_promo: pd.Series, note_eleve=None):
    # calcul des informations
    # on récupère seulement les notes :

    # notes_promo=[eleve['note'] for eleve in notes_promo]

    if note_eleve == None:
        note_eleve = notes_promo.iloc[0]


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

def get_notes_eleves(token, id_etudiant):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/evaluations/classical/etudiants/{id_etudiant}"),
        token=token
    )
    return df

def get_average_notes_promo(token, id_module):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/evaluations/classical/modules/{id_module}/average/"),
        token=token
    )
    return df

def get_data_promo(token, id_module):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/evaluations/classical/modules/{id_module}/"),
        token=token
    )
    return df

def get_modules_byIdEtudiant(token, id_etudiant):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/modules/etudiants/{id_etudiant}/"),
        token=token
    )
    return df

def get_data_prof(token, id_enseignant):
    df = app_tools.get_endpoint(
        url=app_tools.get_python_backend_url(f"/evaluations/classical/enseignants/{id_enseignant}"),
        token=token
    )
    return df
