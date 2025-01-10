import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Données
noms = ['Charlotte', 'Axelle', 'Arno', 'Livio', 'Cyprien', 'Louna', 'Mathieu', 'Emma', 'Thomas', 'Corentin', 'Ibtissam', 'Ikram', 'Sami', 'Walid', 'Maxens', 'Baptiste']
stages = [0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]

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
fig.update_traces(marker=dict(colors=['#ff9999', '#66b3ff']))
fig.update_layout(title_text="Répartition des étudiants avec ou sans stage")

def get_eleves_sans():
    eleves_sans=[]
    for i in range (0, len(noms)):
        if (stages[i] == 0):
            eleves_sans.append(noms[i])
    print(eleves_sans)
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