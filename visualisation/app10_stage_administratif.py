from dash import html, dcc
import dash_bootstrap_components as dbc
import mysql
import plotly.graph_objects as go
import app10_stage_tools

df_stages_with_supervisor = app10_stage_tools.get_stages_with_supervisorId()

df_stages_without_supervisor = app10_stage_tools.get_stages_without_supervisorId()

df_students_without_stage = app10_stage_tools.get_students_without_stage()

# Compter les étudiants avec et sans stage
avec_stage = df_stages_with_supervisor.shape[0] + df_stages_without_supervisor.shape[0]
sans_stage = df_students_without_stage.shape[0]

# Données pour le pie chart
labels = ['Avec Stage', 'Sans Stage']
values = [avec_stage, sans_stage]

# Création du pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

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
    html.H1(children='Représentation des Stages'), 
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