import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from datetime import datetime

# Nom du fichier
file = 'visualisation/data/charge_ensegnants.csv'

# Charger le fichier CSV
df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=',')

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
df_calcule = df.groupby(['nom', 'type'], as_index=False).agg({
    'nb_heur': 'sum',
    'matiere': 'first',
    'date': 'first',
    'jour_semaine': 'first',  # Conserver le jour de la semaine
    'mois': 'first',           # Conserver le mois
    'jour': 'first'            # Conserver le jour complet pour "Aujourd'hui"
})

# Créer l'application Dash
app = Dash(__name__)

# Layout de l'application
app.layout = html.Div([
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
    dcc.Graph(id='graphique-charge')
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output('graphique-charge', 'figure'),
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
        y='nb_heur',  # Axe Y : nombre d'heures
        color='matiere',  # Couleur par matière
        title=f"Charge de travail des enseignants ({filtre_periode})",
        labels={'nom': 'Enseignant', 'nb_heur': 'Nombre d\'heures', 'matiere': 'Matière'},
        text='type'  # Afficher le type de cours sur les barres
    )

    fig.update_traces(textposition='outside')  # Placer les labels à l'extérieur des barres
    return fig

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)

