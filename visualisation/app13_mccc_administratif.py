from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import app_tools
import app13_mccc_tools

def update_table_m2c3(id_filiere, id_statut):
    df = app13_mccc_tools.get_list_modules_m2c3(id_filiere, id_statut)
    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in
                           dfi.iterrows()]
    table_m2c3 = dash_table.DataTable(
        id='table_m2c3',
        columns=[{"name": i, "id": i}
                 for i in df.columns] + [{"name": 'nouveau_responsable', "id": 'nouveau_responsable', "editable": True,
                                          "presentation": "dropdown", }],
        # columns must be defined so that DataTable be editable
        data=df.to_dict('records'),
        sort_action='native',
        sort_mode="multi",
        row_deletable=False,
        dropdown={
            "nouveau_responsable": {
                "options": intervenant_options,
                "clearable": True,
            }
        },
        style_cell_conditional=[
            {'if': {'column_id': 'id_module', },
             'display': 'None', }],
    )
    return table_m2c3

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
            html.Div(id='div_table_m2c3')])
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
        Output(component_id='div_table_m2c3', component_property='children'),
        Input(component_id='filiere_input', component_property='value'),
        Input(component_id='statut_input', component_property='value'),
        prevent_initial_call=True
    )
    def display_table_m2c3(id_filiere, id_statut):
        if id_filiere and id_statut :
            table_m2c3 = update_table_m2c3(id_filiere, id_statut)
        else :
            table_m2c3 = dbc.Table()
        return [table_m2c3]

        # Changement d'intervenant principal au niveau séquençage

    @app.callback(
        Output('div_table_m2c3', 'children', allow_duplicate=True),
        Input('table_m2c3', 'data_previous'),
        State('table_m2c3', 'data'),
        State(component_id='filiere_input', component_property='value'),
        State(component_id='statut_input', component_property='value'),
        prevent_initial_call=True,
    )
    def cb_change_intervenant_sequencage(previous, current, id_filiere, id_statut):
        if previous is not None:
            row_changed = [row for row in current if row not in previous]
            if len(row_changed) > 0:  # else callback invoked by data deleted
                row_changed = row_changed[0]
                new_intervenant_id = row_changed['nouveau_responsable']
                id_module = row_changed['id_module']
                ret = app13_mccc_tools.set_modules_responsable(id_module, new_intervenant_id)
        return update_table_m2c3(id_filiere, id_statut)
