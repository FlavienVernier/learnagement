"""
Composant visuel du chatbot APC — bulle flottante + fenêtre de conversation.
"""
from dash import dcc, html, Input, Output, State, callback_context
from dash.exceptions import PreventUpdate

from .apc20_layout import COLORS
from .apc20_chatbot_backend import process_message


# ── Helpers de rendu ──────────────────────────────────────────────

def _bubble(role: str, text: str):
    is_user = role == "user"
    return html.Div(
        [
            html.Div(
                "Vous" if is_user else "Assistant APC",
                style={
                    "fontSize":    "10px",
                    "fontWeight":  "600",
                    "color":       "#9CA3AF",
                    "marginBottom":"3px",
                    "textAlign":   "right" if is_user else "left",
                },
            ),
            html.Div(
                text,
                style={
                    "backgroundColor": COLORS["primary"] if is_user else "#F3F4F6",
                    "color":           "white"            if is_user else "#111827",
                    "borderRadius":    "12px 12px 2px 12px" if is_user else "12px 12px 12px 2px",
                    "padding":         "10px 14px",
                    "fontSize":        "13px",
                    "lineHeight":      "1.5",
                    "whiteSpace":      "pre-wrap",
                    "maxWidth":        "100%",
                    "wordBreak":       "break-word",
                },
            ),
        ],
        style={
            "display":       "flex",
            "flexDirection": "column",
            "alignItems":    "flex-end" if is_user else "flex-start",
            "marginBottom":  "12px",
            "paddingLeft":   "0"        if is_user else "0",
        },
    )


def _render_messages(history: list):
    if not history:
        return [
            html.Div(
                "👋 Bonjour ! Je suis votre assistant APC. Posez-moi une question sur les modules, "
                "les apprentissages critiques ou la couverture du référentiel.",
                style={
                    "color": "#6B7280", "fontSize": "13px", "textAlign": "center",
                    "padding": "20px 10px", "lineHeight": "1.6",
                },
            )
        ]
    return [_bubble(m["role"], m["content"]) for m in history]


# ── Layout ────────────────────────────────────────────────────────

chatbot_layout = html.Div(
    [
        dcc.Store(id="chatbot-open",    data=False),
        dcc.Store(id="chatbot-history", data=[]),

        # ── Bulle flottante ───────────────────────────────────────
        html.Button(
            html.I(className="fa-solid fa-comments", style={"fontSize": "20px"}),
            id="chatbot-toggle",
            title="Assistant APC",
            style={
                "position":        "fixed",
                "bottom":          "24px",
                "right":           "24px",
                "width":           "54px",
                "height":          "54px",
                "borderRadius":    "50%",
                "backgroundColor": COLORS["primary"],
                "color":           "white",
                "border":          "none",
                "cursor":          "pointer",
                "zIndex":          "1001",
                "boxShadow":       "0 4px 14px rgba(59,130,246,0.5)",
                "display":         "flex",
                "alignItems":      "center",
                "justifyContent":  "center",
                "transition":      "transform 0.15s",
            },
        ),

        # ── Fenêtre de chat ───────────────────────────────────────
        html.Div(
            [
                # En-tête
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="fa-solid fa-robot",
                                    style={"marginRight": "8px", "fontSize": "15px"},
                                ),
                                html.Span(
                                    "Assistant APC",
                                    style={"fontWeight": "700", "fontSize": "14px"},
                                ),
                            ],
                            style={"display": "flex", "alignItems": "center"},
                        ),
                        html.Button(
                            html.I(className="fa-solid fa-xmark"),
                            id="chatbot-close",
                            style={
                                "background": "transparent",
                                "border":     "none",
                                "color":      "white",
                                "cursor":     "pointer",
                                "fontSize":   "16px",
                                "padding":    "0",
                            },
                        ),
                    ],
                    style={
                        "display":         "flex",
                        "justifyContent":  "space-between",
                        "alignItems":      "center",
                        "backgroundColor": COLORS["primary"],
                        "color":           "white",
                        "padding":         "12px 16px",
                        "borderRadius":    "12px 12px 0 0",
                        "flexShrink":      "0",
                    },
                ),

                # Zone de messages
                dcc.Loading(
                    html.Div(
                        id="chatbot-messages",
                        children=_render_messages([]),
                        style={
                            "flex":       "1",
                            "overflowY":  "auto",
                            "padding":    "16px",
                            "backgroundColor": "#FAFAFA",
                        },
                    ),
                    type="circle",
                    color=COLORS["primary"],
                ),

                # Zone de saisie
                html.Div(
                    [
                        dcc.Input(
                            id="chatbot-input",
                            type="text",
                            placeholder="Posez votre question...",
                            debounce=False,
                            style={
                                "flex":        "1",
                                "border":      "1px solid #E5E7EB",
                                "borderRadius":"8px",
                                "padding":     "9px 12px",
                                "fontSize":    "13px",
                                "outline":     "none",
                                "fontFamily":  "Inter, sans-serif",
                            },
                        ),
                        html.Button(
                            html.I(className="fa-solid fa-paper-plane"),
                            id="chatbot-send",
                            n_clicks=0,
                            style={
                                "backgroundColor": COLORS["primary"],
                                "color":           "white",
                                "border":          "none",
                                "borderRadius":    "8px",
                                "padding":         "9px 14px",
                                "cursor":          "pointer",
                                "fontSize":        "14px",
                                "flexShrink":      "0",
                            },
                        ),
                    ],
                    style={
                        "display":      "flex",
                        "gap":          "8px",
                        "padding":      "12px",
                        "borderTop":    "1px solid #E5E7EB",
                        "backgroundColor": "white",
                        "borderRadius": "0 0 12px 12px",
                        "flexShrink":   "0",
                    },
                ),
            ],
            id="chatbot-panel",
            style={
                "display":       "none",
                "position":      "fixed",
                "bottom":        "90px",
                "right":         "24px",
                "width":         "370px",
                "height":        "500px",
                "borderRadius":  "12px",
                "boxShadow":     "0 8px 30px rgba(0,0,0,0.18)",
                "zIndex":        "1000",
                "flexDirection": "column",
                "fontFamily":    "Inter, sans-serif",
                "overflow":      "hidden",
            },
        ),
    ]
)


