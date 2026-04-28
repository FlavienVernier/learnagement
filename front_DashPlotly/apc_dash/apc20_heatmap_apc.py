
import logging
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
from io import StringIO

from .apc20_heatmap_apc_tools import (
    get_apc_competences,
    get_apc_niveaux,
    get_apc_apprentissages,
    get_apc_ac_modules,
    get_apc_modules,
    get_apc_composantes,
)


# ═══════════════════════════════════════════════════════════════════
#                         DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════════

COLORS = {
    "primary": "#3B82F6",
    "light": "#F8FAFC",
    "competences": {
        "COMP_IDU1": "#FF513F",
        "COMP_IDU2": "#FFA03F",
        "COMP_IDU3": "#3B82F6",
        "COMP_IDU4": "#10B981",
    },
}

KNOWN_COMPETENCES = ["COMP_IDU1", "COMP_IDU2", "COMP_IDU3", "COMP_IDU4"]
KNOWN_NIVEAUX = [1, 2, 3]
KNOWN_TYPES_LIEN = ["Requis", "Recommandé", "Complémentaire"]


def get_competence_color(comp):
    return COLORS["competences"].get(comp, "#777777")


# ═══════════════════════════════════════════════════════════════════
#                    FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════

def parse_competencies(row):
    if "niveau_code" in row.index and pd.notna(row["niveau_code"]):
        return row["niveau_code"]
    return None


def compute_competency_counts_per_module(df_input):
    df_work = df_input.copy()
    if "libelle_apprentissage" not in df_work.columns:
        df_work = df_work.assign(libelle_apprentissage=df_work.index.astype(str))

    df_work = df_work.assign(All_Competencies=df_work["niveau_code"])
    df_exploded = df_work.copy()

    df_pivot_global = (
        df_exploded
        .groupby(["niveau", "competence_label"], as_index=False)
        .size()
        .pivot(index="niveau", columns="competence_label", values="size")
        .fillna(0)
        .astype("Float64")
    )

    df_count = (
        df_exploded
        .groupby(["niveau", "id_module", "competence_label"], as_index=False)
        .size()
    )

    df_pivot_niveau = (
        df_count
        .pivot(index=["niveau", "id_module"], columns="competence_label", values="size")
        .fillna(0)
        .astype("Float64")
    )

    df_pivot_module = (
        df_exploded
        .pivot(
            index=["niveau", "id_module", "libelle_apprentissage"],
            columns="competence_label",
            values="type_lien",
        )
        .fillna("")
    )

    return df_pivot_global, df_pivot_niveau, df_pivot_module


# ═══════════════════════════════════════════════════════════════════
#                    FONCTIONS HEATMAP
# ═══════════════════════════════════════════════════════════════════

def create_heatmap_for_global(df_pivot_global):
    fig = go.Figure()
    for j in range(df_pivot_global.shape[1]):
        comp = df_pivot_global.columns[j]
        color_scale = ["white", get_competence_color(comp)]
        df_comp = df_pivot_global.copy()
        for col in df_comp.columns:
            if col != comp:
                df_comp.loc[:, col] = pd.NA
        fig.add_trace(
            go.Heatmap(
                z=df_comp.values,
                x=df_pivot_global.columns,
                y=df_pivot_global.index,
                colorscale=color_scale,
                showscale=False,
                hoverongaps=False,
                hovertemplate="<b>Niveau %{y}</b><br>%{x}<br>AC: %{z}<extra></extra>",
            )
        )
    fig.update_layout(
        title=dict(
            text="Répartition des compétences<br>"
                 "<sub>Cliquez sur un niveau pour voir les modules</sub>",
            x=0.5, xanchor="center",
            font=dict(size=20, family="Inter, sans-serif"),
        ),
        xaxis_title="Compétences",
        xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
        yaxis_title="Niveaux",
        yaxis=dict(type="category", autorange="reversed", showgrid=False, tickfont=dict(size=12)),
        height=600,
        font=dict(size=11, family="Inter, sans-serif"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=100, r=60, t=120, b=150),
        clickmode="event+select",
    )
    return fig


