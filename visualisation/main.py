from dotenv import load_dotenv
import os
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import json, base64, hmac, hashlib, time
import traceback
import urllib.parse

load_dotenv()

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

registered_callbacks = set()

icon_map = {
    'app1': 'fa-solid fa-map',
    'app2': 'fa-solid fa-chart-pie',
    'app3': 'fa-solid fa-user-minus',
    'app4': 'fa-solid fa-user-graduate',
    'app5': 'fa-solid fa-chalkboard-teacher',
    'app6': 'fa-solid fa-bars-progress', 
    'app7': 'fa-solid fa-briefcase',
    'app8': 'fa-solid fa-book',
    'app9': 'fa-solid fa-tasks',
    'app10': 'fa-solid fa-percentage',
    'connected': 'fa-solid fa-check',
    'disconnected': 'fa-solid fa-xmark'
}

    
# Importer les layouts des différentes applications
def import_apps():
    from app1_map_generation import app1_layout, register_callbacks as register_callbacks_app1
    from app2_spyder_plot_competences import app2_layout, register_callbacks as register_callbacks_app2
    from app3_absenteisme_administratif import app3_administratif_layout, register_callbacks as register_callbacks_app3_administratif
    from app3_absenteisme_enseignant import app3_enseignant_layout, register_callbacks as register_callbacks_app3_enseignant
    from app3_absenteisme_etudiant import app3_etudiant_layout, register_callbacks as register_callbacks_app3_etudiant
    from app4_notes_enseignant import app4_enseignant_layout, register_callbacks as register_callbacks_app4_enseignant
    from app4_notes_eleve import app4_etudiant_layout, register_callbacks as register_callbacks_app4_etudiant
    from app5_module_enseignant_view import app5_enseignant_view_layout, register_callbacks_view as register_callbacks_app5_enseignant_view
    from app5_module_enseignant_edit import app5_enseignant_edit_layout, register_callbacks_edit as register_callbacks_app5_enseignant_edit
    from app7_charge_enseignant import app7_enseignant_layout, register_callbacks as register_callbacks_app7_enseignant
    from app7_charge_etudiant import app7_etudiant_layout, register_callbacks as register_callbacks_app7_etudiant
    from app9_rendus_etudiant import app9_layout, register_callbacks as register_callbacks_app9
    from app10_stage_administratif import app10_administratif_layout, register_callbacks as register_callbacks_app10_administratif
    from app10_stage_enseignant import app10_enseignant_layout, register_callbacks as register_callbacks_app10_enseignant
    from app10_stage_etudiant import app10_etudiant_layout, register_callbacks as register_callbacks_app10_etudiant
    from app11_dag_dependance import app11_layout, register_callbacks as register_callbacks_app11
    from app13_mccc_administratif import app13_administratif_layout, register_callbacks as register_callbacks_app13_administratif
    from app14_check_administratif import app14_administratif_layout, register_callbacks as register_callbacks_app14_administratif
    return {
        'app1': (app1_layout, register_callbacks_app1),
        'app2': (app2_layout, register_callbacks_app2),
        'app3_administratif': (app3_administratif_layout, register_callbacks_app3_administratif),
        'app3_enseignant': (app3_enseignant_layout, register_callbacks_app3_enseignant),
        'app3_etudiant': (app3_etudiant_layout, register_callbacks_app3_etudiant),
        'app4_enseignant': (app4_enseignant_layout, register_callbacks_app4_enseignant),
        'app4_etudiant': (app4_etudiant_layout, register_callbacks_app4_etudiant),
        'app5_enseignant_view': (app5_enseignant_view_layout, register_callbacks_app5_enseignant_view),
        'app5_enseignant_edit': (app5_enseignant_edit_layout, register_callbacks_app5_enseignant_edit),
        'app7_enseignant': (app7_enseignant_layout, register_callbacks_app7_enseignant),
        'app7_etudiant': (app7_etudiant_layout, register_callbacks_app7_etudiant),
        'app9': (app9_layout, register_callbacks_app9),
        'app10_administratif': (app10_administratif_layout, register_callbacks_app10_administratif),
        'app10_enseignant': (app10_enseignant_layout, register_callbacks_app10_enseignant),
        'app10_etudiant': (app10_etudiant_layout, register_callbacks_app10_etudiant),
        'app11': (app11_layout, register_callbacks_app11),
        'app13_administratif': (app13_administratif_layout, register_callbacks_app13_administratif),
        'app14_administratif': (app14_administratif_layout, register_callbacks_app14_administratif),
    }

