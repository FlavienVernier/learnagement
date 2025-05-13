import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import mysql
import plotly.graph_objects as go
import pandas as pd

'''
# Données
noms = ['Charlotte', 'Axelle', 'Arno', 'Livio', 'Cyprien', 'Louna', 'Mathieu', 'Emma', 'Thomas', 'Corentin', 'Ibtissam', 'Ikram', 'Sami', 'Walid', 'Maxens', 'Baptiste']
stages = [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]'''

# Lire les informations de connexion depuis logs_db.txt
with open('logs_db.txt', 'r') as file:
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    host = lines[2].strip()
    port = lines[3].strip()
    database = lines[4].strip()
    
# Se connecter à la base de données MySQL
conn = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    port=port,
    database=database
)

# Exécuter la requête pour récupérer les dépendances
cur = conn.cursor()

def get_etudiant_promo(id_promo) : 
    cur.execute(f"SELECT id_etudiant, nom, prenom FROM LNM_etudiant as etu JOIN LNM_promo as promo ON etu.id_promo=promo.id_promo WHERE etu.id_promo = {id_promo};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["id_etudiant", "nom", "prenom"])
    return data

id_promo=25
noms=get_etudiant_promo(id_promo)['nom'].tolist()

def get_etudiant_stage(id_promo, noms_etudiant) : 
    cur.execute(f"SELECT etu.id_etudiant, nom, prenom, stage.id_stage FROM LNM_etudiant as etu JOIN LNM_promo as promo ON etu.id_promo=promo.id_promo JOIN LNM_stage as stage ON stage.id_etudiant=etu.id_etudiant WHERE etu.id_promo = {id_promo};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["id_etudiant", "nom", "prenom", "stage"])
    
    stages = []
    for nom in noms_etudiant:
        if nom in data['nom'].values:
            # Vérifier si l'étudiant a un stage
            stage_value = data.loc[data['nom'] == nom, 'stage'].values[0]
            stages.append(1 if pd.notna(stage_value) else 0)
        else:
            # Si l'étudiant n'est pas trouvé dans data, ajouter 0
            stages.append(0)
    
    return stages

stages = get_etudiant_stage(id_promo, noms)

# Création du DataFrame
data = {
    "nom": noms,
    "stage": stages
}
df = pd.DataFrame(data)

# Compter les étudiants avec et sans stage
avec_stage = stages.count(1)
sans_stage = stages.count(0)

# Données pour le pie chart
labels = ['Avec Stage', 'Sans Stage']
values = [avec_stage, sans_stage]

# Création du pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Personnalisation du pie chart
fig.update_traces(marker=dict(colors=['#007BFF', '#FF8400']))
fig.update_layout(title_text="Répartition des étudiants avec ou sans stage")

def get_eleves_sans():
    eleves_sans=[]
    for i in range (0, len(noms)):
        if (stages[i] == 0):
            eleves_sans.append(noms[i])
    return eleves_sans

"""# Initialisation de l'application Dash
app = dash.Dash(__name__)"""

# Définition de la mise en page de l'application
app10_layout = html.Div(children=[
    html.H1(children='Représentation des Stages'), 
    html.Div(
       style={'display': 'inline-block', 'verticalAlign': 'top',}, 
       children=[ 
            dcc.Graph(id='pie-chart', figure=fig) ]), 
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',}, 
        children=[ 
            html.H2(children='Étudiants sans stage'), 
            html.Ul(children=[html.Li(etudiant) for etudiant in get_eleves_sans()])])
])
"""
# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
"""