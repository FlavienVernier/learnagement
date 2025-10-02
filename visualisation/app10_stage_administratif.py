from time import sleep
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import app10_stage_tools
import app_tools
from datetime import date, datetime



def get_entreprises():
    df_stages_with_supervisor = app10_stage_tools.get_stages_with_supervisorId()
    df_stages_without_supervisor = app10_stage_tools.get_stages_without_supervisorId()

    # liste des entreprises
    entreprises = []
    if "entreprise" in df_stages_with_supervisor.columns.tolist() :
        entreprises = entreprises + df_stages_with_supervisor["entreprise"].tolist()
    if "entreprise" in df_stages_without_supervisor.columns.tolist() :
        entreprises = entreprises + df_stages_without_supervisor["entreprise"].tolist()
    return entreprises

def get_teachers():
    # liste des enseignants
    df_enseignants = app_tools.get_list_enseignants()
    enseignants = []
    if "nom" in df_enseignants.columns.tolist() :
        enseignants = df_enseignants["nom"].map(str) + " " + df_enseignants["prenom"].map(str)
        enseignants = enseignants.tolist()
    return enseignants



def get_internship_with_supervisor():
    df_stages_with_supervisor = app10_stage_tools.get_stages_with_supervisorId()
    return df_stages_with_supervisor

def update_table_stages_with_supervisor(nom_promo):
    df = app10_stage_tools.get_stages_with_supervisorId()

    if nom_promo and not df.empty:
        df = df[df["promo"]==nom_promo]

    # table_stages_with_supervisor = dbc.Table.from_dataframe(
    #     df,
    #     # Key styling options:
    #     striped=True,
    #     bordered=True,
    #     hover=True,
    # )
    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]

    table_stages_with_supervisor = dash_table.DataTable(
        id='table_stages_with_supervisor',
        columns=[{"name": i, "id": i}
                 for i in df.columns] + [{"name": 'nouveau_tuteur', "id": 'nouveau_tuteur', "editable": True, "presentation": "dropdown", }],
        editable=True,
        data=df.to_dict('records'),
        row_deletable=True,
        dropdown={
            "nouveau_tuteur": {
                "options": intervenant_options,
                "clearable":True,
            }
        },
        style_cell_conditional=[
            {'if': {'column_id': 'id_stage', },
             'display': 'None', }
        ],
    )
    return table_stages_with_supervisor

def get_internship_without_supervisor():
    df_stages_without_supervisor = app10_stage_tools.get_stages_without_supervisorId()
    return df_stages_without_supervisor

def update_table_stages_without_supervisor(nom_promo):

    df = app10_stage_tools.get_stages_without_supervisorId()

    if nom_promo and not df.empty:
        df = df[df["promo"]==nom_promo]
        


    # table_stages_without_supervisor = dbc.Table.from_dataframe(
    #     df,
    #     # Key styling options:
    #     striped=True,
    #     bordered=True,
    #     hover=True,
    # )
    dfi = app_tools.get_explicit_keys("LNM_enseignant")
    intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]

    table_stages_without_supervisor = dash_table.DataTable(
        id='table_stages_without_supervisor',
        columns=[{"name": i, "id": i}
                 for i in df.columns] + [{"name": 'nouveau_tuteur', "id": 'nouveau_tuteur', "editable": True, "presentation": "dropdown", }],
        editable=True,
        data=df.to_dict('records'),
        row_deletable=True,
        dropdown={
            "nouveau_tuteur": {
                "options": intervenant_options,
                "clearable":True,
            }
        },
        style_cell_conditional=[
            {'if': {'column_id': 'id_stage', },
             'display': 'None', }
        ],
    )
    return table_stages_without_supervisor

