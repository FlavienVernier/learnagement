from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import mysql
import mysql.connector
import app3_taux_absenteisme_tools

load_dotenv()

# user = os.getenv("MYSQL_USER_LOGIN")
# password = os.getenv("MYSQL_USER_PASSWORD")
# host = os.getenv("MYSQL_SERVER")
# port = os.getenv("MYSQL_PORT")
# database = os.getenv("MYSQL_DB")
#
# # Se connecter à la base de données MySQL
# conn = mysql.connector.connect(
#     user=user,
#     password=password,
#     host=host,
#     port=port,
#     database=database
# )
#
# # Exécuter la requête pour récupérer les dépendances
# cur = conn.cursor()
#
# #cur.execute("SELECT * FROM VIEW_graphe_dependances")
# cur.execute("SELECT abs.id_seance_to_be_affected_as_enseignant, abs.id_etudiant, id_promo, YEAR(sess.schedule) FROM CLASS_absence as abs INNER JOIN LNM_etudiant as etu ON abs.id_etudiant=etu.id_etudiant INNER JOIN CLASS_session_to_be_affected_as_enseignant as sess ON abs.id_seance_to_be_affected_as_enseignant=sess.id_seance_to_be_affected_as_enseignant;")
#
# rows = cur.fetchall()
#
# data = pd.DataFrame(rows, columns=["seance", "etudiant", "promo", "annee"])
data = app3_taux_absenteisme_tools.get_all_anonymous_absence()
data = data.rename(columns={"id_seance_to_be_affected_as_enseignant" : "seance", "id_etudiant" : "etudiant", "id_promo" : "promo", "annee" : "annee"})

# Calculer les heures d'absence totales et la taille des promotions
fusion = (
    pd.DataFrame(data)
    .groupby(["etudiant", "promo", "annee"])
    .agg(total_heures_absence=("seance", "count"),
         taille_promo=("promo", "count"))  # 'size' pour compter les lignes
    .reset_index()
)

# Calcul de l'absence moyenne par étudiant (total des heures d'absence divisé par la taille de la promo)
fusion["absence_moyenne"] = fusion["total_heures_absence"] / fusion["taille_promo"]

default_annee = 0
default_filiere = "No Filiere"
if 'annee' in fusion and 'promo' in fusion and len(fusion["annee"]) > 0 and len(fusion["promo"]) > 0:
    # Créer des figures par défaut
    default_annee = fusion['annee'][0]  # La première année par défaut
    default_figure_annee = px.bar(
        fusion[fusion['annee'] == default_annee],
        x='promo',
        y='absence_moyenne',
        title=f"Répartition des absences par filière pour l'année {default_annee}",
        labels={"promo": "Filière", "absence_moyenne": "Absence moyenne"}
    )

    default_filiere = fusion['promo'][0]  # La première filière par défaut
    default_figure_filiere = px.bar(
        fusion[fusion['promo'] == default_filiere],
        x='promo',
        y='absence_moyenne',
        title=f"Répartition des absences pour la filière {default_filiere} sur plusieurs années",
        labels={"annee": "Année", "absence_moyenne": "Absence moyenne"}
    )
else:
    default_figure_annee = px.bar(
        title=f"No Data",
    )

    default_figure_filiere = px.bar(
        title=f"No Data",
    )
default_figure_filiere.update_layout(
    xaxis=dict(
        type='category'  # Forcer l'axe x à être catégoriel
    )
)
"""
# Application Dash
app = Dash(__name__)
"""
app3_layout = html.Div([
    # Dropdown pour sélectionner l'année
    html.Div([
        html.Label("Sélectionnez une année :"),
        dcc.Dropdown(
            id='dropdown-annee',
            options=[{'label': str(annee), 'value': annee} for annee in sorted(fusion['annee'].unique())],
            value=default_annee,  # Valeur par défaut
            className="dropdown-style"  # Classe CSS pour le Dropdown
        )
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS

    # Bar chart pour les filières d'une année avec figure par défaut
    dcc.Graph(
        id='bar-chart-annee',
        figure=default_figure_annee,  # Figure par défaut
        className="graph-style"  # Classe CSS pour le graphique
    ),

    html.Hr(),

    # Dropdown pour sélectionner la filière
    html.Div([
        html.Label("Sélectionnez une filière :"),
        dcc.Dropdown(
            id='dropdown-filiere',
            options=[{'label': filiere, 'value': filiere} for filiere in sorted(fusion['promo'].unique())],
            value=default_filiere,  # Valeur par défaut
            className="dropdown-style"  # Classe CSS pour le Dropdown
        )
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS

    # Bar chart pour les années d'une filière avec figure par défaut
    dcc.Graph(
        id='bar-chart-filiere',
        figure=default_figure_filiere,  # Figure par défaut
        className="graph-style"  # Classe CSS pour le graphique
    )
])


def register_callbacks(app):
    # Callbacks pour mettre à jour les graphiques en fonction des sélections
    @app.callback(
        Output('bar-chart-annee', 'figure'),
        Input('dropdown-annee', 'value')
    )
    def update_bar_chart_annee(selected_annee):
        if 'annee' in fusion and len(fusion["annee"]) > 0 :
            # Filtrer les données pour l'année sélectionnée
            filtered_df = fusion[fusion['annee'] == selected_annee]
            # Créer le bar chart avec l'absence moyenne
            fig = px.bar(
                filtered_df,
                x='promo',
                y='absence_moyenne',
                title=f"Répartition des absences par filière pour l'année {selected_annee}",
                labels={"promo": "Filière", "absence_moyenne": "Absence moyenne"},
                color_discrete_sequence=['#007bff']  # ← couleur personnalisée
            )
        else:
            fig = px.bar(
                title="No Data",
            )
        return fig

    @app.callback(
        Output('bar-chart-filiere', 'figure'),
        Input('dropdown-filiere', 'value')
    )
    def update_bar_chart_filiere(selected_filiere):
        if 'promo' in fusion and len(fusion["promo"]) > 0 :
            # Filtrer les données pour la filière sélectionnée
            filtered_df = fusion[fusion['promo'] == selected_filiere]
            # Créer le bar chart avec l'absence moyenne
            fig = px.bar(
                filtered_df,
                x='annee',
                y='absence_moyenne',
                title=f"Répartition des absences pour la filière {selected_filiere} sur plusieurs années",
                labels={"annee": "Année", "absence_moyenne": "Absence moyenne"},
                color_discrete_sequence=['#007bff']  # ← couleur personnalisée
            )
        else:
            fig = px.bar(
                title="No Data",
            )
        
        # Forcer l'axe x à être catégoriel
        fig.update_layout(
            xaxis=dict(
                type='category'  # Assurez-vous que l'axe des années est catégoriel
            )
        )
        
        return fig
"""
# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
"""
