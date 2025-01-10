import statistics
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json
import math

# données à récupérer dans la bdd (fichier json)
with open('visualisation/data/INFO_notes.json', 'r') as fichier:
    data=json.load(fichier)

# pour avoir les notes par promotion, 
# il faudra récupérer les numéros étudiants 
# de tous ceux qui correspondent à la promotion voulue

promo_disponibles=[
    {'nom': 'IDU4-A1', 'etudiants': [356, 734, 912, 783, 528, 699]},  # exemple pour la promo 1
    {'nom': 'IDU4-A2', 'etudiants': [223, 441, 849, 867, 611]},  # exemple pour la promo 2
    {'nom': 'IDU3', 'etudiants': [146, 624, 111, 863, 328]}  # exemple pour la promo 3
]

# variables globales pour garder en mémoire les choix de l'utilisateur
dernier_controle_selectionne=None
derniere_matiere_selectionnee=None

def get_classement_podium(notes, liste_promo):
    """
    Fonction qui permet d'avoir le classement et le podium
    input : notes (liste de dictionnaires), liste_promo (liste de numéros étudiants)
    output : classement (liste de dictionnaires), podium (liste de dictionnaires)
    """
    # on récupère les notes des étudiants de la promo selectionnée
    notes_promo=[etudiant for etudiant in notes if etudiant['num_etu'] in liste_promo]
    # on trie les notes par ordre décroissant
    classement=sorted(notes_promo, key=lambda x: x['note'], reverse=True)
    top=classement[:3]
    podium=[]
    for eleve in top :
        podium.append(eleve['num_etu']) # on pourrait plus tard lier le numéro étudiant au nom/prénom de l'étudiant
    return classement, podium
    
    
def calcul_informations(notes_promo, liste_promo):
    """
    Fonction qui permet d'avoir la moyenne, la médiane et l'écart-type des notes
    input : notes_promo (liste de dictionnaires), liste_promo (liste de numéros étudiants)
    output : moyenne (float), mediane (float), ecart_type (float)
    """
    # on récupère les notes des étudiants de la promo selectionnée
    etudiants_promo=[etudiant['note'] for etudiant in notes_promo if etudiant['num_etu'] in liste_promo]
    if not etudiants_promo:
        print("Il n'y a pas d'étudiants dans la promotion selectionnée")

    # on trie les notes par ordre croissant
    notes_promo=sorted(etudiants_promo)
    # moyenne :
    moyenne=sum(etudiants_promo)/len(etudiants_promo)
    # médiane :
    n=len(etudiants_promo)
    if n%2==1 : # si on a un nombre impair :
        mediane=etudiants_promo[n//2]
    else : # si on a un nombre pair
        mediane=(etudiants_promo[n//2 -1]+etudiants_promo[n//2])/2 #on fait la moyenne entre celle d'avant et celle d'après
    # écart-type :
    ecart_type=statistics.stdev(etudiants_promo) if len(etudiants_promo) > 1 else 0.0  # Ecart-type est 0 si 1 seul étudiant

    X_notes=list(range(21)) #liste qui va de 0 à 20 
    Y_notes=[0]*len(X_notes) # initialisation de la liste
    for note in etudiants_promo :
        note_arrondie=math.floor(note)
        Y_notes[note_arrondie]+=1
    return moyenne, mediane, ecart_type, X_notes, Y_notes

def calcul_moyenne(matiere_selectionnee):
    notes_promo=[]
    # on récupère les données de la matière
    data_matiere=next(m for m in data if m['matiere']==matiere_selectionnee)
    notes_promo=[]
    # pour chaque élève, on calcule sa note moyenne en fonction des coefs
    for etudiant in range(len(data_matiere['controles'][0]['notes'])):
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

# lancement de Dash
app=dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f"Visualisation des notes - prof ", style={'textAlign': 'center', 'marginBottom': '5px'}),

    html.Div(
        children=[
            # choix de la promo
            dcc.Dropdown(
                id='choix_promo',
                options=[
                        {'label': 'Toutes les promos', 'value': 'all'}]
                    +[{'label': promo['nom'], 'value': ', '.join(map(str, promo['etudiants']))} for promo in promo_disponibles],
                # value=', '.join(map(str, promo_disponibles[0]['etudiants'])),
                value='all',
                style={'width': '48%'}
            ),

            # choix de la matière
            dcc.Dropdown(
                id='choix_matiere',
                options=[{'label': matiere['matiere'], 'value': matiere['matiere']} for matiere in data],
                value=data[0]['matiere'],
                style={'width': '48%'}
            ),

            # choix du contrôle
            dcc.Dropdown(
                id='choix_controle',
                style={'width': '48%', 'margin': 'auto'}
            ),
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '3px'}
    ),

    # affichage des notes
    dcc.Graph(
        id='bar-chart',
        config={'displayModeBar': False},
        style={'margin': '10px auto', 'marginTop': '5px', 'marginBottom': '0px'}
    ),

    # affichage du classement
    html.Div(
        id='affichage_classement',
        style={'textAlign': 'center', 'fontSize': 18, 'marginTop': '0px', 'whiteSpace': 'pre-wrap'}, 
    )
])

