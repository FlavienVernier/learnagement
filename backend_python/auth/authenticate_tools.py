import os
import dotenv
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import logger, get_user, Token

from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("SESSION_TIMEOUT"))



# def authenticate_user(user_login: str, password: str, method: str = "byMail"):
#     if method == "LNM":
#         user = get_user(user_login, method=method)
#         if not user:
#             logger.info(f"User {user_login} does not exist")
#             return False
#
#         if not verify_password(password, user.password):
#             logger.info(f"User {user_login} password does not match")
#             return False
#     elif method == "LDAP":
#         is_ldap_user = validate_ldap(user_login, password)
#         if not is_ldap_user:
#             logger.info(f"Incorect LDAP user or password")
#             return False
#         user = get_user_from_ldap(user_login)
#     return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

