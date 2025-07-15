from dash import html, dcc, Input, State, Output, dash_table
import dash_bootstrap_components as dbc
from pandas.core.interchange.dataframe_protocol import DataFrame
import pandas as pd

import app5_module_tools
import app_tools

app5_enseignant_layout = html.Div([
    html.H1(children='Modules et intervenants'),
    dcc.Dropdown(
        id='filtre_semestre',
        options=[ {'label': 'Tous les semestres', 'value': 'all'}],
        value='all',  # Valeur par défaut
    ),
    html.Div([
        html.Label("Mes modules :"),
        html.Div(id='modules_div'),
    ]),
    html.Div([
        html.Label("Résumé de mes intervenants :"),
        html.Div(id='intervenants_div'),
    ]),
    html.H1(children='Séquençage'),
    dcc.Dropdown(
        id='filtre_module',
        options=[],
        placeholder="Sélectionnez un module",
    ),
    html.Div([
        html.Label("Add Séquencage :"),
        html.Div(id='add_sequencage_div'),
    ]),
    html.Button('Add', id='add_sequencage_button', n_clicks=0),
    html.Label('', id='sequencage_info_status'),
    html.Div([
        html.Label("Séquencage :"),
        html.Div(id='sequencage_div'),
    ]),
    html.H1(children='Séances'),
    dcc.Dropdown(
        id='filtre_type',
        options=[],
        placeholder="Sélectionnez un type de séance",
    ),
    html.Div([
        html.Label("Séances :"),
        html.Div(id='seance_div'),
    ]),
    html.H1(children='Session'),
    dcc.Dropdown(
        id='filtre_promo',
        options=[],
        placeholder="Sélectionnez une promotion",
    ),
    html.Div([
        html.Label("Session :"),
        html.Div(id='session_div'),
    ]),
])


def update_table_sequencage(user_id, selected_module):
    if not selected_module:
        return []
    df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
    df = df[df['id_module'] == selected_module][['nombre', 'type', 'duree_h', 'groupe_type', 'intervenant_principal']]
    #df = df[df['id_module'] == selected_module]
    #data=df.to_dict('records')
    #print(data, flush=True)
    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]

    table_intervenants = dash_table.DataTable(
        id='table_sequencage',
        columns=[{"name": i, "id": i}
                 for i in df.columns],  # columns must be defined so that DataTable be editable
        data=df.to_dict('records'),
        row_deletable=True,
        dropdown={
            "intervenant_principal": {
                "options": intervenant_options
            },
        },
    )
    return [table_intervenants]


