import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from datetime import datetime
import app7_charge_tools

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
def update_df(df):
    # Ajouter les colonnes "jour_semaine" et "mois" dans le DataFrame initial
    df['schedule'] = pd.to_datetime(df['schedule'])
    df['jour_semaine'] = df['schedule'].dt.day_name()  # Ex : Monday, Tuesday
    df['mois'] = df['schedule'].dt.month_name()       # Ex : January, February
    df['jour'] = df['schedule'].dt.date               # Ex : 2025-01-07, utilisé pour filtrer aujourd'hui

    # Regroupement par "nom" et "type" et somme des heures
    df_calcule = df.groupby(['nom'], as_index=False).agg({
        'duree_h': 'sum',
        'nom': 'first',
        'schedule': 'first',
        'jour_semaine': 'first',  # Conserver le jour de la semaine
        'mois': 'first',           # Conserver le mois
        'jour': 'first'            # Conserver le jour complet pour "Aujourd'hui"
    })

    return df_calcule



# Layout de l'application
app7_enseignant_layout = html.Div([
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
        Input('filtre-periode', 'value'),
        Input('user_id', 'data')
    )
    def update_graph(filtre_periode, user_id):
        df = app7_charge_tools.get_chargeByEnseignantId(user_id)
        df_calcule = update_df(df)

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
            y='duree_h',  # Axe Y : nombre d'heures
            color='nom',  # Couleur par matière
            title=f"Charge de travail des enseignants ({filtre_periode})",
            labels={ 'duree_h': 'Nombre d\'heures', 'nom': 'Matière'},
            text='nom',  # Afficher la matière des cours sur les barres
            color_discrete_sequence=app7_charge_tools.custom_palette  # ou 'Bold', 'Dark2', etc.
        )

        fig.update_traces(textposition='outside')  # Placer les labels à l'extérieur des barres
        return fig
