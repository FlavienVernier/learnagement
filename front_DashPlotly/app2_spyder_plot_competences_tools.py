from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()


def get_evaluation_apprentissage_critique_by_studentId(token, id_etudiant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/evaluations/apc/etudiants/{id_etudiant}"),
        token = token
    )
    return df

