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
#from app11_dag_dependance import app11_layout, register_callbacks as register_callbacks_app11
#from app12_dag_dependances_modules import app12_layout, register_callbacks as register_callbacks_app12

# Initialiser l'application Dash principale
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Pour le déploiement

"""# Layout principal avec des onglets
app.layout = html.Div([
    html.H1("Tableau de Bord - Learnagement", style={"textAlign": "center"}),  # Titre principal
    dcc.Tabs([
        dcc.Tab(label="Carte des Universités", children=app1_layout, className="tab-style"),
        dcc.Tab(label="Compétences", children=app2_layout, className="tab-style"),
        dcc.Tab(label="Absences", children=app3_layout, className="tab-style"),
        dcc.Tab(label="Notes (élèves)", children=app4_layout, className="tab-style"),
        dcc.Tab(label="Visualisation des notes (professeurs)", children=app5_layout, className="tab-style"),
        dcc.Tab(label="Avancement des cours", children=app6_layout, className="tab-style"),
        dcc.Tab(label="Charge de travail (enseignant)", children=app7_layout, className="tab-style"),
        dcc.Tab(label="Charge de travail (étudiant)", children=app8_layout, className="tab-style"),
        dcc.Tab(label="Avancement rendus", children=app9_layout, className="tab-style"),
        dcc.Tab(label="Proportion stages", children=app10_layout, className="tab-style")
        #dcc.Tab(label="Dépendance des cours", children=[app11_layout, app12_layout], className="tab-style"),
    ])
])"""

# Layout principal avec un menu burger sur la gauche et un contenu dynamique à droite
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  
    dbc.Row([
        # Sidebar avec le menu burger
        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavLink("Carte des Universités", href="/app1", id="link-app1", className="menu-item"),
                    dbc.NavLink("Compétences", href="/app2", id="link-app2", className="menu-item"),
                    dbc.NavLink("Absences", href="/app3", id="link-app3", className="menu-item"),
                    dbc.NavLink("Notes (élèves)", href="/app4", id="link-app4", className="menu-item"),
                    dbc.NavLink("Visualisation des notes (professeurs)", href="/app5", id="link-app5", className="menu-item"),
                    dbc.NavLink("Avancement des cours", href="/app6", id="link-app6", className="menu-item"),
                    dbc.NavLink("Charge de travail (enseignant)", href="/app7", id="link-app7", className="menu-item"),
                    dbc.NavLink("Charge de travail (étudiant)", href="/app8", id="link-app8", className="menu-item"),
                    dbc.NavLink("Avancement rendus", href="/app9", id="link-app9", className="menu-item"),
                    dbc.NavLink("Proportion stages", href="/app10", id="link-app10", className="menu-item"),
                    # Ajoutez d'autres liens ici
                ],
                vertical=True,
                pills=True,
                className="sidebar"
            ),
            width=2,  # Sidebar à gauche, 2/12 de la largeur de l'écran
            className="sidebar-container"
        ),
        
        # Conteneur principal pour le graphique
        dbc.Col(
            html.Div(id='page-content', children=[]),  # Ce contenu change en fonction de l'onglet sélectionné
            width=10,  # Le reste de la page sera occupé par le graphique
            className="main-content"
        ),
    ]),
])

# Callback pour changer le contenu central (graphique) selon le menu sélectionné
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/app1':
        return app1_layout  # Graphique de l'app1
    elif pathname == '/app2':
        return app2_layout  # Graphique de l'app2
    elif pathname == '/app3':
        return app3_layout  # Graphique de l'app3
    elif pathname == '/app4':
        return app4_layout  # Graphique de l'app4
    elif pathname == '/app5':
        return app5_layout  # Graphique de l'app5
    elif pathname == '/app6':
        return app6_layout  # Graphique de l'app6
    elif pathname == '/app7':
        return app7_layout  # Graphique de l'app7
    elif pathname == '/app8':
        return app8_layout  # Graphique de l'app8
    elif pathname == '/app9':
        return app9_layout  # Graphique de l'app9
    elif pathname == '/app10':
        return app10_layout  # Graphique de l'app10
    # Ajoutez d'autres conditions pour d'autres applications si nécessaire
    else:
        return html.Div("Page non trouvée")

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
#register_callbacks_app11(app)
#register_callbacks_app12(app)

if __name__ == "__main__":
    try:
        app.run(host= '0.0.0.0', debug=True)
    except Exception as e:
        print("COIN COIN")
        print(e)
