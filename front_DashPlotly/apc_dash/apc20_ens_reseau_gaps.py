"""
Viz 3 : Réseau de modules (liés par AC partagés)
Viz 4 : Analyse des trous APC (AC sans Requis, modules sans Requis)

Questions enseignant :
  - "Quels modules travaillent les mêmes compétences que le mien ?"
  - "Y a-t-il des AC ou des modules sans ancrage APC fort ?"
"""
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from dash import dcc, html, Input, Output
from io import StringIO

from .apc20_layout import COLORS, KNOWN_COMPETENCES, get_competence_color, empty_fig


# ─── Layout ───────────────────────────────────────────────────────

reseau_gaps_content = html.Div(
    [
        # ── Section Réseau ────────────────────────────────────────
        html.Div(
            [
                html.H3(
                    "Réseau de modules",
                    style={"margin": "0 0 4px 0", "fontSize": "16px", "fontWeight": "700"},
                ),
                html.P(
                    "Deux modules sont reliés s'ils partagent au moins un apprentissage critique. "
                    "La taille du nœud reflète le nombre d'AC couverts, "
                    "la couleur indique la compétence dominante.",
                    style={"margin": "0 0 14px 0", "color": "#6B7280", "fontSize": "13px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Filtrer par compétence",
                            style={"fontWeight": "500", "fontSize": "13px", "marginBottom": "6px", "display": "block"},
                        ),
                        dcc.Dropdown(
                            id="reseau-comp-filter",
                            options=[{"label": c, "value": c} for c in KNOWN_COMPETENCES],
                            value=KNOWN_COMPETENCES,
                            multi=True,
                            placeholder="Toutes les compétences",
                            style={"maxWidth": "520px"},
                        ),
                    ],
                    style={"marginBottom": "14px"},
                ),
                html.Div(
                    dcc.Graph(
                        id="reseau-graph",
                        figure=empty_fig(),
                        config={"displayModeBar": True, "displaylogo": False},
                        style={"height": "560px"},
                    ),
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                        "padding": "12px",
                    },
                ),
            ],
            style={"marginBottom": "28px"},
        ),

        # ── Section Gaps ──────────────────────────────────────────
        html.Div(
            [
                html.H3(
                    "Analyse des trous APC",
                    style={"margin": "0 0 4px 0", "fontSize": "16px", "fontWeight": "700"},
                ),
                html.P(
                    "Les AC sans module 'Requis' risquent de ne pas être réellement maîtrisés. "
                    "Les modules sans AC 'Requis' ont un ancrage APC faible.",
                    style={"margin": "0 0 14px 0", "color": "#6B7280", "fontSize": "13px"},
                ),
                html.Div(
                    [
                        html.Div(id="gaps-ac-orphans",     style={"flex": "1"}),
                        html.Div(id="gaps-module-orphans", style={"flex": "1"}),
                    ],
                    style={"display": "flex", "gap": "16px"},
                ),
            ],
        ),
    ],
    style={"padding": "20px"},
)


# ─── Callbacks ────────────────────────────────────────────────────

