import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Importer les layouts des différentes applications (vous pouvez copier leurs layouts dans des fonctions ou fichiers séparés)
from app1_map_generation import app1_layout  # Votre première application
from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
from app3_taux_absenteisme import app3_layout, register_callbacks as register_callbacks_app3
from app4_eleve_visu_notes import app4_layout, register_callbacks as register_callbacks_app4
from app5_prof_visu_notes import app5_layout, register_callbacks as register_callbacks_app5
from app6_graph_avancement import app6_layout, register_callbacks as register_callbacks_app6

# Initialiser l'application Dash principale
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Pour le déploiement

# Layout principal avec des onglets
app.layout = html.Div([
    html.H1("Tableau de Bord - Learnagement", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Carte des Universités", children=app1_layout),
        dcc.Tab(label="Spyder Charts des Compétences", children=app2_layout),
        dcc.Tab(label="Analyse des Absences", children=app3_layout),
        dcc.Tab(label="Visualisation des notes élèves", children=app4_layout),
        dcc.Tab(label="Visualisation des notes professeurs", children=app5_layout),
        dcc.Tab(label="Avancement", children=app6_layout),
    ])
])

# Enregistrer les callbacks des sous-modules
register_callbacks_app2(app)
register_callbacks_app3(app)
register_callbacks_app4(app)
register_callbacks_app5(app)
register_callbacks_app6(app)

if __name__ == "__main__":
    app.run_server(debug=True)
