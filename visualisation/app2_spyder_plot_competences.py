from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import app2_spyder_plot_competences_tools

# Fonction pour filtrer les apprentissages critiques
def choix_apprentissage_critique(df, competence, niveau):
    filtered_df = df[(df['libelle_competence'] == competence) & (df['id_competence'] == niveau)]
    if filtered_df.empty:
        return pd.DataFrame(dict(r=[], theta=[]))
    return pd.DataFrame(dict(
        r=[niveau] * len(filtered_df),
        theta=filtered_df['libelle_apprentissage']
    ))


app2_layout = html.Div([
    # Premier Spyder Chart
    dcc.Graph(
        id="spyder_competence_globale",
    ),
    
    # Deuxième Spyder Chart
    dcc.Graph(
        id="niveau_apprentissage_critique",
        figure=go.Figure().update_traces(fill="toself", 
                mode="markers",  # Ajoute des marqueurs cliquables
                marker=dict(size=10, color='#007bff')).update_layout(title="Niveau par apprentissage critique")
    ),
])

# Callbacks pour l'interaction entre les graphiques
def register_callbacks(app):
    @app.callback(
        Output("spyder_competence_globale", "figure"),
        Input('user_id', 'data')  # Réagit au clic sur le premier graphique
    )

    def create_chart(user_id):
        data = app2_spyder_plot_competences_tools.get_evaluation_apprentissage_critique_by_studentId(user_id)
        figure=px.line_polar(
            data,
            r="evaluation",
            theta="libelle_competence",
            line_close=True
        ).update_traces(
                fill="toself",
                mode="markers+lines",  # Ajoute des marqueurs cliquables
                marker=dict(size=10, color='#007bff'),  # Augmente la visibilité des points
                line=dict(color="#007bff", width=3)
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
        return figure


    @app.callback(
        Output("niveau_apprentissage_critique", "figure"),  # Met à jour le second Spyder Chart
        Input("spyder_competence_globale", "clickData"),
        Input('user_id', 'data')  # Réagit au clic sur le premier graphique
    )
        
    def update_chart(click_data, user_id):
        if click_data and "points" in click_data:
            data = app2_spyder_plot_competences_tools.get_evaluation_apprentissage_critique_by_studentId(user_id)
            # Extraire le libellé de la compétence (theta)
            points = click_data["points"][0]
            clicked_theta = points.get("theta")  # Compétence cliquée

            if not clicked_theta:
                return go.Figure().update_layout(title="Aucune compétence détectée.")

            # Filtrer les apprentissages critiques pour la compétence cliquée
            filtered_df = data[data["libelle_competence"] == clicked_theta]

            if filtered_df.empty:
                return go.Figure().update_layout(title=f"Aucune donnée pour '{clicked_theta}'.").update_traces(fill='toself')

            # Créer le deuxième graphique
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=filtered_df["evaluation"],
                theta=filtered_df["libelle_apprentissage"], # + " - " + filtered_df["Matiere"],
                mode="markers+text",
                text=filtered_df["evaluation"],
                textposition="top center",
                fill="toself",
                name="Apprentissages Critiques",
                line=dict(color="#007bff", width=3),  # ← ligne orange ici
                marker=dict(size=10, color="#007bff")  # ← points oranges
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