#
# CallBack
#
def register_callbacks(app):

    #
    # Display Modules et Intervenants
    #

    # Remplissage des valeurs du filtre par semestre selon l'utilisateur
    @app.callback(
        Output('filtre_semestre', 'options'),
        Input('user_id', 'data')
    )
    def update_options(user_id):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['semestre']].drop_duplicates()
        options = [{'label': 'Tous les semestres', 'value': 'all'}]
        options = options + [{'label': s, 'value': s} for s in df['semestre']]
        return options

    # Création de la table des modules selon l'utilisateur et le semestre sélectionné
    @app.callback(
        Output('modules_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
    )
    def update_table_modules(user_id, selected_semestre):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['code_module', 'nom_module', 'semestre', 'hCM', 'hTD', 'hTP', 'hTPTD', 'hPROJ', 'hPersonnelle', 'commentaire']].drop_duplicates()
        if selected_semestre != 'all':
            df = df[df['semestre'] == selected_semestre]

        table_modules = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules]

    # Création de la table des intervenants selon l'utilisateur et le semestre sélectionné
    @app.callback(
        Output('intervenants_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
    )
    def update_table_intervenants(user_id, selected_semestre):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['code_module', 'nom_module', 'semestre', 'nom']].drop_duplicates().replace([None], [''], regex=True)
        if selected_semestre != 'all':
            df = df[df['semestre'] == selected_semestre]
        df = df.groupby(['code_module', 'nom_module'])['nom'].apply(','.join).to_frame().reset_index(level=[0,1])

        table_intervenants = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_intervenants]


    #
    # Séquençage
    #

    # Mise à jour du filtre des modules en fonction de l'utilisateur
    @app.callback(
        Output('filtre_module', 'options'),
        Input('user_id', 'data'),
    )
    def update_filter_sequencage_option(user_id):
        df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
        options = [{'label': row['code_module'], 'value': row['id_module']} for _, row in df[['id_module', 'code_module']].drop_duplicates().iterrows()]
        return options

    # Création de la ligne d'ajout de séquençage
    @app.callback(
        Output('add_sequencage_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
    )
    def add_table_sequencage(user_id,selected_module):
        if not selected_module:
            return []
        df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)[['nombre', 'type', 'duree_h', 'groupe_type', 'intervenant_principal']]
        columns = [{"name": i, "id": i, "editable": True, "presentation": "dropdown"}
                     if  i in ["intervenant_principal", "type", "groupe_type"]
                     else {"name": i, "id": i, "editable": True}
                     for i in df.columns] # columns must be defined so that DataTable be editable
        data = {}
        for i in df.columns:
            data[i]= ""
        df = app_tools.get_explicit_keys("LNM_groupe_type")
        groupe_type_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in df.iterrows()]
        df = app_tools.get_explicit_keys("LNM_enseignant")
        intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in df.iterrows()]
        df = app_tools.get_explicit_keys("LNM_seanceType")
        seance_type_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in df.iterrows()]

        table_intervenants = dash_table.DataTable(
            id='add_table',
            columns= columns,
            data=[data],
            dropdown={
                "type": {
                    "options": seance_type_options
                },
                "intervenant_principal": {
                    "options": intervenant_options
                },
                "groupe_type": {
                    "options": groupe_type_options
                }
            },
        )
        return [table_intervenants]

    # Ajout d'un séquençage au "clique" bouton (ajout à la BD et mise à jour de la table de séquençage)
    @app.callback(
        Output('sequencage_div', 'children', allow_duplicate=True),
        #Output('sequencage_info_status', 'children', allow_duplicate=True),
        State('user_id', 'data'),
        State('filtre_module', 'value'),
        State('add_table', 'data'),
        Input('add_sequencage_button', 'n_clicks'),
        prevent_initial_call=True,
    )
    def cb_add_sequencage(user_id,selected_module, data, button_n_clicks):
        if not selected_module:
            return []
        data[0]["module"] = selected_module
        print(data[0], flush=True)
        ret = app5_module_tools.add_moduleSequencage(data[0])
        print(ret)
        return update_table_sequencage(user_id,selected_module)#, ret

    # Remove
    @app.callback(
        #Output('sequencage_info_status', 'children'),
        Input('table_sequencage', 'data_previous'),
        State('table_sequencage', 'data'),
        State('user_id', 'data'),
        prevent_initial_call=True,
    )
    def cb_remove_sequencag(previous, current, user_id):
        if previous is None:
            print("Kaboum", flush=True)
            #return "Kaboum"
        else:
            df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
            to_remove = [row for row in previous if row not in current][0]
            #print('toRemove', to_remove, flush=True)
            id_to_remove = df[(df['nombre'] == to_remove['nombre'])
                             & (df['type'] == to_remove['type'])
                             & (df['duree_h'] == to_remove['duree_h'])
                             & (df['groupe_type'] == to_remove['groupe_type'])][['id_module_sequencage']].iat[0, 0]
            #print('id_toRemove', id_to_remove, flush=True)
            app5_module_tools.remove_moduleSequencage(id_to_remove)

    # Mise à jour de la table des séquençages selon le module sélectionné
    @app.callback(
        Output('sequencage_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
    )
    def cb_update_table_sequencage(user_id,selected_module):
        return update_table_sequencage(user_id,selected_module)

    #
    # Séances
    #
    @app.callback(
        Output('seance_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        Input('filtre_type', 'value'),
    )
    def cb_update_table_seance(user_id,selected_type):
        return []


    #
    # Session
    #
    @app.callback(
        Output('seance_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        Input('filtre_type', 'value'),
        Input('filtre_promo', 'value'),
    )
    def cb_update_table_seance(user_id,selected_promo):
        return []