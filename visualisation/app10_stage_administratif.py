from time import sleep

from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import mysql
import plotly.graph_objects as go
import app10_stage_tools
import app_tools
from datetime import date, datetime

df_stages_with_supervisor = app10_stage_tools.get_stages_with_supervisorId()

df_stages_without_supervisor = app10_stage_tools.get_stages_without_supervisorId()

df_students_without_stage = app10_stage_tools.get_students_without_stage()

# liste des étudiants sans stage
etudiants_sans_stage_label = df_students_without_stage["nom"].map(str) + " " + df_students_without_stage["prenom"].map(str)
etudiants_sans_stage_label = etudiants_sans_stage_label.tolist()
etudiants_sans_stage_value = df_students_without_stage["id_etudiant"].tolist()
etudiants_sans_stage = dict(zip(etudiants_sans_stage_label, etudiants_sans_stage_value))

# liste des entreprises
entreprises = df_stages_with_supervisor["entreprise"].tolist() + df_stages_without_supervisor["entreprise"].tolist()

# liste des enseignants
df_enseignants = app_tools.get_students_without_stage()
enseignants = df_enseignants["nom"].map(str) + " " + df_enseignants["prenom"].map(str)
enseignants = enseignants.tolist()

# Compter les étudiants avec et sans stage
avec_stage_avec_tuteur = df_stages_with_supervisor.shape[0]
avec_stage_sans_tuteur = df_stages_without_supervisor.shape[0]
sans_stage = df_students_without_stage.shape[0]

# Données pour le pie chart
fig_labels = ['Avec Stage et tuteur', 'Avec Stage, sans tuteur', 'Sans Stage']
fig_values = [avec_stage_avec_tuteur, avec_stage_sans_tuteur, sans_stage]

# Création du pie chart
fig = go.Figure(data=[go.Pie(labels=fig_labels, values=fig_values, hole=.3)])

# Personnalisation du pie chart
fig.update_traces(marker=dict(colors=['#007BFF', '#FF8400']))
fig.update_layout(title_text="Répartition des étudiants avec ou sans stage")

#
table_stages_with_supervisor = dbc.Table.from_dataframe(
    df_stages_with_supervisor,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)
table_stages_without_supervisor = dbc.Table.from_dataframe(
    df_stages_without_supervisor,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)

table_students_without_stage = dbc.Table.from_dataframe(
    df_students_without_stage,
    # Key styling options:
    striped=True,
    bordered=True,
    hover=True,
)

# Définition de la mise en page de l'application
app10_administratif_layout = html.Div(children=[
    html.H1(children='Gestion des Stages'),
    html.Div([
        dcc.Input(id='stage_id', value='0', type='hidden'),
        dbc.Row([
            dbc.Label("Etudiant", html_for="etudiant_input", width=2),
            dbc.Col(dcc.Dropdown(id="etudiant_input",
                                 options=[{'label': k, 'value': v} for k, v in etudiants_sans_stage.items()],
                                 placeholder="Please select student"), width=8),

        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Entreprise", html_for="entreprise_input", width=2),
            dbc.Col(dcc.Dropdown(id="entreprise_input",
                                 options=[{'label': v, 'value': v} for v in entreprises],
                                 placeholder="Please enter the entreprise name"), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Sujet", html_for="sujet_input", width=2),
            dbc.Col(dbc.Input(id="sujet_input", placeholder="Please enter the subject"), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Mission", html_for="mission_input", width=2),
            dbc.Col(dbc.Textarea(id="mission_input", placeholder="Please enter the mission"), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Dates", html_for="dates_input", width=2),
            dbc.Col(dcc.DatePickerRange(
                id='dates_input',
                min_date_allowed=date(2025, 1, 1),
                max_date_allowed=date(2026, 12, 31),
                initial_visible_month=datetime.now(),
                start_date=datetime.now(),
                end_date=datetime.now()
            ), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Tuteur", html_for="tuteur_input", width=2),
            dbc.Col(dcc.Dropdown(id="tuteur_input",
                                 options=[{'label': "Please select tuteur", 'value': "NULL"}] + [{'label': v, 'value': v} for v in enseignants],
                                 placeholder="Please select tuteur"), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Button("Save the data", id="submit-button", color="primary", outline=True, disabled=False)],
            className="mb-3")
    ]),
    html.Div(
       style={'display': 'inline-block', 'verticalAlign': 'top',}, 
       children=[ 
            dcc.Graph(id='pie-chart', figure=fig) ]), 
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',}, 
        children=[ 
            html.H2(children='Stage avec tuteur'),
            html.Div([table_stages_with_supervisor])]),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Stage sans tuteur'),
            html.Div([table_stages_without_supervisor])]),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            html.H2(children='Etudiants sans stage'),
            html.Div([table_students_without_stage])])
])


def register_callbacks(app):
    @app.callback(
        Output(component_id='submit-button', component_property='children', allow_duplicate=True),
        Input(component_id='submit-button', component_property='n_clicks'),
        State('etudiant_input', 'value'),
        State('entreprise_input', 'value'),
        State('sujet_input', 'value'),
        State('mission_input', 'value'),
        State('dates_input', 'start_date'),
        State('dates_input', 'end_date'),
        State('tuteur_input', 'value'),
        prevent_initial_call=True,
        running=[(Output("submit-button", "disabled"), True, False)]

    )
    def save_stage(save_button, etudiant, entreprise, sujet, mission, start_date, end_date, enseignant):
        print(etudiant, entreprise, sujet, mission, start_date, end_date, enseignant, flush=True)
        if etudiant and entreprise and sujet and mission and start_date and end_date:
            print(etudiant, entreprise, sujet, mission, start_date, end_date, enseignant, flush=True)
            save_status = app10_stage_tools.add_stage(etudiant, entreprise, sujet, mission, start_date, end_date, enseignant)
            return save_status
        else:
            print("prout", flush=True)
            raise PreventUpdate

    @app.callback(
        Output(component_id='submit-button', component_property='children'),
        Input(component_id='submit-button', component_property='children')
    )
    def button_text(text):
        sleep(1)
        return "Save the data"