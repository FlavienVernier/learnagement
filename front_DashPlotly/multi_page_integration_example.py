"""
Exemple d'intégration du dashboard Learnagement refactorisé
avec les autres pages/composants du projet
"""

from dash import Dash, html, dcc
from dash_pages import register_page, construct_id

# ═══════════════════════════════════════════════════════════════════
# IMPORTER LE LAYOUT ET LES CALLBACKS DU DASHBOARD
# ═══════════════════════════════════════════════════════════════════

from apc_dash.learnagement_dashboard_final_refactored import (
    layout as dashboard_layout,
    register_callbacks as register_dashboard_callbacks
)

# Vous pouvez aussi importer d'autres fichiers du projet de la même manière
# from app3_absenteisme_etudiant import (
#     app3_etudiant_layout,
#     register_callbacks as register_app3_callbacks
# )

# ═══════════════════════════════════════════════════════════════════
# CRÉER L'APPLICATION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='assets',
    title="Learnagement - Plateforme complète"
)

# ═══════════════════════════════════════════════════════════════════
# CRÉER LE LAYOUT PRINCIPAL (MULTI-PAGES OU SYSTÈME D'ONGLETS)
# ═══════════════════════════════════════════════════════════════════

app.layout = html.Div([
    dcc.Tabs(id='main-tabs', value='dashboard', children=[
        dcc.Tab(
            label='📊 Dashboard Learnagement',
            value='dashboard',
            children=[dashboard_layout]  # Importer le layout du dashboard
        ),
        # Vous pouvez ajouter d'autres onglets ici
        # dcc.Tab(
        #     label='📝 Absences Étudiants',
        #     value='absences',
        #     children=[app3_etudiant_layout]
        # ),
    ])
])

# ═══════════════════════════════════════════════════════════════════
# ENREGISTRER LES CALLBACKS DE TOUS LES COMPOSANTS
# ═══════════════════════════════════════════════════════════════════

# Enregistrer les callbacks du dashboard
register_dashboard_callbacks(app)

# Enregistrer les callbacks d'autres composants
# register_app3_callbacks(app)
# ... et autres ...

# ═══════════════════════════════════════════════════════════════════
# LANCEMENT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
