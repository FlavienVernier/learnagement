import mysql
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from datetime import datetime
'''
# Nom du fichier
file = '../data/charge_ensegnants.csv'

# Charger le fichier CSV
df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=',')'''

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

def get_data(id_enseignant) : 
    cur.execute(f"SELECT ens.nom, ens.prenom, sessens.schedule, sequencage.duree_h, module.nom FROM CLASS_session_to_be_affected as sess JOIN CLASS_session_to_be_affected_as_enseignant as sessens ON sessens.id_seance_to_be_affected=sess.id_seance_to_be_affected JOIN LNM_enseignant as ens ON ens.id_enseignant=sessens.id_enseignant JOIN MAQUETTE_module_sequence as sequence ON sess.id_module_sequence=sequence.id_module_sequence JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module WHERE ens.id_enseignant={id_enseignant};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["nom", "prenom", "date", "nb_heure", "matiere"])
    return data

id_enseignant = 16
df = get_data(id_enseignant)

# Fonction pour calculer le numéro de la semaine
def calculer_semaine(date_cours, format_date='%Y-%m-%d'):
    try:
        # Convertir la date en objet datetime
        date_obj = datetime.strptime(date_cours, format_date)
        # Obtenir le numéro de la semaine
        numero_semaine = date_obj.isocalendar()[1]
        return numero_semaine
    except ValueError:
        return "Erreur : Format de date invalide. Veuillez vérifier la date et le format."

# Ajouter les colonnes "jour_semaine" et "mois" dans le DataFrame initial
df['date'] = pd.to_datetime(df['date'])
df['jour_semaine'] = df['date'].dt.day_name()  # Ex : Monday, Tuesday
df['mois'] = df['date'].dt.month_name()       # Ex : January, February
df['jour'] = df['date'].dt.date               # Ex : 2025-01-07, utilisé pour filtrer aujourd'hui

# Regroupement par "nom" et "type" et somme des heures
df_calcule = df.groupby(['nom', 'matiere'], as_index=False).agg({
    'nb_heure': 'sum',
    'matiere': 'first',
    'date': 'first',
    'jour_semaine': 'first',  # Conserver le jour de la semaine
    'mois': 'first',           # Conserver le mois
    'jour': 'first'            # Conserver le jour complet pour "Aujourd'hui"
})

# Créer l'application Dash
# app = Dash(__name__)

# Layout de l'application
app7_layout = html.Div([
    html.H1("Visualisation de la charge de travail des enseignants"),
    
    # Dropdown pour sélectionner le filtre de période
    dcc.Dropdown(
        id='filtre-periode',
        options=[
            {'label': 'Tous les jours', 'value': 'all'},
            {'label': 'Aujourd\'hui', 'value': 'today'},
            {'label': 'Ce mois', 'value': 'this_month'}
        ],
        value='all',  # Valeur par défaut
        placeholder="Sélectionnez une période",
    ),
    
    # Graphique
    dcc.Graph(id='graphique-charge_enseignant')
])

def register_callbacks(app):
    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graphique-charge_enseignant', 'figure'),
        [Input('filtre-periode', 'value')]
    )
    def update_graph(filtre_periode):
        today = datetime.today().date()  # Date d'aujourd'hui
        current_month = datetime.today().strftime('%B')  # Mois courant, par exemple "January"

        # Filtrer les données selon la sélection
        if filtre_periode == 'all':
            df_filtered = df_calcule
        elif filtre_periode == 'today':
            df_filtered = df_calcule[df_calcule['jour'] == today]  # Filtre pour le jour d'aujourd'hui
        elif filtre_periode == 'this_month':
            df_filtered = df_calcule[df_calcule['mois'] == current_month]  # Filtre pour le mois en cours
        else:
            df_filtered = df_calcule  # Par défaut, toutes les données

        # Créer le graphique
        fig = px.bar(
            df_filtered,
            x='nom',  # Axe X : noms des enseignants
            y='nb_heure',  # Axe Y : nombre d'heures
            color='matiere',  # Couleur par matière
            title=f"Charge de travail des enseignants ({filtre_periode})",
            labels={'nom': 'Enseignant', 'nb_heure': 'Nombre d\'heures', 'matiere': 'Matière'},
            text='matiere'  # Afficher la matière des cours sur les barres
        )

        fig.update_traces(textposition='outside')  # Placer les labels à l'extérieur des barres
        return fig

# Lancer l'application
# if __name__ == '__main__':
#     app.run_server(debug=True)

