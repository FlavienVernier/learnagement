import os
import dotenv
import logging
import json

import mysql.connector

from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

logger = logging.getLogger(__name__)

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    mail: str | None = None

class User(BaseModel):
    prenom: str
    nom: str
    mail: str | None = None

class UserInDB(User):
    type: str
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")

def db_connexion():
    try:
        db_info={
            "host": os.getenv("MYSQL_SERVER"),
            "user": os.getenv("MYSQL_USER_LOGIN"),
            "port": int(os.getenv("MYSQL_PORT")),
            "password": os.getenv("MYSQL_USER_PASSWORD"),
            "database": os.getenv("MYSQL_DB"),}
        return db_info
    except Exception as e:
        logger.exception(e)
        raise e

def get_user(user_login: str):
    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM LNM_enseignant WHERE mail = %s", (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        user_dict["type"] = "enseignant"
        return UserInDB(**user_dict)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userlogin = payload.get("sub")
        if userlogin is None:
            raise credentials_exception
        token_data = TokenData(mail=userlogin)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.mail)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    #if current_user.disabled: utfytfugy
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def db_request(sql_request):
    rows = []
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_request)
        rows = cursor.fetchall()
        connection.commit()
        connection.close()
    except Exception as e:
        logger.exception(e)
    return json.dumps([dict(ix) for ix in rows])

def main():
    return True

if __name__ == '__main__':
    main()