from auth import login_throttle
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from api.dependencies import logger, get_user
from models.token import Token
from auth.authenticate_tools import create_access_token


password_hash = PasswordHash((BcryptHasher(),))

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def __authenticate_user_lnm(user_login: str, password: str):
    user = get_user(user_login)
    if not user:
        logger.info(f"User {user_login} does not exist")
        return None

    if not verify_password(password, user.password):
        logger.info(f"User {user_login} password does not match")
        return None
    return user

async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
) -> Token:
    ip = request.client.host if request.client else "unknown"
    login_throttle.check(form_data.username, ip)          # 429 avant tout travail

    user = __authenticate_user_lnm(form_data.username, form_data.password)
    if not user:
        login_throttle.register_failure(form_data.username, ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Réinitialisation du nombre de tentatives en cas de login success
    login_throttle.reset(form_data.username, ip)

    access_token = create_access_token(
        data={"id": user.id,
              "login": user.mail,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              },
    )
    logger.info(f"LNM user {user.mail} connected with roles {user.roles}")
    return Token(access_token=access_token, token_type="bearer")


def logout():
    return {"message": "Logout page in construction"}
