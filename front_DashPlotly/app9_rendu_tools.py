from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()


def get_renduByEtudianttId(token, id_etudiant):
    df = app_tools.get_endpoint_data(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/rendus/"),
        data={'id_etudiant': id_etudiant},
        token=token)
    return df
