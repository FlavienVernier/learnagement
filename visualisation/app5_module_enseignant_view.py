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