def get_students_without_internship():
    df_students_without_stage = app10_stage_tools.get_students_without_stage()

    # liste des étudiants sans stage
    etudiants_sans_stage = {}
    if "nom" in df_students_without_stage.columns.tolist() :
        etudiants_sans_stage_label = (df_students_without_stage["nom"].map(str) + " " + df_students_without_stage["prenom"].map(str))
        etudiants_sans_stage_label = etudiants_sans_stage_label.tolist()
        etudiants_sans_stage_value = df_students_without_stage["id_etudiant"].tolist()
        etudiants_sans_stage = dict(zip(etudiants_sans_stage_label, etudiants_sans_stage_value))
    return etudiants_sans_stage

def update_table_students_without_internship(nom_promo):

    df = app10_stage_tools.get_students_without_stage()

    if nom_promo and not df.empty:
        df = df[df["promo"]==nom_promo]

    # table_students_without_stage = dbc.Table.from_dataframe(
    #     df,
    #     # Key styling options:
    #     striped=True,
    #     bordered=True,
    #     hover=True,
    # )
    table_students_without_stage = dash_table.DataTable(
        id='table_students_without_stage',
        columns=[{"name": i, "id": i}
                 for i in df.columns],
        editable=False,
        data=df.to_dict('records'),
        row_deletable=False,
        style_cell_conditional=[
            {'if': {'column_id': 'id_etudiant', },
             'display': 'None', }
        ],
    )
    return table_students_without_stage

def update_pie_chart(nom_promo):
    # Compter les étudiants avec et sans stage
    #avec_stage_avec_tuteur = df_stages_with_supervisor().shape[0]
    #avec_stage_sans_tuteur = df_stages_without_supervisor().shape[0]
    #sans_stage = df_students_without_stage().shape[0]

    df_stages_with_supervisor = get_internship_with_supervisor()
    df_stages_without_supervisor = get_internship_without_supervisor()
    df_students_without_stage = app10_stage_tools.get_students_without_stage()


    if nom_promo:
        if not df_stages_with_supervisor.empty:
            df_stages_with_supervisor = df_stages_with_supervisor[df_stages_with_supervisor["promo"]==nom_promo]
        if not df_stages_without_supervisor.empty:
            df_stages_without_supervisor = df_stages_without_supervisor[df_stages_without_supervisor["promo"]==nom_promo]
        if not df_students_without_stage.empty:
            df_students_without_stage = df_students_without_stage[df_students_without_stage["promo"]==nom_promo]

    avec_stage_avec_tuteur = len(df_stages_with_supervisor)
    avec_stage_sans_tuteur = len(df_stages_without_supervisor)
    sans_stage = len(df_students_without_stage)

    # Données pour le pie chart
    fig_labels = ['Avec Stage et tuteur', 'Avec Stage, sans tuteur', 'Sans Stage']
    fig_values = [avec_stage_avec_tuteur, avec_stage_sans_tuteur, sans_stage]

    # Création du pie chart
    fig = go.Figure(data=[go.Pie(labels=fig_labels, values=fig_values, hole=.3)])

    # Personnalisation du pie chart
    fig.update_traces(marker=dict(colors=['#00FF00', '#0000FF', '#FF0000']))
    fig.update_layout(title_text="Répartition des étudiants avec ou sans stage")

    return dcc.Graph(id='pie_chart', figure=fig)


