from dash import Input, Output, State, html
from apc_dash.polytech_rag.app.services.file_service import FileService

def register_callbacks(app):
    service = FileService()

    @app.callback(
        Output("rag-project-filters", "style"),
        Input("rag-category-dropdown", "value")
    )
    def toggle_project_filters(category):
        if category == "projets":
            return {"display": "block"}
        return {"display": "none"}

    @app.callback(
        Output("rag-chat-box", "children"),
        Output("rag-answer-output", "children"),
        Input("rag-generate-button", "n_clicks"),
        State("rag-formation-dropdown", "value"),
        State("rag-category-dropdown", "value"),
        State("rag-level-dropdown", "value"),
        State("rag-keyword-input", "value"),
        prevent_initial_call=True
    )
    def generate_response(n_clicks, formation, category, level, keyword):
        if not keyword:
            keyword = ""

        user_message = f"Formation : {formation.upper()} | Catégorie : {category}"

        if category == "projets":
            user_message += f" | Niveau : {level}"
            if keyword:
                user_message += f" | Mot-clé : {keyword}"

        answer = service.generate_answer(
            formation=formation,
            category=category,
            level=level,
            keyword=keyword
        )

        chat_children = [
            html.Div(
                "Bonjour 👋 Je suis ton assistant Polytech. "
                "Choisis une formation et une catégorie pour commencer.",
                className="chat-message bot-message"
            ),
            html.Div(
                user_message,
                className="chat-message user-message"
            ),
            html.Div(
                "Voici la réponse générée à partir des fichiers PDF.",
                className="chat-message bot-message"
            ),
        ]

        return chat_children, answer