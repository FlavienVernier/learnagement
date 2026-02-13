from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import app14_check_tools
import pandas as pd

# Définition de la mise en page de l'application
app14_administratif_layout = html.Div(children=[
    dbc.Button(
        'Séquençage VS Maquette',
            id="collapse-button1",
            className="mb-3",
            color="primary",
            n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
                 style={'display': 'inline-block', 'verticalAlign': 'top',},
                 children=[
                    dcc.Input(id='fake', value='0', type='hidden'),
                     html.Div(id='table_sequencage_vs_maquette')]
             ),
        id="collapse1",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Session VS Maquette',
            id="collapse_button_session_vs_maquette",
            className="mb-3",
            color="primary",
            n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
                 style={'display': 'inline-block', 'verticalAlign': 'top',},
                 children=[
                    dcc.Input(id='fake', value='0', type='hidden'),
                     html.Div(id='table_session_vs_maquette')]
             ),
        id="collapse_session_vs_maquette",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Modules sans UE',
        id="collapse-button2",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='table_modules_sans_ue')]
        ),
        id="collapse2",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Modules sans AC',
        id="collapse-button3",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='table_modules_sans_ac')]
        ),
        id="collapse3",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Enseignant sans cours',
        id="collapse-button4",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_enseignant_sans_cours')]
        ),
        id="collapse4",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Session sans enseignant',
        id="collapse-button5",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_session_sans_enseignant')]
        ),
        id="collapse5",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Poids ECTS',
        id="collapse-button6",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_modules_ects')]
        ),
        id="collapse6",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Corruption d\'intégrité référentielle dans la table session',
        id="collapse-button7",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_session_corruption')]
        ),
        id="collapse7",
        is_open=False,
    ),
])


######################################
# Callbacks
######################################

def register_callbacks(app):

    @app.callback(
        Output("collapse1", "is_open"),
        [Input("collapse-button1", "n_clicks")],
        [State("collapse1", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse_session_vs_maquette", "is_open"),
        [Input("collapse_button_session_vs_maquette", "n_clicks")],
        [State("collapse_session_vs_maquette", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse2", "is_open"),
        [Input("collapse-button2", "n_clicks")],
        [State("collapse2", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse3", "is_open"),
        [Input("collapse-button3", "n_clicks")],
        [State("collapse3", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse4", "is_open"),
        [Input("collapse-button4", "n_clicks")],
        [State("collapse4", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse5", "is_open"),
        [Input("collapse-button5", "n_clicks")],
        [State("collapse5", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse6", "is_open"),
        [Input("collapse-button6", "n_clicks")],
        [State("collapse6", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse7", "is_open"),
        [Input("collapse-button7", "n_clicks")],
        [State("collapse7", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output(component_id='table_sequencage_vs_maquette', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df = app14_check_tools.check_sequencage_vs_maquette()
        table_sequencage_vs_maquette = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_sequencage_vs_maquette]

    @app.callback(
        Output(component_id='table_session_vs_maquette', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_session_vs_maquette(token)
        if df.empty:
            df = pd.DataFrame(columns=['truc', 'bidule'])
        table_session_vs_maquette = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_session_vs_maquette]


    @app.callback(
        Output(component_id='table_modules_sans_ue', component_property='children'),
        Input(component_id='fake', component_property='value')
    )
    def display_table(user_id_fake):
        df = app14_check_tools.check_module_without_learning_unit()
        table_modules_sans_ue = dbc.Table.from_dataframe(
            df,
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
        df = app14_check_tools.check_module_without_learning_unit()
        table_modules_sans_ac = dbc.Table.from_dataframe(
            df,
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

    @app.callback(
        Output(component_id='div_session_corruption', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_session_corruption(token)
        if not df.empty:
            table_session_corruption = dbc.Table.from_dataframe(
                df,
                # Key styling options:
                striped=True,
                bordered=True,
                hover=True,
            )
            return [table_session_corruption]
        return [html.Label("No data available")]