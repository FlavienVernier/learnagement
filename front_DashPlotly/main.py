from datetime import timedelta
import logging
from logging import exception

from dotenv import load_dotenv
import os
import jwt
import dash_bootstrap_components as dbc
from flask import session, jsonify
from dash import Input, Output, dcc, html, State
from urllib.parse import urlparse
from urllib.parse import parse_qs
from auth import FlaskAuth, decode_token

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')

load_dotenv()



# Utilisation
app = FlaskAuth(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

server = app.server
server.secret_key = os.getenv('INSTANCE_SECRET')
time_out = int(os.getenv('SESSION_TIMEOUT'))

registered_callbacks = set()

icon_map = {
    'app2': 'fa-solid fa-chart-pie',
    'app3': 'fa-solid fa-user-minus',
    'app4': 'fa-solid fa-user-graduate',
    'app5': 'fa-solid fa-chalkboard-teacher',
    'app7': 'fa-solid fa-briefcase',
    'app8': 'fa-solid fa-book',
    'app9': 'fa-solid fa-tasks',
    'app10': 'fa-solid fa-percentage',
    'apc_ens_dashboard': 'fa-solid fa-graduation-cap',
    'connected': 'fa-solid fa-check',
    'disconnected': 'fa-solid fa-xmark',
    'apc20_hub': 'fa-solid fa-graduation-cap',
    'dashboard': 'fa-solid fa-terminal',
    'exit': 'fa-solid fa-arrow-right-from-bracket',
}

# Importer les layouts des différentes applications
def import_apps():
    from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
    from app3_absenteisme_administratif import app3_administratif_layout, register_callbacks as register_callbacks_app3_administratif
    from app3_absenteisme_enseignant import app3_enseignant_layout, register_callbacks as register_callbacks_app3_enseignant
    from app3_absenteisme_etudiant import app3_etudiant_layout, register_callbacks as register_callbacks_app3_etudiant
    from app4_notes_enseignant import app4_enseignant_layout, register_callbacks as register_callbacks_app4_enseignant
    from app4_notes_eleve import app4_etudiant_layout, register_callbacks as register_callbacks_app4_etudiant
    from app5_module_enseignant_view import app5_enseignant_view_layout, register_callbacks_view as register_callbacks_app5_enseignant_view
    from app5_module_enseignant_edit import app5_enseignant_edit_layout, register_callbacks_edit as register_callbacks_app5_enseignant_edit
    from app7_charge_administratif import app7_administratif_layout, register_callbacks as register_callbacks_app7_administratif
    from app7_charge_enseignant import app7_enseignant_layout, register_callbacks as register_callbacks_app7_enseignant
    from app7_charge_etudiant import app7_etudiant_layout, register_callbacks as register_callbacks_app7_etudiant
    from app9_rendus_etudiant import app9_layout, register_callbacks as register_callbacks_app9
    from app10_stage_administratif import app10_administratif_layout, register_callbacks as register_callbacks_app10_administratif
    from app10_stage_enseignant import app10_enseignant_layout, register_callbacks as register_callbacks_app10_enseignant
    from app10_stage_etudiant import app10_etudiant_layout, register_callbacks as register_callbacks_app10_etudiant
    from app11_dag_dependance import app11_layout, register_callbacks as register_callbacks_app11
    from app11_dag_dependance_new import app11_new_layout, register_callbacks as register_callbacks_app11_new
    from app13_mccc_administratif import app13_administratif_layout, register_callbacks as register_callbacks_app13_administratif
    from app14_check_administratif import app14_administratif_layout, register_callbacks as register_callbacks_app14_administratif    
    from apc_dash.apc_hub import apc_hub_layout, register_apc_hub_callbacks

    return {
        'app2': (app2_layout, register_callbacks_app2),
        'app3_administratif': (app3_administratif_layout, register_callbacks_app3_administratif),
        'app3_enseignant': (app3_enseignant_layout, register_callbacks_app3_enseignant),
        'app3_etudiant': (app3_etudiant_layout, register_callbacks_app3_etudiant),
        'app4_enseignant': (app4_enseignant_layout, register_callbacks_app4_enseignant),
        'app4_etudiant': (app4_etudiant_layout, register_callbacks_app4_etudiant),
        'app5_enseignant_view': (app5_enseignant_view_layout, register_callbacks_app5_enseignant_view),
        'app5_enseignant_edit': (app5_enseignant_edit_layout, register_callbacks_app5_enseignant_edit),
        'app7_administratif': (app7_administratif_layout, register_callbacks_app7_administratif),
        'app7_enseignant': (app7_enseignant_layout, register_callbacks_app7_enseignant),
        'app7_etudiant': (app7_etudiant_layout, register_callbacks_app7_etudiant),
        'app9': (app9_layout, register_callbacks_app9),
        'app10_administratif': (app10_administratif_layout, register_callbacks_app10_administratif),
        'app10_enseignant': (app10_enseignant_layout, register_callbacks_app10_enseignant),
        'app10_etudiant': (app10_etudiant_layout, register_callbacks_app10_etudiant),
        'app11': (app11_layout, register_callbacks_app11),
        'app11_new': (app11_new_layout, register_callbacks_app11_new),
        'app13_administratif': (app13_administratif_layout, register_callbacks_app13_administratif),
        'app14_administratif': (app14_administratif_layout, register_callbacks_app14_administratif),
        'apc20_hub': (apc_hub_layout, register_apc_hub_callbacks),

    }

LOGO = "https://placehold.co/100x100"
apps = import_apps()

environment =  SECRET_KEY = os.getenv("ENV") # prod or dev
# Prod config
# Default sidebar menu
menu_items = {
    'administratif': [
        ('Absences', 'app3_administratif'),
        ('Gestion des stages', 'app10_administratif'),
        ('MCCC', 'app13_administratif'),
        ('Check', 'app14_administratif'),
        ('Charge enseignant', 'app7_administratif'),
        ('Approche par compétences', 'apc20_hub'),
    ],
    'enseignant': [
        ('Vue modules', 'app5_enseignant_view'),
        ('MaJ modules', 'app5_enseignant_edit'),
        ('Dépendance Séances', 'app11'),
        ('MaJ Dépendance Séances', 'app11_new'),
        ('Absences', 'app3_enseignant'),
        ('Notes', 'app4_enseignant'),
        ('Charge de travail', 'app7_enseignant'),
        ('Tutorat stages', 'app10_enseignant'),
        ('Approche par compétences', 'apc20_hub'),
      
    ],
    'etudiant': [
        ('Stages', 'app10_etudiant'),
    ]
}

if environment == "dev":
    menu_items['etudiant'] += [
        ('Compétences', 'app2'),
        ('Absences', 'app3_etudiant'),
        ('Notes', 'app4_etudiant'),
        ('Dépendance Séances', 'app11'),
        ('Charge de travail', 'app7_etudiant'),
        ('Avancement rendus', 'app9'),
        ('Approche par compétences', 'apc20_hub'),
    ]

#SECRET_KEY = os.getenv("INSTANCE_SECRET").encode()

def render_sidebar(section, token_arg, status):
    # AJOUTE CES DEUX LIGNES POUR LE DÉBOGAGE :
    print(f"====== CRÉATION DU MENU POUR : {section} ======", flush=True)
    print(f"====== CONTENU DU MENU : {menu_items[section]} ======", flush=True)
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
        href = f"/{section}/{key}?" + token_arg 
        icon_class = icon_map.get(key, 'fa-solid fa-circle')  # icône par défaut si manquante
        navs.append(
            dbc.NavLink([
                html.I(className=icon_class, style={'marginRight': '2rem'}),
                label
            ], href=href, id=f"link-{key}", className='menu-item')
        )
    navs.append(html.Hr())
    instance_protocol = os.getenv("INSTANCE_PROTOCOL")
    instance_url = os.getenv("INSTANCE_URL")
    php_port = os.getenv("FRONT_PHP_PORT")
    icon_class = icon_map.get("dashboard", 'fa-solid fa-circle')
    navs.append(
        dbc.NavLink([
            html.I(className=icon_class, style={'marginRight': '2rem'}),
            "PHP Dashboard"
        ], href=f"{instance_protocol}://{instance_url}:{php_port}", id=f"link-php-dashboard", className='menu-item')
    )
    env = os.getenv("ENV")
    if env == "dev":
        next_auth_port = os.getenv("FRONT_NEXTAUTH_PORT")
        navs.append(
            dbc.NavLink([
                html.I(className=icon_class, style={'marginRight': '2rem'}),
                "NextJS Dashboard"
            ], href=f"{instance_protocol}://{instance_url}:{next_auth_port}", id=f"link-php-dashboard", className='menu-item')
        )
    icon_class = icon_map.get("exit", 'fa-solid fa-circle')
    navs.append(
        dbc.NavLink([
            html.I(className=icon_class, style={'marginRight': '2rem'}),
            "Déconnexion"
        ], href=f"{instance_protocol}://{instance_url}:{php_port}/logout", id=f"link-php-dashboard", className='menu-item')
    )

    links.append(dbc.Nav(navs, vertical=True, pills=True))

    return html.Div(links, className='sidebar',style={'overflowY': 'auto', 'maxHeight': '100vh', 'paddingBottom': '50px'})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='token', storage_type="memory", data='none'),
    dcc.Store(id='user_id', storage_type="memory", data='0'),
    dcc.Store(id='role', storage_type="memory", data='none'),
    dcc.Store(id='status', storage_type="memory", data='not connected'), #deprecated
    # Stores des dashboards APC — toujours dans le DOM pour que leurs callbacks se déclenchent dès le token disponible
    dcc.Store(id='apc-ens-raw-store'),
    dcc.Location(id="url-redirect", refresh=True),
    html.Div(id='sidebar'),
    html.Div(id='page-content', className='content')
])


