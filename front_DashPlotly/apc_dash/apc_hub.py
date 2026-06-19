"""
Hub APC : regroupe toutes les sous-pages APC sous un seul item de menu.

Architecture :
- Une navbar interne avec un onglet par sous-page
- Une zone de KPI affichée en haut (sera enrichie quand on intégrera apc20_KPI)
- Une zone de contenu qui affiche la sous-page sélectionnée
- Routing par URL : /<role>/apc_hub/<subpage_key>
"""

from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc

from apc_dash.polytech_rag.app.ui.layout import create_layout as create_rag_layout

from apc_dash.polytech_rag.app.ui.callbacks import register_callbacks as reg_rag_orientation

# ── Imports des sous-pages APC ────────────────────────────────────────────────
from apc_dash.apc20_heatmap_apc import (
    heatmap_apc_layout,
    register_callbacks as reg_heatmap,
)
from apc_dash.apc20_KPI import (
    apc_layout as kpi_layout,
    register_callbacks as reg_kpi,
)
from apc_dash.apc20_competence_ac import (
    apc20_competence_ac_layout,
    register_callbacks as reg_competence,
)
from apc_dash.app_reseaupolytech_etudiant import (
    polytech_analysis_layout,
    register_reseau_polytech_callbacks,
)
from apc_dash.apc20_trajectoire import (
    trajectoire_layout,
    register_trajectoire_callbacks,
)
from apc_dash.apc20_poids_modules import (
    audit_poids_modules_layout,
    register_poids_modules_callbacks,
)
from apc_dash.apc20_metier_orientation import (
    apc20_metier_orientation_layout,
    register_callbacks as reg_orientation,
)

from apc_dash.apc20_ens_fiche_module import (
    fiche_module_content,
    register_callbacks as reg_fiche,
)
from apc_dash.apc20_ens_couverture import (
    couverture_content,
    register_callbacks as reg_couverture,
)
from apc_dash.apc20_ens_reseau_gaps import (
    reseau_gaps_content,
    register_callbacks as reg_reseau_gaps,
)
from apc_dash.apc20_ens_contribution import (
    contribution_content,
    register_callbacks as reg_contribution,
)
from apc_dash.apc20_ens_data_loader import register_ens_data_loader


# ── Définition des sous-pages ─────────────────────────────────────────────────
# 'kpi' n'apparaît PAS ici car il sera affiché en haut de toutes les sous-pages
# (à intégrer dans une 2e étape)
SUBPAGES = {
    'reseau': {
        'label': 'Réseau Polytech',
        'icon': 'fa-solid fa-network-wired',
        'layout': polytech_analysis_layout,
        'register': register_reseau_polytech_callbacks,
    },
    'heatmap': {
        'label': 'Cartographie des compétences',
        'icon': 'fa-solid fa-fire',
        'layout': heatmap_apc_layout,
        'register': reg_heatmap,
    },
    'competence': {
    'label': 'Analyse des compétences',
    'icon': 'fa-solid fa-graduation-cap',
    'layout': html.Div([
        html.Div(kpi_layout, style={
            "marginBottom": "25px",
            "padding": "16px",
            "backgroundColor": "white",
            "borderRadius": "8px",
            "boxShadow": "0 1px 4px rgba(0,0,0,0.08)"
        }),

        html.Div(apc20_competence_ac_layout)
    ]),
    'register': reg_competence,
},
    'trajectoire': {
        'label': "Trajectoire d'étude",
        'icon': 'fa-solid fa-route',
        'layout': trajectoire_layout,
        'register': register_trajectoire_callbacks,
    },
    'orientation': {
        'label': 'Orientation par métier',
        'icon': 'fa-solid fa-briefcase',
        'layout': apc20_metier_orientation_layout,
        'register': reg_orientation,
    },
    'poids': {
        'label': 'Poids des modules',
        'icon': 'fa-solid fa-balance-scale',
        'layout': audit_poids_modules_layout,
        'register': register_poids_modules_callbacks,
    },
    'fiche_module': {
    'label': 'Fiche Module',
    'icon': 'fa-solid fa-file-lines',
    'layout': fiche_module_content,
    'register': reg_fiche,
},
'couverture_apc': {
    'label': 'Couverture APC',
    'icon': 'fa-solid fa-table-cells',
    'layout': couverture_content,
    'register': reg_couverture,
},
'reseau_trous': {
    'label': 'Réseau et Trous',
    'icon': 'fa-solid fa-diagram-project',
    'layout': reseau_gaps_content,
    'register': reg_reseau_gaps,
},
'ma_contribution': {
    'label': 'Ma Contribution',
    'icon': 'fa-solid fa-person-chalkboard',
    'layout': contribution_content,
    'register': reg_contribution,
},
'orientation_rag': {
    'label': 'Assistant orientation',
    'icon': 'fa-solid fa-robot',
    'layout': create_rag_layout(),
    'register': reg_rag_orientation,
},
}
ROLE_SUBPAGES = {
    "etudiant":["reseau","competence", "heatmap", "trajectoire", "orientation","orientation_rag"],
    "enseignant": ["competence", "poids","fiche_module","couverture_apc","reseau_trous","ma_contribution",],
    "administratif": ["competence", "poids","couverture_apc","reseau_trous"],
}

