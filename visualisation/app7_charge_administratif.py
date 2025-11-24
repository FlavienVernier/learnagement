import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime
import app7_charge_tools
import app_tools


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

def get_semester():
    today = datetime.today().date()  # Date d'aujourd'hui
    semester = 0  # even semester
    if (today > date(today.year, 8, 1) and today < date(today.year + 1, 1, 15)):
        semester = 1  # odd semester
    return semester

# Layout de l'application
app7_administratif_layout = html.Div([
    html.H1("Visualisation de la charge de travail des enseignants"),
    dbc.Row([
        dbc.Label("Enseignant", html_for="enseignant_input", width=2),
        dbc.Col(dcc.Dropdown(id="enseignant_input_administratif",
                             #options=[{'label': "Please select tuteur", 'value': "NULL"}] + [{'label': v, 'value': v} for v in get_teachers()],
                             options=[],
                             placeholder="Please select enseignant",
                             value=""), width=8),
    ]),
    
    # Dropdown pour sélectionner le filtre de période
    dcc.Dropdown(
        id='filtre-periode',
        options=[
            {'label': 'Tous les jours', 'value': 'all'},
            {'label': 'Ce Semestre', 'value': 'semester'},
            {'label': 'Ce mois', 'value': 'this_month'},
            {'label': "Aujourd'hui", 'value': 'today'}
        ],
        value='all',  # Valeur par défaut
        placeholder="Sélectionnez une période",
    ),
    
    # Graphique
    dcc.Graph(id='graphique-charge_administratif'),
    html.Div(id='summary_div_administratif'),
    html.Div(id='total_div_administratif')
])

def register_callbacks(app):
    @app.callback(
        Output('enseignant_input_administratif', 'options'),
        Input('user_id', 'data'),
    )
    def update_options(user_id):
        dfi = app_tools.get_explicit_keys("LNM_enseignant")
        intervenant_options = [{'label': row['ExplicitSecondaryK'], 'value': row['id']} for _, row in dfi.iterrows()]
        return intervenant_options
    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('graphique-charge_administratif', 'figure'),
        Input('filtre-periode', 'value'),
        Input('enseignant_input_administratif', 'value'),
        prevent_initial_call=True
    )
    def update_graph(filtre_periode, user_id):
        print(filtre_periode, user_id, flush=True)
        df = app7_charge_tools.get_chargeByEnseignantId(user_id)


        today = datetime.today().date()  # Date d'aujourd'hui
        current_month = datetime.today().strftime('%B')  # Mois courant, par exemple "January"

        # Filtrer les données selon la sélection
        if filtre_periode == 'all':
            df_filtered = update_df(df)
        elif filtre_periode == 'semester':
            semester = get_semester()

            df_filtered = update_df(df[df['id_semestre']%2 == semester])

        elif filtre_periode == 'today':
            df_calcule = update_df(df)
            df_filtered = df_calcule[df_calcule['jour'] == today]  # Filtre pour le jour d'aujourd'hui
        elif filtre_periode == 'this_month':
            df_calcule = update_df(df)
            df_filtered = df_calcule[df_calcule['mois'] == current_month]  # Filtre pour le mois en cours
        else:
            df_calcule = update_df(df)
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

    # Callback pour mettre à jour le graphique
    @app.callback(
        Output('summary_div_administratif', 'children'),
        Output('total_div_administratif', 'children'),
        Input('filtre-periode', 'value'),
        Input('enseignant_input_administratif', 'value'),
        prevent_initial_call=True
    )
    def display_table(period, user_id):
        print(period, user_id, flush=True)
        df = app7_charge_tools.get_chargeByEnseignantId(user_id)
        if period == 'all':
            df = df[['type', 'duree_h']].groupby(['type']).sum().reset_index()
        elif    period == 'semester':
            semester = get_semester()
            df = df[df['id_semestre']%2 == semester][['type', 'duree_h']].groupby(['type']).sum().reset_index()
        elif period == 'this_month':
            current_month = datetime.today().strftime('%B')  # Mois courant, par exemple "January"
            df = update_df(df)
            df = df[df['mois'] == current_month]  # Filtre pour le mois en cours
        elif period == 'today':
            today = datetime.today().date()  # Date d'aujourd'hui
            df = update_df(df)
            df = df[df['jour'] == today]  # Filtre pour le jour d'aujourd'hui
        table_1 = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        ),
        table_2 = dbc.Table.from_dataframe(
            pd.DataFrame({'sum': df[['duree_h']].sum()}),
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        ),


        return table_1, table_2