# Callback pour mettre à jour la sidebar
@app.callback(
    Output('sidebar', 'children'),
    Input('url', 'href'),
    Input('url', 'pathname'),
    Input('status', 'data')
)
def update_sidebar(url, pathname, status):
    logging.info("update_sidebar")
    token_arg = url.strip().split('?')[1]
    if pathname and pathname.startswith('/enseignant'):
        return render_sidebar('enseignant', token_arg, status)
    elif pathname and pathname.startswith('/etudiant'):
        return render_sidebar('etudiant', token_arg, status)
    elif pathname and pathname.startswith('/administratif'):
        return render_sidebar('administratif', token_arg, status)
    else:
        # Chemin non reconnu : sidebar vide ou message par défaut
        return html.Div([
            html.H2("Bienvenue"),
            html.P("Veuillez sélectionner une section valide dans l'URL.")
        ], className='p-3')



# Callback pour rendre le bon contenu
@app.callback(
    Output('page-content', 'children'),
    Output('token', 'data'),
    Output('user_id', 'data'), # ToDo must be moved to session
    Output('role', 'data'), # ToDo must be moved to session
    Output('status', 'data'), # ToDo must be moved to session
    Input('url', 'href'),
    Input('url', 'pathname'),
    State('token', 'data')
)

def render_page(url, pathname, token):
    try:
        jwt_token, user_id, main_role, status = check_auth_token(url) # if token is none, check_auth_token will get it
        page_content = render_page_content(url, pathname, jwt_token)
        return page_content, jwt_token, user_id, main_role, status
    except Exception as e:
        logging.exception(e)
        instance_protocol = os.getenv("INSTANCE_PROTOCOL")
        instance_url = os.getenv("INSTANCE_URL")
        front_php_port = os.getenv("FRONT_PHP_PORT")
        return html.Div(
            [html.A(href=f"{instance_protocol}://{instance_url}:{front_php_port}/logout", target="_top",
                    children="Session closed, connection required.")]), "-1", "none", "none", "no token"


