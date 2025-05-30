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

df_stages = app10_stage_tools.get_stages_by_supervisorId(14)
#df_stages = app10_stage_tools.get_stages_by_supervisorId(int(session.get('id_enseignant')))
table_stages = dbc.Table.from_dataframe(
    df_stages,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)

# Définition de la mise en page de l'application
app10_enseignant_layout = html.Div(children=[
    html.H1(children='Représentation des Stages'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Encadrement de stages'),
            html.Div([table_stages])])
])



def register_callbacks(app):
    @app.callback(
        Output("table_stages", "figure"),
        #Input("dashboard_option_dropdown", "value"),
        State("user_id_store", "data")
    )
    def display_table(user_id):
        df_stages = app10_stage_tools.get_stages_by_supervisorId(int(session.get('id_enseignant')))
        table_stages = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return table_stages

