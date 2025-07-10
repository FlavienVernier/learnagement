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
        placeholder="Sélectionnez une période",
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
        id='filtre_sequencage',
        options=[],
        placeholder="Sélectionnez une période",
    ),
    html.Div([
        html.Label("Add Séquencage :"),
        html.Div(id='add_sequencage_div'),
    ]),
    html.Button('Add', id='add_sequencage_button', n_clicks=0),
    html.Div([
        html.Label("Séquencage :"),
        html.Div(id='sequencage_div'),
    ]),
    html.H1(children='Mise à jour modules et intervenants'),
])


def update_table_sequencage(user_id, selected_module):
    if not selected_module:
        return []
    df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
    df = df[df['code_module'] == selected_module]

    table_intervenants = dbc.Table.from_dataframe(
        df,
        # Key styling options:
        striped=True,
        bordered=True,
        hover=True,
    )
    table_intervenants = dash_table.DataTable(
        columns=[{"name": i, "id": i} if i != "intervenant_principal"
                 else {"name": i, "id": i, "editable": True, "presentation": "dropdown", }
                 for i in df.columns],  # columns must be defined so that DataTable be editable
        data=df.to_dict('records'),
        row_deletable=True,
        dropdown={
            "intervenant_principal": {
                "options": [{"label": i, "value": i} for i in ["Low", "Medium", "High"]]
            },
        },
    )
    return [table_intervenants]

def register_callbacks(app):
    @app.callback(
        Output('filtre_semestre', 'options'),
        Input('user_id', 'data')
    )
    def update_options(user_id):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['semestre']].drop_duplicates()
        options = [{'label': 'Tous les semestres', 'value': 'all'}]
        options = options + [{'label': s, 'value': s} for s in df['semestre']]
        return options

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

    @app.callback(
        Output('filtre_sequencage', 'options'),
        Input('user_id', 'data'),
    )
    def update_filter_sequencage_option(user_id):
        df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
        options = [{'label': code_module, 'value': code_module} for code_module in df['code_module'].drop_duplicates()]
        return options

    @app.callback(
        Output('add_sequencage_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_sequencage', 'value'),
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

    @app.callback(
        Output('sequencage_div', 'children', allow_duplicate=True),
        State('user_id', 'data'),
        State('filtre_sequencage', 'value'),
        State('add_table', 'data'),
        Input('add_sequencage_button', 'n_clicks'),
        prevent_initial_call=True,
    )
    def cb_add_sequencage(user_id,selected_module, data, button_n_clicks):
        if not selected_module:
            return []
        print("data", data, flush=True)
        return update_table_sequencage(user_id,selected_module)

    @app.callback(
        Output('sequencage_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_sequencage', 'value'),
    )
    def cb_update_table_sequencage(user_id,selected_module):
        return update_table_sequencage(user_id,selected_module)
        # if not selected_module:
        #     return []
        # df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
        # df = df[df['code_module'] == selected_module]
        #
        # table_intervenants = dbc.Table.from_dataframe(
        #     df,
        #     # Key styling options:
        #     striped=True,
        #     bordered=True,
        #     hover=True,
        # )
        # table_intervenants = dash_table.DataTable(
        #     columns=[{"name": i, "id": i} if  i != "intervenant_principal"
        #              else {"name": i, "id": i, "editable": True, "presentation": "dropdown",}
        #              for i in df.columns], # columns must be defined so that DataTable be editable
        #     data=df.to_dict('records'),
        #     row_deletable=True,
        #     dropdown={
        #         "intervenant_principal": {
        #             "options": [{"label": i, "value": i} for i in ["Low","Medium","High"]]
        #         },
        #     },
        # )
        # return [table_intervenants]