import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import importlib

# Importer les fichiers dash existants
import taux_absenteisme  # Ce fichier contient l'application Dash pour 
import spyder_plot_competences
import map_generation

# Créer l'application principale Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Créer un layout pour la page principale
app.layout = html.Div([
    html.H1("Tableau de Bord Principal"),
    html.Div([
        html.H2("Graphique 1 : Taux d'Absence"),
        dcc.Graph(
            id='graph-absence',
            figure=taux_absenteisme.app.layout.children[1].figure  # Récupérer la figure de `taux_absenteisme.py`
        )
    ]),
    html.Hr(),
    html.Div([
        html.H2("Graphique 2 : Araignée des compétences"),
        dcc.Graph(
            id='graph-spyder1',
            figure=spyder_plot_competences.app.layout.children[0].figure  # Récupérer la figure de `spyder_plot_competences.py`
        )
    ]),
    html.Hr(),
    html.Div([
        dcc.Graph(
            id='graph-spyder2',
            figure=spyder_plot_competences.app.layout.children[1].figure  # Récupérer la figure de `spyder_plot_competences.py`
        )
    ]),
    html.Hr(),
    html.Div([
        html.H2("Graphique 3 : Carte des mobilités"),
        dcc.Graph(
            id='university-map',
            figure=map_generation.app.layout.children[1].figure  # Récupérer la figure de `map_generation.py`
        )
    ])
])

# Lancer l'application Dash principale
if __name__ == '__main__':
    app.run_server(debug=True)
