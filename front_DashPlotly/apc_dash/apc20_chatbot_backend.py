"""
Backend du chatbot APC — appel API REST Gemini via requests (pas de dépendance externe).
"""
import os
import logging
import requests as http

from .apc20_chatbot_tools import GEMINI_TOOLS, execute_tool


_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

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


def process_message(message: str, history: list, token: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "⚠️ Clé API Gemini non configurée. "
            "Ajoutez `GEMINI_API_KEY=...` dans le fichier `.env`."
        )

    # Construire l'historique au format Gemini (role: user/model)
    contents = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    contents.append({"role": "user", "parts": [{"text": message}]})

    body = {
        "system_instruction": {"parts": [{"text": _SYSTEM}]},
        "tools": [{"function_declarations": GEMINI_TOOLS}],
        "contents": contents,
    }

    for iteration in range(_MAX_ITERATIONS):
        resp = http.post(
            f"{_API_URL}?key={api_key}",
            json=body,
            timeout=60,
        )

        if resp.status_code == 429:
            return "⏳ Limite de requêtes atteinte (tier gratuit Gemini). Attendez quelques secondes avant de réessayer."
        if resp.status_code == 403:
            return "⚠️ Clé API invalide ou accès refusé. Vérifiez votre `GEMINI_API_KEY`."
        if not resp.ok:
            try:
                detail = resp.json().get("error", {}).get("message", resp.text[:200])
            except Exception:
                detail = resp.text[:200]
            return f"⚠️ Erreur API Gemini ({resp.status_code}) : {detail}"

        data = resp.json()

        candidate = data["candidates"][0]
        parts      = candidate["content"]["parts"]

        # Collecter les appels de fonctions
        function_calls = [p["functionCall"] for p in parts if "functionCall" in p]

        if not function_calls:
            # Réponse textuelle finale
            text_parts = [p["text"] for p in parts if "text" in p]
            return "\n".join(text_parts)

        # Ajouter la réponse du modèle (avec les function calls) à l'historique
        logging.info(f"[chatbot] iter={iteration} — {len(function_calls)} appel(s) d'outil")
        body["contents"].append({"role": "model", "parts": parts})

        # Exécuter les outils et renvoyer les résultats
        function_responses = []
        for fc in function_calls:
            logging.info(f"[chatbot] tool={fc['name']} args={fc.get('args', {})}")
            result = execute_tool(fc["name"], fc.get("args", {}), token)
            function_responses.append({
                "functionResponse": {
                    "name":     fc["name"],
                    "response": {"result": result},
                }
            })

        body["contents"].append({"role": "user", "parts": function_responses})

    return "Je n'ai pas pu générer une réponse complète. Veuillez reformuler votre question."