# ── Callbacks ─────────────────────────────────────────────────────

def register_callbacks(app):

    # ── Ouverture / fermeture du panneau ──────────────────────────
    @app.callback(
        Output("chatbot-open", "data"),
        Input("chatbot-toggle", "n_clicks"),
        Input("chatbot-close",  "n_clicks"),
        State("chatbot-open",   "data"),
        prevent_initial_call=True,
    )
    def toggle_chat(n_toggle, n_close, is_open):
        ctx = callback_context
        triggered = ctx.triggered[0]["prop_id"].split(".")[0]
        if triggered == "chatbot-close":
            return False
        return not is_open

    @app.callback(
        Output("chatbot-panel", "style"),
        Input("chatbot-open", "data"),
        prevent_initial_call=False,
    )
    def show_panel(is_open):
        base = {
            "position":      "fixed",
            "bottom":        "90px",
            "right":         "24px",
            "width":         "370px",
            "height":        "500px",
            "borderRadius":  "12px",
            "boxShadow":     "0 8px 30px rgba(0,0,0,0.18)",
            "zIndex":        "1000",
            "flexDirection": "column",
            "fontFamily":    "Inter, sans-serif",
            "overflow":      "hidden",
        }
        base["display"] = "flex" if is_open else "none"
        return base

    # ── Envoi d'un message ────────────────────────────────────────
    @app.callback(
        Output("chatbot-history",  "data"),
        Output("chatbot-messages", "children"),
        Output("chatbot-input",    "value"),
        Input("chatbot-send",  "n_clicks"),
        Input("chatbot-input", "n_submit"),
        State("chatbot-input",   "value"),
        State("chatbot-history", "data"),
        State("token",           "data"),
        prevent_initial_call=True,
    )
    def send_message(n_clicks, n_submit, message, history, token):
        if not message or not message.strip():
            raise PreventUpdate

        history = history or []

        if not token or token == "none":
            new_history = history + [
                {"role": "user",      "content": message.strip()},
                {"role": "assistant", "content": "⚠️ Session non authentifiée. Veuillez vous reconnecter."},
            ]
            return new_history, _render_messages(new_history), ""

        new_history = history + [{"role": "user", "content": message.strip()}]
        response    = process_message(message.strip(), history, token)
        new_history = new_history + [{"role": "assistant", "content": response}]

        return new_history, _render_messages(new_history), ""
