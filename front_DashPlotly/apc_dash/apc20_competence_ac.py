from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app_tools import get_endpoint, get_python_backend_url
import pandas as pd
import plotly.express as px


COLOR_MAP = {
    "COMP_IDU1": "#FF4E3A",
    "COMP_IDU2": "#F39C3D",
    "COMP_IDU3": "#3F7EE8",
    "COMP_IDU4": "#1FB985"
}


apc20_competence_ac_layout = html.Div([

    # =========================
    # STORE AC
    # =========================
    dcc.Store(id="competence-data-store"),

    # =========================
    # STORE CE
    # =========================
    dcc.Store(id="competence-ce-data-store"),

    # =========================================================
    # PARTIE 1 : COMPETENCE / APPRENTISSAGES CRITIQUES
    # =========================================================
    html.H3("Compétences et Apprentissages critiques", style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Choisir une compétence :"),
        dcc.Dropdown(
            id="competence-dropdown",
            placeholder="Choisir une compétence",
            clearable=False
        ),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Div([
            dcc.Graph(id="competence-graph")
        ], style={
            "width": "60%",
            "display": "inline-block",
            "verticalAlign": "top"
        }),

        html.Div([
            html.Div(id="competence_ac")
        ], style={
            "width": "38%",
            "display": "inline-block",
            "verticalAlign": "top",
            "paddingLeft": "20px",
            "maxHeight": "520px",
            "overflowY": "auto"
        }),
    ], style={"marginBottom": "50px"}),

    html.Hr(),

    # =========================================================
    # PARTIE 2 : COMPETENCE / COMPOSANTES ESSENTIELLES
    # =========================================================
    html.H3("Compétences et Composantes essentielles", style={"marginTop": "30px", "marginBottom": "20px"}),

    html.Div([
        html.Label("Choisir une compétence :"),
        dcc.Dropdown(
            id="competence-ce-dropdown",
            placeholder="Choisir une compétence",
            clearable=False
        ),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Div([
            dcc.Graph(id="competence-ce-graph")
        ], style={
            "width": "60%",
            "display": "inline-block",
            "verticalAlign": "top"
        }),

        html.Div([
            html.Div(id="competence_ce")
        ], style={
            "width": "38%",
            "display": "inline-block",
            "verticalAlign": "top",
            "paddingLeft": "20px",
            "maxHeight": "520px",
            "overflowY": "auto"
        }),
    ])
])


