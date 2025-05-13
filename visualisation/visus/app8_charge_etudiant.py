import mysql
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from datetime import datetime

'''
# Nom du fichier
file = '../data/charge_eleves.csv'

# Charger le fichier CSV
df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=',')'''

# Palette originale
original_palette = px.colors.qualitative.Alphabet

# Retirer une couleur (ex : '#FFB5E8')
custom_palette = [c for c in original_palette if c.lower() != '#85660d']

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

def get_data(id_etudiant) : 
    cur.execute(f"SELECT etu.nom, sessens.schedule as date_prevue, promo.annee, sequencage.duree_h, module.nom FROM CLASS_session_to_be_affected as sess JOIN CLASS_session_to_be_affected_as_enseignant as sessens ON sessens.id_seance_to_be_affected=sess.id_seance_to_be_affected JOIN LNM_groupe as grp ON sess.id_groupe = grp.id_groupe JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo JOIN MAQUETTE_module_sequence as sequence ON sess.id_module_sequence=sequence.id_module_sequence JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module WHERE etu.id_etudiant = {id_etudiant};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["nom", "date", "annee", "nb_heure", "matiere"])
    return data

id_etudiant = 259
df = get_data(id_etudiant)

# Convertir la colonne "date" en format datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Gérer les erreurs éventuelles de conversion
# Ajouter une colonne "semaine" pour le numéro de la semaine
df['semaine'] = df['date'].dt.isocalendar().week  # Numéro de la semaine ISO
df['annee'] = df['date'].dt.year  # Ajouter l'année pour gérer les années distinctes

# Créer une liste unique des semaines disponibles
semaine_options = [{'label': f"Semaine {semaine} - {annee}", 'value': f"{annee}-{semaine}"}
                   for annee, semaine in df[['annee', 'semaine']].drop_duplicates().sort_values(['annee', 'semaine']).values]

# Créer l'application Dash
# app = Dash(__name__)

# Layout de l'application
app8_layout = html.Div([
    html.H1("Visualisation de la charge de travail d'un élève semaine par semaine"),

    # Dropdown pour sélectionner un élève
    dcc.Dropdown(
        id='filtre-eleve',
        options=[{'label': nom, 'value': nom} for nom in df['nom'].unique()],
        value=df['nom'].unique()[0],  # Sélectionner le premier élève par défaut
        placeholder="Sélectionnez un élève",
    ),

    # Dropdown pour sélectionner une semaine
    dcc.Dropdown(
        id='filtre-semaine',
        options=semaine_options,
        value=semaine_options[0]['value'],  # Par défaut, la première semaine disponible
        placeholder="Sélectionnez une semaine",
    ),

    # Graphique
    dcc.Graph(id='graphique-charge_etudiant')
])

def register_callbacks(app):
    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graphique-charge_etudiant', 'figure'),
        [Input('filtre-eleve', 'value'),
        Input('filtre-semaine', 'value')]
    )
    def update_graph(filtre_eleve, filtre_semaine):
        # Décomposer la valeur de la semaine en année et numéro de semaine
        annee, semaine = map(int, filtre_semaine.split('-'))

        # Filtrer les données pour l'élève sélectionné et la semaine
        df_filtered = df[(df['nom'] == filtre_eleve) & (df['semaine'] == semaine) & (df['annee'] == annee)]

        # Vérifier si des données sont disponibles pour cette semaine
        if df_filtered.empty:
            # Si aucune donnée n'est disponible, retourner un graphique vide
            fig = px.bar(
                title=f"Aucune donnée disponible pour l'élève {filtre_eleve} (Semaine {semaine}, {annee})",
                labels={'date': 'Date', 'nb_heure': 'Nombre d\'heures', 'matiere': 'Matière'}
            )
            return fig
        # Regrouper les données par date et matière, et additionner les heures
        df_grouped = df_filtered.groupby(['date', 'matiere'], as_index=False).agg({'nb_heure': 'sum'})


        # Créer le graphique
        fig = px.bar(
            df_filtered,
            x='date',  # Axe X : jours de la semaine
            y='nb_heure',  # Axe Y : nombre d'heures
            color='matiere',  # Couleur par matière
            title=f"Charge de travail de l'élève {filtre_eleve} - Semaine {semaine}, {annee}",
            labels={'date': 'Date', 'nb_heure': 'Nombre d\'heures', 'matiere': 'Matière'},
            text='matiere',  # Afficher le type de cours sur les barres
            color_discrete_sequence=custom_palette  # ou 'Bold', 'Dark2', etc. 
        )

        fig.update_traces(
            textposition='outside'  # Positionner les étiquettes à l'extérieur
        )

        fig.update_xaxes(
            title_text="Jour"
        )
        fig.update_yaxes(title_text="Nombre d'heures")

        return fig

# Lancer l'application
# if __name__ == '__main__':
#     app.run_server(debug=True)
