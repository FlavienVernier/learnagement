from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import requests

# ==========================================
# LAYOUT DE LA PAGE
# ==========================================
app16_layout = html.Div([
    html.H1("Audit Sémantique des Données", style={'textAlign': 'center', 'marginBottom': '5px'}),
    html.P("Détection des erreurs de saisie dans les compétences via l'Intelligence Artificielle.", style={'textAlign': 'center'}),

    html.Div(  
        children=[
            # Bouton pour déclencher l'API
            html.Button(
                "Lancer l'analyse", 
                id="btn-audit", 
                style={'padding': '10px 20px', 'fontSize': '16px', 'cursor': 'pointer'}
            )
        ],
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap':'10px', 'marginBottom': '15px'}
    ),

    # Affichage du chargement et du tableau des résultats
    dcc.Loading(
        id="loading-audit",
        children=[
            html.Div(
                id='audit-results-table', 
                style={'margin': '10px auto', 'width': '80%'}
            )
        ]
    ),

    # Affichage des messages d'erreur si l'API ne répond pas
    html.Div(
        id='audit-message',
        style={'textAlign': 'center', 'fontSize': 18, 'marginTop': 5, 'color': 'red'}
    )
])


# ==========================================
# CALLBACKS
# ==========================================
def register_callbacks(app):

    @app.callback(
        Output('audit-results-table', 'children'),
        Output('audit-message', 'children'),
        Input('btn-audit', 'n_clicks'),
        State('token', 'data'),
        prevent_initial_call=True
    )
    def run_semantic_audit(n_clicks, token):
        # Sécurité si le clic n'a pas encore eu lieu
        if not n_clicks:
            return "", ""

        # 1. On appelle ton API FastAPI (Ajuste le port si ce n'est pas le 8000)
        api_url = "http://localhost:8000/audit/competences/incoherences" 
        
        # On attache le token JWT de l'utilisateur connecté
        headers = {"Authorization": f"Bearer {token}"} if token and token != 'none' else {}
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return "", f"Erreur de connexion à l'API FastAPI : {str(e)}"

        if not data:
            return "", "Aucune anomalie détectée ou aucune donnée retournée."

        # 2. Transformation des données pour Dash
        df = pd.DataFrame(data)
        
        # 3. Création du tableau de résultats interactif
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {"name": "ID", "id": "id_competence"},
                {"name": "Libellé", "id": "libelle_niveau"},
                {"name": "Score de Cohérence", "id": "score_coherence"},
            ],
            # On met en évidence (rouge) les lignes avec un mauvais score
            style_data_conditional=[
                {
                    'if': {'filter_query': '{score_coherence} < 0.4'},
                    'backgroundColor': '#FF4136',
                    'color': 'white'
                }
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            page_size=15,          # Pagination à 15 lignes
            sort_action="native"   # Permet de trier les colonnes (très utile pour trier par score)
        )
        
        return table, ""