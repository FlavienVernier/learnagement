from dotenv import load_dotenv
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import mysql
import plotly.graph_objects as go
import pandas as pd
import requests
import app10_stage_tools

'''
# Données
noms = ['Charlotte', 'Axelle', 'Arno', 'Livio', 'Cyprien', 'Louna', 'Mathieu', 'Emma', 'Thomas', 'Corentin', 'Ibtissam', 'Ikram', 'Sami', 'Walid', 'Maxens', 'Baptiste']
stages = [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]'''

load_dotenv()

user = os.getenv("MYSQL_USER_LOGIN")
password = os.getenv("MYSQL_USER_PASSWORD")
host = os.getenv("MYSQL_SERVER")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB")
    
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

id_promo=25
noms=app10_stage_tools.get_etudiants_by_promo(cur, id_promo)['nom'].tolist()

stages = app10_stage_tools.get_etudiant_stage(cur, id_promo, noms)

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

#
df_stages = app10_stage_tools.get_stages()
table_stages = dbc.Table.from_dataframe(
    df_stages,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)

# Définition de la mise en page de l'application
app10_administratif_layout = html.Div(children=[
    html.H1(children='Représentation des Stages'), 
    html.Div(
       style={'display': 'inline-block', 'verticalAlign': 'top',}, 
       children=[ 
            dcc.Graph(id='pie-chart', figure=fig) ]), 
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',}, 
        children=[ 
            html.H2(children='Étudiants sans stage'), 
            html.Ul(children=[html.Li(etudiant) for etudiant in app10_stage_tools.get_eleves_sans(stages, noms)])]),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Gestion des stages'),
            html.Div([table_stages])])
])
  
