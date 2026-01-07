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
    roles: list = []

class UserInDB(User):
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

def get_administratif(user_login: str):
    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM LNM_administratif WHERE mail = %s", (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        user_dict["roles"] = ["user", "administratif"]
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor()
        cursor.execute(
            """SELECT LNM_role.role 
                        FROM LNM_administratif 
                        JOIN LNM_administratif_as_role on LNM_administratif_as_role.id_administratif = LNM_administratif.id_administratif
                        JOIN LNM_role on LNM_role.id_role = LNM_administratif_as_role.id_role
                        WHERE mail = %s""",
            (user_login,))
        roles = cursor.fetchall()
        user_dict["roles"] += [item for t in roles for item in t]
        return UserInDB(**user_dict)
    return None

def get_enseignant(user_login: str):
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
        user_dict["roles"] = ["user", "enseignant"]
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor()
        cursor.execute(
            """SELECT LNM_role.role 
                        FROM LNM_enseignant 
                        JOIN LNM_enseignant_as_role on LNM_enseignant_as_role.id_enseignant = LNM_enseignant.id_enseignant
                        JOIN LNM_role on LNM_role.id_role = LNM_enseignant_as_role.id_role
                        WHERE mail = %s""",
            (user_login,))
        roles = cursor.fetchall()
        user_dict["roles"] += [item for t in roles for item in t]
        return UserInDB(**user_dict)
    return None


def get_etudiant(user_login: str):
    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM LNM_etudiant WHERE mail = %s", (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        user_dict["roles"] = ["user", "etudiant"]
        return UserInDB(**user_dict)
    return None

def get_user(user_login: str):
    administratif = get_administratif(user_login)
    if administratif is not None:
        return get_administratif(user_login)

    enseignant = get_enseignant(user_login)
    if enseignant is not None:
        return get_enseignant(user_login)

    etudiant = get_etudiant(user_login)
    if etudiant is not None:
        return get_etudiant(user_login)

    return None

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
    #if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def has_role(role_required: str):
    async def check_role(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        if role_required not in current_user.roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role

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