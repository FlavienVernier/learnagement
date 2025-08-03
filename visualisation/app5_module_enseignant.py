from dash import html, dcc, Input, State, Output, dash_table
import dash_bootstrap_components as dbc
from pandas.core.interchange.dataframe_protocol import DataFrame
import pandas as pd

import app5_module_tools
import app_tools

app5_enseignant_view_layout = html.Div([
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
    html.Div([
        html.Label("Résumé de mes interventions :"),
        html.Div(id='interventions_div'),
    ]),
])
app5_enseignant_edit_layout = html.Div([
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
    html.Div([
        html.Label("Séquencage vs Maquette :"),
        html.Div(id='sequencage_vs_maquette_div'),
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

    table_sequencage = dash_table.DataTable(
        id='table_sequencage',
        # columns=[{"name": i, "id": i}
        #          if i != 'intervenant_principal'
        #          else {"name": i, "id": i, "editable": True, "presentation": "dropdown",}
        #          for i in df.columns],  # columns must be defined so that DataTable be editable
        columns=[{"name": i, "id": i}
                 if i != 'intervenant_principal'
                 else {"name": i, "id": i, "editable": True, "presentation": "dropdown", }
                 for i in df.columns] + [{"name": 'nouvel_intervenant', "id": 'nouvel_intervenant', "editable": True, "presentation": "dropdown", }],  # columns must be defined so that DataTable be editable
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        dropdown={
            #"intervenant_principal": {
            "nouvel_intervenant": {
                "options": intervenant_options,
                "clearable":True,
            }
        },
    )
    return [table_sequencage]

def update_table_sequence(user_id, selected_module, selected_seance_type):
    if not selected_module:
        return []
    df = app5_module_tools.get_moduleSequenceByEnseignantId(user_id)
    if selected_seance_type:
        df = df[(df['id_module'] == selected_module) & (df['id_seance_type'] == selected_seance_type)][['type', 'duree_h', 'groupe_type', 'numero_ordre', 'intervenant_principal', 'commentaire']]
    else:
        df = df[df['id_module'] == selected_module][['type', 'numero_ordre', 'duree_h', 'groupe_type', 'intervenant_principal', 'commentaire']]

    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]

    table_sequence = dash_table.DataTable(
        id='table_sequence',
        columns=[{"name": i, "id": i}
                 for i in df.columns],  # columns must be defined so that DataTable be editable
        editable=True,
        data=df.to_dict('records'),
        row_deletable=False,
        dropdown={
            "intervenant_principal": {
                "options": intervenant_options
            }
        },
    )
    return [table_sequence]

def update_table_session(user_id, selected_module, selected_seance_type, selected_promotion):
    if not selected_module:
        return []
    df = app5_module_tools.get_moduleSessionByEnseignantId(user_id)

    if selected_seance_type and selected_promotion:
        df = df[(df['id_module'] == selected_module) &
                (df['id_seance_type'] == selected_seance_type) &
                (df['id_promotion'] == selected_promotion)][['type', 'duree_h', 'nom_groupe', 'numero_ordre', 'intervenant', 'commentaire']]
    elif selected_seance_type:
        df = df[(df['id_module'] == selected_module) &
                (df['id_seance_type'] == selected_seance_type)][['type', 'numero_ordre', 'duree_h', 'nom_groupe', 'intervenant', 'commentaire']]
    else:
        df = df[(df['id_module'] == selected_module)][
            ['type', 'numero_ordre', 'duree_h', 'nom_groupe', 'intervenant', 'commentaire']]

    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]

    table_session = dash_table.DataTable(
        id='table_session',
        columns=[{"name": i, "id": i}
                 for i in df.columns],  # columns must be defined so that DataTable be editable
        data=df.to_dict('records'),
        row_deletable=False,
        dropdown={
            "intervenant": {
                "options": intervenant_options
            },
        },
    )
    return [table_session]
#
# CallBack
#
def register_callbacks_view(app):

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

    # Création de la table des interventions selon l'utilisateur et le semestre sélectionné

    @app.callback(
        Output('interventions_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
    )
    def update_table_intervenants(user_id, selected_semestre):
        df = app5_module_tools.get_moduleByIntervenantId(user_id)[
            ['semestre', 'code_module', 'nom_module', 'nom_groupe', 'type', 'numero_ordre', 'duree_h']].drop_duplicates().replace([None], [''], regex=True).sort_values(by=['semestre', 'code_module'])
        if selected_semestre != 'all':
            df = df[df['semestre'] == selected_semestre]
        #df = df.groupby(['code_module', 'nom_module']).apply(','.join).to_frame().reset_index(level=[0, 1])

        table_intervenants = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_intervenants]

####################################################
# Edit Callbacks
####################################################
def register_callbacks_edit(app):
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
        #print(data[0], flush=True)
        ret = app5_module_tools.add_moduleSequencage(data[0])
        #print(ret)
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
        elif len(previous) > len(current): #else row updated
            to_remove = [row for row in previous if row not in current][0]
            df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
            #print('toRemove', to_remove, flush=True)
            id_to_remove = df[(df['nombre'] == to_remove['nombre'])
                              & (df['type'] == to_remove['type'])
                              & (df['duree_h'] == to_remove['duree_h'])
                              & (df['groupe_type'] == to_remove['groupe_type'])][['id_module_sequencage']].iat[0, 0]
            #print('id_toRemove', id_to_remove, flush=True)
            app5_module_tools.remove_moduleSequencage(id_to_remove)

    # Changement d'intervenant principal au niveau séquençage
    @app.callback(
        Output('sequencage_div', 'children', allow_duplicate=True),
        Input('table_sequencage', 'data_previous'),
        State('table_sequencage', 'data'),
        State('user_id', 'data'),
        State('filtre_module', 'value'),
        prevent_initial_call=True,
    )
    def cb_change_intervenant(previous, current, user_id, selected_module):
        if previous is None:
            return update_table_sequencage(user_id, selected_module)
        else:
            row_changed = [row for row in current  if row not in previous]
            if len(row_changed) > 0: # else callback invoked by data deleted
                df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
                row_changed = row_changed[0]
                new_intervenant_id = row_changed['nouvel_intervenant']
                id_sequencage = df[(df['nombre'] == row_changed['nombre'])
                                  & (df['type'] == row_changed['type'])
                                  & (df['duree_h'] == row_changed['duree_h'])
                                  & (df['groupe_type'] == row_changed['groupe_type'])][['id_module_sequencage']].iat[0, 0]
                ret = app5_module_tools.set_intervenant_principal(id_sequencage, new_intervenant_id)
                return update_table_sequencage(user_id, selected_module)

    # Mise à jour de la table des séquençages selon le module sélectionné
    @app.callback(
        Output('sequencage_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
    )
    def cb_update_table_sequencage(user_id,selected_module):
        return update_table_sequencage(user_id,selected_module)

    @app.callback(
        Output('sequencage_vs_maquette_div', 'children'),
        Input('table_sequencage', 'data'),
        State('filtre_module', 'value'),
        State('user_id', 'data'),
    )
    def cb_check_sequencage_vs_maquette(data, id_module, user_id):
        df = app5_module_tools.check_moduleSequencage(user_id)
        if id_module:
            df = df[df['id_module'] == id_module][['code_module', 'ecart_CM', 'ecart_TD', 'ecart_TP', 'ecart_TPTD']]

        table_check = dash_table.DataTable(
            id='check_table',
            data=df.to_dict('records'),
        )
        return [table_check]

    #
    # Séances (Séquences)
    #

    # Mise à jour du filtre des types de cours en fonction du module selectionné
    @app.callback(
        Output('filtre_type', 'options'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        prevent_initial_call=True,
    )
    def update_filter_sequence_option(user_id, selected_module):
        df = app5_module_tools.get_moduleSequenceByEnseignantId(user_id)
        options = [{'label': row['type'], 'value': row['id_seance_type']} for _, row in df[df['id_module'] == selected_module][['id_seance_type', 'type']].drop_duplicates().iterrows()]
        return options

    # Mise à jour de la table des séances (séquences) selon le module sélectionné et le type de cours
    @app.callback(
        Output('seance_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        Input('filtre_type', 'value'),
        prevent_initial_call=True,
    )
    def cb_update_table_seance(user_id, selected_module, selected_type):
        return update_table_sequence(user_id, selected_module, selected_type)


    #
    # Session
    #

    # Mise à jour du filtre des promo en fonction du module selectionné
    @app.callback(
        Output('filtre_promo', 'options'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        prevent_initial_call=True,
    )
    def update_filter_session_option(user_id, selected_module):
        df = app5_module_tools.get_moduleSessionByEnseignantId(user_id)
        options = [{'label': row['promo'], 'value': row['id_promo']} for _, row in df[df['id_module'] == selected_module][['id_promo', 'promo']].drop_duplicates().iterrows()]
        return options

    @app.callback(
        Output('session_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_module', 'value'),
        Input('filtre_type', 'value'),
        Input('filtre_promo', 'value'),
        prevent_initial_call=True,
    )
    def cb_update_table_seance(user_id, selected_module, selected_type, selected_promo):
        return update_table_session(user_id, selected_module, selected_type, selected_promo)