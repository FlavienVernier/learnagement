import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

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

LOGO = "https://placehold.co/100x100"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server  # Pour le déploiement

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=LOGO, style={"width": "3rem"}),
                html.H2("Sidebar"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
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
                dbc.NavLink("Proportion stages", href="/app10", id="link-app10", className="menu-item")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(id="page-content", className="content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# set the content according to the current pathname
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
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
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

register_callbacks_app1(app)
register_callbacks_app2(app)
register_callbacks_app3(app)
register_callbacks_app4(app)
register_callbacks_app5(app)
register_callbacks_app6(app)
register_callbacks_app7(app)
register_callbacks_app8(app)
register_callbacks_app9(app)

if __name__ == "__main__":
    app.run(debug=True)