DEFAULT_SUBPAGE_BY_ROLE = {
    "enseignant": "competence",
    "etudiant": "reseau",
    "administratif": "competence",
}


# ── Styles de la navbar interne ───────────────────────────────────────────────
NAVBAR_STYLE = {
    'display': 'flex',
    'alignItems': 'stretch',
    'gap': '4px',
    'padding': '0 24px',
    'height': '48px',
    'backgroundColor': '#ffffff',
    'borderBottom': '1px solid #e0e0e0',
    'boxShadow': '0 1px 3px rgba(0,0,0,0.05)',
    'overflowX': 'auto',
}

TAB_BASE = {
    'display': 'flex',
    'alignItems': 'center',
    'padding': '0 16px',
    'fontSize': '13px',
    'textDecoration': 'none',
    'whiteSpace': 'nowrap',
    'borderBottom': '3px solid transparent',
}

TAB_ACTIVE = {
    **TAB_BASE,
    'fontWeight': '600',
    'color': '#0056b3',
    'borderBottom': '3px solid #0056b3',
}

TAB_INACTIVE = {
    **TAB_BASE,
    'fontWeight': '400',
    'color': '#666',
}


# ── Layout exposé à l'app principale ──────────────────────────────────────────
apc_hub_layout = html.Div([
    # Zone réservée pour le KPI (à brancher dans une 2e étape)
    # html.Div(id='apc-hub-kpi-banner'),

    # Navbar interne
    html.Div(id='apc-hub-navbar', style=NAVBAR_STYLE),

    # Contenu de la sous-page
    html.Div(id='apc-hub-content', style={'minHeight': '80vh'}),
])


# ── Callbacks ─────────────────────────────────────────────────────────────────
def register_apc_hub_callbacks(app):
    reg_kpi(app)
    register_ens_data_loader(app)
    # 1) Enregistrer les callbacks de toutes les sous-pages, une seule fois
    for key, page in SUBPAGES.items():
        if page['register']:
            page['register'](app)

    # 2) Callback unique : lit l'URL, met à jour la navbar ET le contenu
    @app.callback(
        Output('apc-hub-navbar', 'children'),
        Output('apc-hub-content', 'children'),
        Input('url', 'pathname'),
        Input('url', 'search'),  # pour conserver ?jwt_token=... dans les liens
    )
    def render_apc_hub(pathname, search):
        if not pathname:
            return no_update, no_update

        parts = pathname.strip('/').split('/')
        # On attend au moins ['<role>', 'apc20_hub']
        if len(parts) < 2 or parts[1] != 'apc20_hub':
            return no_update, no_update

        role = parts[0]
        # parts[2] = sous-page choisie, sinon défaut
        allowed_pages = ROLE_SUBPAGES.get(role, [])

        if not allowed_pages:
            return [], html.Div("Aucune page APC disponible pour ce rôle.")

        default_subpage = DEFAULT_SUBPAGE_BY_ROLE.get(role, allowed_pages[0])

        requested_subpage = parts[2] if len(parts) >= 3 else default_subpage

        if requested_subpage in allowed_pages:
            subpage_key = requested_subpage
        else:
            subpage_key = default_subpage

        # Construire la navbar avec dcc.Link (pas de rechargement de page)
        # On préserve la query string (?jwt_token=...) pour garder l'auth
        query = search or ''
        navbar_children = [
            dcc.Link(
            children=[
            html.I(className=page['icon'], style={'marginRight': '8px'}),
            page['label'],
            ],
                href=f"/{role}/apc20_hub/{key}{query}",
            style=TAB_ACTIVE if key == subpage_key else TAB_INACTIVE,
        )
    for key, page in SUBPAGES.items()
    if key in allowed_pages
]
        

        # Contenu de la sous-page
        content = SUBPAGES[subpage_key]['layout']

        return navbar_children, content