def register_callbacks(app):

    # ── Viz 3 : Réseau de modules ─────────────────────────────────
    @app.callback(
        Output("reseau-graph", "figure"),
        Input("reseau-comp-filter", "value"),
        Input("apc-ens-raw-store",  "data"),
        prevent_initial_call=False,
    )
    def update_reseau(competences, raw_data):
        if not competences or raw_data is None:
            return empty_fig("Données non disponibles")

        df_main      = pd.read_json(StringIO(raw_data["df_main"]), orient="split")
        module_names = raw_data.get("module_names", {})

        df_f = df_main[df_main["competence_label"].isin(competences)].copy()
        df_f = df_f[df_f["id_module"] != 0]

        if df_f.empty:
            return empty_fig("Aucun module pour les compétences sélectionnées")

        mod_acs = (
            df_f.groupby("id_module")["id_apprentissage_critique"]
            .apply(set)
            .to_dict()
        )

        mod_dom_comp = (
            df_f.groupby(["id_module", "competence_label"])["id_apprentissage_critique"]
            .nunique()
            .reset_index(name="n")
            .sort_values("n", ascending=False)
            .drop_duplicates("id_module")
            .set_index("id_module")["competence_label"]
            .to_dict()
        )

        G = nx.Graph()
        modules = list(mod_acs.keys())
        for mod in modules:
            G.add_node(mod, n_ac=len(mod_acs[mod]))

        for i in range(len(modules)):
            for j in range(i + 1, len(modules)):
                shared = mod_acs[modules[i]] & mod_acs[modules[j]]
                if shared:
                    G.add_edge(modules[i], modules[j], weight=len(shared))

        if not G.nodes():
            return empty_fig("Aucun module à afficher")

        pos = nx.spring_layout(G, seed=42, k=3.0)

        edge_x, edge_y = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines",
            line=dict(width=0.8, color="#D1D5DB"),
            hoverinfo="none",
        )

        node_traces = []
        for comp in competences:
            comp_mods = [m for m in G.nodes() if mod_dom_comp.get(m) == comp]
            if not comp_mods:
                continue
            nx_ = [pos[m][0] for m in comp_mods]
            ny_ = [pos[m][1] for m in comp_mods]
            sizes = [max(14, min(45, G.nodes[m]["n_ac"] * 3)) for m in comp_mods]

            def _mod_label(m):
                raw = module_names.get(str(int(m)), module_names.get(str(m), f"M{m}"))
                return str(raw)[:28]

            labels      = [_mod_label(m) for m in comp_mods]
            hover_texts = [
                f"<b>{_mod_label(m)}</b><br>"
                f"AC couverts : {G.nodes[m]['n_ac']}<br>"
                f"Compétence dominante : {comp}<br>"
                f"Connexions : {G.degree(m)}"
                for m in comp_mods
            ]

            node_traces.append(go.Scatter(
                x=nx_, y=ny_,
                mode="markers+text",
                marker=dict(
                    size=sizes,
                    color=get_competence_color(comp),
                    opacity=0.85,
                    line=dict(width=1.5, color="white"),
                ),
                text=labels,
                textposition="top center",
                textfont=dict(size=9, color="#374151"),
                name=comp,
                hovertext=hover_texts,
                hoverinfo="text",
            ))

        fig = go.Figure(data=[edge_trace] + node_traces)
        fig.update_layout(
            title=dict(
                text="Réseau de modules — liens par apprentissages critiques partagés",
                x=0.5, xanchor="center",
                font=dict(size=15, family="Inter, sans-serif"),
            ),
            showlegend=True,
            legend=dict(title="Compétence dominante", font=dict(size=11)),
            height=560,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=70, b=20),
            font=dict(family="Inter, sans-serif"),
            hovermode="closest",
        )
        return fig

    # ── Viz 4 : Analyse des trous ─────────────────────────────────
    @app.callback(
        Output("gaps-ac-orphans",     "children"),
        Output("gaps-module-orphans", "children"),
        Input("apc-ens-raw-store",    "data"),
        prevent_initial_call=False,
    )
    def update_gaps(raw_data):
        _na = html.P("Données non disponibles", style={"color": "#6B7280"})
        if raw_data is None:
            return _na, _na

        df_main      = pd.read_json(StringIO(raw_data["df_main"]), orient="split")
        module_names = raw_data.get("module_names", {})

        def _badge(text, color):
            return html.Span(text, style={
                "fontSize": "11px", "fontWeight": "600",
                "color": color, "backgroundColor": color + "22",
                "borderRadius": "4px", "padding": "2px 7px", "marginRight": "6px",
            })

        # ── AC sans aucun module "Requis" ──────────────────────────
        ac_with_requis = set(
            df_main[df_main["type_lien"] == "Requis"]["id_apprentissage_critique"].unique()
        )
        all_acs    = df_main[["id_apprentissage_critique", "libelle_apprentissage", "competence_label", "niveau"]].drop_duplicates("id_apprentissage_critique")
        ac_orphans = all_acs[~all_acs["id_apprentissage_critique"].isin(ac_with_requis)]

        ac_rows = []
        for _, row in ac_orphans.sort_values(["competence_label", "niveau", "libelle_apprentissage"]).iterrows():
            ac_rows.append(
                html.Div(
                    [
                        _badge(str(row["competence_label"]), get_competence_color(str(row["competence_label"]))),
                        _badge(f"N{int(row['niveau'])}", "#6B7280"),
                        html.Span(str(row["libelle_apprentissage"]), style={"fontSize": "13px"}),
                    ],
                    style={
                        "display": "flex", "alignItems": "center", "flexWrap": "wrap",
                        "padding": "7px 10px", "borderRadius": "6px",
                        "backgroundColor": "#FEF2F2", "marginBottom": "4px",
                        "borderLeft": "3px solid #EF4444",
                    },
                )
            )

        ac_panel = html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "AC sans module 'Requis'",
                            style={"margin": "0", "fontSize": "14px", "fontWeight": "700"},
                        ),
                        html.Span(
                            f"{len(ac_orphans)} / {len(all_acs)} AC",
                            style={"fontSize": "12px", "color": "#EF4444", "fontWeight": "600"},
                        ),
                    ],
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "12px"},
                ),
                html.Div(
                    ac_rows or [html.P("Aucun trou détecté.", style={"color": "#10B981", "fontSize": "13px"})],
                    style={"maxHeight": "360px", "overflowY": "auto"},
                ),
            ],
            style={
                "backgroundColor": "white", "borderRadius": "10px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)", "padding": "16px",
            },
        )

        # ── Modules sans aucun AC "Requis" ─────────────────────────
        mod_with_requis = set(
            df_main[df_main["type_lien"] == "Requis"]["id_module"].unique()
        )
        all_modules = df_main[df_main["id_module"] != 0]["id_module"].unique()
        mod_orphans = [m for m in all_modules if m not in mod_with_requis]

        mod_rows = []
        for m in sorted(mod_orphans):
            name = module_names.get(str(int(m)), module_names.get(str(m), f"Module {m}"))
            mod_rows.append(
                html.Div(
                    html.Span(str(name), style={"fontSize": "13px"}),
                    style={
                        "padding": "7px 10px", "borderRadius": "6px",
                        "backgroundColor": "#FFFBEB", "marginBottom": "4px",
                        "borderLeft": "3px solid #F59E0B",
                    },
                )
            )

        mod_panel = html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Modules sans AC 'Requis'",
                            style={"margin": "0", "fontSize": "14px", "fontWeight": "700"},
                        ),
                        html.Span(
                            f"{len(mod_orphans)} / {len(all_modules)} modules",
                            style={"fontSize": "12px", "color": "#F59E0B", "fontWeight": "600"},
                        ),
                    ],
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "12px"},
                ),
                html.Div(
                    mod_rows or [html.P("Tous les modules ont au moins un AC Requis.", style={"color": "#10B981", "fontSize": "13px"})],
                    style={"maxHeight": "360px", "overflowY": "auto"},
                ),
            ],
            style={
                "backgroundColor": "white", "borderRadius": "10px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)", "padding": "16px",
            },
        )

        return ac_panel, mod_panel
