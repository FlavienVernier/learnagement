import os
import mysql.connector

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional
from pydantic import BaseModel

from dependencies import logger, db_connexion, get_user, Token

# --- Schéma pour le provisionnement CAS ---
class CasUserProvision(BaseModel):
    login:  str
    email:  str
    nom:    str
    prenom: str
    type:   str

# --- Vérification du token de service CAS ---
def verify_cas_service_token(x_cas_token: Annotated[Optional[str], Header()] = None):
    expected = os.getenv("CAS_SERVICE_TOKEN")
    if not x_cas_token or x_cas_token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid CAS service token"
        )

async def authenticate_cas(data: CasUserProvision) -> Token:
    """
    Point d'entrée unique pour l'auth CAS.
    Cherche l'user, le crée si premier login, retourne toujours un JWT.
    """
    user = get_user(data.mail)

    if not user:
        logger.info(f"Premier login CAS pour '{data.login}', provisionnement...")
        user = _create_cas_user(data)

    if not user:
        logger.error(f"Échec provisionnement CAS pour '{data.login}'")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CAS authentication failed"
        )

    logger.info(f"Login CAS réussi pour '{data.login}'")
    return _build_token(user)

def _create_cas_user(data: CasUserProvision) -> dict | None:
    """
    INSERT en base pour un nouvel utilisateur CAS.
    À adapter selon ton ORM / connectDB.
    """
    # Exemple brut — remplace par ton pattern SQL/ORM habituel

    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO users (login, email, nom, prenom, type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data.login, data.email, data.nom, data.prenom, data.type)
        )
        connection.commit()
        return get_user(data.login, method="byLogin")
    except Exception as e:
        logger.error(f"DB error during CAS provisioning: {e}")
        return None