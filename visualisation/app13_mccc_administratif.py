from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import app_tools
import app13_mccc_tools

# Définition de la mise en page de l'application
app13_administratif_layout = html.Div(children=[
    html.H1(children='Responsabilités de modules'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_responsabilites')]),
    dcc.Dropdown(id="filiere_input",
                    options=[],
                    placeholder="Please select filiere",
                    value=""),
    dcc.Dropdown(id="statut_input",
                    options=[],
                    placeholder="Please select statut",
                    value=""),
    html.H1(children='M2C3'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            html.Div(id='table_m2c3')])
])

def register_callbacks(app):
    @app.callback(
        Output(component_id='filiere_input', component_property='options'),
        Input(component_id='fake', component_property='value')
    )
    def update_filiere_input_options(value):
        options = []
        df = app_tools.get_list_filieres()
        options = [{'label': row['nom_filiere'], 'value': row['id_filiere']} for _, row in df.iterrows()]
        return options

    @app.callback(
        Output(component_id='statut_input', component_property='options'),
        Input(component_id='fake', component_property='value')
    )
    def update_statut_input_options(value):
        options = []
        df = app_tools.get_list_statuts()
        options = [{'label': row['nom_statut'], 'value': row['id_statut']} for _, row in df.iterrows()]
        return options

    @app.callback(
        Output(component_id='table_responsabilites', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table_responsabilites(user_id_fake):
        df_stages = app13_mccc_tools.get_list_enseignants_responsabilites()
        table_responsabilites = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_responsabilites]
    @app.callback(
        Output(component_id='table_m2c3', component_property='children'),
        Input(component_id='filiere_input', component_property='value'),
        Input(component_id='statut_input', component_property='value'),
        prevent_initial_call=True
    )
    def display_table_m2c3(id_filiere, id_statut):
        if id_filiere and id_statut :
            df_stages = app13_mccc_tools.get_list_modules_m2c3(id_filiere, id_statut)
            table_m2c3 = dbc.Table.from_dataframe(
                df_stages,
                # Key styling options:
               striped=True,
                bordered=True,
                hover=True,
            )
        else :
            table_m2c3 = dbc.Table()
        return [table_m2c3]

