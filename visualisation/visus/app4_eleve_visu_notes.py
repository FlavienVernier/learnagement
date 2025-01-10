import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import math

# données à récupérer dans la bdd (fichier json)
with open('visualisation/data/INFO_notes.json', 'r') as fichier:
    data=json.load(fichier)

num_etu=528

def get_note_eleve(notes_promo, num_etu):
    for note in notes_promo:
        if note['num_etu']==num_etu:
            return note['note']
    return None  # dans le cas où l'étudiant n'est pas dans la promo

def calcul_informations(notes_promo, note_eleve):
    # print("notes promo", notes_promo)
    # print("note eleve", note_eleve)
    # calcul des informations
    # on récupère seulement les notes :
    notes_promo=[eleve['note'] for eleve in notes_promo]
    # on trie les notes par ordre croissant
    notes_promo=sorted(notes_promo)  
    # print("notes promo", notes_promo)
    moyenne=sum(notes_promo)/len(notes_promo)
    ordre_notes=sorted(notes_promo, reverse=True)
    classement=ordre_notes.index(note_eleve)+1
    
    # médiane :
    n=len(notes_promo)
    if n%2==1 : # si on a un nombre impair :
        mediane=notes_promo[n//2]
    else : # si on a un nombre pair
        mediane=(notes_promo[n//2 -1]+notes_promo[n//2])/2 #on fait la moyenne entre celle d'avant et celle d'après

    X_notes=list(range(21)) #liste qui va de 0 à 20 
    Y_notes=[0]*len(X_notes) # initialisation de la liste
    for note in notes_promo :
        # print("note", note)
        note_arrondie=math.floor(note)
        # print("note arrondie", note_arrondie)
        # print("Y_notes", Y_notes)
        Y_notes[note_arrondie]+=1

    couleur=['#bddcf3' if math.floor(i)!=math.floor(note_eleve) else '#b14bd5' if i<10 else '#13a999' for i in X_notes]

    return classement, moyenne, mediane, X_notes, Y_notes, couleur

def calcul_moyenne(matiere_selectionnee):
    notes_promo=[]
    # on récupère les données de la matière
    data_matiere=next(m for m in data if m['matiere']==matiere_selectionnee)
    notes_promo=[]
    # pour chaque élève, on calcule sa note moyenne en fonction des coefs
    for etudiant in range(len(data_matiere['controles'][0]['notes'])):
        # print("etudiant", etudiant)
        somme_notes_ponderees=0
        somme_coef=0
        for controle in data_matiere['controles']:
            coef=controle['coef']
            note_etudiant=controle['notes'][etudiant]['note']
            somme_notes_ponderees+=note_etudiant*coef
            somme_coef+=coef    
        note_etu=somme_notes_ponderees/somme_coef
        num_etu=controle['notes'][etudiant]['num_etu']
        notes_promo.append({'num_etu':num_etu, 'note':note_etu})
    return notes_promo

def matieres_pour_etudiant(data, num_etu):
    """Permet de récupérer les matières pour lesquelles un étudiant a des notes"""
    matieres_disponibles=[]
    for matiere in data:
        for controle in matiere['controles']:
            # on regarde si le num_etudiant est dans les notes des contrôles des matières
            if any(note['num_etu']==num_etu for note in controle['notes']):
                matieres_disponibles.append(matiere)
                break  # si o a trouvé l'étudiant dans une matière, on passe à la suivante
    return matieres_disponibles

"""
# lancement de Dash
app=dash.Dash(__name__)
"""
app4_layout=html.Div([
    html.H1(f"Visualisation des notes", style={'textAlign': 'center', 'marginBottom': '5px'}),

    html.Div(  
    children=[
        # choix de la matière
        dcc.Dropdown(
            id='choix_matiere_eleve',
            options=[{'label' : matiere['matiere'], 'value':matiere['matiere']} for matiere in matieres_pour_etudiant(data, num_etu)],
            value=matieres_pour_etudiant(data, num_etu)[0]['matiere'],
            style={'width': '48%'}
        ),

        # choix du contrôle
        dcc.Dropdown(
            id='choix_controle_eleve',
            style={'width': '48%', 'margin':'auto'}
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
    # Callback en fonction de la matière sélectionnée
    @app.callback(
        [Output('choix_controle_eleve', 'options'), Output('choix_controle_eleve', 'value')],
        [Input('choix_matiere_eleve', 'value')]
    )
    def update_controles(matiere_selectionnee):

        #on récupère les données de la matière sélectionnée
        data_matiere=next(matiere for matiere in data if matiere['matiere']==matiere_selectionnee)

        # contrôles disponibles pour cette matière :
        if (len(data_matiere['controles'])>1): # s'il y a qu'un seul controle, pas besoin de faire la moyenne
            options_controles=[{'label': 'Moyenne', 'value': 'moyenne'}]
            options_controles.extend({'label' : controle['type'], 'value':controle['type']} for controle in data_matiere['controles'])
        else : # s'il y a qu'un seul contrôle :
            options_controles=[{'label' : controle['type'], 'value':controle['type']} for controle in data_matiere['controles']]
            
        controle_par_defaut=options_controles[0]['value'] # on prend la moyenne ou le seul CC (en fonction de la matière sélectionnée)

        return options_controles, controle_par_defaut

    # Callback en fonction du controle sélectionné
    @app.callback(
        [Output('affichage_note_eleve', 'figure'), Output('affichage_classement_eleve', 'children')],
        [Input('choix_matiere_eleve', 'value'), Input('choix_controle_eleve', 'value')]
    )

    def update_graphique(matiere_selectionnee, controle_selectionne):
        # print(matiere_selectionnee, controle_selectionne)
        # le calcul des notes de la promo est différent si on veut la moyenne de tous les contrôles ou seulement un cc
        if controle_selectionne=='moyenne' :
            notes_promo=calcul_moyenne(matiere_selectionnee)
            # print("moyenne", notes_promo)

        else :
            # on récupère les données correspondant à la matière et au contrôle
            data_matiere=next(m for m in data if m['matiere']==matiere_selectionnee)
            data_controle=next(c for c in data_matiere['controles'] if c['type']==controle_selectionne)

            # on récupère les notes des contrôles
            notes_promo = [{'num_etu': note['num_etu'], 'note': note['note']} for note in data_controle['notes']]
            # print("notes controle", notes_promo)

        note_eleve=get_note_eleve(notes_promo, num_etu)

        classement, moyenne, mediane, X_notes, Y_notes, couleur=calcul_informations(notes_promo, note_eleve)

        fig=go.Figure()

        # ajout de la moyenne
        fig.add_vline(
            x=moyenne,
            line=dict(color='#2e6f9f', dash='dash'),
            annotation_text=f"Moyenne : {moyenne:.2f}",
            annotation_position="top right"
        )


        # ajout de la médiane
        fig.add_vline(
            x=mediane,
            line=dict(color='#167fb7', dash='dash'),
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
    
"""
if __name__=='__main__':
    app.run_server(debug=True)
"""