def create_heatmap_for_niveau(niveau, df_pivot_niveau, module_names):
    df_used = df_pivot_niveau.xs(niveau, level="niveau")
    fig = go.Figure()
    z_max = df_pivot_niveau.max().max()

    module_names_list = [
        module_names.get(mod, module_names.get(float(mod) if not isinstance(mod, float) else mod, f"Module {mod}"))
        for mod in df_used.index
    ]
    # customdata : ID du module pour chaque cellule (utilisé par le callback pour le drill-down)
    module_ids_customdata = [[str(mod)] * len(df_used.columns) for mod in df_used.index]

    for j in range(df_used.shape[1]):
        comp = df_used.columns[j]
        color_scale = ["white", get_competence_color(comp)]
        df_comp = df_used.copy()
        for col in df_comp.columns:
            if col != comp:
                df_comp.loc[:, col] = pd.NA
        fig.add_trace(
            go.Heatmap(
                z=df_comp.values,
                x=df_used.columns,
                y=module_names_list,
                zmin=0,
                zmax=z_max,
                colorscale=color_scale,
                showscale=False,
                hoverongaps=False,
                xgap=1,
                ygap=1,
                customdata=module_ids_customdata,
                hovertemplate="<b>%{y}</b><br>%{x}<br>AC: %{z}<extra></extra>",
            )
        )
    fig.update_layout(
        title=dict(
            text=f"Modules du niveau {niveau}<br>"
                 "<sub>Cliquez sur un module pour voir les apprentissages critiques</sub>",
            x=0.5, xanchor="center",
            font=dict(size=20, family="Inter, sans-serif"),
        ),
        xaxis_title="Compétences",
        yaxis_title="Modules",
        xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        height=max(500, len(df_used.index) * 35 + 180),
        font=dict(size=11, family="Inter, sans-serif"),
        plot_bgcolor="white",
        paper_bgcolor=COLORS["light"],
        margin=dict(l=280, r=60, t=120, b=180),
        clickmode="event+select",
    )
    return fig


def create_heatmap_for_module(module_id, df_pivot_module, module_names):
    df_reorganized = df_pivot_module.replace(
        {"Requis": 3, "Recommandé": 2, "Complémentaire": 1, "Non associé": 0, "": 0}
    )
    df_used = df_reorganized.xs(module_id, level="id_module").astype("Int64")
    fig = go.Figure()

    for j in range(df_used.shape[1]):
        comp = df_used.columns[j]
        color_scale = ["white", get_competence_color(comp)]
        df_comp = df_used.copy()
        for col in df_comp.columns:
            if col != comp:
                df_comp.loc[:, col] = pd.NA
        hover_text = [
            idx[-1] if isinstance(idx, tuple) else idx
            for idx in df_used.index
        ]
        fig.add_trace(
            go.Heatmap(
                z=df_comp.values,
                x=df_used.columns,
                y=hover_text,
                zmin=0,
                zmax=3,
                colorscale=color_scale,
                showscale=False,
                hoverongaps=False,
                xgap=1,
                ygap=1,
                customdata=df_comp.values,
                hovertemplate="<b>%{y}</b><br>%{x}<br>Type: %{customdata}<extra></extra>",
            )
        )

    module_name = module_names.get(
        module_id,
        module_names.get(float(module_id) if not isinstance(module_id, float) else module_id, f"Module {module_id}")
    )
    fig.update_layout(
        title=dict(
            text=f"{module_name} — Apprentissages critiques",
            x=0.5, xanchor="center",
            font=dict(size=20, family="Inter, sans-serif"),
        ),
        xaxis_title="Compétences",
        yaxis_title="Apprentissages critiques",
        xaxis=dict(tickangle=-45, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=10)),
        height=max(600, len(df_used.index) * 25 + 180),
        font=dict(size=11, family="Inter, sans-serif"),
        plot_bgcolor="white",
        paper_bgcolor=COLORS["light"],
        margin=dict(l=400, r=60, t=120, b=180),
    )
    return fig


