import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
import app7_charge_tools

def update_df(df):
    # Convertir la colonne "date" en format datetime
    df['schedule'] = pd.to_datetime(df['schedule'], errors='coerce')  # Gérer les erreurs éventuelles de conversion
    # Ajouter une colonne "semaine" pour le numéro de la semaine
    df['semaine'] = df['schedule'].dt.isocalendar().week  # Numéro de la semaine ISO
    df['annee'] = df['schedule'].dt.year  # Ajouter l'année pour gérer les années distinctes


# Layout de l'application
app7_etudiant_layout = html.Div([
    html.H1("Visualisation de la charge de travail d'un élève semaine par semaine"),

    # Dropdown pour sélectionner une semaine
    dcc.Dropdown(
        id='filtre-semaine',
        options=[],
        #value=semaine_options[0]['value'],  # don't select default if no data Par défaut, la première semaine disponible
        placeholder="Sélectionnez une semaine",
    ),

    # Graphique
    dcc.Graph(id='graphique-charge_etudiant')
])

def register_callbacks(app):
    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graphique-charge_etudiant', 'figure'),
        Output('graphique-charge_etudiant', 'options'),
        Input('filtre-semaine', 'value'),
        Input('user_id', 'data')
    )
    def update_graph(filtre_semaine, user_id):
        df = app7_charge_tools.get_chargeByEtudianttId(user_id)

        if df.empty or filtre_semaine is None:
            # Si aucune donnée n'est disponible, retourner un graphique vide
            fig = px.bar(
                title=f"Aucune donnée disponible",
                labels={'schedule': 'Date', 'duree_h': 'Nombre d\'heures', 'nom': 'Matière'}
            )
            return fig, []

        update_df(df)
        # Créer une liste unique des semaines disponibles
        semaine_options = [{'label': f"Semaine {semaine} - {annee}", 'value': f"{annee}-{semaine}"}
                           for annee, semaine in
                           df[['annee', 'semaine']].drop_duplicates().sort_values(['annee', 'semaine']).values]

        # Décomposer la valeur de la semaine en année et numéro de semaine
        annee, semaine = map(int, filtre_semaine.split('-'))

        # Filtrer les données pour l'élève sélectionné et la semaine
        df_filtered = df[(df['semaine'] == semaine) & (df['annee'] == annee)]

        # Vérifier si des données sont disponibles pour cette semaine
        if df_filtered.empty:
            # Si aucune donnée n'est disponible, retourner un graphique vide
            fig = px.bar(
                title=f"Aucune donnée disponible (Semaine {semaine}, {annee})",
                labels={'schedule': 'Date', 'duree_h': 'Nombre d\'heures', 'nom': 'Matière'}
            )
            return fig, []
        # Regrouper les données par date et matière, et additionner les heures
        df_grouped = df_filtered.groupby(['schedule', 'nom'], as_index=False).agg({'duree_h': 'sum'})


        # Créer le graphique
        fig = px.bar(
            df_filtered,
            x='schedule',  # Axe X : jours de la semaine
            y='duree_h',  # Axe Y : nombre d'heures
            color='nom',  # Couleur par matière
            title=f"Charge de travail - Semaine {semaine}, {annee}",
            labels={'schedule': 'Date', 'duree_h': 'Nombre d\'heures', 'nom': 'Matière'},
            text='nom',  # Afficher le type de cours sur les barres
            color_discrete_sequence=app7_charge_tools.custom_palette  # ou 'Bold', 'Dark2', etc.
        )

        fig.update_traces(
            textposition='outside'  # Positionner les étiquettes à l'extérieur
        )

        fig.update_xaxes(
            title_text="Jour"
        )
        fig.update_yaxes(title_text="Nombre d'heures")

        return fig, semaine_options
