"""
Viz 1 : Fiche APC d'un module
Question enseignant : "Quels AC est-ce que je couvre, avec quel engagement ?"

Affiche pour un module sélectionné :
  - Cartes info (ECTS, semestre, heures, nombre d'AC)
  - Donut : répartition Requis / Recommandé / Complémentaire
  - Histogramme : AC par compétence
  - Liste détaillée des AC groupés par compétence et niveau
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc, html, Input, Output, State
from io import StringIO

from .apc20_layout import COLORS, get_competence_color, empty_fig


# ─── Constantes locales ───────────────────────────────────────────

_LIEN_COLORS = {
    "Requis":         "#EF4444",
    "Recommandé":     "#F59E0B",
    "Complémentaire": "#10B981",
}


# ─── Layout ───────────────────────────────────────────────────────

fiche_module_content = html.Div(
    [
        # Sélection du module
        html.Div(
            [
                html.Label(
                    "Module",
                    style={"fontWeight": "600", "marginBottom": "8px", "display": "block"},
                ),
                dcc.Dropdown(
                    id="fiche-module-select",
                    options=[],
                    value=None,
                    placeholder="Choisir un module...",
                    clearable=True,
                    style={"maxWidth": "560px"},
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Cartes info (remplies par callback)
        html.Div(
            id="fiche-info-cards",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(150px, 1fr))",
                "gap": "12px",
                "marginBottom": "20px",
            },
        ),

        # Donut + Histogramme
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="fiche-donut-chart",
                        figure=empty_fig(),
                        config={"displayModeBar": False},
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                        "padding": "12px",
                        "flex": "0 0 320px",
                    },
                ),
                html.Div(
                    dcc.Graph(
                        id="fiche-bar-chart",
                        figure=empty_fig(),
                        config={"displayModeBar": False},
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                        "padding": "12px",
                        "flex": "1",
                    },
                ),
            ],
            style={"display": "flex", "gap": "16px", "marginBottom": "20px"},
        ),

        # Liste des AC
        html.Div(
            id="fiche-ac-list",
            style={
                "backgroundColor": "white",
                "borderRadius": "10px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                "padding": "20px",
            },
        ),
    ],
    style={"padding": "20px"},
)


# ─── Callbacks ────────────────────────────────────────────────────

def register_callbacks(app):

    @app.callback(
        Output("fiche-module-select", "options"),
        Input("apc-ens-raw-store", "data"),
        prevent_initial_call=False,
    )
    def populate_module_options(raw_data):
        if raw_data is None:
            return []
        module_names = raw_data.get("module_names", {})
        opts = []
        for k, v in module_names.items():
            try:
                if float(k) == 0:
                    continue
            except (ValueError, TypeError):
                continue
            opts.append({"label": v, "value": k})
        return sorted(opts, key=lambda x: x["label"])

    @app.callback(
        Output("fiche-info-cards",  "children"),
        Output("fiche-donut-chart", "figure"),
        Output("fiche-bar-chart",   "figure"),
        Output("fiche-ac-list",     "children"),
        Input("fiche-module-select", "value"),
        State("apc-ens-raw-store",   "data"),
        prevent_initial_call=False,
    )
    def update_fiche(module_id_str, raw_data):
        _empty = empty_fig("Sélectionnez un module")
        _placeholder = html.P(
            "Sélectionnez un module pour afficher ses apprentissages critiques.",
            style={"color": "#6B7280"},
        )

        if not module_id_str or raw_data is None:
            return [], _empty, _empty, _placeholder

        df_main    = pd.read_json(StringIO(raw_data["df_main"]),    orient="split")
        df_modules = pd.read_json(StringIO(raw_data["df_modules"]), orient="split")

        try:
            module_id = float(module_id_str)
        except (ValueError, TypeError):
            return [], empty_fig("Module introuvable"), _empty, html.P("Module introuvable.")

        df_mod = df_main[df_main["id_module"] == module_id].copy()
        if df_mod.empty:
            return [], empty_fig("Aucun AC pour ce module"), _empty, html.P("Aucun apprentissage critique associé.")

        # ── Cartes info ────────────────────────────────────────────
        mod_row = df_modules[df_modules["id_module"] == module_id]
        if not mod_row.empty:
            r       = mod_row.iloc[0]
            ects    = r.get("ECTS", "—")
            sem     = r.get("id_semestre", "—")
            hcm     = float(r.get("hCM", 0) or 0)
            htd     = float(r.get("hTD", 0) or 0)
            htp     = float(r.get("hTP", 0) or 0)
            total_h = hcm + htd + htp
        else:
            ects, sem, total_h = "—", "—", "—"

        def _info_card(label, value, color):
            return html.Div(
                [
                    html.Div(label, style={"fontSize": "11px", "color": "#6B7280", "marginBottom": "4px"}),
                    html.Div(str(value), style={"fontSize": "22px", "fontWeight": "700", "color": color}),
                ],
                style={
                    "backgroundColor": "white",
                    "padding": "14px",
                    "borderRadius": "8px",
                    "boxShadow": "0 1px 3px rgba(0,0,0,0.08)",
                    "borderLeft": f"3px solid {color}",
                    "textAlign": "center",
                },
            )

        cards = [
            _info_card("ECTS",        ects,                                                  COLORS["primary"]),
            _info_card("Semestre",    f"S{sem}",                                             COLORS["success"]),
            _info_card("Heures",      f"{total_h:.0f}h" if total_h != "—" else "—",         COLORS["warning"]),
            _info_card("AC couverts", df_mod["id_apprentissage_critique"].nunique(),          COLORS["danger"]),
        ]

        # ── Donut type de lien ──────────────────────────────────────
        lien_counts  = df_mod["type_lien"].value_counts()
        donut_colors = [_LIEN_COLORS.get(l, "#999") for l in lien_counts.index]
        fig_donut = go.Figure(data=[go.Pie(
            labels=lien_counts.index.tolist(),
            values=lien_counts.values.tolist(),
            hole=0.55,
            marker_colors=donut_colors,
            textinfo="label+percent",
            insidetextorientation="radial",
        )])
        fig_donut.update_layout(
            title=dict(text="Répartition des types de lien", x=0.5, xanchor="center", font=dict(size=13)),
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="white",
            showlegend=False,
            font=dict(family="Inter, sans-serif"),
        )

        # ── Histogramme AC par compétence ──────────────────────────
        df_bar = (
            df_mod.groupby("competence_label")["id_apprentissage_critique"]
            .nunique()
            .reset_index(name="nb_ac")
        )
        fig_bar = px.bar(
            df_bar, x="competence_label", y="nb_ac", text="nb_ac",
            color="competence_label",
            color_discrete_map={c: get_competence_color(c) for c in df_bar["competence_label"]},
            title="AC couverts par compétence",
        )
        fig_bar.update_traces(textposition="outside", cliponaxis=False)
        fig_bar.update_layout(
            showlegend=False, height=300,
            paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="", yaxis_title="Nombre d'AC",
            font=dict(family="Inter, sans-serif"),
        )

        # ── Liste des AC groupés par compétence ────────────────────
        sections = []
        for comp in sorted(df_mod["competence_label"].dropna().unique()):
            df_c       = df_mod[df_mod["competence_label"] == comp].drop_duplicates("id_apprentissage_critique")
            comp_color = get_competence_color(comp)

            rows = []
            for _, row in df_c.sort_values(["niveau", "libelle_apprentissage"]).iterrows():
                lien = row.get("type_lien", "")
                lc   = _LIEN_COLORS.get(lien, "#9CA3AF")
                rows.append(
                    html.Div(
                        [
                            html.Span(
                                f"N{int(row['niveau'])}",
                                style={
                                    "fontSize": "11px", "fontWeight": "600",
                                    "backgroundColor": "#E5E7EB", "borderRadius": "4px",
                                    "padding": "2px 6px", "marginRight": "8px", "flexShrink": "0",
                                },
                            ),
                            html.Span(
                                row["libelle_apprentissage"],
                                style={"flex": "1", "fontSize": "13px"},
                            ),
                            html.Span(
                                lien,
                                style={
                                    "fontSize": "11px", "fontWeight": "600",
                                    "color": lc, "backgroundColor": lc + "20",
                                    "borderRadius": "4px", "padding": "2px 8px",
                                    "flexShrink": "0",
                                },
                            ),
                        ],
                        style={
                            "display": "flex", "alignItems": "center", "gap": "8px",
                            "padding": "8px 10px", "borderRadius": "6px",
                            "backgroundColor": "#F9FAFB", "marginBottom": "4px",
                        },
                    )
                )

            sections.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(style={
                                    "width": "12px", "height": "12px",
                                    "borderRadius": "3px", "backgroundColor": comp_color,
                                    "marginRight": "8px",
                                }),
                                html.Span(comp, style={"fontWeight": "700", "fontSize": "14px"}),
                                html.Span(
                                    f"  {len(rows)} AC",
                                    style={"fontSize": "12px", "color": "#6B7280", "marginLeft": "8px"},
                                ),
                            ],
                            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
                        ),
                        html.Div(rows),
                    ],
                    style={"marginBottom": "16px"},
                )
            )

        ac_list = html.Div([
            html.H4("Apprentissages critiques couverts", style={"margin": "0 0 16px 0", "fontSize": "15px"}),
            html.Div(sections),
        ])

        return cards, fig_donut, fig_bar, ac_list
