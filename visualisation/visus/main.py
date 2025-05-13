import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

registered_callbacks = set()

icon_map = {
    'app1': 'fa-solid fa-map',
    'app2': 'fa-solid fa-chart-pie',
    'app3': 'fa-solid fa-user-minus',
    'app4': 'fa-solid fa-user-graduate',
    'app5': 'fa-solid fa-chalkboard-teacher',
    'app6': 'fa-solid fa-progress-bar',  # exemple, à adapter
    'app7': 'fa-solid fa-briefcase',
    'app8': 'fa-solid fa-book',
    'app9': 'fa-solid fa-tasks',
    'app10': 'fa-solid fa-percentage'
}

# Importer les layouts des différentes applications
def import_apps():
    from app1_map_generation import app1_layout, register_callbacks as register_callbacks_app1
    from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
    from app3_taux_absenteisme import app3_layout, register_callbacks as register_callbacks_app3
    from app4_eleve_visu_notes import app4_layout, register_callbacks as register_callbacks_app4
    from app5_prof_visu_notes import app5_layout, register_callbacks as register_callbacks_app5
    from app6_graph_avancement import app6_layout, register_callbacks as register_callbacks_app6
    from app7_charge_enseignant import app7_layout, register_callbacks as register_callbacks_app7
    from app8_charge_etudiant import app8_layout, register_callbacks as register_callbacks_app8
    from app9_avancement_rendus import app9_layout, register_callbacks as register_callbacks_app9
    from app10_proportion_stages import app10_layout
    return {
        'app1': (app1_layout, register_callbacks_app1),
        'app2': (app2_layout, register_callbacks_app2),
        'app3': (app3_layout, register_callbacks_app3),
        'app4': (app4_layout, register_callbacks_app4),
        'app5': (app5_layout, register_callbacks_app5),
        'app6': (app6_layout, register_callbacks_app6),
        'app7': (app7_layout, register_callbacks_app7),
        'app8': (app8_layout, register_callbacks_app8),
        'app9': (app9_layout, register_callbacks_app9),
        'app10': (app10_layout, None)
    }

LOGO = "https://placehold.co/100x100"
apps = import_apps()

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

# MENU DE LA SIDEBAR (EDITABLE)
menu_items = {
    'enseignant': [
        ('Absences', 'app3'),
        ('Notes (professeurs)', 'app5'),
        ('Avancement des cours', 'app6'),
        ('Charge de travail (enseignant)', 'app7'),
        ('Proportion stages', 'app10')
    ],
    'etudiant': [
        ('Carte des Universités', 'app1'),
        ('Compétences', 'app2'),
        ('Notes (élèves)', 'app4'),
        ('Avancement des cours', 'app6'),
        ('Charge de travail (étudiant)', 'app8'),
        ('Avancement rendus', 'app9'),
    ]
}

def render_sidebar(section):
    links = []
    # Logo + titre
    links.append(html.Div([
        html.Img(src=LOGO, style={ 'width': '3rem' }),
        html.H2(section.capitalize())
    ], className='sidebar-header'))
    links.append(html.Hr())
    # Navigation
    navs = []
    for label, key in menu_items[section]:
        href = f"/{section}/{key}"
        icon_class = icon_map.get(key, 'fa-solid fa-circle')  # icône par défaut si manquante
        navs.append(
            dbc.NavLink([
                html.I(className=icon_class, style={'marginRight': '2rem'}),
                label
            ], href=href, id=f"link-{key}", className='menu-item')
        )

    links.append(dbc.Nav(navs, vertical=True, pills=True))
    return html.Div(links, className='sidebar')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='sidebar'),
    html.Div(id='page-content', className='content')
])

# Callback pour mettre à jour la sidebar
@app.callback(
    Output('sidebar', 'children'),
    Input('url', 'pathname')
)
def update_sidebar(pathname):
    if pathname and pathname.startswith('/enseignant'):
        return render_sidebar('enseignant')
    elif pathname and pathname.startswith('/etudiant'):
        return render_sidebar('etudiant')
    else:
        # Chemin non reconnu : sidebar vide ou message par défaut
        return html.Div([
            html.H2("Bienvenue"),
            html.P("Veuillez sélectionner une section valide dans l'URL.")
        ], className='p-3')

# Callback pour rendre le bon contenu
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def render_page_content(pathname):
    if not pathname or pathname == '/':
        return html.Div()
    parts = pathname.strip('/').split('/')  # ['enseignant', 'app1'] ou ['etudiant','app7'] ou ['enseignant'] etc.
    if len(parts) == 1:
        # page section landing
        return html.Div([
            html.H2(f"Section: {parts[0].capitalize()}"),
            html.P('Sélectionnez une rubrique dans la barre latérale.')
        ], className='p-3')
    section, key = parts[0], parts[1]
    if section in menu_items and key in apps:
        layout, register_cb = apps[key]
        if register_cb and key not in registered_callbacks:
            register_cb(app)
            registered_callbacks.add(key)

        return layout
    return html.Div([
        html.H1('404: Not found', className='text-danger'),
        html.Hr(),
        html.P(f"La page {pathname} n'existe pas." )
    ], className='p-3 bg-light rounded-3')

for key, (_, register_cb) in apps.items():
    if register_cb and key not in registered_callbacks:
        register_cb(app)
        registered_callbacks.add(key)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)