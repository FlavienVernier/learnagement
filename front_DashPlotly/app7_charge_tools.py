from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import app_tools

load_dotenv()

# Palette originale
original_palette = px.colors.qualitative.Alphabet

# Retirer une couleur (ex : '#FFB5E8')
custom_palette = [c for c in original_palette if c.lower() != '#85660d']

def get_etudiant_edt(token, id_etudiant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/edt/"),
        token=token)
    return df

def get_etudiant_pastedt(token, id_etudiant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/pastedt/"),
        token=token)
    return df

# Calculer les avancements
def calcul_avancement(data_done, data_all):
    res = {'Année': 0,
           'Année_total': 0}

    res['Année'] = data_done['nb_heure'].sum()
    res['Année_total'] = data_all['nb_heure'].sum()

    return res

def transforme_données(data):
    rows = []
    for key, value in data.items():
        if "_total" not in key:  # Ignorer les clés '_total' dans cette boucle
            total_key = f"{key}_total"
            if total_key in data:
                rows.append({
                    "Category": key,
                    "Realized": value,
                    "Total": data[total_key],
                    "Completion (%)": (value / data[total_key]) * 100 if data[total_key] > 0 else 0
                })
    return pd.DataFrame(rows)

def get_chargeByEnseignantId(token, id_enseignant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/enseignants/{id_enseignant}/charge/"),
        token=token)
    return df

def get_chargeByEtudianttId(token, id_etudiant):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/load/"),
        token=token)
    return df