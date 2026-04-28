import dash
from dash import dcc, html, Output, Input, State, ALL, callback_context
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import dash_leaflet as dl
#==============================================================================
# 1. FONCTIONS DE NETTOYAGE & TRAITEMENT DES DONNÉES
# ==============================================================================

def reparer_texte(texte):
    if not isinstance(texte, str): return texte
    try:
        return texte.encode('cp1252').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        try:
            return texte.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return texte

def count_competences(competences):
    if not isinstance(competences, list): return 0
    if len(competences) > 0 and isinstance(competences[0], str) and "Erreur" in competences[0]:
        return 0
    return len(competences)

def count_metiers(metiers):
    if not isinstance(metiers, list): return 0
    flat_metiers = []
    for item in metiers:
        if isinstance(item, list): flat_metiers.extend(item)
        elif isinstance(item, str): flat_metiers.append(item)
    return len([m for m in flat_metiers if isinstance(m, str) and len(m) > 3])

# ==============================================================================
# 2. CHARGEMENT DES DONNÉES
# ==============================================================================

file_name = '../data/data_reseau_polytech.json'
try:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Erreur: Le fichier {file_name} est introuvable.")
    data = {}

coords_ecoles = {
    "Polytech Nantes":        [47.282, -1.520],
    "Polytech Montpellier":   [43.632,  3.863],
    "Polytech Annecy":        [45.920,  6.138],
    "Polytech Paris saclay":  [48.706,  2.169],
    "Polytech Tours":         [47.354,  0.704],
    "Polytech Nice Sophia":   [43.616,  7.072],
    "Polytech Angers":        [47.481, -0.594],
    "Polytech Clermont":      [45.758,  3.111],
    "Polytech Grenoble":      [45.193,  5.767],
    "Polytech Lyon":          [45.783,  4.868],
    "Polytech Nancy":         [48.665,  6.155],
}

records = []
for school, formations in data.items():
    for f_data in formations:
        raw_nom = f_data.get('formation', 'Inconnu')
        nom_clean = reparer_texte(raw_nom.replace('-', ' ').title())
        records.append({
            'Ecole':                  school,
            'Formation':              nom_clean,
            'Nombre de Compétences':  count_competences(f_data.get('competences', [])),
            'Nombre de Métiers':      count_metiers(f_data.get('metiers', [])),
        })

df          = pd.DataFrame(records)
if not df.empty:
    df_filtered = df[df['Nombre de Compétences'] > 0].copy()
else:
    df_filtered = None
