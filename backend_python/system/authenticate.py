import os
import dotenv
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import logger, get_user, Token

from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from typing import Annotated

import mysql.connector


dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("SESSION_TIMEOUT"))

router = APIRouter()

def validate_ldap(user_login, password):
    import ldap

    LDAP_HOST = os.getenv("LDAP_HOST")
    LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
    LDAP_UID_ATTR = os.getenv("LDAP_UID_ATTR", "uid")  # "uid" par défaut

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

    except ldap.INVALID_CREDENTIALS:
        print("Erreur : identifiants invalides.")
    except ldap.SERVER_DOWN:
        print("Erreur : serveur LDAP inaccessible.")
    finally:
        conn.unbind_s()





# @router.post("/authenticate",
#     tags=["Auth"],
#     summary="User login",
#     description="Authenticate user and return JWT token")
# def authenticate(username:str, password:str):
# #def authenticate(data: AuthRequest):
#     return {"message": "Auth page in construction Mr. " + username}

password_hash = PasswordHash((BcryptHasher(),))

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)



def authenticate_user(user_login: str, password: str, method: str = "LNM"):
    if method == "LNM":
        user = get_user(user_login)
        if not user:
            logger.info(f"User {user_login} does not exist")
            return False

        if not verify_password(password, user.password):
            logger.info(f"User {user_login} password does not match")
            return False
    elif method == "LDAP":
        is_ldap_user = validate_ldap(user_login, password)
        if not is_ldap_user:
            logger.info(f"Incorect LDAP user or password")
            return False
        user = get_user_from_ldap(user_login)
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token",
    tags=["Auth"],
    summary="Token",
    description="Authenticate user and return JWT token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    logger.info(f"Token timeout {access_token_expires}")
    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              }, expires_delta=access_token_expires
    )
    logger.info(f"User {user.mail} connected with roles {user.roles}")
    return Token(access_token=access_token, token_type="bearer")


@router.post("/tokenViaLDAB",
    tags=["Auth"],
    summary="Token",
    description="Authenticate user and return JWT token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, methode="LDAP")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    logger.info(f"Token timeout {access_token_expires}")
    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              }, expires_delta=access_token_expires
    )
    logger.info(f"User {user.mail} connected with roles {user.roles}")
    return Token(access_token=access_token, token_type="bearer")
@router.post("/logout",
    tags=["Auth"],
    summary="User logout",
    description="...")
def logout():
    return {"message": "Logout page in construction"}

def permission(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def main():
    return {"message": "authenticate module"}

if __name__ == '__main__':
    main()