LOGO = "https://placehold.co/100x100"
apps = import_apps()

# MENU DE LA SIDEBAR (EDITABLE)
menu_items = {
    'administratif': [
        ('Absences', 'app3_administratif'),
        ('Gestion des stages', 'app10_administratif'),
        ('MCCC', 'app13_administratif'),
        ('Check', 'app14_administratif')
    ],
    'enseignant': [
        ('Carte des Universités', 'app1'),
        ('Vue modules', 'app5_enseignant_view'),
        ('MaJ modules', 'app5_enseignant_edit'),
        ('Dépendance Séances', 'app11'),
        ('Absences', 'app3_enseignant'),
        ('Notes', 'app4_enseignant'),
        ('Charge de travail', 'app7_enseignant'),
        ('Tutorat stages', 'app10_enseignant'),
    ],
    'etudiant': [
        ('Carte des Universités', 'app1'),
        ('Compétences', 'app2'),
        ('Absences', 'app3_etudiant'),
        ('Notes', 'app4_etudiant'),
        ('Dépendance Séances', 'app11'),
        ('Charge de travail', 'app7_etudiant'),
        ('Avancement rendus', 'app9'),
        ('Stages', 'app10_etudiant')
    ]
}

SECRET_KEY = os.getenv("INSTANCE_SECRET").encode()

def render_sidebar(section, token_arg, status):
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

    links.append(dbc.Nav(navs, vertical=True, pills=True))
    links.append(html.Div([
        html.I(className='fa-solid fa-check', style={'marginRight': '2rem'}),
        html.P("(" + status + ")")], className='sidebar-header'))
    return html.Div(links, className='sidebar')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user_id', storage_type="memory", data='0'),
    dcc.Store(id='role', storage_type="memory", data='none'),
    dcc.Store(id='status', storage_type="memory", data='not connected'),
    html.Div(id='sidebar'),
    html.Div(id='page-content', className='content')
])

'''
@app.server.before_request
def prout():
    token = request.args.get('auth_token')
    #print("t",token,  type(token))
'''

@app.callback(
    Output('user_id', 'data'),
    Output('role', 'data'),
    Output('status', 'data'),
    Input('url', 'href')
)
def check_auth_token(url):
    #print(url)
    token = urllib.parse.unquote(url.strip().split('=')[1])#.decode('utf8')
    #print(token)

    #if not session.get("token") or not token:
    if not token:
        #print("no token", flush=True)
        return "-1", "none", "no token"
    try:
        payload_b64, signature = token.split('.')
        payload_json = base64.b64decode(payload_b64 + '=' * (-len(payload_b64) % 4)).decode()
        expected_sig = hmac.new(SECRET_KEY, payload_json.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            #print("Signature mismatch", flush=True)
            return "-1", "none", "Signature mismatch"

        payload = json.loads(payload_json)
        if payload['expires'] < time.time():
            #print("time out", flush=True)
            return "-1", "none", "time out"
            
        #print("done", flush=True)
        # Attach user info to the Flask global context
        if 'id_enseignant' in payload:
            return payload['id_enseignant'], "enseignant", "Connected"
        elif 'id_etudiant' in payload:
            return payload['id_etudiant'], "etudiant", "Connected"
        elif 'id_administratif' in payload:
            return payload['id_administratif'], "administratif", "Connected"
        else:
            raise Exception("Unknown user class")
    
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return "-1", "none", "Exception"



# Callback pour mettre à jour la sidebar
@app.callback(
    Output('sidebar', 'children'),
    Input('url', 'href'),
    Input('url', 'pathname'),
    Input('status', 'data')
)
def update_sidebar(url, pathname, status):
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
    Input('url', 'href'),
    Input('url', 'pathname')
)
def render_page_content(url, pathname):
    token_arg = url.strip().split('?')[1]
    #print('token',token_arg)
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
