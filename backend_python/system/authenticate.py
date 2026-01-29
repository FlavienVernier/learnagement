import os
import dotenv
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import get_user, Token

from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from typing import Annotated

import mysql.connector

logger = logging.getLogger(__name__)

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SESSION_TIMEOUT"))

router = APIRouter()

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



def authenticate_user(user_login: str, password: str):
    user = get_user(user_login)
    if not user:
        logger.info(f"User {user_login} does not exist")
        return False

    if not verify_password(password, user.password):
        logger.info(f"User {user_login} password does not match")
        return False
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              }, expires_delta=access_token_expires
    )
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