def check_auth_token(url):
    logging.info("check_auth_token")
    # print(url, flush=True)
    parsed_url = urlparse(url)
    instance_protocol = os.getenv("INSTANCE_PROTOCOL")
    instance_url = os.getenv("INSTANCE_URL")
    front_php_port = os.getenv("FRONT_PHP_PORT")

    jwt_token = parse_qs(parsed_url.query)['jwt_token'][0]
    # print(jwt_token, flush=True)

    session['token'] = jwt_token

    # if not session.get("token") or not token:
    if not jwt_token:
        logging.info("no token")
        app.layout = html.Div([html.A(href=f"{instance_protocol}://{instance_url}:{front_php_port}/logout", target="_top", children="No Token, session closed, connection required.")])
        return "-1", "none", "none", "no token"
    #try:
    payload = decode_token(jwt_token)
    print(payload, flush=True)
    # Attach user info to the Flask global context
    if 'enseignant' in payload["roles"]:
        return jwt_token, payload['id'], "enseignant", "Connected"
    elif 'etudiant' in payload["roles"]:
        return jwt_token, payload['id'], "etudiant", "Connected"
    elif 'administratif' in payload["roles"]:
        return jwt_token, payload['id'], "administratif", "Connected"
    else:
        logging.exception("Unknown user class")
        raise Exception("Unknown user class")


def render_page_content(url, pathname, token):
    logging.info("render_page_content " + token)

    parts = pathname.strip('/').split('/')  # ['enseignant', 'app2'] ou ['etudiant','app7'] ou ['enseignant'] etc.
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
    is_prod = os.getenv("ENV", "dev") == "prod"
    ssl_dir = os.getenv("DOCKER_SSL_DIR")

    if is_prod:
        import gunicorn.app.base

        class StandaloneApp(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            "bind": "0.0.0.0:8050",
            "workers": 2,
            "certfile": os.path.join(ssl_dir, "cert.pem"),
            "keyfile": os.path.join(ssl_dir, "key.pem"),
        }
        StandaloneApp(server, options).run()
    else:
        app.run(host='0.0.0.0', debug=True)
