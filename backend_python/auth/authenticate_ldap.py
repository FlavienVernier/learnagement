import os
import dotenv
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import logger, get_user, Token
from auth.authenticate_tools import create_access_token

dotenv.load_dotenv(".env")

LDAP_HOST = os.getenv("LDAP_HOST")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
LDAP_UID_ATTR = os.getenv("LDAP_UID_ATTR", "uid")  # "uid" par défaut

def authenticate_user_ldap(user_login: str, password: str):

    is_ldap_user = validate_ldap(user_login, password)
    if not is_ldap_user:
        logger.info(f"Incorect LDAP user or password")
        return None
    user = get_user(user_login, method="byLogin")
    return user

def validate_ldap(user_login, password):
    import ldap

    # Connexion au serveur LDAP
    conn = ldap.initialize(LDAP_HOST)

    # Paramètres de bind
    dn = f"{LDAP_UID_ATTR}={user_login},{LDAP_BASE_DN}"

    try:
        # Authentification (équivalent du -x -D -W)
        conn.simple_bind_s(dn, password)

        # Équivalent du ldapwhoami : extended operation "Who Am I?"
        res = conn.whoami_s()
        print("You are:", res)
        return True

    except ldap.INVALID_CREDENTIALS:
        print("Erreur : identifiants invalides.")
        return False
    except ldap.SERVER_DOWN:
        print("Erreur : serveur LDAP inaccessible.")
        return False
    finally:
        conn.unbind_s()

async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user_ldap(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              },
    )
    logger.info(f"User {user.mail} connected with roles {user.roles}")
    return Token(access_token=access_token, token_type="bearer")

def logout():
    return {"message": "Logout page in construction"}