import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import mysql.connector
import mysql

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

def get_data (id_etudiant) :
    #cur.execute("SELECT * FROM VIEW_graphe_dependances")
    cur.execute(f"SELECT eval.id_etudiant, eval.evaluation, ac.libelle_apprentissage, niveau.libelle_niveau, competence.libelle_competence, competence.id_competence FROM ETU_competence_evaluation as eval INNER JOIN APC_apprentissage_critique as ac ON eval.id_apprentissage_critique=ac.id_apprentissage_critique INNER JOIN APC_niveau as niveau ON ac.id_niveau=niveau.id_niveau INNER JOIN APC_competence as competence ON niveau.id_competence=competence.id_competence WHERE eval.id_etudiant = {id_etudiant};")

    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["etudiant", "evaluation", "libelle_apprentissage", "libelle_niveau", "libelle_competence", "id_competence"])
    return data

# Temporaire : UPDATE A FAIRE = numéro étudiant de l'étudiant connecté
data = get_data(2)

# Charger les données pour le deuxième graphique
'''data = pd.DataFrame({
    "id_etudiant": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    "evaluation": [1, 1, 2, 3, 3,2,1,2,3],
    "libelle_competence": [
        "Concevoir et mettre en œuvre des systèmes informatiques",
        "Concevoir et mettre en œuvre des systèmes informatiques",
        "Concevoir et mettre en œuvre des systèmes informatiques",
        "Concevoir et mettre en œuvre des systèmes informatiques",
        "Concevoir et mettre en œuvre des systèmes informatiques",
        "Collecter et traiter des données numériques",
        "Collecter et traiter des données numériques",
        "Collecter et traiter des données numériques",
        "Collecter et traiter des données numériques"
    ],
    "libelle_apprentissage": [
        "Concevoir et gérer une base de données",
        "Mettre en œuvre une architecture client-serveur",
        "Choisir une méthode de développement adaptée",
        "Définir une architecture de système logiciel",
        "Évaluer et optimiser les performances",
        "Choisir et mettre en œuvre des outils d’IA (approches stochastiques deep learning) pour l’analyse et la prédiction de données",
        "Implémenter des outils mathématiques",
        "Répartir les fonctionnalités (acquisition stockage traitements visualisation...) sur un système N-Tieris",
        "Développer des rendus visuels divers en vue d’une aide à la décision multi-critères"
    ]
    })'''

# Fonction pour filtrer les apprentissages critiques
def choix_apprentissage_critique(df, competence, niveau):
    filtered_df = df[(df['libelle_competence'] == competence) & (df['id_competence'] == niveau)]
    if filtered_df.empty:
        return pd.DataFrame(dict(r=[], theta=[]))
    return pd.DataFrame(dict(
        r=[niveau] * len(filtered_df),
        theta=filtered_df['libelle_apprentissage']
    ))
"""
# Créer l'application Dash
app = dash.Dash(__name__)
"""
app2_layout = html.Div([
    # Premier Spyder Chart
    dcc.Graph(
        id="spyder-competence-globale",
        figure=px.line_polar(
            data,
            r="evaluation",
            theta="libelle_competence",
            line_close=True
        ).update_traces(
                fill="toself",
                mode="markers+lines",  # Ajoute des marqueurs cliquables
                marker=dict(size=10, color='blue')  # Augmente la visibilité des points
        ).update_layout(
            polar=dict(
            radialaxis=dict(
                dtick=1,
                range=[0, 3],
                tickfont=dict(size=12)
                )
            ),
            title="Niveau par compétence globale"
        )
    ),
    
    # Deuxième Spyder Chart
    dcc.Graph(
        id="niveau-apprentissage-critique",
        figure=go.Figure().update_traces(fill="toself", 
                mode="markers",  # Ajoute des marqueurs cliquables
                marker=dict(size=10, color='blue')).update_layout(title="Niveau par apprentissage critique")
    ),
])

# Callbacks pour l'interaction entre les graphiques
def register_callbacks(app):
    @app.callback(
        Output("niveau-apprentissage-critique", "figure"),  # Met à jour le second Spyder Chart
        Input("spyder-competence-globale", "clickData")  # Réagit au clic sur le premier graphique
    )
        
    def update_chart(click_data):
        if click_data and "points" in click_data:
            # Extraire le libellé de la compétence (theta)
            points = click_data["points"][0]
            clicked_theta = points.get("libelle_competence")  # Compétence cliquée

            if not clicked_theta:
                return go.Figure().update_layout(title="Aucune compétence détectée.")

            # Filtrer les apprentissages critiques pour la compétence cliquée
            filtered_df = data[data["libelle_competence"] == clicked_theta]

            if filtered_df.empty:
                return go.Figure().update_layout(title=f"Aucune donnée pour '{clicked_theta}'.").update_traces(fill='toself')

            # Créer le deuxième graphique
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=filtered_df["Niveau"],
                theta=filtered_df["Apprentissages_critiques"] + " - " + filtered_df["Matiere"],
                mode="markers+text",
                text=filtered_df["Niveau"],
                textposition="top center",
                fill="toself",
                name="Apprentissages Critiques"
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        dtick=1,
                        range=[0, 3],
                        tickfont=dict(size=12)
                    )
                ),
                title=f"Apprentissage critique (Compétence : {clicked_theta})"
            )
            return fig

        # Graphique vide si aucun clic
        return go.Figure().update_layout(title="Cliquez sur une compétence.")
"""
# Lancer l'application
if __name__ == "__main__":
    app.run_server(debug=True)
"""    
