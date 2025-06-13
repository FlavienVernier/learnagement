from flask import request, session
import dash
from dash import html, dcc, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import mysql
import plotly.graph_objects as go
import pandas as pd
import requests
import app10_stage_tools


#

#df_stages = app10_stage_tools.get_stages_by_supervisorId(14)
#df_stages = app10_stage_tools.get_stages_by_supervisorId(int(session.get('id_enseignant')))
'''
table_stages = dbc.Table.from_dataframe(
    df_stages,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)
'''

# Définition de la mise en page de l'application
app10_enseignant_layout = html.Div(children=[
    html.H1(children='Représentation des Stages'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Encadrement de stages'),
            dcc.Input(id='fake', value='0', type='hidden'),
            #html.Div([table_stages])])
            html.Div(id='table_stages')])
])



def register_callbacks(app):
    @app.callback(
        Output(component_id='table_stages', component_property='children'),
        #Output(component_id='my-id', component_property='value'),
        #"table_stages", "figure"),
        Input(component_id='fake', component_property='value'),
        Input('user_id', 'data')
        #Input(component_id='my-id', component_property='value')
    )
    def display_table(user_id_fake, user_id):
        print("user-id:'",user_id,"'", flush=True)
        df_stages = app10_stage_tools.get_stages_by_supervisorId(user_id)
        #df_stages = app10_stage_tools.get_stages_by_supervisorId(int(session.get('id_enseignant')))
        table_stages = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        #print("user-id:'",user_id,"'")
        #return [table_stages], user_id
        return [table_stages]

