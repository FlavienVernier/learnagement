import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, Input, Output, State
import app7_charge_tools

def update_df(df):
    # Convertir la colonne "date" en format datetime
    df['schedule'] = pd.to_datetime(df['schedule'], errors='coerce')  # Gérer les erreurs éventuelles de conversion
    # Ajouter une colonne "semaine" pour le numéro de la semaine
    df['semaine'] = df['schedule'].dt.isocalendar().week  # Numéro de la semaine ISO
    df['annee'] = df['schedule'].dt.year  # Ajouter l'année pour gérer les années distinctes

levels = {"Année": ["Année"]}

# Layout de l'application
app7_etudiant_layout = html.Div([
    html.H1("Suivi d'Avancement des Cours",
            style={'font-family': 'verdana'}
            ),

    # Premier menu déroulant (niveau d'agrégation)
    html.Label("Sélectionnez :",
               style={'margin-left': '5px'}),
    dcc.Dropdown(
        id='level-dropdown',
        options=[{"label": key, "value": key} for key in levels.keys()],
        value="Année",
        style={
            'width': '50%',
            'margin-left': '5px'
        }
    ),

    # Deuxième menu déroulant (catégorie)
    html.Label("Sélectionnez les détails :",
               style={'margin-left': '5px'}),
    dcc.Dropdown(
        id='category-dropdown',
        style={
            'width': '50%',
            'margin-left': '5px'
        }
    ),

    # Graphique
    dcc.Graph(id='progress-chart', style={'marginTop': '30px'}),

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
    # Callback pour mettre à jour le deuxième menu déroulant
    @app.callback(
        Output('category-dropdown', 'options'),
        Output('category-dropdown', 'value'),
        Input('level-dropdown', 'value'),
        State('token', 'data'),
    )
    def update_category_dropdown(selected_level, token):
        categories = levels[selected_level]
        options = [{"label": cat, "value": cat} for cat in categories]
        return options, categories[0]

        # Callback pour mettre à jour le graphique en fonction des sélections

    @app.callback(
        Output('progress-chart', 'figure'),
        Input('level-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        State('user_id', 'data'),
        State('token', 'data'),
    )
    def update_graph(selected_level, selected_category, user_id, token):
        data_done = app7_charge_tools.get_etudiant_pastedt(token, user_id)
        data_all = app7_charge_tools.get_etudiant_edt(token, user_id)
        data = app7_charge_tools.calcul_avancement(data_done, data_all)
        df = app7_charge_tools.transforme_données(data)

        # Calculer les pourcentages
        df["Completion (%)"] = (df["Realized"] / df["Total"]) * 100


        # Filtrer les données pour la catégorie sélectionnée
        filtered_df = df[df["Category"] == selected_category]

        background_trace = go.Bar(
            x=[100] * len(filtered_df),  # Toutes les barres atteignent 100 %
            y=filtered_df["Category"],
            orientation='h',
            marker=dict(
                color='rgba(200, 200, 200, 0.4)',
                line=dict(color='rgba(148, 150, 152, 1)', width=3)
            ),
            hoverinfo='none',
        )

        # Création de la trace des valeurs réelles
        actual_trace = go.Bar(
            x=filtered_df["Completion (%)"],
            y=filtered_df["Category"],
            orientation='h',
            text=filtered_df["Completion (%)"].map(lambda x: f"{x:.0f}%"),
            textposition='inside',
            marker=dict(
                color='rgba(0, 123, 255, 0.6)',
                line=dict(color='rgba(0, 123, 255, 1)', width=3)
            ),
            hoverinfo='none'
        )

        # Création de la figure
        fig = go.Figure(data=[background_trace, actual_trace])

        # Mise en forme de la figure
        fig.update_layout(
            title=f"{selected_category}",
            xaxis=dict(title="Pourcentage d'achèvement", range=[0, 110]),
            yaxis=dict(title='', showticklabels=False),
            barmode='overlay',  # Superposer les barres
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig


    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graphique-charge_etudiant', 'figure'),
        Output('graphique-charge_etudiant', 'options'),
        Input('filtre-semaine', 'value'),
        State('user_id', 'data'),
        State('token', 'data'),
    )
    def update_graph(filtre_semaine, user_id, token):
        df = app7_charge_tools.get_chargeByEtudianttId(token, user_id)

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
