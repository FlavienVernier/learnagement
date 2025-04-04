import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Importer les layouts des différentes applications (vous pouvez copier leurs layouts dans des fonctions ou fichiers séparés)
from app1_map_generation import app1_layout, register_callbacks as register_callbacks_app1 
from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
from app3_taux_absenteisme import app3_layout, register_callbacks as register_callbacks_app3
from app4_eleve_visu_notes import app4_layout, register_callbacks as register_callbacks_app4
from app5_prof_visu_notes import app5_layout, register_callbacks as register_callbacks_app5
from app6_graph_avancement import app6_layout, register_callbacks as register_callbacks_app6
from app7_charge_enseignant import app7_layout, register_callbacks as register_callbacks_app7
from app8_charge_etudiant import app8_layout, register_callbacks as register_callbacks_app8

from app9_avancement_rendus import app9_layout, register_callbacks as register_callbacks_app9
from app10_proportion_stages  import app10_layout
from app11_dag_dependance import app11_layout, register_callbacks as register_callbacks_app11
from app12_dag_dependances_modules import app12_layout, register_callbacks as register_callbacks_app12

# Initialiser l'application Dash principale
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Pour le déploiement

# Layout principal avec des onglets
app.layout = html.Div([
    html.H1("Tableau de Bord - Learnagement", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Carte des Universités", children=app1_layout),
        dcc.Tab(label="Compétences", children=app2_layout),
        dcc.Tab(label="Absences", children=app3_layout),
        dcc.Tab(label="Notes (élèves)", children=app4_layout),
        dcc.Tab(label="Visualisation des notes (professeurs)", children=app5_layout),
        dcc.Tab(label="Avancement des cours", children=app6_layout),
        dcc.Tab(label="Charge de travail (enseignant)", children=app7_layout),
        dcc.Tab(label="Charge de travail (étudiant)", children=app8_layout),
        dcc.Tab(label="Avancement rendus", children=app9_layout),
        dcc.Tab(label="Proportion stages", children=app10_layout),
        dcc.Tab(label="Dépendance des cours", children=[app11_layout,app12_layout]),
    ])
])

# Enregistrer les callbacks des sous-modules
register_callbacks_app1(app)
register_callbacks_app2(app)
register_callbacks_app3(app)
register_callbacks_app4(app)
register_callbacks_app5(app)
register_callbacks_app6(app)
register_callbacks_app7(app)
register_callbacks_app8(app)
register_callbacks_app9(app)
register_callbacks_app11(app)
register_callbacks_app12(app)


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
