"""
Dashboard APC Enseignant — point d'entrée principal.

Architecture :
  - Chargement unique des données dans apc-ens-raw-store (partagé par tous les panneaux)
  - Navbar latérale pour naviguer entre les 4 thèmes de visualisation
  - Tous les panneaux sont dans le DOM ; seul le panneau actif est visible

Visualisations disponibles :
  1. Fiche Module       — AC couverts, types de lien, ECTS, heures
  2. Couverture APC     — heatmap AC × semestre par compétence
  3. Réseau & Trous     — graphe de voisinage + analyse des gaps
  4. Ma Contribution    — vue personnalisée (sélection de modules)
"""
import logging
import pandas as pd
import dash
from dash import dcc, html, Input, Output

from .apc20_layout import COLORS
from .apc20_heatmap_apc_tools import (
    get_apc_competences,
    get_apc_niveaux,
    get_apc_apprentissages,
    get_apc_ac_modules,
    get_apc_modules,
    get_apc_composantes,
)
from .apc20_ens_fiche_module import fiche_module_content,  register_callbacks as _reg_fiche
from .apc20_ens_couverture   import couverture_content,    register_callbacks as _reg_couverture
from .apc20_ens_reseau_gaps  import reseau_gaps_content,   register_callbacks as _reg_reseau_gaps
from .apc20_ens_contribution import contribution_content,  register_callbacks as _reg_contribution
from .apc20_chatbot          import chatbot_layout,        register_callbacks as _reg_chatbot


# ─── Configuration de la navigation ───────────────────────────────

VIEWS = ["fiche", "couverture", "reseau", "contribution"]

_NAV_ITEMS = [
    {
        "key":      "fiche",
        "label":    "Fiche Module",
        "sublabel": "AC couverts et types de lien",
        "icon":     "fa-solid fa-file-lines",
    },
    {
        "key":      "couverture",
        "label":    "Couverture APC",
        "sublabel": "Carte AC par semestre",
        "icon":     "fa-solid fa-table-cells",
    },
    {
        "key":      "reseau",
        "label":    "Réseau et Trous",
        "sublabel": "Voisinage et gaps du référentiel",
        "icon":     "fa-solid fa-diagram-project",
    },
    {
        "key":      "contribution",
        "label":    "Ma Contribution",
        "sublabel": "Vue personnalisée par modules",
        "icon":     "fa-solid fa-person-chalkboard",
    },
]

_NAV_BASE = {
    "display": "flex",
    "alignItems": "flex-start",
    "padding": "10px 12px",
    "cursor": "pointer",
    "borderRadius": "8px",
    "border": "none",
    "width": "100%",
    "textAlign": "left",
    "marginBottom": "4px",
    "background": "transparent",
    "transition": "background 0.15s",
}
_NAV_INACTIVE = {**_NAV_BASE, "backgroundColor": "transparent", "color": "#374151"}
_NAV_ACTIVE   = {**_NAV_BASE, "backgroundColor": "#EFF6FF",     "color": COLORS["primary"]}


def _nav_btn(item):
    return html.Button(
        [
            html.I(
                className=item["icon"],
                style={"marginRight": "10px", "marginTop": "2px", "flexShrink": "0", "width": "16px"},
            ),
            html.Div(
                [
                    html.Div(item["label"],    style={"fontWeight": "600", "fontSize": "13px"}),
                    html.Div(item["sublabel"], style={"fontSize": "11px", "color": "#9CA3AF", "marginTop": "1px"}),
                ]
            ),
        ],
        id=f"apc-ens-nav-{item['key']}",
        n_clicks=0,
        style=_NAV_INACTIVE,
    )


# ─── Layout ───────────────────────────────────────────────────────

