import os
import dotenv
import logging
import json

import sqlalchemy
import mysql.connector

from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')

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
    id: int
    prenom: str
    nom: str
    mail: str | None = None
    ExplicitSecondaryK: str
    roles: list = []
    password2update: bool = False

class UserInDB(User):
    password: str

class SQLRequest(BaseModel):
    request: str
    params: dict | None = None
    allowedRolesRequester: list[str]

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
        cursor.execute("""SELECT LNM_administratif.id_administratif AS id, 
                                 LNM_administratif.*, 
                                 ExplicitSecondaryKs_LNM_administratif.ExplicitSecondaryK
                          FROM LNM_administratif 
                          JOIN ExplicitSecondaryKs_LNM_administratif ON ExplicitSecondaryKs_LNM_administratif.id_administratif = LNM_administratif.id_administratif
                          WHERE mail = %s""", (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        if not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["roles"] = ["user", "administratif", users[0]['ExplicitSecondaryK']]
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
        cursor.execute("""
                       SELECT LNM_enseignant.id_enseignant AS id, 
                              LNM_enseignant.*,
                              ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK
                       FROM LNM_enseignant 
                       JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
                       WHERE mail = %s""",
                       (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        if not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["roles"] = ["user", "enseignant", users[0]['ExplicitSecondaryK']]
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
        cursor.execute("""SELECT LNM_etudiant.id_etudiant AS id, 
                                 LNM_etudiant.*,
                                 ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK
                          FROM LNM_etudiant 
                          JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                          WHERE mail = %s""",
                       (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        if not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["roles"] = ["user", "etudiant", users[0]['ExplicitSecondaryK']]
        return UserInDB(**user_dict)
    return None

def get_user(user_login: str):
    administratif = get_administratif(user_login)
    user = None
    if administratif is not None:
        user = get_administratif(user_login)

    enseignant = get_enseignant(user_login)
    if enseignant is not None:
        user = get_enseignant(user_login)

    etudiant = get_etudiant(user_login)
    if etudiant is not None:
        user = get_etudiant(user_login)
    if user is not None:
        logger.info(f"User {user_login} logged as {user}")
    else:
        logger.error(f"Logging error with login: {user_login}")
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #print(token, flush=True)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userlogin = payload.get("email")
        #print("userlogin", userlogin, flush=True)
        if userlogin is None:
            logger.error(f"Login error with payload: {payload}")
            raise credentials_exception
        token_data = TokenData(mail=userlogin)
        #print("token_data", token_data, flush=True)
    except InvalidTokenError as e:
        logger.error(f"Invalid token : {e}")
        raise credentials_exception
    user = get_user(token_data.mail)
    if user is None:
        logger.error(f"Login error with payload: {payload}")
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
            logger.error(f"User {current_user.id} has no role {role_required}")
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role



def db_request(requester: User, request: SQLRequest):
    if not "anonymous" in request.allowedRolesRequester:
        # check if there is no intersection between requester roles and request allowed roles
        if not bool(set(requester.roles) & set(request.allowedRolesRequester)):
            logger.error(f"User {requester.id} hasn't role {request.allowedRolesRequester}")
            raise HTTPException(status_code=403, detail="Unauthorized access")

    if requester:
        logger.info(f"User {requester.id} has role {requester.roles} requests {request}")
    else:
        logger.info(f"Anonymous user requests {request}")

    rows = []
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)

        if request.params:
            cursor.execute(request.request, request.params)
            #cursor.execute(sqlalchemy.text(request.request), request.params)
        else:
            cursor.execute(request.request)
            #cursor.execute(sqlalchemy.text(request.request))

        rows = cursor.fetchall()
        #logger.info(f"User {requester.id} has {rows}")
        connection.commit()
        connection.close()
    except Exception as e:
        logger.exception(e)
    finally:
        cursor.close()
        connection.close()
    #return json.dumps([dict(ix) for ix in rows]) # return string
    return [dict(ix) for ix in rows] # return list that will be converted to json

def main():
    return True

if __name__ == '__main__':
    main()