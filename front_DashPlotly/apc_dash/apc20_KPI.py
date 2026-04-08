from dash import html, Input, Output, State
import dash_bootstrap_components as dbc
from app_tools import get_endpoint, get_python_backend_url
from dash import html

apc_layout = html.Div(
    [
        html.H2(
            "Vue d'ensemble de Polytech Annecy",
            style={
                "textAlign": "center",
                "color": "#1f3c88",
                "marginBottom": "30px",
                "fontSize": "32px",
                "fontWeight": "bold",
            },
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "APPRENTISSAGES CRITIQUES",
                            style={
                                "fontSize": "16px",
                                "color": "#555",
                                "marginBottom": "12px",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.H2(
                            id="card_apprentissages",
                            style={
                                "fontSize": "38px",
                                "color": "#1f3c88",
                                "margin": "12px 0",
                                "fontWeight": "bold",
                            },
                        ),
                       
                    ],
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "padding": "25px",
                        "width": "250px",
                        "minHeight": "180px",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.12)",
                        "textAlign": "center",
                    },
                ),

                html.Div(
                    [
                        html.H4(
                            " NOMBRE TOTALE DE COMPÉTENCES",
                            style={
                                "fontSize": "16px",
                                "color": "#555",
                                "marginBottom": "12px",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.H2(
                            id="card_competences",
                            style={
                                "fontSize": "38px",
                                "color": "#1f3c88",
                                "margin": "12px 0",
                                "fontWeight": "bold",
                            },
                        ),
                      
                    ],
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "padding": "25px",
                        "width": "250px",
                        "minHeight": "180px",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.12)",
                        "textAlign": "center",
                    },
                ),

                html.Div(
                    [
                        html.H4(
                            " NOMBRE TOTALE DE MODULES",
                            style={
                                "fontSize": "16px",
                                "color": "#555",
                                "marginBottom": "12px",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.H2(
                            id="card_modules",
                            style={
                                "fontSize": "38px",
                                "color": "#1f3c88",
                                "margin": "12px 0",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                           "",
                            style={
                                "fontSize": "14px",
                                "color": "#777",
                                "marginTop": "10px",
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "padding": "25px",
                        "width": "250px",
                        "minHeight": "180px",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.12)",
                        "textAlign": "center",
                    },
                ),

                html.Div(
                    [
                        html.H4(
                            "COMPOSANTES ESSENTIELLES",
                            style={
                                "fontSize": "16px",
                                "color": "#555",
                                "marginBottom": "12px",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.H2(
                            id="card_composantes",
                            style={
                                "fontSize": "38px",
                                "color": "#1f3c88",
                                "margin": "12px 0",
                                "fontWeight": "bold",
                            },
                        ),
                       
                    ],
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "16px",
                        "padding": "25px",
                        "width": "250px",
                        "minHeight": "180px",
                        "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.12)",
                        "textAlign": "center",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "justifyContent": "center",
            },
        ),
    ],
    style={
        "padding": "30px",
        "backgroundColor": "#f4f6fb",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif",
    },
)

def register_callbacks(app):

    @app.callback(
        Output("card_apprentissages", "children"),
        Output("card_competences", "children"),
        Output("card_modules", "children"),
        Output("card_composantes", "children"),
        Input('user_id', 'data'),
        State('token', 'data'),
    )
    def update_cards(user_id,token):

        url = get_python_backend_url("/acp_kpi/")
    

        data = get_endpoint(url, token)
        print(data)

        if data is None or data.empty:
            print("Aucune donnée")
            return 0, 0, 0, 0

        # calcul des KPI
        
        nb_comp = data["nb_competences"][0]["nb_competences"]
        nb_mod = data["nb_module"][0]["nb_module"]
        nb_ac = data["nb_ac"][0]["nb_ac"]
        nb_compose = data["nb_composante_essentielle"][0]["nb_composante_essentielle"]
        return nb_ac, nb_comp, nb_mod, nb_compose