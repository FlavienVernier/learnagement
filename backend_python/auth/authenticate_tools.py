import os
import dotenv

from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from fastapi import HTTPException, status

dotenv.load_dotenv(".env")

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY")
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
    encoded_jwt = jwt.encode(to_encode, JWT_SIGNING_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Décode et valide un JWT. Lève HTTPException(401) si invalide."""
    try:
        return jwt.decode(token, JWT_SIGNING_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e