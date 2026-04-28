from dash import html, dcc
import dash_bootstrap_components as dbc


FORMATIONS = ["idu", "eit", "meca", "sni", "bee"]

CATEGORIES = [
    "competences",
    "metiers",
    "projets",
    "techniques",
    "bonnes_pratiques",
    "experiences"
]

LEVELS = ["tous", "débutant", "intermédiaire", "avancé"]


def create_layout():
    return html.Div(
        className="app-shell",
        children=[
            html.Div(
                className="rag-sidebar",
                children=[
                    html.Div(
                        className="brand-box",
                        children=[
                            html.Div("🎓", className="brand-icon"),
                            html.H3("Polytech Assistant", className="brand-title"),
                            html.P("Orientation intelligente basée sur tes PDF", className="brand-subtitle"),
                        ],
                    ),

                    html.Div(
                        className="form-card",
                        children=[
                            html.Label("Formation", className="form-label"),
                            dcc.Dropdown(
                                id="rag-formation-dropdown",
                                options=[{"label": f.upper(), "value": f} for f in FORMATIONS],
                                value="idu",
                                clearable=False,
                                className="custom-dropdown",
                            ),

                            html.Label("Catégorie", className="form-label mt-3"),
                            dcc.Dropdown(
                                id="rag-category-dropdown",
                                options=[
                                    {"label": c.replace("_", " ").title(), "value": c}
                                    for c in CATEGORIES
                                ],
                                value="projets",
                                clearable=False,
                                className="custom-dropdown",
                            ),

                            html.Div(
                                id="rag-project-filters",
                                children=[
                                    html.Label("Niveau", className="form-label mt-3"),
                                    dcc.Dropdown(
                                        id="rag-level-dropdown",
                                        options=[{"label": l.title(), "value": l} for l in LEVELS],
                                        value="tous",
                                        clearable=False,
                                        className="custom-dropdown",
                                    ),

                                    html.Label("Mot-clé", className="form-label mt-3"),
                                    dbc.Input(
                                        id="rag-keyword-input",
                                        placeholder="BIM, Kafka, ACV, CAO, IoT...",
                                        type="text",
                                        className="custom-input",
                                    ),
                                ],
                            ),

                            dbc.Button(
                                "Générer la réponse",
                                id="rag-generate-button",
                                n_clicks=0,
                                className="generate-btn",
                            ),
                        ],
                    ),

                    html.Div(
                        className="hint-box",
                        children=[
                            html.H6("Exemples"),
                            html.P("IDU + Projets + Avancé + Spark"),
                            html.P("BEE + Projets + BIM"),
                            html.P("SNI + Projets + IoT"),
                        ],
                    ),
                ],
            ),

            html.Div(
                className="main-content",
                children=[
                    html.Div(
                        className="top-header",
                        children=[
                            html.H1("Assistant d’orientation Polytech"),
                            html.P("Sélectionne une formation, puis explore les métiers, compétences, projets et ressources."),
                        ],
                    ),

                    html.Div(
                        className="chat-panel",
                        children=[
                            html.Div(
                                id="rag-chat-box",
                                className="chat-box",
                                children=[
                                    html.Div(
                                        "Bonjour 👋 Je suis ton assistant Polytech. Choisis une formation et une catégorie pour commencer.",
                                        className="message bot-message",
                                    )
                                ],
                            ),

                            html.Div(
                                className="answer-card",
                                children=[
                                    dcc.Markdown(
                                        id="rag-answer-output",
                                        className="answer-output",
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )