from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import mysql
import mysql.connector
import app3_absenteisme_tools


app3_enseignant_layout = html.Div([
    html.Div([
        html.Label("Absences à mes séances :"),
        html.Div(id='seance_enseignant')
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS
    html.Div([
        html.Label("Absences dans mes modules :"),
        html.Div(id='module_enseignant')
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS


])


def register_callbacks(app):
    @app.callback(
        Output('seance_enseignant', 'children'),
        Input('user_id', 'data')
    )
    def update_table_abs_seance(user_id):
        df_abs = app3_absenteisme_tools.get_absenceByResponsableId(user_id)
        table_absence = dbc.Table.from_dataframe(
            df_abs,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_absence]

    @app.callback(
        Output('module_enseignant', 'children'),
        Input('user_id', 'data')
    )
    def update_table_abs_module(user_id):
        df_abs = app3_absenteisme_tools.get_absenceByEnseignantId(user_id)
        table_absence = dbc.Table.from_dataframe(
            df_abs,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_absence]