apc_ens_dashboard_layout = html.Div(
    [
        dcc.Store(id="apc-ens-active-nav", data="fiche"),

        # ── En-tête ───────────────────────────────────────────────
        html.Div(
            [
                html.Div(
                    html.I(className="fa-solid fa-graduation-cap", style={"fontSize": "22px", "color": COLORS["primary"]}),
                    style={"marginRight": "14px", "display": "flex", "alignItems": "center"},
                ),
                html.Div(
                    [
                        html.H1(
                            "Dashboard APC Enseignant",
                            style={"margin": "0", "fontSize": "20px", "fontWeight": "700"},
                        ),
                        html.P(
                            "Explorez l'Approche Par Compétences pour vos modules et le référentiel de formation",
                            style={"margin": "2px 0 0 0", "color": "#6B7280", "fontSize": "13px"},
                        ),
                    ]
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "backgroundColor": "white",
                "padding": "14px 24px",
                "borderBottom": "1px solid #E5E7EB",
                "position": "sticky",
                "top": "0",
                "zIndex": "999",
            },
        ),

        # ── Corps : navbar + contenu ───────────────────────────────
        html.Div(
            [
                # ── Navbar latérale ──────────────────────────────
                html.Div(
                    [
                        html.Div(
                            "VISUALISATIONS",
                            style={
                                "fontSize": "10px",
                                "fontWeight": "700",
                                "color": "#9CA3AF",
                                "letterSpacing": "0.08em",
                                "marginBottom": "10px",
                                "padding": "0 4px",
                            },
                        ),
                        *[_nav_btn(item) for item in _NAV_ITEMS],
                    ],
                    style={
                        "width": "220px",
                        "flexShrink": "0",
                        "padding": "16px 10px",
                        "backgroundColor": "white",
                        "borderRight": "1px solid #E5E7EB",
                        "minHeight": "calc(100vh - 62px)",
                    },
                ),

                # ── Panneaux de contenu (tous dans le DOM) ────────
                html.Div(
                    [
                        html.Div(fiche_module_content, id="apc-ens-panel-fiche"),
                        html.Div(couverture_content,   id="apc-ens-panel-couverture",   style={"display": "none"}),
                        html.Div(reseau_gaps_content,  id="apc-ens-panel-reseau",       style={"display": "none"}),
                        html.Div(contribution_content, id="apc-ens-panel-contribution", style={"display": "none"}),
                    ],
                    style={"flex": "1", "overflow": "auto", "minHeight": "calc(100vh - 62px)"},
                ),
            ],
            style={"display": "flex"},
        ),
    ],
    style={"fontFamily": "Inter, sans-serif", "backgroundColor": "#F9FAFB"},
)

# Ajout du chatbot dans le layout du dashboard enseignant
apc_ens_dashboard_layout = html.Div([apc_ens_dashboard_layout, chatbot_layout])


# ─── Callbacks ────────────────────────────────────────────────────

def register_callbacks(app):

    # ── Chargement des données (store partagé) ────────────────────
    @app.callback(
        Output("apc-ens-raw-store", "data"),
        Input("token", "data"),
        prevent_initial_call=False,
    )
    def load_ens_data(token):
        if not token or token == "none":
            logging.info("[apc20_ens_dashboard] token absent, chargement ignoré")
            return None
        try:
            logging.info("[apc20_ens_dashboard] début chargement données")

            df_competences    = get_apc_competences(token)
            df_niveaux        = get_apc_niveaux(token)
            df_apprentissages = get_apc_apprentissages(token)
            df_ac_modules_raw = get_apc_ac_modules(token)
            df_modules        = get_apc_modules(token)
            df_composantes    = get_apc_composantes(token)

            logging.info(f"[apc20_ens_dashboard] données reçues — modules:{len(df_modules)}, ac:{len(df_apprentissages)}, ac_modules:{len(df_ac_modules_raw)}")

            df_base = (
                df_apprentissages
                .merge(df_niveaux,     on="id_niveau",     how="left")
                .merge(df_competences, on="id_competence", how="left")
            )

            # Merge avec df_modules uniquement si elle contient des données
            if not df_modules.empty and "id_module" in df_modules.columns:
                df_ac_mod_full = df_ac_modules_raw.merge(df_modules, on="id_module", how="left")
            else:
                logging.warning("[apc20_ens_dashboard] df_modules vide — données modules non disponibles (MAQUETTE_module vide ?)")
                df_ac_mod_full = df_ac_modules_raw.copy()

            df_main = df_base.merge(df_ac_mod_full, on="id_apprentissage_critique", how="left")
            df_main["competence_label"] = df_main["code_competence"]
            df_main["niveau_code"]      = df_main["competence_label"] + "-N" + df_main["niveau"].astype(str)
            df_main["id_module"]        = pd.to_numeric(df_main["id_module"],   errors="coerce").fillna(0)
            df_main["id_semestre"]      = pd.to_numeric(df_main["id_semestre"], errors="coerce")

            module_names: dict[str, str] = {"0": "Non associé"}
            for _, row in df_modules.iterrows():
                mid  = row["id_module"]
                code = row.get("code_module") if pd.notna(row.get("code_module", float("nan"))) else f"M{mid}"
                nom  = row.get("nom")         if pd.notna(row.get("nom",  float("nan")))         else "Module"
                module_names[str(int(float(mid)))] = f"{code} - {nom}"

            logging.info(f"[apc20_ens_dashboard] store prêt — {len(df_main)} lignes, {len(module_names)} modules")
            return {
                "df_main":        df_main.to_json(date_format="iso", orient="split"),
                "df_modules":     df_modules.to_json(date_format="iso", orient="split"),
                "df_composantes": df_composantes.to_json(date_format="iso", orient="split"),
                "module_names":   module_names,
            }

        except Exception as e:
            logging.exception(f"[apc20_ens_dashboard] ERREUR chargement : {type(e).__name__} — {e}")
            return None

    # ── Navigation : mise à jour de la vue active ─────────────────
    @app.callback(
        Output("apc-ens-active-nav", "data"),
        [Input(f"apc-ens-nav-{v}", "n_clicks") for v in VIEWS],
        prevent_initial_call=True,
    )
    def update_active_nav(*_args):
        ctx = dash.callback_context
        if not ctx.triggered:
            return "fiche"
        return ctx.triggered[0]["prop_id"].split(".")[0].replace("apc-ens-nav-", "")

    # ── Visibilité des panneaux ───────────────────────────────────
    @app.callback(
        [Output(f"apc-ens-panel-{v}", "style") for v in VIEWS],
        Input("apc-ens-active-nav", "data"),
        prevent_initial_call=False,
    )
    def toggle_panels(active):
        return [{"display": "block"} if v == active else {"display": "none"} for v in VIEWS]

    # ── Style actif/inactif des boutons nav ───────────────────────
    @app.callback(
        [Output(f"apc-ens-nav-{v}", "style") for v in VIEWS],
        Input("apc-ens-active-nav", "data"),
        prevent_initial_call=False,
    )
    def style_nav_buttons(active):
        return [_NAV_ACTIVE if v == active else _NAV_INACTIVE for v in VIEWS]

    # ── Enregistrement des sous-callbacks ─────────────────────────
    _reg_fiche(app)
    _reg_couverture(app)
    _reg_reseau_gaps(app)
    _reg_contribution(app)
    _reg_chatbot(app)
