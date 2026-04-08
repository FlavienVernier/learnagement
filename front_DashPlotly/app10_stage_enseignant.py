from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import app10_stage_tools

# Définition de la mise en page de l'application
app10_enseignant_layout = html.Div(children=[
    html.H1(children='Représentation des Stages'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Encadrement de stages'),
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_stages')])
])

def register_callbacks(app):
    @app.callback(
        Output(component_id='table_stages', component_property='children'),
        Input(component_id='fake', component_property='value'),
        Input('user_id', 'data'),
        State('token', 'data'),
    )
    def display_table(user_id_fake, user_id, token):
        df = app10_stage_tools.get_stages_by_supervisorId(token, user_id)
        table_stages = dash_table.DataTable(
            id='table_stage',
            data=df.to_dict('records'),
            style_cell_conditional=[
                {'if': {'column_id': 'id_stage', },
                 'display': 'None', }]
        )

        # table_stages = dbc.Table.from_dataframe(
        #     df,
        #     # Key styling options:
        #     striped=True,
        #     bordered=True,
        #     hover=True
        # )
        return [table_stages]

