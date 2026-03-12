from dash import html, dcc, Input, State, Output
import dash_bootstrap_components as dbc
from pandas.core.interchange.dataframe_protocol import DataFrame
import pandas as pd

import app5_module_tools

app5_enseignant_view_layout = html.Div([
    html.H1(children='Modules et intervenants'),
    dcc.Dropdown(
        id='filtre_semestre',
        options=[ {'label': 'Tous les semestres', 'value': 'all'}],
        value='all',  # Valeur par défaut
    ),
    html.Div([
        html.Br(),
        html.Label("Mes modules :"),
        html.Div(id='modules_div'),
        html.Br(),
    ]),
    html.Div([
        html.Br(),
        html.Label("Résumé de mes intervenants :"),
        html.Div(id='intervenants_div'),
        html.Br(),
    ]),
    html.Div([
        html.Br(),
        html.Label("Résumé de mes interventions :"),
        html.Div(id='interventions_summary_div'),
        html.Br(),
    ]),
    html.Div([
        html.Br(),
        html.Label("Détail de mes interventions :"),
        html.Div(id='interventions_div'),
        html.Br(),
    ]),
])


################################################
# CallBack
#
def register_callbacks_view(app):

    #
    # Display Modules et Intervenants
    #

    # Remplissage des valeurs du filtre par semestre selon l'utilisateur
    @app.callback(
        Output('filtre_semestre', 'options'),
        Input('user_id', 'data'),
        State('token', 'data'),
    )
    def update_options(user_id, token):
        df = app5_module_tools.get_moduleByEnseignantId(token, user_id)[['semestre']].drop_duplicates()
        options = [{'label': 'Tous les semestres', 'value': 'all'}]
        options = options + [{'label': s, 'value': s} for s in df['semestre']]
        return options

    # Création de la table des modules selon l'utilisateur et le semestre sélectionné
    @app.callback(
        Output('modules_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
        State('token', 'data'),
    )
    def update_table_modules(user_id, selected_semestre, token):
        df = app5_module_tools.get_moduleByEnseignantId(token, user_id)[['code_module', 'nom_module', 'semestre', 'hCM', 'hTD', 'hTP', 'hPROJ', 'hPersonnelle', 'commentaire']].drop_duplicates()
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
        State('token', 'data'),
    )
    def update_table_intervenants(user_id, selected_semestre, token):
        df = app5_module_tools.get_moduleByEnseignantId(token, user_id)
        if df.empty:
            df = pd.DataFrame(columns=['code_module', 'nom_module', 'semestre', 'nom'])
        else:
            df = df[['code_module', 'nom_module', 'semestre', 'nom']].drop_duplicates().replace([None], [''], regex=True)
            if selected_semestre != 'all':
                df = df[df['semestre'] == selected_semestre]
            try:
                df = df.groupby(['code_module', 'nom_module'])['nom'].apply(','.join).to_frame().reset_index(level=[0,1])
            except:
                df = pd.DataFrame(columns=['code_module', 'nom_module', 'nom'])

        table_intervenants = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_intervenants]

    # Création de la table résumée des interventions selon l'utilisateur et le semestre sélectionné

    @app.callback(
        Output('interventions_summary_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
        State('token', 'data')
    )
    def update_table_interventions_summary(user_id, selected_semestre, token):
        df = app5_module_tools.get_moduleByIntervenantId(token, user_id)
        if df.empty:
            df = pd.DataFrame(columns=['semestre', 'code_module', 'nom_module', 'nom_groupe', 'type', 'numero_ordre', 'duree_h'])
        df = df[['semestre', 'code_module', 'nom_module', 'nom_groupe', 'type', 'numero_ordre', 'duree_h']].drop_duplicates().replace([None], [''], regex=True).sort_values(by=['semestre', 'code_module'])
        if selected_semestre != 'all':
            df = df[df['semestre'] == selected_semestre]

        # ToDo Compute summary
        dfs = df[['type','duree_h']].groupby('type').sum().reset_index()


        table_interventions_summary = dbc.Table.from_dataframe(
            dfs,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )

        sum = df['duree_h'].sum()

        return [table_interventions_summary,html.Label("Total face à face : " + str(sum) + "h"),]

    # Création de la table des interventions selon l'utilisateur et le semestre sélectionné

    @app.callback(
        Output('interventions_div', 'children'),
        State('user_id', 'data'),
        Input('filtre_semestre', 'value'),
        State('token', 'data')
    )
    def update_table_interventions(user_id, selected_semestre, token):
        df = app5_module_tools.get_moduleByIntervenantId(token, user_id)
        if df.empty:
            df = pd.DataFrame(columns=['semestre', 'code_module', 'nom_module', 'nom_groupe', 'type', 'numero_ordre', 'duree_h'])
        df = df[['semestre', 'code_module', 'nom_module', 'nom_groupe', 'type', 'numero_ordre', 'duree_h']].drop_duplicates().replace([None], [''], regex=True).sort_values(by=['semestre', 'code_module'])
        if selected_semestre != 'all':
            df = df[df['semestre'] == selected_semestre]
        #df = df.groupby(['code_module', 'nom_module']).apply(','.join).to_frame().reset_index(level=[0, 1])

        table_interventions = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_interventions]