# Définition de la mise en page de l'application
app10_administratif_layout = html.Div(children=[
    html.H1(children='Gestion des Stages'),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            html.H2(children='Sélection de promo'),
            dcc.Dropdown(
                id='app10_filtre_promo',
                options=[],
                placeholder="Sélectionnez une promotion",
            ),
        ]),
    html.Div(
       id="div_pie_chart",
       style={'display': 'inline-block', 'verticalAlign': 'top',},
       children=[
            update_pie_chart(None)]),
    html.Br(),
    html.Div([
        html.H2(children='Nouveau stage'),
        dcc.Input(id='stage_id', value='0', type='hidden'),
        dbc.Row([
            dbc.Label("Etudiant", html_for="etudiant_input", width=2),
            dbc.Col(dcc.Dropdown(id="etudiant_input",
                                 options=[{'label': k, 'value': v} for k, v in get_students_without_internship().items()],
                                 placeholder="Please select student"), width=8),

        ], className="mb-3",),
        dbc.Row([
            dbc.Label("Entreprise", html_for="entreprise_input", width=2),
            dbc.Col(dcc.Dropdown(id="entreprise_input",
                                 options=[{'label': v, 'value': v} for v in get_entreprises()],
                                 placeholder="Please enter the entreprise name",
                                 search_value='',
                                 clearable=True,
                                 ), width=8),
            dbc.Input(id="new_entreprise_input", type='hidden', value=''),
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
            dbc.Label("Ville", html_for="ville_input", width=2),
            dbc.Col(dbc.Input(id="ville_input", placeholder="Please enter the location"), width=8),
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
                                 options=[{'label': "Please select tuteur", 'value': "NULL"}] + [{'label': v, 'value': v} for v in get_teachers()],
                                 placeholder="Please select tuteur",
                                 value=""), width=8),
        ], className="mb-3",),
        dbc.Row([
            dbc.Button("Save the data", id="submit-button", color="primary", outline=True, disabled=False)],
            className="mb-3")
    ]),
    html.Br(),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',}, 
        children=[ 
            html.H2(children='Stage avec tuteur'),
            html.Div(id="div_stages_with_supervisor")
        ]),
    html.Br(),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[ 
            html.H2(children='Stage sans tuteur'),
            html.Div(id="div_stages_without_supervisor")
        ]),
    html.Br(),
    html.Div(
        style={'display': 'inline-block', 'verticalAlign': 'top',},
        children=[
            html.H2(children='Etudiants sans stage'),
            html.Div(id="div_students_without_stage")
        ])
])




#################################
# CallBack
#################################

