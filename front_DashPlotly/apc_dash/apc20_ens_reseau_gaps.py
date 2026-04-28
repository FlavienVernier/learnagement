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
from dash import dcc, html, Input, Output, callback_context
from io import StringIO

from .apc20_layout import COLORS, KNOWN_COMPETENCES, get_competence_color, empty_fig


# ─── Layout ───────────────────────────────────────────────────────

reseau_gaps_content = html.Div(
    [
        dcc.Store(id="reseau-selected-node", data=None),

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
                    "la couleur indique la compétence dominante. "
                    "Cliquez sur un nœud pour zoomer sur ses connexions.",
                    style={"margin": "0 0 14px 0", "color": "#6B7280", "fontSize": "13px"},
                ),
                html.Div(
                    [
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
                                ),
                            ],
                            style={"flex": "1"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Rechercher un module",
                                    style={"fontWeight": "500", "fontSize": "13px", "marginBottom": "6px", "display": "block"},
                                ),
                                dcc.Dropdown(
                                    id="reseau-search-module",
                                    options=[],
                                    value=None,
                                    searchable=True,
                                    clearable=True,
                                    placeholder="Tapez le nom ou code d'un module...",
                                ),
                            ],
                            style={"flex": "1"},
                        ),
                    ],
                    style={"display": "flex", "gap": "16px", "marginBottom": "14px"},
                ),

                # Graphe + bouton reset superposé
                html.Div(
                    [
                        dcc.Graph(
                            id="reseau-graph",
                            figure=empty_fig(),
                            config={"displayModeBar": True, "displaylogo": False},
                            style={"height": "560px"},
                        ),
                        html.Button(
                            [
                                html.I(className="fa-solid fa-arrow-rotate-left",
                                       style={"marginRight": "6px"}),
                                "Retour vue globale",
                            ],
                            id="reseau-reset-btn",
                            n_clicks=0,
                            style={
                                "display":        "none",
                                "position":       "absolute",
                                "top":            "14px",
                                "left":           "14px",
                                "zIndex":         "10",
                                "backgroundColor": COLORS["primary"],
                                "color":          "white",
                                "border":         "none",
                                "borderRadius":   "6px",
                                "padding":        "7px 13px",
                                "fontSize":       "13px",
                                "fontWeight":     "600",
                                "cursor":         "pointer",
                                "boxShadow":      "0 2px 6px rgba(0,0,0,0.2)",
                                "fontFamily":     "Inter, sans-serif",
                            },
                        ),
                    ],
                    style={
                        "position":        "relative",
                        "backgroundColor": "white",
                        "borderRadius":    "10px",
                        "boxShadow":       "0 1px 4px rgba(0,0,0,0.08)",
                        "padding":         "12px",
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

    # ── Peuplement du dropdown de recherche ──────────────────────
    @app.callback(
        Output("reseau-search-module", "options"),
        Input("apc-ens-raw-store", "data"),
        prevent_initial_call=False,
    )
    def populate_search_options(raw_data):
        if not raw_data:
            return []
        module_names = raw_data.get("module_names", {})
        return [
            {"label": label, "value": mid}
            for mid, label in sorted(module_names.items(), key=lambda x: x[1])
            if mid != "0"
        ]

    # ── Vidage du dropdown sur reset ou changement de filtre ─────
    @app.callback(
        Output("reseau-search-module", "value"),
        Input("reseau-reset-btn",   "n_clicks"),
        Input("reseau-comp-filter", "value"),
        prevent_initial_call=True,
    )
    def clear_search(_reset, _filter):
        return None

    # ── Mise à jour du nœud sélectionné (clic, recherche ou reset) ──
    @app.callback(
        Output("reseau-selected-node", "data"),
        Input("reseau-graph",         "clickData"),
        Input("reseau-reset-btn",     "n_clicks"),
        Input("reseau-comp-filter",   "value"),
        Input("reseau-search-module", "value"),
        prevent_initial_call=True,
    )
    def update_selected_node(click_data, _reset, _filter, search_value):
        ctx = callback_context
        triggered = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

        # Reset ou changement de filtre → on efface la sélection
        if triggered in ("reseau-reset-btn", "reseau-comp-filter"):
            return None

        # Sélection via le dropdown de recherche
        if triggered == "reseau-search-module":
            if search_value is not None:
                try:
                    return float(search_value)
                except (ValueError, TypeError):
                    pass
            return None

        # Clic sur le graphe
        if triggered == "reseau-graph" and click_data and click_data.get("points"):
            pt = click_data["points"][0]
            cd = pt.get("customdata")
            if cd is not None:
                try:
                    return float(cd)
                except (ValueError, TypeError):
                    pass
        return None

    # ── Visibilité du bouton reset ────────────────────────────────
    @app.callback(
        Output("reseau-reset-btn", "style"),
        Input("reseau-selected-node", "data"),
        prevent_initial_call=False,
    )
    def toggle_reset_btn(selected):
        base = {
            "position":        "absolute",
            "top":             "14px",
            "left":            "14px",
            "zIndex":          "10",
            "backgroundColor": COLORS["primary"],
            "color":           "white",
            "border":          "none",
            "borderRadius":    "6px",
            "padding":         "7px 13px",
            "fontSize":        "13px",
            "fontWeight":      "600",
            "cursor":          "pointer",
            "boxShadow":       "0 2px 6px rgba(0,0,0,0.2)",
            "fontFamily":      "Inter, sans-serif",
        }
        base["display"] = "flex" if selected is not None else "none"
        base["alignItems"] = "center"
        return base

    # ── Viz 3 : Réseau de modules ─────────────────────────────────
    @app.callback(
        Output("reseau-graph", "figure"),
        Input("reseau-comp-filter",   "value"),
        Input("apc-ens-raw-store",    "data"),
        Input("reseau-selected-node", "data"),
        prevent_initial_call=False,
    )
    def update_reseau(competences, raw_data, clicked_mod):
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

        def _mod_label(m):
            raw = module_names.get(str(int(m)), module_names.get(str(m), f"M{m}"))
            return str(raw)[:30]

        # Vérifier que le nœud sélectionné existe toujours dans ce graphe
        if clicked_mod is not None and clicked_mod not in G.nodes():
            clicked_mod = None

        neighbors = set(G.neighbors(clicked_mod)) if clicked_mod is not None else set()

        # ── Traces d'arêtes ───────────────────────────────────────
        edge_traces = []
        if clicked_mod is not None:
            dim_x, dim_y, hi_x, hi_y = [], [], [], []
            for u, v in G.edges():
                x0, y0 = pos[u]; x1, y1 = pos[v]
                if u == clicked_mod or v == clicked_mod:
                    hi_x += [x0, x1, None]; hi_y += [y0, y1, None]
                else:
                    dim_x += [x0, x1, None]; dim_y += [y0, y1, None]
            if dim_x:
                edge_traces.append(go.Scatter(
                    x=dim_x, y=dim_y, mode="lines",
                    line=dict(width=0.4, color="#EBEBEB"),
                    hoverinfo="none", showlegend=False,
                ))
            if hi_x:
                edge_traces.append(go.Scatter(
                    x=hi_x, y=hi_y, mode="lines",
                    line=dict(width=2.5, color=COLORS["primary"]),
                    hoverinfo="none", showlegend=False,
                ))
        else:
            ex, ey = [], []
            for u, v in G.edges():
                x0, y0 = pos[u]; x1, y1 = pos[v]
                ex += [x0, x1, None]; ey += [y0, y1, None]
            edge_traces.append(go.Scatter(
                x=ex, y=ey, mode="lines",
                line=dict(width=0.8, color="#D1D5DB"),
                hoverinfo="none", showlegend=False,
            ))

        # ── Traces de nœuds ───────────────────────────────────────
        seen_comps = set()
        node_traces = []

        for comp in competences:
            comp_mods = [m for m in G.nodes() if mod_dom_comp.get(m) == comp]
            for m in comp_mods:
                is_clicked  = clicked_mod is not None and m == clicked_mod
                is_neighbor = m in neighbors
                is_dimmed   = clicked_mod is not None and not is_clicked and not is_neighbor

                base_size = max(14, min(45, G.nodes[m]["n_ac"] * 3))
                size      = base_size + 14 if is_clicked else base_size
                opacity   = 0.15 if is_dimmed else 0.88
                border_w  = 3.5 if is_clicked else (2 if is_neighbor else 1.5)
                border_c  = "#1D4ED8" if is_clicked else ("white" if not is_neighbor else COLORS["primary"])
                txt_color = "#D1D5DB" if is_dimmed else "#374151"
                txt_size  = 11 if is_clicked else 9

                hover = (
                    f"<b>{_mod_label(m)}</b><br>"
                    f"AC couverts : {G.nodes[m]['n_ac']}<br>"
                    f"Compétence dominante : {comp}<br>"
                    f"Connexions : {G.degree(m)}"
                )
                if is_clicked and neighbors:
                    lines = [
                        f"  • {_mod_label(nb)} — {G.edges[m, nb]['weight']} AC partagés"
                        for nb in sorted(neighbors, key=lambda n: -G.edges[m, n]["weight"])
                    ]
                    hover += "<br><br><b>Modules voisins :</b><br>" + "<br>".join(lines)

                first_of_comp = comp not in seen_comps
                if first_of_comp:
                    seen_comps.add(comp)

                node_traces.append(go.Scatter(
                    x=[pos[m][0]], y=[pos[m][1]],
                    mode="markers+text",
                    marker=dict(
                        size=size,
                        color=get_competence_color(comp),
                        opacity=opacity,
                        line=dict(width=border_w, color=border_c),
                    ),
                    text=[_mod_label(m)],
                    textposition="top center",
                    textfont=dict(size=txt_size, color=txt_color),
                    name=comp,
                    legendgroup=comp,
                    showlegend=first_of_comp,
                    hovertext=[hover],
                    hoverinfo="text",
                    customdata=[m],
                ))

        # ── Zoom sur le voisinage si nœud sélectionné ─────────────
        if clicked_mod is not None and clicked_mod in pos:
            focus = list(neighbors | {clicked_mod})
            xs = [pos[n][0] for n in focus]; ys = [pos[n][1] for n in focus]
            pad = 0.6
            xaxis_cfg = dict(range=[min(xs)-pad, max(xs)+pad], showgrid=False, zeroline=False, showticklabels=False)
            yaxis_cfg = dict(range=[min(ys)-pad, max(ys)+pad], showgrid=False, zeroline=False, showticklabels=False)
            title_text = f"{_mod_label(clicked_mod)} — {G.degree(clicked_mod)} connexion(s)"
        else:
            xaxis_cfg = dict(showgrid=False, zeroline=False, showticklabels=False)
            yaxis_cfg = dict(showgrid=False, zeroline=False, showticklabels=False)
            title_text = "Réseau de modules — liens par apprentissages critiques partagés"

        fig = go.Figure(data=edge_traces + node_traces)
        fig.update_layout(
            title=dict(text=title_text, x=0.5, xanchor="center", font=dict(size=14, family="Inter, sans-serif")),
            showlegend=True,
            legend=dict(title="Compétence dominante", font=dict(size=11)),
            height=560,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=xaxis_cfg,
            yaxis=yaxis_cfg,
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
