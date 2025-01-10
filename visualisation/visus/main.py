import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Importer les layouts des différentes applications (vous pouvez copier leurs layouts dans des fonctions ou fichiers séparés)
from app1_map_generation import app1_layout  # Votre première application
from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
from app3_taux_absenteisme import app3_layout, register_callbacks as register_callbacks_app3

# Initialiser l'application Dash principale
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Pour le déploiement

# Layout principal avec des onglets
app.layout = html.Div([
    html.H1("Tableau de Bord - Applications Fusionnées", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Carte des Universités", children=app1_layout),
        dcc.Tab(label="Spyder Charts des Compétences", children=app2_layout),
        dcc.Tab(label="Analyse des Absences", children=app3_layout),
    ])
])

# Enregistrer les callbacks des sous-modules
register_callbacks_app2(app)
register_callbacks_app3(app)

if __name__ == "__main__":
    app.run_server(debug=True)
