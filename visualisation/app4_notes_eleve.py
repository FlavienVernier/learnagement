from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import app4_notes_tools

app4_etudiant_layout=html.Div([
    html.H1(f"Visualisation des notes", style={'textAlign': 'center', 'marginBottom': '5px'}),

    html.Div(  
    children=[
        # choix de la matière
        dcc.Dropdown(
            id='choix_matiere_eleve',
            options = [],
            style={'width': '48%'}
        ),

        # choix du contrôle
        dcc.Dropdown(
            id='choix_controle_eleve',
            style={'width': '48%', 'margin':'auto'},
            options=[{'label': 'Moyenne', 'value': 'moyenne'}],
            value='moyenne'
        ),],

        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap':'10px', 'marginBottom': '3px'}
    ),


    # affichage des notes
    dcc.Graph(
        id='affichage_note_eleve',
        config={'displayModeBar': False},
        style={'margin': '10px auto', 'marginTop':'5px', 'marginBottom':'3px'}
    ),

    # affichage du classement
    html.Div(
        id='affichage_classement_eleve',
        style={'textAlign': 'center', 'fontSize': 18, 'marginTop': 5}
    )
])

def register_callbacks(app):

    @app.callback(
        Output('choix_matiere_eleve', 'options'),
        Input('user_id', 'data')
    )
    def update_choix_matiere_eleve(id_etudiant):
        modules = app4_notes_tools.get_modules_byIdEtudiant(id_etudiant)
        return [{'label': row['code_module']+" "+row['nom'], 'value': row['id_module']} for i, row in modules.iterrows()]

    # Callback en fonction de la matière sélectionnée
    @app.callback(
        Output('choix_controle_eleve', 'options'),
        #Output('choix_controle_eleve', 'value'),
        Input('choix_matiere_eleve', 'value'),
        Input('user_id', 'data')
    )
    def update_controles(matiere_selectionnee, user_id):

        #on récupère les données de la matière sélectionnée
        data_matiere = app4_notes_tools.get_notes_eleves(user_id)
        data_matiere = data_matiere[data_matiere['id_module'] == matiere_selectionnee]


        # contrôles disponibles pour cette matière :
        if (len(data_matiere)>1): # s'il y a qu'un seul controle, pas besoin de faire la moyenne
            options_controles=[{'label': 'Moyenne', 'value': 'moyenne'}]
            options_controles.extend({'label':  "Eval. du " + str(row['date']), 'value': str(row['date'])} for _, row in data_matiere.iterrows())
        else : # s'il y a qu'un seul contrôle :
            options_controles = [{'label': "Eval. du " + str(row['date']), 'value': str(row['date'])} for _, row in data_matiere.iterrows()]

        options_controles = [{'label': 'Moyenne', 'value': 'moyenne'}]
        options_controles.extend({'label': "Eval. du " + str(row['date']), 'value': str(row['date'])} for _, row in data_matiere.iterrows())

        #controle_par_defaut=options_controles[0]['value'] # on prend la moyenne ou le seul CC (en fonction de la matière sélectionnée)

        return options_controles#, controle_par_defaut

    # Callback en fonction du controle sélectionné
    @app.callback(
        Output('affichage_note_eleve', 'figure'),
        Output('affichage_classement_eleve', 'children'),
        Input('choix_matiere_eleve', 'value'),
        Input('choix_controle_eleve', 'value'),
        Input('user_id', 'data')
    )

    def update_graphique(matiere_selectionnee, controle_selectionne, user_id):
        # print(matiere_selectionnee, controle_selectionne)
        # le calcul des notes de la promo est différent si on veut la moyenne de tous les contrôles ou seulement un cc
        #data_matiere = app4_notes_tools.get_data_promo(matiere_selectionnee)  # mettre matiere_selectionnee au format id

        data_matiere = app4_notes_tools.get_notes_eleves(user_id)
        notes_eleve = data_matiere[data_matiere['id_module'] == matiere_selectionnee]

        # Vérifiez si la note existe
        if notes_eleve.empty:
            return go.Figure().update_layout(title="Aucune note disponible"), "Aucune note disponible"

        if controle_selectionne=='moyenne' :
            notes_promo = app4_notes_tools.get_average_notes_promo(matiere_selectionnee)["evaluation"]
            note_eleve = notes_eleve.loc[:, 'evaluation'].mean()

        else :
            # on récupère les données correspondant à la matière et au contrôle
            data_matiere = app4_notes_tools.get_data_promo(matiere_selectionnee)
            notes_promo = data_matiere[data_matiere['date'] == controle_selectionne]["evaluation"]
            note_eleve = notes_eleve[notes_eleve['date'] == controle_selectionne]
            note_eleve = note_eleve.iloc[0]['evaluation']

        # Calcul des informations
        classement, moyenne, mediane, ecart_type, X_notes, Y_notes, couleur = app4_notes_tools.calcul_informations(notes_promo, note_eleve)

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
            marker_color=couleur,
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
        classement_text=f"Note : {note_eleve:.2f}/20 - Classement : {classement}e/{len(notes_promo)} ",

        return fig, classement_text