# Callback pour choisir la matiere
@app.callback(
    [Output('choix_matiere', 'value'), Output('choix_matiere', 'options')],
    [Input('choix_promo', 'value')]
)

def update_matiere(promo_selectionnee):
    global derniere_matiere_selectionnee

    if promo_selectionnee=='all':  # si on veut toutes les promos
        promo_selectionnee=[etu for promo in promo_disponibles for etu in promo['etudiants']]
    else:
        promo_selectionnee=list(map(int, promo_selectionnee.split(', ')))


    # on récupère les matières disponibles pour la promo sélectionnée
    matieres_promo=[]

    for matiere in data :
        # on vérifie si la promo a des notes pour cette matière
        for controle in matiere['controles']:
            for note in controle['notes']:
                if note['num_etu'] in promo_selectionnee:
                    matieres_promo.append(matiere)
                    break
            else:
                continue
            break
    options_matiere=[
        {'label': matiere['matiere'], 'value': matiere['matiere']}
        for matiere in matieres_promo]
    matiere_selectionnee=(
        derniere_matiere_selectionnee
        if derniere_matiere_selectionnee in [opt['value'] for opt in options_matiere] 
        else options_matiere[0]['value']
        )

    derniere_matiere_selectionnee=matiere_selectionnee

    return matiere_selectionnee, options_matiere


# Callback choix de controle en fonction de la matière sélectionnée
@app.callback(
    [Output('choix_controle', 'options'), Output('choix_controle', 'value')],
    [Input('choix_matiere', 'value'), Input('choix_promo', 'value')],
    prevent_initial_call=True
)
def update_controles(matiere_selectionnee, promo_selectionnee):
    global dernier_controle_selectionne

    if promo_selectionnee=='all':  # on veut toutes les promos
        promo_selectionnee=[etu for promo in promo_disponibles for etu in promo['etudiants']]
    else:
        promo_selectionnee=list(map(int, promo_selectionnee.split(', ')))

    #on récupère les données de la matière sélectionnée
    data_matiere=next(matiere for matiere in data if matiere['matiere']==matiere_selectionnee)

    # contrôles disponibles pour cette matière :
    if len(data_matiere['controles'])>1: # s'il y a qu'un seul controle, pas besoin de faire la moyenne
        options_controles=[{'label': 'moyenne', 'value': 'moyenne'}]
        options_controles.extend({'label' : controle['type'], 'value':controle['type']} for controle in data_matiere['controles'])
    else : # s'il y a qu'un seul contrôle :
        options_controles=[{'label' : controle['type'], 'value':controle['type']} for controle in data_matiere['controles']]

    if dernier_controle_selectionne in [controle['value'] for controle in options_controles]:
        controle_par_defaut=dernier_controle_selectionne
    else:
        controle_par_defaut=options_controles[0]['value']

    dernier_controle_selectionne=controle_par_defaut

    return options_controles, controle_par_defaut

# Callback en fonction du controle sélectionné
@app.callback(
    [Output('bar-chart', 'figure'), Output('affichage_classement', 'children')],
    [Input('choix_promo', 'value'), Input('choix_matiere', 'value'), Input('choix_controle', 'value')]
)

def update_graphique(liste_promo, matiere_selectionnee, controle_selectionne):
    # print("liste_promo", liste_promo)
    # print("matiere_selectionnee", matiere_selectionnee)
    # print("controle_selectionne", controle_selectionne)

    global dernier_controle_selectionne, derniere_matiere_selectionnee
    derniere_matiere_selectionnee=matiere_selectionnee
    dernier_controle_selectionne=controle_selectionne

    if liste_promo == 'all': # si on veut toutes les promos
        liste_promo = [etu for promo in promo_disponibles for etu in promo['etudiants']]
    else:
        liste_promo = list(map(int, liste_promo.split(', ')))
    
    # le calcul des notes de la promo est différent si on veut la moyenne de tous les contrôles ou seulement un cc
    if controle_selectionne=='moyenne' or controle_selectionne==None:
        notes_promo=calcul_moyenne(matiere_selectionnee)

    else :
        # on récupère les données correspondant à la matière et au contrôle
        data_matiere=next(m for m in data if m['matiere']==matiere_selectionnee)
        data_controle=next(c for c in data_matiere['controles'] if c['type']==controle_selectionne)

        # on récupère les notes des contrôles
        notes_promo=data_controle['notes']

    moyenne, mediane, ecart_type, X_notes, Y_notes=calcul_informations(notes_promo, liste_promo)
    _, podium=get_classement_podium(notes_promo, liste_promo)

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
        marker_color='#2e6f9f',
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
    classement_text=f"Moyenne : {moyenne:.2f}/20 , Médiane : {mediane:.2f}/20 , Ecart-type : {ecart_type:.2f}, \nPodium : {' - '.join(map(str, podium))}",

    return fig, classement_text
    

if __name__=='__main__':
    app.run_server(debug=True)
