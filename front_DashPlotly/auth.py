import logging
import os
import jwt
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from functools import wraps

from flask import redirect, session, request, jsonify
from dash import Dash,  Input, Output, State

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')

load_dotenv()

def _load_signing_key() -> str:
    key = os.getenv("JWT_SIGNING_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "JWT_SIGNING_KEY est absente ou vide : refus de démarrer sans clé de signature."
        )
    if len(key) < 32:  # HS256 : au moins 256 bits recommandés
        raise RuntimeError("JWT_SIGNING_KEY trop courte (32 caractères minimum).")
    return key

# Échoue à l'import, donc au démarrage de l'application
SECRET_KEY = _load_signing_key()

def decode_token(token, leeway=30) -> dict:
    """Décode et vérifie le JWT. Lève jwt.InvalidTokenError sinon."""
    if not token:
        raise jwt.InvalidTokenError("Token manquant")

    return jwt.decode(
        token,
        key=SECRET_KEY,
        algorithms=["HS256"],            # liste fermée, jamais "none"
        leeway=timedelta(seconds=leeway),
        options={
            "verify_signature": True,    # jamais conditionnel
            "verify_exp": True,
            "require": ["exp"],          # un token sans expiration est refusé
        },
    )


def is_token_valid(token, leeway=30) -> bool:
    try:
        decode_token(token, leeway)
        return True
    except jwt.InvalidTokenError:        # plus de `except:` nu
        return False

class FlaskAuth(Dash):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Intercepter toutes les requêtes de callback
        @self.server.before_request
        def check_authentication():

            # Vérifier si c'est un callback Dash
            if request.path != '/_dash-update-component':
                return None

            data = request.get_json(silent=True) or {}
            output = data.get("output", "")

            if output == "token.data":
                return None

            if not is_token_valid(session.get("token")):
                session.pop("token", None)
                return jsonify({"error": "unauthorized"}), 401
            return None
