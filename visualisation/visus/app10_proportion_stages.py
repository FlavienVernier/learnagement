import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import mysql.connector

# Données
#Récupération des données de logs
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
#cur.execute("SELECT * FROM VIEW_graphe_dependances")
cur.execute("SELECT prenom, nom FROM LNM_etudiant")

rows = cur.fetchall()

print(rows)
'''
data = lien_db.get_data(db, 'LNM_stage')
noms = lien_db.execute_query(db, "SELECT prenom, nom FROM LNM_etudiant")

data = pd.DataFrame(data)

# Compter les étudiants avec et sans stage
print(lien_db.execute_query(db, "SELECT prenom, nom FROM LNM_etudiant WHERE id_etudiant IN (SELECT id_etudiant FROM LNM_stage);"))
pers_avec_stage = lien_db.execute_query(db, "SELECT prenom, nom FROM LNM_etudiant WHERE id_etudiant IN (SELECT id_etudiant FROM LNM_stage);")
print(pers_avec_stage)
pers_sans_stage = lien_db.execute_query(db, "SELECT prenom, nom FROM LNM_etudiant WHERE id_etudiant IN (SELECT id_etudiant FROM LNM_stage);")
print(pers_sans_stage)

# Données pour le pie chart
labels = ['Avec Stage', 'Sans Stage']
values = [len(pers_avec_stage), len(pers_sans_stage)]

# Création du pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Personnalisation du pie chart
fig.update_traces(marker=dict(colors=['#ff9999', '#66b3ff']))
fig.update_layout(title_text="Répartition des étudiants avec ou sans stage")

def get_eleves_sans():
    eleves_sans=[]
    for prenom, nom in pers_sans_stage:
        eleves_sans.append((prenom, nom))
    return eleves_sans

lien_db.close_db(db)

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
'''

"""
# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
"""