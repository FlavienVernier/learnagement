from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app_tools import get_endpoint, get_python_backend_url
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


trajectoire_layout = html.Div([
    html.H3("Ma Trajectoire de Compétences Polytech", style={"marginBottom": "20px"}),
    
    html.Div([
        html.Label("Dans quelle année es-tu ?"),
        dcc.Dropdown(
            id="annee-dropdown",
            options=[
                {"label": "1ère Année (Niveau 1)", "value": "label_annee_1"},
                {"label": "2ème Année (Niveau 2)", "value": "label_annee_2"},
                {"label": "3ème Année (Niveau 3)", "value": "label_annee_3"},
            ],
            value="label_annee_1",
            clearable=False,
            style={"width": "300px"}
        ),
    ], style={"marginBottom": "30px"}),

    # Zone d'affichage des cartes de trajectoire
    html.Div(id="trajectoire-container")
])

def render_step(label_annee, texte_niveau, liste_modules, is_active):
    """Dessine une étape avec le libellé du niveau ET les modules associés"""
    bg_color = "#3F7EE8" if is_active else "#f8f9fa"
    text_color = "white" if is_active else "black"
    border = "2px solid #3F7EE8" if is_active else "1px solid #dee2e6"
    modules_color = "#e0e0e0" if is_active else "#6c757d" # Gris clair si actif, gris foncé sinon
    
    return html.Div([
        html.Div(label_annee, style={
            "fontWeight": "bold", 
            "color": "#3F7EE8" if not is_active else "white",
            "marginBottom": "5px"
        }),
        html.Div([
            # Le libellé de la compétence
            html.Div(texte_niveau, style={"fontWeight": "bold", "marginBottom": "10px"}),
            
            # Les modules
            html.Div(f"📚 {liste_modules}", style={
                "fontSize": "0.8rem", 
                "fontStyle": "italic", 
                "color": modules_color
            })
        ], style={
            "padding": "15px",
            "backgroundColor": bg_color,
            "color": text_color,
            "borderRadius": "5px",
            "border": border,
            "minHeight": "100px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "textAlign": "center"
        })
    ])

def register_trajectoire_callbacks(app):
    @app.callback(
        Output("trajectoire-container", "children"),
        Input("annee-dropdown", "value"),
        Input("user_id", "data"),
        State("token", "data")
    )
    def update_trajectoire(selected_annee, user_id, token):
        # 1. On récupère TOUTES les tables nécessaires
        df_comp = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/competences/"), token=token))
        df_niv = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/niveaux/"), token=token))
        df_ac = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/apprentissages/"), token=token))
        df_ac_mod = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/ac_modules/"), token=token))
        df_mod = pd.DataFrame(get_endpoint(get_python_backend_url("/apc/modules/"), token=token))
        
        if df_comp.empty or df_niv.empty:
            return html.P("Données indisponibles.")

        # ==========================================
        # ETAPE A : TRAITEMENT DES NIVEAUX (Comme avant)
        # ==========================================
        df_base = pd.merge(df_comp, df_niv, on="id_competence")
        df_pivot_niveaux = df_base.pivot(
            index='id_competence', columns='niveau', values='libelle_niveau'
        ).reset_index().fillna("Niveau non défini")

        # ==========================================
        # ETAPE B : LA CHASSE AUX MODULES (Les Jointures)
        # ==========================================
        if not df_ac.empty and not df_ac_mod.empty and not df_mod.empty:
            # On relie Niveau -> AC
            df_link = pd.merge(df_niv[['id_niveau', 'id_competence', 'niveau']], df_ac, on="id_niveau", how="left")
            # On relie AC -> AC_Module
            df_link = pd.merge(df_link, df_ac_mod, on="id_apprentissage_critique", how="left")
            # On relie AC_Module -> Module (Pour récupérer le code_module)
            df_link = pd.merge(df_link, df_mod[['id_module', 'code_module']], on="id_module", how="left")
            
            # On regroupe par Compétence et par Niveau pour lister tous les modules
            df_modules = df_link.groupby(['id_competence', 'niveau'])['code_module'].unique().apply(
                lambda x: ", ".join([str(m) for m in x if pd.notna(m)])
            ).reset_index()
            
            # On remplace les cases vides par "Aucun module"
            df_modules['code_module'] = df_modules['code_module'].replace("", "Les modules seront mis à disposition bientôt")

            # On pivote les modules pour avoir 1, 2 et 3 sur la même ligne
            df_pivot_modules = df_modules.pivot(
                index='id_competence', columns='niveau', values='code_module'
            ).reset_index().fillna("Aucun module")
        else:
            # Sécurité au cas où la base de données n'a pas encore de modules
            df_pivot_modules = pd.DataFrame({'id_competence': df_pivot_niveaux['id_competence']})
            for i in [1, 2, 3]:
                df_pivot_modules[i] = "Aucun module"

        # ==========================================
        # ETAPE C : FUSION FINALE ET AFFICHAGE
        # ==========================================
        cards = []
        for _, row in df_comp.iterrows():
            id_comp = row['id_competence']
            
            # On récupère la ligne correspondante pour les libellés et les modules
            row_niv = df_pivot_niveaux[df_pivot_niveaux['id_competence'] == id_comp].squeeze()
            row_mod = df_pivot_modules[df_pivot_modules['id_competence'] == id_comp].squeeze()
            
            # Sécurité si les données n'existent pas
            if row_niv.empty: continue

            # Attention : adapte le get(1) selon le type de ta colonne niveau (entier 1, ou texte '1')
            label_n1 = row_niv.get(1, "N/A")
            label_n2 = row_niv.get(2, "N/A")
            label_n3 = row_niv.get(3, "N/A")
            
            mod_n1 = row_mod.get(1, "Aucun") if not row_mod.empty else "Aucun"
            mod_n2 = row_mod.get(2, "Aucun") if not row_mod.empty else "Aucun"
            mod_n3 = row_mod.get(3, "Aucun") if not row_mod.empty else "Aucun"

            cards.append(dbc.Card([
                dbc.CardHeader(html.B(f"{row['code_competence']} : {row['libelle_competence']}")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(render_step("1A", label_n1, mod_n1, selected_annee == "label_annee_1"), width=4),
                        dbc.Col(render_step("2A", label_n2, mod_n2, selected_annee == "label_annee_2"), width=4),
                        dbc.Col(render_step("3A", label_n3, mod_n3, selected_annee == "label_annee_3"), width=4),
                    ])
                ])
            ], style={"marginBottom": "15px"}))
            
        return cards