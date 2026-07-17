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
    members: list[str] = []

# --- Vérification du token de service CAS ---
def verify_cas_service_token(x_cas_token: Annotated[Optional[str], Header()] = None):
    expected = os.getenv("INSTANCE_SECRET")
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
    user = get_user(data.email)
    main_role = ""
    if not user:

        logger.info(f"Premier login CAS pour '{data.login}', provisionnement...")

        # Détermination du rôle depuis les groupes CAS
        main_role = _determine_role_from_cas_groups(data.members)

        if main_role is None:
            logger.error(f"Aucun groupe autorisé pour '{data.login}' : {data.members}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas accès à cette application"
            )

        user = _create_cas_user(data, main_role=main_role)

    if not user:
        logger.error(f"Échec provisionnement CAS pour '{data.login}' avec le rôle principal '{main_role}'")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CAS authentication failed"
        )

    logger.info(f"Login CAS réussi pour '{data.login}'")
    return _build_token(user)


def _determine_role_from_cas_groups(members: list[str]) -> str | None:
    """
    Détermine le rôle principal depuis les groupes CAS.
    Les groupes dans .env sont des CN (ex: "personnels-enseignants.polytech").
    Les membres CAS sont des DN complets (ex: "cn=personnels-enseignants.polytech,ou=groups,...").
    On extrait le CN pour comparer.
    """
    # Extrait les CN depuis les DN complets
    # "cn=personnels-enseignants.polytech,ou=groups,dc=uds,dc=fr" → "personnels-enseignants.polytech"
    member_cns = set()
    for dn in members:
        parts = dn.split(",")
        if parts and parts[0].startswith("cn="):
            member_cns.add(parts[0][3:])  # supprime "cn="

    def groups_from_env(key: str) -> set[str]:
        val = os.getenv(key, "").strip()
        return set(val.split()) if val else set()

    # Ordre de priorité : administratif > enseignant > etudiant
    if member_cns & groups_from_env("CAS_ALLOWED_GROUPS_4_ADMINISTRATIF"):
        return "administratif"
    if member_cns & groups_from_env("CAS_ALLOWED_GROUPS_4_ENSEIGNANT"):
        return "enseignant"
    if member_cns & groups_from_env("CAS_ALLOWED_GROUPS_4_ETUDIANT"):
        return "etudiant"

    return None  # aucun groupe autorisé

def _create_cas_user(data: CasUserProvision, main_role) -> dict | None:
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
            (data.login, data.email, data.nom, data.prenom, main_role)
        )
        connection.commit()
        return get_user(data.login, method="byLogin")
    except Exception as e:
        logger.error(f"DB error during CAS provisioning: {e}")
        return None