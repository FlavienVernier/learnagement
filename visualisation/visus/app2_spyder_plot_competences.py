import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Charger les données pour le deuxième graphique
df_competences = pd.DataFrame({
    "Niveau": [1, 1, 2, 3, 3,2,1,2,3],
    "Competence": [
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
    "Apprentissages_critiques": [
        "Concevoir et gérer une base de données",
        "Mettre en œuvre une architecture client-serveur",
        "Choisir une méthode de développement adaptée",
        "Définir une architecture de système logiciel",
        "Évaluer et optimiser les performances",
        "Choisir et mettre en œuvre des outils d’IA (approches stochastiques deep learning) pour l’analyse et la prédiction de données",
        "Implémenter des outils mathématiques",
        "Répartir les fonctionnalités (acquisition stockage traitements visualisation...) sur un système N-Tieris",
        "Développer des rendus visuels divers en vue d’une aide à la décision multi-critères"
    ],
    "Matiere": ["INFO501", "INFO502", "INFO734", "INFO833", "DATA831","MATH741","MATH641","INFO834","INFO931"]
})

# Créer le DataFrame pour le premier Spyder Chart
df_competence_globale = pd.DataFrame(dict(
    r=[2, 2, 3, 2],  # Scores pour les compétences
    theta=[
        'Concevoir et mettre en œuvre des systèmes informatiques',
        'Collecter et traiter des données numériques',
        'Gérer les usages des données numériques en lien avec le client',
        'Gérer un projet informatique'
    ]
))

# Fonction pour filtrer les apprentissages critiques
def choix_apprentissage_critique(df, competence, niveau):
    filtered_df = df[(df['Competence'] == competence) & (df['Niveau'] == niveau)]
    if filtered_df.empty:
        return pd.DataFrame(dict(r=[], theta=[]))
    return pd.DataFrame(dict(
        r=[niveau] * len(filtered_df),
        theta=filtered_df['Apprentissages_critiques'] + " - " + filtered_df['Matiere']
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
            df_competence_globale,
            r="r",
            theta="theta",
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
            clicked_theta = points.get("theta")  # Compétence cliquée

            if not clicked_theta:
                return go.Figure().update_layout(title="Aucune compétence détectée.")

            # Filtrer les apprentissages critiques pour la compétence cliquée
            filtered_df = df_competences[df_competences["Competence"] == clicked_theta]

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
