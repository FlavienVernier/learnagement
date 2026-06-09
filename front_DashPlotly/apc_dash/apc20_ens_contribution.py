"""
Viz 5 : Ma contribution APC personnelle
Question enseignant : "Quelle est ma contribution globale au référentiel APC ?"

L'enseignant sélectionne ses modules et voit :
  - Stat cards : AC couverts, % du référentiel, AC Requis
  - Radar : couverture par compétence (mes modules vs formation entière)
  - Histogramme : AC couverts par chacun de mes modules
  - Liste des AC couverts
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc, html, Input, Output, State
from io import StringIO

from .apc20_layout import COLORS, KNOWN_COMPETENCES, get_competence_color, empty_fig


_LIEN_COLORS = {
    "Requis":         "#EF4444",
    "Recommandé":     "#F59E0B",
    "Complémentaire": "#10B981",
}


# ─── Layout ───────────────────────────────────────────────────────

contribution_content = html.Div(
    [
        # Sélection des modules
        html.Div(
            [
                html.Label(
                    "Mes modules",
                    style={"fontWeight": "600", "marginBottom": "6px", "display": "block"},
                ),
                html.P(
                    "Sélectionnez les modules dont vous êtes responsable pour visualiser votre contribution APC.",
                    style={"margin": "0 0 10px 0", "color": "#6B7280", "fontSize": "13px"},
                ),
                dcc.Dropdown(
                    id="contribution-modules-select",
                    options=[],
                    value=[],
                    multi=True,
                    placeholder="Sélectionner vos modules...",
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Stat cards
        html.Div(
            id="contribution-stats-row",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                "gap": "12px",
                "marginBottom": "20px",
            },
        ),

        # Radar + Histogramme
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="contribution-radar",
                        figure=empty_fig("Sélectionnez vos modules"),
                        config={"displayModeBar": False},
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                        "padding": "12px",
                        "flex": "0 0 400px",
                    },
                ),
                html.Div(
                    dcc.Graph(
                        id="contribution-bar",
                        figure=empty_fig("Sélectionnez vos modules"),
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
            id="contribution-ac-list",
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
        Output("contribution-modules-select", "options"),
        Input("apc-ens-raw-store", "data"),
        prevent_initial_call=False,
    )
    def populate_contribution_options(raw_data):
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
        Output("contribution-stats-row", "children"),
        Output("contribution-radar",     "figure"),
        Output("contribution-bar",       "figure"),
        Output("contribution-ac-list",   "children"),
        Input("contribution-modules-select", "value"),
        State("apc-ens-raw-store",           "data"),
        prevent_initial_call=False,
    )
    def update_contribution(selected_strs, raw_data):
        _empty = empty_fig("Sélectionnez vos modules")
        _hint  = html.P("Sélectionnez vos modules pour voir votre contribution.", style={"color": "#6B7280"})

        if not selected_strs or raw_data is None:
            return [], _empty, _empty, _hint

        df_main = pd.read_json(StringIO(raw_data["df_main"]), orient="split")

        try:
            selected_ids = [float(s) for s in selected_strs]
        except (ValueError, TypeError):
            return [], _empty, _empty, html.P("Erreur de sélection.")

        df_mine = df_main[df_main["id_module"].isin(selected_ids)].copy()
        if df_mine.empty:
            return [], empty_fig("Aucun AC pour les modules sélectionnés"), _empty, html.P("Aucun AC trouvé.")

        nb_ac_mine  = df_mine["id_apprentissage_critique"].nunique()
        nb_ac_total = df_main["id_apprentissage_critique"].nunique()
        pct         = round(nb_ac_mine / nb_ac_total * 100) if nb_ac_total else 0
        nb_requis   = df_mine[df_mine["type_lien"] == "Requis"]["id_apprentissage_critique"].nunique()

        def _stat(title, value, subtitle, color):
            return html.Div(
                [
                    html.Div(title,    style={"fontSize": "12px", "color": "#6B7280", "marginBottom": "4px"}),
                    html.Div(str(value), style={"fontSize": "24px", "fontWeight": "700", "color": color}),
                    html.Div(subtitle, style={"fontSize": "11px", "color": "#9CA3AF", "marginTop": "2px"}),
                ],
                style={
                    "backgroundColor": "white", "padding": "14px", "borderRadius": "8px",
                    "boxShadow": "0 1px 3px rgba(0,0,0,0.08)", "borderLeft": f"3px solid {color}",
                },
            )

        stats = [
            _stat("AC couverts",           nb_ac_mine,        f"{pct}% du référentiel", COLORS["primary"]),
            _stat("AC avec lien Requis",   nb_requis,         "sur vos modules",         COLORS["danger"]),
            _stat("Modules sélectionnés",  len(selected_ids), "modules",                 COLORS["success"]),
        ]

        # ── Radar : mes modules vs formation entière ──────────────
        comp_mine = (
            df_mine.groupby("competence_label")["id_apprentissage_critique"]
            .nunique()
            .reindex(KNOWN_COMPETENCES, fill_value=0)
        )
        comp_all = (
            df_main.groupby("competence_label")["id_apprentissage_critique"]
            .nunique()
            .reindex(KNOWN_COMPETENCES, fill_value=0)
        )
        cats = KNOWN_COMPETENCES + [KNOWN_COMPETENCES[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=comp_all.tolist() + [comp_all.iloc[0]],
            theta=cats,
            fill="toself",
            name="Formation entière",
            line=dict(color="#D1D5DB", width=2),
            fillcolor="rgba(209,213,219,0.15)",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=comp_mine.tolist() + [comp_mine.iloc[0]],
            theta=cats,
            fill="toself",
            name="Mes modules",
            line=dict(color=COLORS["primary"], width=2),
            fillcolor="rgba(59,130,246,0.15)",
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, tickfont=dict(size=9))),
            showlegend=True,
            legend=dict(font=dict(size=11)),
            title=dict(text="Couverture par compétence", x=0.5, xanchor="center", font=dict(size=13)),
            height=380,
            paper_bgcolor="white",
            margin=dict(l=30, r=30, t=60, b=20),
            font=dict(family="Inter, sans-serif"),
        )

        # ── Histogramme AC par module ──────────────────────────────
        module_names = raw_data.get("module_names", {})
        df_bar = (
            df_mine.groupby("id_module")["id_apprentissage_critique"]
            .nunique()
            .reset_index(name="nb_ac")
        )
        df_bar["module_name"] = df_bar["id_module"].apply(
            lambda m: str(module_names.get(str(int(m)), module_names.get(str(m), f"M{m}")))[:40]
        )
        df_bar = df_bar.sort_values("nb_ac", ascending=True)

        fig_bar = px.bar(
            df_bar, x="nb_ac", y="module_name",
            orientation="h", text="nb_ac",
            title="AC couverts par module",
        )
        fig_bar.update_traces(
            marker_color=COLORS["primary"],
            textposition="outside", cliponaxis=False,
        )
        fig_bar.update_layout(
            height=max(220, len(df_bar) * 38 + 80),
            paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(l=20, r=40, t=50, b=20),
            xaxis_title="Nombre d'AC", yaxis_title="",
            font=dict(family="Inter, sans-serif"),
        )

        # ── Liste des AC couverts ──────────────────────────────────
        ac_data = (
            df_mine[["libelle_apprentissage", "competence_label", "niveau", "type_lien"]]
            .drop_duplicates("libelle_apprentissage")
            .sort_values(["competence_label", "niveau", "libelle_apprentissage"])
        )

        rows = []
        for _, row in ac_data.iterrows():
            lc = _LIEN_COLORS.get(row.get("type_lien", ""), "#9CA3AF")
            cc = get_competence_color(str(row["competence_label"]))
            rows.append(
                html.Div(
                    [
                        html.Span(
                            str(row["competence_label"]),
                            style={
                                "fontSize": "11px", "fontWeight": "600",
                                "color": cc, "backgroundColor": cc + "20",
                                "borderRadius": "4px", "padding": "2px 7px", "marginRight": "6px",
                            },
                        ),
                        html.Span(
                            f"N{int(row['niveau'])}",
                            style={
                                "fontSize": "11px", "color": "#6B7280",
                                "backgroundColor": "#F3F4F6",
                                "borderRadius": "4px", "padding": "2px 6px", "marginRight": "8px",
                            },
                        ),
                        html.Span(str(row["libelle_apprentissage"]), style={"fontSize": "13px", "flex": "1"}),
                        html.Span(
                            str(row.get("type_lien", "")),
                            style={
                                "fontSize": "11px", "fontWeight": "600",
                                "color": lc, "backgroundColor": lc + "20",
                                "borderRadius": "4px", "padding": "2px 7px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex", "alignItems": "center", "flexWrap": "wrap",
                        "padding": "7px 10px", "borderRadius": "6px",
                        "backgroundColor": "#F9FAFB", "marginBottom": "4px",
                    },
                )
            )

        ac_list = html.Div([
            html.H4(
                f"Apprentissages critiques couverts ({len(rows)} AC)",
                style={"margin": "0 0 12px 0", "fontSize": "15px"},
            ),
            html.Div(rows, style={"maxHeight": "420px", "overflowY": "auto"}),
        ])

        return stats, fig_radar, fig_bar, ac_list
