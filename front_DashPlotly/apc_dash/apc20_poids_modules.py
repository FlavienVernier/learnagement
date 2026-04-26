import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
from app_tools import get_endpoint, get_python_backend_url

# ==========================================
# 1. LE LAYOUT (L'interface visuelle)
# ==========================================
audit_poids_modules_layout = html.Div([
    html.H3("Audit : Poids Réel des Compétences", style={"marginBottom": "10px"}),
    html.P("Ce graphique analyse le volume horaire réel (CM + TD + TP + Projet + En autonomie) alloué à chaque compétence de la formation.", className="text-muted"),
    
    dbc.Card(
        dbc.CardBody([
            # Un petit loader (cercle qui tourne) le temps que les données se calculent
            dcc.Loading(
                id="loading-graph",
                type="circle", # <--- C'est souvent cette virgule qui manque !
                children=dcc.Graph(
                    id="graph-poids-competences",
                    config={
                        'displaylogo': False,
                        'displayModeBar': False # Optionnel : cache toute la barre pour faire plus propre
                    }
                )
            )
        ]),
        className="shadow-sm",
        style={"marginTop": "20px"}
    )
])

# ==========================================
# 2. LE CALLBACK (Le cerveau / calcul des données)
# ==========================================
def register_poids_modules_callbacks(app):
    @app.callback(
        Output("graph-poids-competences", "figure"),
        Input("url", "pathname"), # Se déclenche automatiquement quand on ouvre la page
        State("token", "data")
    )
    def update_graph(pathname, token):
        # A. Récupération des données via tes APIs existantes
        df_comp = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/competences/"), token=token))
        df_niv = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/niveaux/"), token=token))
        df_ac = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/apprentissages/"), token=token))
        df_ac_mod = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/ac_modules/"), token=token))
        df_mod = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/modules/"), token=token))
        
        # Sécurité : Si la base est vide
        if df_comp.empty or df_mod.empty or df_ac_mod.empty:
            return px.pie(title="Données insuffisantes en base de données")

        # B. La Grande Jointure (Chemin : Compétence -> Niveau -> AC -> AC_Module -> Module)
        df = pd.merge(df_comp[['id_competence', 'libelle_competence']], df_niv[['id_niveau', 'id_competence']], on="id_competence")
        df = pd.merge(df, df_ac[['id_apprentissage_critique', 'id_niveau']], on="id_niveau")
        df = pd.merge(df, df_ac_mod[['id_apprentissage_critique', 'id_module']], on="id_apprentissage_critique")
        
        # Nettoyage des heures (on s'assure que ce sont des nombres, on remplace le vide par 0)
        df_mod['hCM'] = pd.to_numeric(df_mod['hCM'], errors='coerce').fillna(0)
        df_mod['hTD'] = pd.to_numeric(df_mod['hTD'], errors='coerce').fillna(0)
        df_mod['hTP'] = pd.to_numeric(df_mod['hTP'], errors='coerce').fillna(0)
        df_mod['hPersonnelle'] = pd.to_numeric(df_mod['hPersonnelle'], errors='coerce').fillna(0)
        
        # On ajoute les infos du module à notre grand tableau
        df = pd.merge(df, df_mod[['id_module', 'hCM', 'hTD', 'hTP','hPersonnelle']], on="id_module")

        # C. LE PIÈGE ! On supprime les doublons (1 module compté 1 seule fois par compétence)
        df_unique = df.drop_duplicates(subset=['id_competence', 'id_module']).copy()

        # D. Calcul du Total des heures pour chaque ligne
        df_unique['Total_Heures'] = df_unique['hCM'] + df_unique['hTD'] + df_unique['hTP'] + df_unique['hPersonnelle']

        # E. Regroupement (On additionne toutes les heures par Compétence)
        df_final = df_unique.groupby('libelle_competence')['Total_Heures'].sum().reset_index()

        # F. Création du Graphique Donut avec Plotly (Version Design Amélioré)
        fig = px.pie(
            df_final, 
            values='Total_Heures', 
            names='libelle_competence', 
            hole=0.45, # Un peu plus large au centre pour faire plus moderne
            title="Poids des Compétences en Volume Horaire (CM+TD+TP)",
            color_discrete_sequence=px.colors.qualitative.Safe # Une palette de couleurs professionnelle
        )
        
        # Options de design des parts (Traces)
        fig.update_traces(
            textposition='inside', 
            textinfo='percent', # <-- La magie est ici : on n'affiche QUE le % sur le graphique
            textfont_size=16,
            textfont_color='white',
            marker=dict(line=dict(color='#FFFFFF', width=2)), # Petites bordures blanches entre les parts
            hovertemplate=(
                "<b style='font-size:14px'>%{label}</b><br><br>"
                "Volume alloué : <b>%{value} Heures</b><br>"
                "Poids dans le diplôme : <b>%{percent}</b><extra></extra>"
            )
        )
        
        # Options de mise en page globale (Layout)
        fig.update_layout(
            margin=dict(t=60, b=80, l=20, r=20), 
            showlegend=True, # On réactive la légende
            legend=dict(
                orientation="h", # Légende horizontale
                yanchor="top",
                y=-0.1, # On la place en bas du graphique
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            hoverlabel=dict(bgcolor="white", font_size=13) # Infobulle propre sur fond blanc
        )
        
        return fig