def register_callbacks(app):

    # =========================================================
    # CALLBACKS AC
    # =========================================================
    @app.callback(
        Output("competence-data-store", "data"),
        Output("competence-graph", "figure"),
        Output("competence-dropdown", "options"),
        Output("competence-dropdown", "value"),
        Input("user_id", "data"),
        State("token", "data"),
    )
    def load_graph_ac(user_id, token):
        if not token:
            raise PreventUpdate

        url = get_python_backend_url("/competence_ac/")
        df = get_endpoint(url, token=token)

        if df is None or len(df) == 0:
            return [], {}, [], None

        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)

        if df.empty:
            return [], {}, [], None

        df = df.copy()

        required_cols = [
            "code_competence",
            "libelle_competence",
            "id_apprentissage_critique",
            "libelle_apprentissage"
        ]
        for col in required_cols:
            if col not in df.columns:
                return [], {}, [], None

        df["code_competence"] = df["code_competence"].fillna("").astype(str).str.strip()
        df["libelle_competence"] = df["libelle_competence"].fillna("").astype(str).str.strip()
        df["libelle_apprentissage"] = df["libelle_apprentissage"].fillna("").astype(str).str.strip()

        df = df.dropna(subset=["id_apprentissage_critique"])
        df = df[df["code_competence"] != ""]

        if df.empty:
            return [], {}, [], None

        comp_df = (
            df[["code_competence", "libelle_competence"]]
            .drop_duplicates(subset=["code_competence"])
            .sort_values("code_competence")
        )

        options = [
            {
                "label": f"{row['code_competence']} - {row['libelle_competence']}",
                "value": row["code_competence"]
            }
            for _, row in comp_df.iterrows()
        ]

        default_value = options[0]["value"] if options else None

        graph_df = (
            df[["code_competence", "libelle_competence", "id_apprentissage_critique"]]
            .drop_duplicates(subset=["code_competence", "id_apprentissage_critique"])
            .groupby(["code_competence", "libelle_competence"], as_index=False)
            .agg(nb_ac=("id_apprentissage_critique", "nunique"))
            .sort_values("nb_ac", ascending=True)
        )

        fig = px.bar(
            graph_df,
            x="nb_ac",
            y="code_competence",
            orientation="h",
            text="nb_ac",
            color="code_competence",
            color_discrete_map=COLOR_MAP,
            custom_data=["libelle_competence"],
            title="Compétences - Nombre d’Apprentissages critiques (AC) associés"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "compétence=%{y}<br>"
                "nb_ac=%{x}<br>"
                "libellé=%{customdata[0]}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="nb_ac",
            yaxis_title="code_competence",
            clickmode="event+select",
            showlegend=False,
            margin=dict(l=40, r=20, t=70, b=40),
            height=520
        )

        return df.to_dict("records"), fig, options, default_value

    @app.callback(
        Output("competence-dropdown", "value", allow_duplicate=True),
        Input("competence-graph", "clickData"),
        State("competence-dropdown", "value"),
        prevent_initial_call=True
    )
    def update_dropdown_from_graph_ac(clickData, current_value):
        if not clickData or "points" not in clickData or len(clickData["points"]) == 0:
            raise PreventUpdate

        selected_competence = clickData["points"][0]["y"]

        if selected_competence == current_value:
            raise PreventUpdate

        return selected_competence

    @app.callback(
        Output("competence_ac", "children"),
        Input("competence-dropdown", "value"),
        State("competence-data-store", "data"),
    )
    def update_ac_list(selected_competence, stored_data):
        if not selected_competence:
            return "Choisissez une compétence"

        if not stored_data:
            return "Aucune donnée disponible"

        df = pd.DataFrame(stored_data)

        if df.empty:
            return "Aucune donnée disponible"

        df_filtre = df[df["code_competence"] == selected_competence].copy()

        if df_filtre.empty:
            return f"Aucune donnée pour {selected_competence}"

        ac_df = (
            df_filtre[["id_apprentissage_critique", "libelle_apprentissage"]]
            .dropna(subset=["id_apprentissage_critique", "libelle_apprentissage"])
            .copy()
        )

        ac_df["libelle_apprentissage"] = ac_df["libelle_apprentissage"].astype(str).str.strip()
        ac_df = ac_df[ac_df["libelle_apprentissage"] != ""]

        ac_df = (
            ac_df
            .drop_duplicates(subset=["id_apprentissage_critique"])
            .sort_values("id_apprentissage_critique")
        )

        if ac_df.empty:
            return html.Div([
                html.H4(f"{selected_competence} — Apprentissages critiques"),
                html.P("Aucun apprentissage critique trouvé.")
            ])

        return html.Div([
            html.H4(
                f"{selected_competence} — Apprentissages critiques",
                style={"fontWeight": "bold", "marginBottom": "15px"}
            ),
            html.Ul([
                html.Li(row["libelle_apprentissage"], style={"marginBottom": "10px"})
                for _, row in ac_df.iterrows()
            ], style={"paddingLeft": "22px"})
        ])

    # =========================================================
    # CALLBACKS CE
    # =========================================================
    @app.callback(
        Output("competence-ce-data-store", "data"),
        Output("competence-ce-graph", "figure"),
        Output("competence-ce-dropdown", "options"),
        Output("competence-ce-dropdown", "value"),
        Input("user_id", "data"),
        State("token", "data"),
    )
    def load_graph_ce(user_id, token):
        if not token:
            raise PreventUpdate

        url = get_python_backend_url("/competence_ce/")
        df = get_endpoint(url, token=token)

        if df is None or len(df) == 0:
            return [], {}, [], None

        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)

        if df.empty:
            return [], {}, [], None

        df = df.copy()

        required_cols = [
            "code_competence",
            "libelle_competence",
            "id_composante_essentielle",
            "libelle_composante_essentielle"
        ]
        for col in required_cols:
            if col not in df.columns:
                return [], {}, [], None

        df["code_competence"] = df["code_competence"].fillna("").astype(str).str.strip()
        df["libelle_competence"] = df["libelle_competence"].fillna("").astype(str).str.strip()
        df["libelle_composante_essentielle"] = df["libelle_composante_essentielle"].fillna("").astype(str).str.strip()

        df = df.dropna(subset=["id_composante_essentielle"])
        df = df[df["code_competence"] != ""]

        if df.empty:
            return [], {}, [], None

        comp_df = (
            df[["code_competence", "libelle_competence"]]
            .drop_duplicates(subset=["code_competence"])
            .sort_values("code_competence")
        )

        options = [
            {
                "label": f"{row['code_competence']} - {row['libelle_competence']}",
                "value": row["code_competence"]
            }
            for _, row in comp_df.iterrows()
        ]

        default_value = options[0]["value"] if options else None

        graph_df = (
            df[["code_competence", "libelle_competence", "id_composante_essentielle"]]
            .drop_duplicates(subset=["code_competence", "id_composante_essentielle"])
            .groupby(["code_competence", "libelle_competence"], as_index=False)
            .agg(nb_ce=("id_composante_essentielle", "nunique"))
            .sort_values("nb_ce", ascending=True)
        )

        fig = px.bar(
            graph_df,
            x="nb_ce",
            y="code_competence",
            orientation="h",
            text="nb_ce",
            color="code_competence",
            color_discrete_map=COLOR_MAP,
            custom_data=["libelle_competence"],
            title="Compétences - Nombre de Composantes essentielles (CE) associées"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "compétence=%{y}<br>"
                "nb_ce=%{x}<br>"
                "libellé=%{customdata[0]}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="nb_ce",
            yaxis_title="code_competence",
            clickmode="event+select",
            showlegend=False,
            margin=dict(l=40, r=20, t=70, b=40),
            height=520
        )

        return df.to_dict("records"), fig, options, default_value

    @app.callback(
        Output("competence-ce-dropdown", "value", allow_duplicate=True),
        Input("competence-ce-graph", "clickData"),
        State("competence-ce-dropdown", "value"),
        prevent_initial_call=True
    )
    def update_dropdown_from_graph_ce(clickData, current_value):
        if not clickData or "points" not in clickData or len(clickData["points"]) == 0:
            raise PreventUpdate

        selected_competence = clickData["points"][0]["y"]

        if selected_competence == current_value:
            raise PreventUpdate

        return selected_competence

    @app.callback(
        Output("competence_ce", "children"),
        Input("competence-ce-dropdown", "value"),
        State("competence-ce-data-store", "data"),
    )
    def update_ce_list(selected_competence, stored_data):
        if not selected_competence:
            return "Choisissez une compétence"

        if not stored_data:
            return "Aucune donnée disponible"

        df = pd.DataFrame(stored_data)

        if df.empty:
            return "Aucune donnée disponible"

        df_filtre = df[df["code_competence"] == selected_competence].copy()

        if df_filtre.empty:
            return f"Aucune donnée pour {selected_competence}"

        ce_df = (
            df_filtre[["id_composante_essentielle", "libelle_composante_essentielle"]]
            .dropna(subset=["id_composante_essentielle", "libelle_composante_essentielle"])
            .copy()
        )

        ce_df["libelle_composante_essentielle"] = ce_df["libelle_composante_essentielle"].astype(str).str.strip()
        ce_df = ce_df[ce_df["libelle_composante_essentielle"] != ""]

        ce_df = (
            ce_df
            .drop_duplicates(subset=["id_composante_essentielle"])
            .sort_values("id_composante_essentielle")
        )

        if ce_df.empty:
            return html.Div([
                html.H4(f"{selected_competence} — Composantes essentielles"),
                html.P("Aucune composante essentielle trouvée.")
            ])

        return html.Div([
            html.H4(
                f"{selected_competence} — Composantes essentielles",
                style={"fontWeight": "bold", "marginBottom": "15px"}
            ),
            html.Ul([
                html.Li(row["libelle_composante_essentielle"], style={"marginBottom": "10px"})
                for _, row in ce_df.iterrows()
            ], style={"paddingLeft": "22px"})
        ])