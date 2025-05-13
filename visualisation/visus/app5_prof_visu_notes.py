import statistics
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql
import pandas as pd
import plotly.graph_objs as go
import json
import math

# Lire les informations de connexion depuis logs_db.txt
with open('logs_db.txt', 'r') as file:
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    host = lines[2].strip()
    port = lines[3].strip()
    database = lines[4].strip()

# Se connecter à la base de données MySQL
conn = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    port=port,
    database=database
)

# Exécuter la requête pour récupérer les dépendances
cur = conn.cursor()

# pour avoir les notes par promotion, 
# il faudra récupérer les numéros étudiants 
# de tous ceux qui correspondent à la promotion voulue
def get_data_as_enseignant(id_enseignant) : 
    cur.execute(f"SELECT evaluation, id_etudiant, module.nom FROM ETU_classical_evaluation as eval JOIN MAQUETTE_module as module ON eval.id_module=module.id_module JOIN LNM_enseignant as enseignant ON module.id_responsable = enseignant.id_enseignant WHERE enseignant.id_enseignant={id_enseignant};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["evaluation", "id_etudiant", "nom_module"])
     # Structurer les données pour inclure des contrôles
    data['controles'] = data.apply(lambda row: [{'type': 'CC', 'evaluation': row['evaluation'], 'id_etudiant': row['id_etudiant']}], axis=1) # Aucunes informations ne sont données sur les types de contrôles que ce sont donc on laisse CC 
    return data

id_enseignant = 16 # Temporaire
data = get_data_as_enseignant(id_enseignant)

def define_promo():
    cur.execute(f"SELECT id_promo, GROUP_CONCAT(id_etudiant) AS etudiants FROM LNM_etudiant GROUP BY id_promo;")
    
    rows = cur.fetchall()

    # Récupération des données 
    # Le résultat est sous forme de liste de tuple  donc : 
    data = []
    for id_promo, etudiants in rows:
        etudiants_list = list(map(int, etudiants.split(','))) if etudiants else []  # Convertir en liste d'entiers
        data.append({'id_promo': id_promo, 'etudiants': etudiants_list})

    data_final = pd.DataFrame(data, columns=["id_promo", "etudiants"])
    return data

promo_disponibles = define_promo()

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
    notes_promo=[etudiant for etudiant in notes if etudiant['id_etudiant'] in liste_promo]
    # on trie les notes par ordre décroissant
    classement=sorted(notes_promo, key=lambda x: x['evaluation'], reverse=True)
    top=classement[:3]
    podium=[]
    for eleve in top :
        podium.append(eleve['id_etudiant']) # on pourrait plus tard lier le numéro étudiant au nom/prénom de l'étudiant
    return classement, podium
    
    
def calcul_informations(notes_promo, liste_promo):
    """
    Fonction qui permet d'avoir la moyenne, la médiane et l'écart-type des notes
    input : notes_promo (liste de dictionnaires), liste_promo (liste de numéros étudiants)
    output : moyenne (float), mediane (float), ecart_type (float)
    """
    # on récupère les notes des étudiants de la promo selectionnée
    etudiants_promo=[etudiant['evaluation'] for etudiant in notes_promo if etudiant['id_etudiant'] in liste_promo]
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
    data_matiere=next(m for m in data if m['nom_module']==matiere_selectionnee)
    notes_promo=[]
    # pour chaque élève, on calcule sa note moyenne en fonction des coefs
    for etudiant in range(len(data_matiere)):
        somme_notes_ponderees=0
        somme_coef=0
        for controle in data_matiere['controles']:
            coef=1
            note_etudiant=controle['evaluation']
            somme_notes_ponderees+=note_etudiant*coef
            somme_coef+=coef    
        note_etu=somme_notes_ponderees/somme_coef
        num_etu=controle['id_etudiant']
        notes_promo.append({'id_etudiant':num_etu, 'evaluation':note_etu})
    return notes_promo

data = get_data_as_enseignant(id_enseignant).to_dict(orient='records')
# # lancement de Dash
# app=dash.Dash(__name__)

app5_layout = html.Div([
    html.H1(f"Visualisation des notes - prof ", style={'textAlign': 'center', 'marginBottom': '5px'}),

    html.Div(
        children=[
            # choix de la promo
            dcc.Dropdown(
                id='choix_promo_prof',
                options=[
                        {'label': 'Toutes les promos', 'value': 'all'}]
                    +[{'label': promo['id_promo'], 'value': promo['etudiants']} for promo in promo_disponibles],
                # value=', '.join(map(str, promo_disponibles[0]['etudiants'])),
                value='all',
                style={'width': '48%'}
            ),

            # choix de la matière
            dcc.Dropdown(
                id='choix_matiere_prof',
                options=[{'label': matiere['nom_module'], 'value': matiere['nom_module']} for matiere in data],
                value=data[0]['nom_module'],
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
    # Callback pour choisir la matiere
    @app.callback(
        [Output('choix_matiere_prof', 'value'), Output('choix_matiere_prof', 'options')],
        [Input('choix_promo_prof', 'value')]
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
                #for note in controle['evaluation']:
                    if controle['id_etudiant'] in promo_selectionnee:
                        matieres_promo.append(matiere)
                        break
                    else:
                        continue
                #break
        options_matiere=[
            {'label': matiere['nom_module'], 'value': matiere['nom_module']}
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
        [Output('choix_controle_prof', 'options'), Output('choix_controle_prof', 'value')],
        [Input('choix_matiere_prof', 'value'), Input('choix_promo_prof', 'value')],
        prevent_initial_call=True
    )
    def update_controles(matiere_selectionnee, promo_selectionnee):
        global dernier_controle_selectionne

        if promo_selectionnee=='all':  # on veut toutes les promos
            promo_selectionnee=[etu for promo in promo_disponibles for etu in promo['etudiants']]
        else:
            promo_selectionnee=list(map(int, promo_selectionnee.split(', ')))

        #on récupère les données de la matière sélectionnée
        data_matiere=next(matiere for matiere in data if matiere['nom_module']==matiere_selectionnee)

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
        [Output('affichage_note_prof', 'figure'), Output('affichage_classement_prof', 'children')],
        [Input('choix_promo_prof', 'value'), Input('choix_matiere_prof', 'value'), Input('choix_controle_prof', 'value')]
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
            data_matiere=next(m for m in data if m['nom_module']==matiere_selectionnee)
            data_controle=next(c for c in data_matiere['controles'] if c['type']==controle_selectionne)

            # on récupère les notes des contrôles
            notes_promo = [{'id_etudiant': data_controle['id_etudiant'], 'evaluation': data_controle['evaluation']}]

        moyenne, mediane, ecart_type, X_notes, Y_notes=calcul_informations(notes_promo, liste_promo)
        _, podium=get_classement_podium(notes_promo, liste_promo)

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
        classement_text=f"Moyenne : {moyenne:.2f}/20 , Médiane : {mediane:.2f}/20 , Ecart-type : {ecart_type:.2f}, \nPodium : {' - '.join(map(str, podium))}",

        return fig, classement_text
        

# if __name__=='__main__':
#     app.run_server(debug=True)
