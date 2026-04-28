"""
Viz 2 : Carte de couverture APC par semestre
Question enseignant : "Les AC d'une compétence sont-ils bien répartis dans le cursus ?"

Heatmap AC × Semestre colorée selon le type de lien le plus fort.
Les cellules grises signalent les AC non couverts dans un semestre donné.
"""
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output
from io import StringIO

from .apc20_layout import COLORS, KNOWN_COMPETENCES, get_competence_color, empty_fig


_LIEN_SCORE = {"Requis": 3, "Recommandé": 2, "Complémentaire": 1}


# ─── Layout ───────────────────────────────────────────────────────

couverture_content = html.Div(
    [
        html.Div(
            [
                html.Label(
                    "Compétence",
                    style={"fontWeight": "600", "marginBottom": "8px", "display": "block"},
                ),
                dcc.Dropdown(
                    id="couverture-comp-select",
                    options=[{"label": c, "value": c} for c in KNOWN_COMPETENCES],
                    value=KNOWN_COMPETENCES[0],
                    clearable=False,
                    style={"maxWidth": "420px"},
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Heatmap
        html.Div(
            dcc.Graph(
                id="couverture-heatmap",
                figure=empty_fig(),
                config={"displayModeBar": True, "displaylogo": False},
            ),
            style={
                "backgroundColor": "white",
                "borderRadius": "10px",
                "boxShadow": "0 1px 4px rgba(0,0,0,0.08)",
                "padding": "12px",
                "marginBottom": "16px",
            },
        ),

        # Légende
        html.Div(
            [
                html.Span("Intensité : ", style={"fontSize": "13px", "color": "#6B7280", "marginRight": "8px"}),
                *[
                    html.Span(
                        label,
                        style={
                            "fontSize": "12px", "fontWeight": "600",
                            "color": color, "backgroundColor": color + "22",
                            "borderRadius": "4px", "padding": "2px 8px", "marginRight": "6px",
                        },
                    )
                    for label, color in [
                        ("Requis",         "#EF4444"),
                        ("Recommandé",     "#F59E0B"),
                        ("Complémentaire", "#10B981"),
                        ("Non couvert",    "#9CA3AF"),
                    ]
                ],
            ],
            style={"padding": "8px 4px"},
        ),
    ],
    style={"padding": "20px"},
)


# ─── Callbacks ────────────────────────────────────────────────────

def register_callbacks(app):

    @app.callback(
        Output("couverture-heatmap", "figure"),
        Input("couverture-comp-select", "value"),
        Input("apc-ens-raw-store",      "data"),
        prevent_initial_call=False,
    )
    def update_couverture(competence, raw_data):
        if not competence or raw_data is None:
            return empty_fig("Données non disponibles")

        df_main = pd.read_json(StringIO(raw_data["df_main"]), orient="split")

        df_comp = df_main[df_main["competence_label"] == competence].copy()
        if df_comp.empty:
            return empty_fig(f"Aucune donnée pour {competence}")

        df_comp["id_semestre"] = pd.to_numeric(df_comp["id_semestre"], errors="coerce")
        df_comp["lien_score"]  = df_comp["type_lien"].map(_LIEN_SCORE).fillna(0)

        all_acs = (
            df_comp[["id_apprentissage_critique", "libelle_apprentissage", "niveau"]]
            .drop_duplicates("id_apprentissage_critique")
            .sort_values(["niveau", "libelle_apprentissage"])
        )

        semestres = sorted(
            df_comp["id_semestre"].dropna().unique().astype(int).tolist()
        )
        if not semestres:
            return empty_fig("Aucun semestre renseigné dans les données modules")

        df_cov = (
            df_comp[df_comp["id_semestre"].notna()]
            .groupby(["id_apprentissage_critique", "id_semestre"])["lien_score"]
            .max()
            .reset_index()
        )

        ac_labels = []
        z_matrix  = []
        for _, ac_row in all_acs.iterrows():
            ac_id  = ac_row["id_apprentissage_critique"]
            label  = f"N{int(ac_row['niveau'])} | {str(ac_row['libelle_apprentissage'])[:55]}"
            ac_labels.append(label)
            row_scores = []
            for sem in semestres:
                match = df_cov[
                    (df_cov["id_apprentissage_critique"] == ac_id) &
                    (df_cov["id_semestre"] == sem)
                ]
                row_scores.append(float(match["lien_score"].iloc[0]) if not match.empty else 0.0)
            z_matrix.append(row_scores)

        comp_color = get_competence_color(competence)

        fig = go.Figure(data=go.Heatmap(
            z=z_matrix,
            x=[f"S{s}" for s in semestres],
            y=ac_labels,
            zmin=0,
            zmax=3,
            colorscale=[
                [0.00, "#F3F4F6"],
                [0.01, "#F3F4F6"],
                [0.34, "#FDE68A"],
                [0.67, "#FCA5A5"],
                [1.00, comp_color],
            ],
            showscale=True,
            colorbar=dict(
                tickvals=[0, 1, 2, 3],
                ticktext=["Non couvert", "Complémentaire", "Recommandé", "Requis"],
                thickness=14,
                title=dict(text="Lien", side="right", font=dict(size=11)),
            ),
            hoverongaps=False,
            xgap=3,
            ygap=2,
            hovertemplate="<b>%{y}</b><br>Semestre %{x}<br>Score : %{z:.0f}<extra></extra>",
        ))

        fig.update_layout(
            title=dict(
                text=(
                    f"Couverture des AC de {competence} par semestre<br>"
                    "<sub>Gris = AC non couvert ce semestre — plus la couleur est intense, plus le lien est fort</sub>"
                ),
                x=0.5, xanchor="center",
                font=dict(size=15, family="Inter, sans-serif"),
            ),
            xaxis=dict(tickfont=dict(size=11), side="top", title="Semestre"),
            yaxis=dict(tickfont=dict(size=10), autorange="reversed", title="Apprentissages critiques"),
            height=max(420, len(ac_labels) * 30 + 180),
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=360, r=120, t=120, b=40),
            font=dict(family="Inter, sans-serif"),
        )
        return fig
