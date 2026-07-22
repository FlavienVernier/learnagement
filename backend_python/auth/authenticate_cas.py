import os
import json
import mysql.connector

from fastapi import HTTPException, status, Header
from typing import Annotated, Optional
from pydantic import BaseModel

from models.token import Token
from api.dependencies import logger, get_user
from db.connection import db_connexion
from auth.authenticate_tools import create_access_token


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
    user = get_user(data.login, method="byLogin")
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

    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles": user.roles,
              "password2update": False
              },
    )

    logger.info(f"CAS user {user.mail} connected with roles {user.roles}")
    logger.info(user)

    return Token(access_token=access_token, token_type="bearer")


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


def _create_cas_user(data: CasUserProvision, main_role: str) -> dict | None:
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)

        if main_role == "enseignant":
            cursor.execute(
                """
                INSERT INTO LNM_enseignant 
                    (prenom, nom, mail, login, password, `service statutaire`, décharge)
                VALUES (%s, %s, %s, %s, NULL, 192, 0)
                """,
                (data.prenom, data.nom, data.email, data.login)
            )

        elif main_role == "administratif":
            cursor.execute(
                """
                INSERT INTO LNM_administratif 
                    (nom, prenom, mail, login, password)
                VALUES (%s, %s, %s, %s, NULL)
                """,
                (data.nom, data.prenom, data.email, data.login)
            )

        elif main_role == "etudiant":
            id_promo = _determine_promo_from_cas_groups(data.members)
            if id_promo is None:
                logger.error(f"Aucune promo trouvée pour '{data.login}' : {data.members}")
                return None
            cursor.execute(
                """
                INSERT INTO LNM_etudiant 
                    (nom, prenom, mail, login, password, id_promo)
                VALUES (%s, %s, %s, %s, NULL, %s)
                """,
                (data.nom, data.prenom, data.email, data.login, id_promo)
            )

        else:
            logger.error(f"Rôle inconnu '{main_role}' pour '{data.login}'")
            return None

        connection.commit()
        return get_user(data.login, method="byLogin")

    except Exception as e:
        logger.error(f"DB error during CAS provisioning: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()


def _determine_promo_from_cas_groups(members: list[str]) -> int | None:
    """
    Détermine l'id_promo d'un étudiant depuis ses groupes CAS
    en croisant avec CAS_ETUDIANTS_2_PROMO du .env.

    CAS_ETUDIANTS_2_PROMO est un JSON :
    [{"groupe": "etudiants-ige4-idu", "promo": "IDU FISE 4 Annecy"}, ...]
    """
    # Extrait les CNs des groupes de l'étudiant
    member_cns = set()
    for dn in members:
        parts = dn.split(",")
        if parts and parts[0].startswith("cn="):
            member_cns.add(parts[0][3:])

    # Charge le mapping groupe → nom de promo depuis .env
    raw = os.getenv("CAS_ETUDIANTS_2_PROMO", "[]")
    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("CAS_ETUDIANTS_2_PROMO mal formé dans .env")
        return None

    # Cherche la première correspondance
    promo_name = None
    for entry in mapping:
        if entry["groupe"] in member_cns:
            promo_name = entry["promo"]
            break

    if promo_name is None:
        logger.warning(f"Aucun groupe étudiant connu parmi : {member_cns}")
        return None

    # Résout le nom de promo → id_promo en BD
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT LNM_promo.id_promo
            FROM LNM_promo
            JOIN ExplicitSecondaryKs_LNM_promo 
                ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            WHERE ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK = %s
            """,
            (promo_name,)
        )
        row = cursor.fetchone()
        return row["id_promo"] if row else None
    except Exception as e:
        logger.error(f"DB error lors de la résolution de promo '{promo_name}': {e}")
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()



# def _create_cas_user(data: CasUserProvision, main_role) -> dict | None:
#     """
#     INSERT en base pour un nouvel utilisateur CAS.
#     À adapter selon ton ORM / connectDB.
#     """
#     # Exemple brut — remplace par ton pattern SQL/ORM habituel
#
#     try:
#         connection = mysql.connector.connect(**db_connexion())
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute(
#             """
#             INSERT INTO users (login, email, nom, prenom, type)
#             VALUES (%s, %s, %s, %s, %s)
#             """,
#             (data.login, data.email, data.nom, data.prenom, main_role)
#         )
#         connection.commit()
#         return get_user(data.login, method="byLogin")
#     except Exception as e:
#         logger.error(f"DB error during CAS provisioning: {e}")
#         return None