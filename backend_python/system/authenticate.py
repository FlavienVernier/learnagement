import os
import dotenv
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependencies import get_token_header, db_connexion

from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from typing import Annotated
from pydantic import BaseModel

import mysql.connector

logger = logging.getLogger(__name__)

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SESSION_TIMEOUT"))


# router = APIRouter(
#     prefix="/authenticate",
#     tags=["authenticate"],
#     dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )
router = APIRouter()

@router.post("/authenticate")
def authenticate(username:str, password:str):
    return {"message": "Auth page in construction Mr. " + username}

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    prenom: str
    nom: str
    mail: str | None = None


class UserInDB(User):
    password: str

#password_hash = PasswordHash.recommended()
password_hash = PasswordHash((BcryptHasher(),))

#import bcrypt

#bcrypt.checkpw(
#    b"toto",
#    b"$2y$10$zESfySbjXHm5w52l.eU4pe4L3lyiK5TPnLaNm7ca9Nqi9W74qxgVO"
#)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


#def get_password_hash(password):
#    return password_hash.hash(password)


def get_user(user_login: str):
    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        #cursor = db_connexion()
        cursor.execute("SELECT * FROM LNM_enseignant WHERE mail = %s", (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        user_dict["type"] = "enseignant"
        return UserInDB(**user_dict)

def authenticate_user(user_login: str, password: str):
    user = get_user(user_login)
    if not user:
        return False

    if not verify_password(password, user.password):
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

@router.post("/token")
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
        data={"sub": user.mail}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
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