def _empty_fig(msg="Chargement des données..."):
    fig = go.Figure()
    fig.add_annotation(
        text=msg, x=0.5, y=0.5, xref="paper", yref="paper",
        showarrow=False, font=dict(size=14, color="#94a3b8"),
    )
    fig.update_layout(height=500, paper_bgcolor="white", plot_bgcolor="white")
    return fig


# ═══════════════════════════════════════════════════════════════════
#                            LAYOUT
# ═══════════════════════════════════════════════════════════════════

heatmap_apc_layout = html.Div(
    [
        # Stores
        dcc.Store(id="heatmap-apc-raw-store"),
        dcc.Store(id="heatmap-apc-filtered-store"),
        dcc.Store(id="heatmap-apc-drill-level", data="global"),
        dcc.Store(id="heatmap-apc-selected-niveau", data=None),
        dcc.Store(id="heatmap-apc-selected-module", data=None),

        # Header
        html.Div(
            [
                html.H1("Heatmap APC — Mon parcours", style={"margin": "0", "fontSize": "22px"}),
                html.P(
                    "Exploration interactive : cliquez sur un niveau pour descendre dans les modules, "
                    "puis sur un module pour voir les apprentissages critiques.",
                    style={"margin": "4px 0 0 0", "color": "#6B7280", "fontSize": "14px"},
                ),
            ],
            style={
                "backgroundColor": "white",
                "padding": "16px 24px",
                "borderBottom": "1px solid #E5E7EB",
                "position": "sticky", "top": "0", "zIndex": "999",
            },
        ),

        # Body : sidebar + contenu principal
        html.Div(
            [
                # Sidebar filtres
                html.Div(
                    [
                        html.H3("Filtres", style={"marginBottom": "16px", "fontSize": "16px", "fontWeight": "600"}),

                        html.Div(
                            [
                                html.Label("Niveaux", style={"fontWeight": "500", "fontSize": "13px"}),
                                dcc.Dropdown(
                                    id="heatmap-apc-niveau-filter",
                                    options=[{"label": f"Niveau {n}", "value": n} for n in KNOWN_NIVEAUX],
                                    value=KNOWN_NIVEAUX,
                                    multi=True,
                                    placeholder="Tous les niveaux",
                                ),
                            ],
                            style={"marginBottom": "14px"},
                        ),

                        html.Div(
                            [
                                html.Label("Compétences", style={"fontWeight": "500", "fontSize": "13px"}),
                                dcc.Dropdown(
                                    id="heatmap-apc-comp-filter",
                                    options=[{"label": c, "value": c} for c in KNOWN_COMPETENCES],
                                    value=KNOWN_COMPETENCES,
                                    multi=True,
                                    placeholder="Toutes les compétences",
                                ),
                            ],
                            style={"marginBottom": "14px"},
                        ),

                        html.Div(
                            [
                                html.Label("Types de lien", style={"fontWeight": "500", "fontSize": "13px"}),
                                dcc.Checklist(
                                    id="heatmap-apc-lien-filter",
                                    options=[{"label": t, "value": t} for t in KNOWN_TYPES_LIEN],
                                    value=KNOWN_TYPES_LIEN,
                                    labelStyle={"display": "block", "marginBottom": "4px"},
                                ),
                            ],
                            style={"marginBottom": "14px"},
                        ),

                        html.Button(
                            "↻ Réinitialiser",
                            id="heatmap-apc-reset-filters",
                            n_clicks=0,
                            style={
                                "width": "100%", "padding": "8px", "cursor": "pointer",
                                "backgroundColor": "#F3F4F6", "border": "1px solid #D1D5DB",
                                "borderRadius": "6px",
                            },
                        ),
                        html.Div(
                            id="heatmap-apc-filter-status",
                            style={"marginTop": "8px", "fontSize": "12px", "color": "#6B7280"},
                        ),
                    ],
                    style={
                        "width": "240px", "flexShrink": "0",
                        "padding": "20px", "backgroundColor": "white",
                        "borderRight": "1px solid #E5E7EB",
                        "minHeight": "calc(100vh - 80px)",
                    },
                ),

                # Contenu principal
                html.Div(
                    [
                        # Breadcrumb + boutons navigation
                        html.Div(
                            [
                                html.Div(id="heatmap-apc-breadcrumb", style={"flex": "1"}),
                                html.Div(
                                    [
                                        html.Button(
                                            "Vue globale",
                                            id="heatmap-apc-btn-global",
                                            n_clicks=0,
                                            style={
                                                "padding": "6px 14px", "cursor": "pointer",
                                                "backgroundColor": COLORS["primary"], "color": "white",
                                                "border": "none", "borderRadius": "6px", "marginRight": "8px",
                                            },
                                        ),
                                        html.Button(
                                            "← Retour",
                                            id="heatmap-apc-btn-back",
                                            n_clicks=0,
                                            style={
                                                "padding": "6px 14px", "cursor": "pointer",
                                                "backgroundColor": "white", "color": "#374151",
                                                "border": "1px solid #D1D5DB", "borderRadius": "6px",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                            style={
                                "display": "flex", "alignItems": "center",
                                "marginBottom": "12px", "gap": "12px",
                            },
                        ),

                        # Graphe heatmap drill-down
                        html.Div(
                            dcc.Graph(
                                id="heatmap-apc-drilldown",
                                figure=_empty_fig(),
                                config={"displayModeBar": True, "displaylogo": False},
                                style={"width": "100%"},
                            ),
                            style={
                                "backgroundColor": "white", "borderRadius": "10px",
                                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)", "padding": "12px",
                            },
                        ),
                    ],
                    style={"flex": "1", "padding": "20px", "overflow": "auto"},
                ),
            ],
            style={"display": "flex", "minHeight": "calc(100vh - 80px)"},
        ),
    ],
    style={"fontFamily": "Inter, sans-serif", "backgroundColor": "#F9FAFB"},
)


# ═══════════════════════════════════════════════════════════════════
#                          CALLBACKS
# ═══════════════════════════════════════════════════════════════════

def register_callbacks(app):

    # ── 1. Chargement des données depuis l'API ──────────────────────
    @app.callback(
        Output("heatmap-apc-raw-store", "data"),
        Input("token", "data"),
        prevent_initial_call=False,
    )
    def load_apc_data(token):
        if not token or token == "none":
            return None
        try:
            df_competences   = get_apc_competences(token)
            df_niveaux       = get_apc_niveaux(token)
            df_apprentissages = get_apc_apprentissages(token)
            df_ac_modules_raw = get_apc_ac_modules(token)
            df_modules       = get_apc_modules(token)
            df_composantes   = get_apc_composantes(token)

            # Construction de df_main (même logique que learnagement_dashboard_final.py)
            df_base = (
                df_apprentissages
                .merge(df_niveaux, on="id_niveau", how="left")
                .merge(df_competences, on="id_competence", how="left")
            )

            ac_agg = (
                df_ac_modules_raw
                .groupby("id_apprentissage_critique")
                .agg({"id_module": list, "type_lien": list})
                .reset_index()
            )
            ac_agg.columns = ["id_apprentissage_critique", "modules_list", "types_lien_list"]

            df_main = df_base.merge(ac_agg, on="id_apprentissage_critique", how="left")
            df_main["modules_list"]    = df_main["modules_list"].apply(lambda x: x if isinstance(x, list) else [])
            df_main["types_lien_list"] = df_main["types_lien_list"].apply(lambda x: x if isinstance(x, list) else [])
            df_main["nb_modules"]      = df_main["modules_list"].apply(len)
            df_main["id_module"]       = df_main["modules_list"].apply(lambda x: x[0] if x else 0)
            df_main["type_lien"]       = df_main["types_lien_list"].apply(lambda x: x[0] if x else "Non associé")
            df_main["competence_label"] = df_main["code_competence"]
            df_main["niveau_code"]     = df_main["competence_label"] + "-N" + df_main["niveau"].astype(str)

            mask = df_main["id_module"].isna()
            if mask.sum() > 0:
                df_main.loc[mask, "id_module"]  = 0.0
                df_main.loc[mask, "type_lien"]  = "Non associé"

            # Dictionnaire module_names (clés en string pour JSON)
            module_names = {"0": "Non associé", "0.0": "Non associé"}
            for _, row in df_modules.iterrows():
                mid  = row["id_module"]
                code = row["code_module"] if pd.notna(row["code_module"]) else f"M{mid}"
                nom  = row["nom"]         if pd.notna(row["nom"])         else "Module"
                module_names[str(mid)] = f"{code} - {nom}"

            # Reverse : nom → id_module (string)
            module_ids = {v: k for k, v in module_names.items()}

            return {
                "df_main":        df_main.to_json(date_format="iso", orient="split"),
                "df_composantes": df_composantes.to_json(date_format="iso", orient="split"),
                "module_names":   module_names,
                "module_ids":     module_ids,
            }

        except Exception as e:
            logging.exception(f"[heatmap_apc] Erreur chargement données APC : {e}")
            return None

    # ── 2. Filtrage ────────────────────────────────────────────────
    @app.callback(
        Output("heatmap-apc-filtered-store", "data"),
        Output("heatmap-apc-filter-status", "children"),
        Input("heatmap-apc-niveau-filter", "value"),
        Input("heatmap-apc-comp-filter",   "value"),
        Input("heatmap-apc-lien-filter",   "value"),
        Input("heatmap-apc-reset-filters", "n_clicks"),
        Input("heatmap-apc-raw-store",     "data"),
        prevent_initial_call=False,
    )
    def filter_data(niveaux, competences, types_lien, reset_clicks, raw_data):
        if raw_data is None:
            return None, "Chargement..."

        df = pd.read_json(StringIO(raw_data["df_main"]), orient="split")
        ctx = dash.callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else ""

        if trigger == "heatmap-apc-reset-filters":
            return raw_data["df_main"], f"{len(df)} objectifs affichés"

        filtered = df.copy()
        if niveaux:
            filtered = filtered[filtered["niveau"].isin(niveaux)]
        if competences:
            filtered = filtered[filtered["competence_label"].isin(competences)]
        if types_lien:
            filtered = filtered[filtered["type_lien"].isin(types_lien)]

        return filtered.to_json(date_format="iso", orient="split"), f"{len(filtered)} / {len(df)} objectifs"

    # ── 3. Drill-down heatmap ──────────────────────────────────────
    @app.callback(
        Output("heatmap-apc-drilldown",       "figure"),
        Output("heatmap-apc-drill-level",     "data"),
        Output("heatmap-apc-selected-niveau", "data"),
        Output("heatmap-apc-selected-module", "data"),
        Output("heatmap-apc-breadcrumb",      "children"),
        Input("heatmap-apc-filtered-store",   "data"),
        Input("heatmap-apc-drilldown",        "clickData"),
        Input("heatmap-apc-btn-global",       "n_clicks"),
        Input("heatmap-apc-btn-back",         "n_clicks"),
        State("heatmap-apc-drill-level",      "data"),
        State("heatmap-apc-selected-niveau",  "data"),
        State("heatmap-apc-selected-module",  "data"),
        State("heatmap-apc-raw-store",        "data"),
        prevent_initial_call=False,
    )
    def update_heatmap_drilldown(
        filtered_json, clickData, _btn_global, _btn_back,
        current_level, current_niveau, current_module, raw_data,
    ):
        if filtered_json is None or raw_data is None:
            return _empty_fig("En attente des données…"), "global", None, None, html.Span("Vue globale")

        # Reconstruction de module_names avec clés numériques
        module_names_str = raw_data.get("module_names", {})
        module_ids_str   = raw_data.get("module_ids",   {})
        module_names = {}
        for k, v in module_names_str.items():
            try:
                module_names[float(k)] = v
            except (ValueError, TypeError):
                module_names[k] = v

        filtered_df = pd.read_json(StringIO(filtered_json), orient="split")
        filtered_df["niveau_code"] = filtered_df.apply(parse_competencies, axis=1)
        filtered_df = filtered_df.assign(All_Competencies=filtered_df["niveau_code"])

        ctx = dash.callback_context
        trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "none"

        new_level  = current_level or "global"
        new_niveau = current_niveau
        new_module = current_module

        if trigger == "heatmap-apc-btn-global":
            new_level, new_niveau, new_module = "global", None, None

        elif trigger == "heatmap-apc-btn-back":
            if current_level == "module":
                new_level, new_module = "semester", None
            elif current_level == "semester":
                new_level, new_niveau = "global", None

        elif trigger == "heatmap-apc-drilldown" and clickData and "points" in clickData:
            point = clickData["points"][0]
            if current_level in [None, "global"]:
                clicked = point.get("y")
                if clicked is not None:
                    try:
                        new_niveau = int(clicked)
                        new_level  = "semester"
                        new_module = None
                    except (ValueError, TypeError):
                        pass
            elif current_level == "semester":
                # Utilise customdata (ID du module) si disponible, sinon fallback sur le nom
                customdata_val = point.get("customdata")
                if customdata_val is not None:
                    try:
                        raw = customdata_val[0] if isinstance(customdata_val, list) else customdata_val
                        new_module = float(raw)
                        new_level  = "module"
                    except (ValueError, TypeError):
                        pass
                else:
                    clicked_name = point.get("y")
                    if clicked_name is not None:
                        clicked_id = module_ids_str.get(clicked_name)
                        if clicked_id is not None:
                            try:
                                new_module = float(clicked_id)
                                new_level  = "module"
                            except (ValueError, TypeError):
                                pass

        try:
            df_pivot_global, df_pivot_niveau, df_pivot_module = compute_competency_counts_per_module(filtered_df)
        except Exception as e:
            return _empty_fig(f"Erreur : {e}"), "global", None, None, html.Span("Erreur")

        # ── Rendu selon le niveau de drill-down ──
        if new_level == "global":
            fig       = create_heatmap_for_global(df_pivot_global)
            breadcrumb = html.Span("Vue globale", style={"fontWeight": "600"})

        elif new_level == "semester" and new_niveau is not None:
            available = df_pivot_niveau.index.get_level_values("niveau").unique().tolist()
            if new_niveau in available:
                fig = create_heatmap_for_niveau(new_niveau, df_pivot_niveau, module_names)
                breadcrumb = html.Span([
                    html.Span("Vue globale", style={"color": "#6B7280"}),
                    html.Span(" / "),
                    html.Span(f"Niveau {new_niveau}", style={"fontWeight": "600"}),
                ])
            else:
                fig        = create_heatmap_for_global(df_pivot_global)
                new_level, new_niveau = "global", None
                breadcrumb = html.Span("Vue globale", style={"fontWeight": "600"})

        elif new_level == "module" and new_module is not None:
            available = df_pivot_module.index.get_level_values("id_module").unique().tolist()
            if new_module in available:
                fig = create_heatmap_for_module(new_module, df_pivot_module, module_names)
                module_name = module_names.get(new_module, f"Module {new_module}")
                breadcrumb = html.Span([
                    html.Span("Vue globale", style={"color": "#6B7280"}),
                    html.Span(" / "),
                    html.Span(f"Niveau {new_niveau}", style={"color": "#6B7280"}),
                    html.Span(" / "),
                    html.Span(module_name, style={"fontWeight": "600"}),
                ])
            else:
                fig        = create_heatmap_for_global(df_pivot_global)
                new_level, new_niveau, new_module = "global", None, None
                breadcrumb = html.Span("Vue globale", style={"fontWeight": "600"})

        else:
            fig        = create_heatmap_for_global(df_pivot_global)
            new_level, new_niveau, new_module = "global", None, None
            breadcrumb = html.Span("Vue globale", style={"fontWeight": "600"})

        return fig, new_level, new_niveau, new_module, breadcrumb
