from dotenv import load_dotenv
import os
import statistics
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import mysql
import pandas as pd
import plotly.graph_objs as go
import json
import math
import app4_notes_tools

app4_enseignant_layout = html.Div([
    html.H1(f"Visualisation des notes - prof ", style={'textAlign': 'center', 'marginBottom': '5px'}),

    html.Div(
        children=[
            # choix de la promo
            dcc.Dropdown(
                id='choix_promo_prof',
                options=[], #[{'label': 'Toutes les promos', 'value': 'all'}],
                # +[{'label': promo['id_promo'], 'value': ', '.join(map(str, promo['etudiants']))} for promo in promo_disponibles],
                # value=', '.join(map(str, promo_disponibles[0]['etudiants'])),
                value='all',
                style={'width': '48%'}
            ),

            # choix de la matière
            dcc.Dropdown(
                id='choix_matiere_prof',
                options=[],
                style={'width': '48%'}
            ),

            # choix du contrôle
            dcc.Dropdown(
                id='choix_controle_prof',
                style={'width': '48%', 'margin': 'auto'}
            ),
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '3px'}
    ),

    # affichage des notes
    dcc.Graph(
        id='affichage_note_prof',
        config={'displayModeBar': False},
        style={'margin': '10px auto', 'marginTop': '5px', 'marginBottom': '0px'}
    ),

    # affichage du classement
    html.Div(
        id='affichage_classement_prof',
        style={'textAlign': 'center', 'fontSize': 18, 'marginTop': '0px', 'whiteSpace': 'pre-wrap'},
    )
])


def register_callbacks(app):

    # mise à jour des promo
    @app.callback(
        Output('choix_promo_prof', 'options'),
        Input('user_id','data')
    )
    def update_options_promo_prof(prof_id):
        promo = app4_notes_tools.get_data_prof(prof_id)['promo'].drop_duplicates()

        options_controles = [] #[{'label': 'Toutes les promos', 'value': 'all'}]
        options_controles.extend([{'label': p, 'value': p} for p in promo])
        return options_controles

    # Callback pour choisir la matiere
    @app.callback(
        Output('choix_matiere_prof', 'value'),
        Output('choix_matiere_prof', 'options'),
        Input('choix_promo_prof', 'value'),
        State('user_id', 'data'),
        prevent_initial_call=True
    )

    def update_matiere(promo_selectionnee, prof_id):

        prof_data = app4_notes_tools.get_data_prof(prof_id)
        modules = prof_data[prof_data['promo'] == promo_selectionnee]['nom'].drop_duplicates()

        options_controles = []  # [{'label': 'Toutes les promos', 'value': 'all'}]
        options_controles.extend([{'label': m, 'value': m} for m in modules])

        if len(options_controles) > 0:
            matiere_selectionnee = options_controles[0]['label']
        else:
            matiere_selectionnee = 'none'

        return matiere_selectionnee, options_controles


    # Callback choix de controle en fonction de la matière sélectionnée
    @app.callback(
        Output('choix_controle_prof', 'options'),
        Output('choix_controle_prof', 'value'),
        Input('choix_matiere_prof', 'value'),
        Input('choix_promo_prof', 'value'),
        State('user_id', 'data'),
        prevent_initial_call=True
    )
    def update_controles(matiere_selectionnee, promo_selectionnee, prof_id):

        prof_data = app4_notes_tools.get_data_prof(prof_id)

        dates = prof_data[prof_data['promo'] == promo_selectionnee][prof_data['nom'] == matiere_selectionnee]['date'].drop_duplicates()

        options_controles = [{'label': 'Moyenne', 'value': 'moyenne'}]
        options_controles.extend({'label': "Eval. du " + str(date), 'value': str(date)} for date in dates)

        return options_controles, "moyenne"

    # Callback en fonction du controle sélectionné
    @app.callback(
        Output('affichage_note_prof', 'figure'),
        Output('affichage_classement_prof', 'children'),
        Input('choix_promo_prof', 'value'),
        Input('choix_matiere_prof', 'value'),
        Input('choix_controle_prof', 'value'),
        State('user_id', 'data'),
        prevent_initial_call=True
    )

    def update_graphique(promo_selectionnee, matiere_selectionnee, controle_selectionne, prof_id):

        prof_data = app4_notes_tools.get_data_prof(prof_id)

        # le calcul des notes de la promo est différent si on veut la moyenne de tous les contrôles ou seulement un cc
        if controle_selectionne=='moyenne':
            prof_data = prof_data[prof_data['promo'] == promo_selectionnee][prof_data['nom'] == matiere_selectionnee]
            notes_promo = prof_data.groupby(['etudiant'])['evaluation'].mean()
            #print("moyenne", type(notes_promo), "\n", notes_promo, flush=True)
        else :
            # on récupère les données correspondant à la matière et au contrôle
            prof_data = prof_data[prof_data['promo'] == promo_selectionnee][prof_data['nom'] == matiere_selectionnee][prof_data['date'] == controle_selectionne]

            # on récupère les notes des contrôles
            prof_data.set_index('etudiant', inplace=True)
            notes_promo = prof_data['evaluation']
            #print("ctrl", type(notes_promo), "\n", notes_promo, flush=True)

        if notes_promo.empty:
            return go.Figure().update_layout(title="Aucune note disponible"), "Aucune note disponible"

        _, moyenne, mediane, ecart_type, X_notes, Y_notes, _ =app4_notes_tools.calcul_informations(notes_promo)

        fig=go.Figure()

        # ajout de la moyenne
        fig.add_vline(
            x=moyenne,
            line=dict(color='#FF0500', dash='dash'),
            annotation_text=f"Moyenne : {moyenne:.2f}",
            annotation_position="top right"
        )

        # ajout de la médiane
        fig.add_vline(
            x=mediane,
            line=dict(color='#FF8400', dash='dash'),
            annotation_text=f"Médiane : {mediane:.2f}",
            annotation_position="top right",
            annotation_y=0.95 # décaller l'affichage pour que la médiane soit en dessous de la moyenne
        )

        # barres des notes des étudiants
        fig.add_trace(go.Bar(
            x=X_notes,
            y=Y_notes,
            marker_color='#007bff',
            text=[str(y) if y>0 else '' for y in Y_notes],
            textposition='inside',
            name="Nombre d'étudiants"
        ))
        
        max_y=max(Y_notes)+1 #on ajoute un espace
        fig.update_layout(
            title=f"Distribution des notes de la promo :",
            title_font=dict(size=15),
            xaxis=dict(title='Notes', tickmode='linear', tick0=0, dtick=1),
            yaxis=dict(title="Nombre d'étudiants", range=[0, max_y]),
            showlegend=False,
            plot_bgcolor="rgba(240,240,240,1)"
        )

        # affichage du classement :
        classement_text=f"Moyenne : {moyenne:.2f}/20 , Médiane : {mediane:.2f}/20 , Ecart-type : {ecart_type:.2f}, \nPodium :",# {' - '.join(map(str, podium))}",

        return fig, classement_text
        

# if __name__=='__main__':
#     app.run_server(debug=True)
