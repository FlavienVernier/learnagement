from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import app14_check_tools

# Définition de la mise en page de l'application
app14_administratif_layout = html.Div(children=[
    html.H1(children='Séquençage VS Maquette'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_sequencage_vs_maquette')]),
    html.H1(children='Modules sans UE'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_modules_sans_ue')]),
    html.H1(children='Modules sans AC'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='table_modules_sans_ac')]),
    html.H1(children='Enseignant sans cours'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='div_enseignant_sans_cours')]),
    html.H1(children='Session sans enseignant'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='div_session_sans_enseignant')]),
    html.H1(children='Poids ECTS'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            dcc.Input(id='fake', value='0', type='hidden'),
            html.Div(id='div_modules_ects')]),
])

def register_callbacks(app):
    @app.callback(
        Output(component_id='table_sequencage_vs_maquette', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df_stages = app14_check_tools.check_sequencage_vs_maquette()
        table_sequencage_vs_maquette = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_sequencage_vs_maquette]


    @app.callback(
        Output(component_id='table_modules_sans_ue', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df_stages = app14_check_tools.check_module_without_learning_unit()
        table_modules_sans_ue = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_sans_ue]


    @app.callback(
        Output(component_id='table_modules_sans_ac', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df_stages = app14_check_tools.check_module_without_learning_unit()
        table_modules_sans_ac = dbc.Table.from_dataframe(
            df_stages,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_sans_ac]


    @app.callback(
        Output(component_id='div_enseignant_sans_cours', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df = app14_check_tools.check_enseignant_sans_cours()
        table_enseignant_sans_cours = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_enseignant_sans_cours]


    @app.callback(
        Output(component_id='div_session_sans_enseignant', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df = app14_check_tools.check_session_sans_enseignant()
        table_session_sans_enseignant = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_session_sans_enseignant]


    @app.callback(
        Output(component_id='div_modules_ects', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df = app14_check_tools.check_module_ects()
        table_modules_ects = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_ects]