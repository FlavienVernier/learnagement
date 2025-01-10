import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from datetime import datetime

# Nom du fichier
file = 'visualisation/data/charge_eleves.csv'

# Charger le fichier CSV
df = pd.read_csv(file, encoding='ISO-8859-1', delimiter=',')

# Convertir la colonne "date" en format datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Gérer les erreurs éventuelles de conversion

# Ajouter une colonne "semaine" pour le numéro de la semaine
df['semaine'] = df['date'].dt.isocalendar().week  # Numéro de la semaine ISO
df['annee'] = df['date'].dt.year  # Ajouter l'année pour gérer les années distinctes

# Créer une liste unique des semaines disponibles
semaine_options = [{'label': f"Semaine {semaine} - {annee}", 'value': f"{annee}-{semaine}"}
                   for annee, semaine in df[['annee', 'semaine']].drop_duplicates().sort_values(['annee', 'semaine']).values]

# Créer l'application Dash
app = Dash(__name__)

# Layout de l'application
app.layout = html.Div([
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
    dcc.Graph(id='graphique-charge')
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output('graphique-charge', 'figure'),
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
            labels={'date': 'Date', 'nb_heur': 'Nombre d\'heures', 'matiere': 'Matière'}
        )
        return fig

    # Créer le graphique
    fig = px.bar(
        df_filtered,
        x='date',  # Axe X : jours de la semaine
        y='nb_heur',  # Axe Y : nombre d'heures
        color='matiere',  # Couleur par matière
        title=f"Charge de travail de l'élève {filtre_eleve} - Semaine {semaine}, {annee}",
        labels={'date': 'Date', 'nb_heur': 'Nombre d\'heures', 'matiere': 'Matière'},
        text='type'  # Afficher le type de cours sur les barres
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
if __name__ == '__main__':
    app.run_server(debug=True)
