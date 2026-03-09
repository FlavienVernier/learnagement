from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()

def get_absences(token, id_responsable=None, id_enseignant=None, id_etudiant=None):
    if id_etudiant:
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/absences/")
    else:
        url = app_tools.get_python_backend_url(f"/etudiants/absences/")
    df = app_tools.get_endpoint(
        url,
        data={'id_responsable': id_responsable,
              'id_enseignant': id_enseignant,
              },
        token=token)
    return df
