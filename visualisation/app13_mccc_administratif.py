from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import app13_mccc_tools

# Définition de la mise en page de l'application
app13_administratif_layout = html.Div(children=[
    html.H1(children='Responsabilités de modules'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_responsabilites')])
])

def register_callbacks(app):
    @app.callback(
        Output(component_id='table_responsabilites', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df_stages = app13_mccc_tools.get_list_enseignants_responsabilites()
        table_responsabilites = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_responsabilites]

