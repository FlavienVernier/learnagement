import logging
import os
import jwt
from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import redirect, session, jsonify
from dash import Dash,  Input, Output, State

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')

def is_token_valid(token, leeway=30):
    """
    Vérifie si le token est valide et non expiré

    Args:
        token: Le JWT à valider

        leeway: Marge en secondes pour l'expiration (utile pour clock skew)

    Returns:
        bool: True si le token est valide, False sinon
    """
    try:
        decode_token(token, leeway)
        return True
    except:
        return False

def decode_token(token, leeway=30):
    """
    Décode le token s'il est valide et non expiré

    Args:
        token: Le JWT à valider

        leeway: Marge en secondes pour l'expiration (utile pour clock skew)

    Returns:
        dict: dictionaire contenant les données du token

    Raises:
        Exception: Si le token est non valide ou expiré
    """

    if not token:
        return False
    secret_key = os.getenv("INSTANCE_SECRET")
    try:
        decode_options = {
            "verify_signature": bool(secret_key),
            "verify_exp": True
        }

        decode_kwargs = {
            "options": decode_options,
            "leeway": timedelta(seconds=leeway)
        }

        if secret_key:
            decode_kwargs["key"] = secret_key
            decode_kwargs["algorithms"] = ["HS256"]

        payload = jwt.decode(token, **decode_kwargs)
        logging.info(payload.__repr__())
        return payload

    except jwt.ExpiredSignatureError as e:
        logging.exception("Token expiré")
        raise

    except jwt.InvalidTokenError as e:
        logging.exception(f"Token invalide")
        raise

class FlaskAuth(Dash):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Intercepter toutes les requêtes de callback
        @self.server.before_request
        def check_authentication():
            from flask import request

            # Vérifier si c'est un callback Dash
            if request.path == '/_dash-update-component':
                data = request.get_json(silent=True)

                if data and "output" in data:

                    # Autoriser le callback qui écrit dans 'token'
                    if "token.data" in data["output"]:
                        return  # on laisse passer

                token = session.get('token')
                logging.info(f"Token: {token}")

                if not is_token_valid(token):
                    session.pop('token', None)
                    #print("Redirection-", flush=True)
                    logging.info(f"destroy token")
                    return
