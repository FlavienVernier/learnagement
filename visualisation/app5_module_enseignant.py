from dash import html, Input, Output
import dash_bootstrap_components as dbc
import app5_module_tools


app5_enseignant_layout = html.Div([
    html.Div([
        html.Label("Mes modules :"),
        html.Div(id='modules_div'),
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS
    html.Div([
        html.Label("Mes intervenants :"),
        html.Div(id='intervenants_div'),
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS
])


def register_callbacks(app):
    @app.callback(
        Output('modules_div', 'children'),
        Input('user_id', 'data')
    )
    def update_table_modules(user_id):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['code_module', 'nom_module', 'semestre', 'hCM', 'hTD', 'hTP', 'hTPTD', 'hPROJ', 'hPersonnelle', 'commentaire']].drop_duplicates()
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
        Input('user_id', 'data')
    )
    def update_table_intervenants(user_id):
        df = app5_module_tools.get_moduleByEnseignantId(user_id)[['code_module', 'nom_module', 'nom']].drop_duplicates().replace([None], [''], regex=True)
        df = df.groupby(['code_module', 'nom_module'])['nom'].apply(','.join).to_frame().reset_index(level=[0,1])

        table_intervenants = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_intervenants]

