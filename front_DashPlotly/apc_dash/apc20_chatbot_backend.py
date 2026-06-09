"""
Backend du chatbot APC — appel API REST Groq (compatible OpenAI) via requests.
Aucune dépendance externe requise.
"""
import os
import json
import logging
import requests as http

from .apc20_chatbot_tools import GEMINI_TOOLS, execute_tool


_API_URL = "https://api.groq.com/openai/v1/chat/completions"
_MODEL   = "llama-3.3-70b-versatile"

_SYSTEM = """Tu es un assistant pédagogique expert en Approche Par Compétences (APC) \
pour une formation universitaire de type BUT/IUT.

Tu aides les enseignants à explorer et comprendre :
- Les modules de la formation et leurs apprentissages critiques (AC)
- Les compétences du référentiel et leur couverture par niveau (N1, N2, N3)
- Les trous du référentiel (AC sans ancrage fort, modules à ancrage faible)
- Les statistiques et la structure globale de la formation

RÈGLES :
- Utilise toujours les outils disponibles pour obtenir les données réelles de la BD
- Ne jamais inventer de noms de modules, d'AC ou de données chiffrées
- Si tu as besoin de plusieurs informations, enchaîne plusieurs appels d'outils
- Réponds toujours en français, de façon claire et structurée
- Pour les listes longues, résume et mets en avant les points importants
- Si une question est hors du périmètre APC/pédagogique, dis poliment que tu es \
spécialisé uniquement dans ce domaine

Rappel sur les types de liens module–AC :
- Requis : l'AC est fondamental, l'étudiant doit le maîtriser via ce module
- Recommandé : l'AC est important mais non obligatoire
- Complémentaire : l'AC est abordé de façon secondaire
"""

_MAX_ITERATIONS = 8


def _groq_tools():
    """Convertit les définitions GEMINI_TOOLS au format OpenAI/Groq."""
    return [
        {"type": "function", "function": {
            "name":        t["name"],
            "description": t["description"],
            "parameters":  t.get("parameters", {"type": "object", "properties": {}}),
        }}
        for t in GEMINI_TOOLS
    ]


def process_message(message: str, history: list, token: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return (
            "⚠️ Clé API Groq non configurée. "
            "Créez un compte sur groq.com et ajoutez `GROQ_API_KEY=...` dans le fichier `.env`."
        )

    # Construire les messages au format OpenAI
    messages = [{"role": "system", "content": _SYSTEM}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "connected_user", "content": message})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    }

    for iteration in range(_MAX_ITERATIONS):
        body = {
            "model":       _MODEL,
            "messages":    messages,
            "tools":       _groq_tools(),
            "tool_choice": "auto",
            "max_tokens":  1500,
        }

        resp = http.post(_API_URL, headers=headers, json=body, timeout=60)

        if resp.status_code == 429:
            return "⏳ Limite de requêtes Groq atteinte. Réessayez dans quelques secondes."
        if resp.status_code == 401:
            return "⚠️ Clé API Groq invalide. Vérifiez votre `GROQ_API_KEY`."
        if not resp.ok:
            try:
                detail = resp.json().get("error", {}).get("message", resp.text[:200])
            except Exception:
                detail = resp.text[:200]
            return f"⚠️ Erreur API Groq ({resp.status_code}) : {detail}"

        data        = resp.json()
        choice      = data["choices"][0]
        msg_out     = choice["message"]
        finish      = choice.get("finish_reason", "stop")

        logging.info(f"[chatbot] iter={iteration} finish_reason={finish}")

        # Réponse textuelle finale
        if finish == "stop" or not msg_out.get("tool_calls"):
            return msg_out.get("content") or "Aucune réponse générée."

        # Appels d'outils
        messages.append(msg_out)

        for tc in msg_out["tool_calls"]:
            fn_name = tc["function"]["name"]
            try:
                fn_args = json.loads(tc["function"]["arguments"])
            except (json.JSONDecodeError, TypeError):
                fn_args = {}

            logging.info(f"[chatbot] tool={fn_name} args={fn_args}")
            result = execute_tool(fn_name, fn_args, token)

            messages.append({
                "role":         "tool",
                "tool_call_id": tc["id"],
                "content":      result,
            })

    return "Je n'ai pas pu générer une réponse complète. Veuillez reformuler votre question."