def register_callbacks(app):
    # Mise à jour du filtre des promo en fonction du module selectionné
    @app.callback(
        Output('app10_filtre_promo', 'options'),
        Input('user_id', 'data'),
    )
    def update_filter_promo_option(user_id):
        df = app_tools.get_list_promo()
        options = [{'label': row['promo'], 'value': row['promo']} for _, row in
                   df[['promo']].iterrows()]
        return options

    @app.callback(
        Output(component_id='div_stages_with_supervisor', component_property='children'),
        Output(component_id='div_stages_without_supervisor', component_property='children'),
        Output(component_id='div_students_without_stage', component_property='children'),
        Input('user_id', 'data'),
        Input('app10_filtre_promo', 'value'),
    )
    def init_tables(user_id, nom_promo):
        return update_table_stages_with_supervisor(nom_promo), update_table_stages_without_supervisor(nom_promo), update_table_students_without_internship(nom_promo)

    # Store entreprise into dash list (not in db)
    @app.callback(
        Output('new_entreprise_input', 'value'),
        Output('entreprise_input', 'placeholder'),
        Input('entreprise_input', 'search_value'),
        State('new_entreprise_input', 'value'),
        prevent_initial_call=True
    )
    def store_new_entreprise(search_value, new_entreprise_input):
        value = search_value
        if search_value == "":
            value = new_entreprise_input
        return value, value

    @app.callback(
        Output(component_id='submit-button', component_property='children', allow_duplicate=True),
        Output(component_id='div_pie_chart', component_property='children', allow_duplicate=True),
        Output(component_id='div_stages_with_supervisor', component_property='children', allow_duplicate=True),
        Output(component_id='div_stages_without_supervisor', component_property='children', allow_duplicate=True),
        Output(component_id='div_students_without_stage', component_property='children', allow_duplicate=True),
        Input(component_id='submit-button', component_property='n_clicks'),
        State('app10_filtre_promo', 'value'),
        State('entreprise_input', 'value'),
        State('new_entreprise_input', 'value'),
        State('sujet_input', 'value'),
        State('mission_input', 'value'),
        State('ville_input', 'value'),
        State('dates_input', 'start_date'),
        State('dates_input', 'end_date'),
        State('etudiant_input', 'value'),
        State('tuteur_input', 'value'),
        prevent_initial_call=True,
        running=[(Output("submit-button", "disabled"), True, False)]

    )
    def save_stage(save_button, nom_promo, entreprise, new_entreprise, sujet, mission, ville, start_date, end_date, id_etudiant, id_enseignant):
        if id_etudiant and (entreprise or new_entreprise) and sujet and mission and start_date and end_date:
            if not entreprise:
                entreprise = new_entreprise
            save_status = app10_stage_tools.add_stage(entreprise, sujet, mission, ville, start_date, end_date, id_etudiant, id_enseignant)
            print(save_status, flush=True)
            return save_status, [update_pie_chart(nom_promo)], update_table_stages_with_supervisor(nom_promo), update_table_stages_without_supervisor(nom_promo), update_table_students_without_internship(nom_promo)
        else:
            raise PreventUpdate

    @app.callback(
        Output(component_id='submit-button', component_property='children'),
        Input(component_id='submit-button', component_property='children'),
        prevent_initial_call=True,
    )
    def button_text(text):
        sleep(1)
        return "Save the data"

    # set internship advisor
    @app.callback(
        Output(component_id='div_pie_chart', component_property='children', allow_duplicate=True),
        Output(component_id='div_stages_with_supervisor', component_property='children',allow_duplicate=True),
        Output(component_id='div_stages_without_supervisor', component_property='children',allow_duplicate=True),
        Input('table_stages_without_supervisor', 'data_previous'),
        State('table_stages_without_supervisor', 'data'),
        State('app10_filtre_promo', 'value'),
        prevent_initial_call=True,
    )
    def cb_set_internship_supervisor(previous, current, nom_promo):
        if previous is None or current is None:
            return [update_pie_chart(nom_promo)], update_table_stages_with_supervisor(nom_promo), update_table_stages_without_supervisor(nom_promo)
        elif len(previous) > len(current):  # else row updated
            to_remove = [row for row in previous if row not in current][0]
            # df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
            # # print('toRemove', to_remove, flush=True)
            # id_to_remove = df[(df['nombre'] == to_remove['nombre'])
            #                   & (df['type'] == to_remove['type'])
            #                   & (df['duree_h'] == to_remove['duree_h'])
            #                   & (df['groupe_type'] == to_remove['groupe_type'])][['id_module_sequencage']].iat[0, 0]
            # print('id_toRemove', id_to_remove, flush=True)
            id_to_remove = to_remove['id_stage']
            app10_stage_tools.remove_stage(id_to_remove)
            #return [update_pie_chart()]
            #return [update_pie_chart()], update_table_stages_with_supervisor(), update_table_stages_without_supervisor()
        else:
            row_changed = [row for row in current if row not in previous]
            if len(row_changed) > 0:  # else callback invoked by data deleted
                    # df = app5_module_tools.get_moduleSequenceByEnseignantId(user_id)
                    row_changed = row_changed[0]
                    new_supervisor_id = row_changed['nouveau_tuteur']
                    id_stage = row_changed['id_stage']
                    # id_sequence = df[(df['type'] == row_changed['type'])
                    #                    & (df['numero_ordre'] == row_changed['numero_ordre'])
                    #                    & (df['duree_h'] == row_changed['duree_h'])
                    #                    & (df['groupe_type'] == row_changed['groupe_type'])][['id_module_sequencage']].iat[0, 0]
                    ret = app10_stage_tools.set_internship_supervisor(id_stage, new_supervisor_id)
        return [update_pie_chart(nom_promo)], update_table_stages_with_supervisor(nom_promo), update_table_stages_without_supervisor(nom_promo)

        # reset internship advisor
    @app.callback(
        Output(component_id='div_stages_with_supervisor', component_property='children', allow_duplicate=True),
        Output(component_id='div_stages_without_supervisor', component_property='children', allow_duplicate=True),
        Input('table_stages_with_supervisor', 'data_previous'),
        State('table_stages_with_supervisor', 'data'),
        State('app10_filtre_promo', 'value'),
        prevent_initial_call=True,
    )
    def cb_reset_internship_supervisor(previous, current, nom_promo):
        if previous is not None and current is not None and len(previous) == len(current):
            row_changed = [row for row in current if row not in previous]
            if len(row_changed) > 0:  # else callback invoked by data deleted
                # df = app5_module_tools.get_moduleSequenceByEnseignantId(user_id)
                row_changed = row_changed[0]
                new_supervisor_id = row_changed['nouveau_tuteur']
                id_stage = row_changed['id_stage']
                # id_sequence = df[(df['type'] == row_changed['type'])
                #                    & (df['numero_ordre'] == row_changed['numero_ordre'])
                #                    & (df['duree_h'] == row_changed['duree_h'])
                #                    & (df['groupe_type'] == row_changed['groupe_type'])][['id_module_sequencage']].iat[0, 0]
                ret = app10_stage_tools.set_internship_supervisor(id_stage, new_supervisor_id)
        return update_table_stages_with_supervisor(nom_promo), update_table_stages_without_supervisor(nom_promo)

    # Remove stage with supervisor
    @app.callback(
        Output(component_id='div_pie_chart', component_property='children', allow_duplicate=True),
        Input('table_stages_with_supervisor', 'data_previous'),
        State('table_stages_with_supervisor', 'data'),
        State('app10_filtre_promo', 'value'),
        prevent_initial_call=True,
    )
    def cb_remove_stage_with(previous, current, nom_promo):
        if previous is not None and current is not None and len(previous) > len(current):  # else row updated
            to_remove = [row for row in previous if row not in current][0]
            # df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
            # # print('toRemove', to_remove, flush=True)
            # id_to_remove = df[(df['nombre'] == to_remove['nombre'])
            #                   & (df['type'] == to_remove['type'])
            #                   & (df['duree_h'] == to_remove['duree_h'])
            #                   & (df['groupe_type'] == to_remove['groupe_type'])][['id_module_sequencage']].iat[0, 0]
            # print('id_toRemove', id_to_remove, flush=True)
            id_to_remove = to_remove['id_stage']
            app10_stage_tools.remove_stage(id_to_remove)
        return [update_pie_chart(nom_promo)]

    # Remove stage without supervisor
    # @app.callback(
    #     Output(component_id='div_pie_chart', component_property='children', allow_duplicate=True),
    #     Input('table_stages_without_supervisor', 'data_previous'),
    #     State('table_stages_without_supervisor', 'data'),
    #     prevent_initial_call=True,
    # )
    # def cb_remove_stage_without(previous, current):
    #     if previous is None:
    #         print("Kaboum", flush=True)
    #         # return "Kaboum"
    #     elif len(previous) > len(current):  # else row updated
    #         to_remove = [row for row in previous if row not in current][0]
    #         # df = app5_module_tools.get_moduleSequencageByEnseignantId(user_id)
    #         # # print('toRemove', to_remove, flush=True)
    #         # id_to_remove = df[(df['nombre'] == to_remove['nombre'])
    #         #                   & (df['type'] == to_remove['type'])
    #         #                   & (df['duree_h'] == to_remove['duree_h'])
    #         #                   & (df['groupe_type'] == to_remove['groupe_type'])][['id_module_sequencage']].iat[0, 0]
    #         # print('id_toRemove', id_to_remove, flush=True)
    #         id_to_remove = to_remove['id_stage']
    #         app10_stage_tools.remove_stage(id_to_remove)
    #         return [update_pie_chart()]