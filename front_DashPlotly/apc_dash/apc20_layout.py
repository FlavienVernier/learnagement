"""
Constantes de style partagées pour tous les tableaux de bord APC.
"""
import plotly.graph_objects as go

COLORS = {
    "primary": "#3B82F6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger":  "#EF4444",
    "light":   "#F8FAFC",
    "competences": {
        "COMP_IDU1": "#FF513F",
        "COMP_IDU2": "#FFA03F",
        "COMP_IDU3": "#3B82F6",
        "COMP_IDU4": "#10B981",
    },
}

KNOWN_COMPETENCES = ["COMP_IDU1", "COMP_IDU2", "COMP_IDU3", "COMP_IDU4"]
KNOWN_NIVEAUX = [1, 2, 3]
KNOWN_TYPES_LIEN = ["Requis", "Recommandé", "Complémentaire", "Non associé"]


def get_competence_color(comp: str) -> str:
    return COLORS["competences"].get(comp, "#777777")


def empty_fig(msg: str = "Chargement des données...") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(
            text=msg,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#9CA3AF"),
        )],
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig
