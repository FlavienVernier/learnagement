import dotenv

import mysql.connector
from db.connection import db_connexion
from models.request import SQLRequest
from models.token import TokenData
from models.user import User, UserInDB
from core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from core.logging import logger

from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Header, HTTPException, Depends, status

from access_control.checker import check_access



dotenv.load_dotenv("../.env")

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def get_administratif(user_login: str):

    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"""SELECT LNM_administratif.id_administratif AS id, 
                                 LNM_administratif.*, 
                                 ExplicitSecondaryKs_LNM_administratif.ExplicitSecondaryK
                          FROM LNM_administratif 
                          JOIN ExplicitSecondaryKs_LNM_administratif ON ExplicitSecondaryKs_LNM_administratif.id_administratif = LNM_administratif.id_administratif
                          WHERE login = %s""",
                       (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        if user_dict.get("intern_account") != 0  and not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["main_role"] = "administratif"
        user_dict["roles"] = ["connected_user", user_dict["main_role"], users[0]['ExplicitSecondaryK']]
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT LNM_role.role 
                        FROM LNM_administratif 
                        JOIN LNM_administratif_as_role on LNM_administratif_as_role.id_administratif = LNM_administratif.id_administratif
                        JOIN LNM_role on LNM_role.id_role = LNM_administratif_as_role.id_role
                        WHERE login = %s""",
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
        cursor.execute(f"""
                       SELECT LNM_enseignant.id_enseignant AS id, 
                              LNM_enseignant.*,
                              ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK
                       FROM LNM_enseignant 
                       JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
                       WHERE login = %s""",
                       (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]
        logger.info(f"{user_dict['intern_account']}, {type(user_dict['intern_account'])}")
        if user_dict.get("intern_account") != 0  and not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["main_role"] = "enseignant"
        user_dict["roles"] = ["connected_user", user_dict["main_role"], users[0]['ExplicitSecondaryK']]
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT LNM_role.role 
                        FROM LNM_enseignant 
                        JOIN LNM_enseignant_as_role ON LNM_enseignant_as_role.id_enseignant = LNM_enseignant.id_enseignant
                        JOIN LNM_role on LNM_role.id_role = LNM_enseignant_as_role.id_role
                        WHERE login = %s""",
            (user_login,))
        roles = cursor.fetchall()
        user_dict["roles"] += [item for t in roles for item in t]

        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            f"""
                SELECT 
                    LNM_enseignant_responsabilites.id_enseignant_responsabilites,
                    LNM_enseignant_responsabilites.type_objet,
                    LNM_enseignant_responsabilite_dimensions.dimension,
                    LNM_enseignant_responsabilite_dimensions.valeur
                FROM LNM_enseignant_responsabilites
                JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_enseignant_responsabilites.id_enseignant
                LEFT JOIN LNM_enseignant_responsabilite_dimensions ON LNM_enseignant_responsabilite_dimensions.id_enseignant_responsabilites = LNM_enseignant_responsabilites.id_enseignant_responsabilites
                WHERE login = %s""",
            (user_login,))
        responsibilities = cursor.fetchall()
        user_dict["responsibilities"] = load_enseignant_responsibilities(responsibilities)

        return UserInDB(**user_dict)
    return None


def get_etudiant(user_login: str):

    users=[]
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"""SELECT LNM_etudiant.id_etudiant AS id, 
                                 LNM_etudiant.*,
                                 ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK
                          FROM LNM_etudiant 
                          JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                          WHERE login = %s""",
                       (user_login,))
        users = cursor.fetchall()
    except Exception as e:
        logger.exception(e)
    if len(users) != 0:
        user_dict = users[0]

        if user_dict.get("intern_account") != 0 and not user_dict.get("password"):
            logger.warning(f"Inactive user '{user_login}' try to connect")
            return None
        user_dict["main_role"] = "etudiant"
        user_dict["roles"] = ["connected_user", user_dict["main_role"], users[0]['ExplicitSecondaryK']]
        return UserInDB(**user_dict)
    return None

def get_user(user_login: str):
    """
    Allowed methods are byMail (default) or byLogin.
    "byMail" is the default local login, it requires a local password.
    "byLogin" is used for remote login like CAS, no local password is required
    """
    fetchers = [get_administratif, get_enseignant, get_etudiant]

    user = next(
        filter(None, (f(user_login) for f in fetchers)),
        None
    )

    if user is not None:
        logger.info(f"User {user_login} logged")
    else:
        logger.error(f"Loging error with login: {user_login}")

    return user



def load_enseignant_responsibilities(rows: list[dict]) -> list[dict]:
    """
    Transforme les lignes SQL à plat en liste de responsabilités avec
    leurs dimensions sous forme de dict.
    """
    print(rows)

    resp_map = {}
    for row in rows:
        rid = row["id_enseignant_responsabilites"]
        if rid not in resp_map:
            resp_map[rid] = {
                "type_objet": row["type_objet"],
                "dimensions": {}   # { "filiere": "IDU", "niveau": "FI4", ... }
            }
        if row["dimension"]:  # LEFT JOIN → peut être NULL si aucune dimension
            resp_map[rid]["dimensions"][row["dimension"]] = row["valeur"]

    return list(resp_map.values())

# ToDo Utiliser get_user_cached dans get_current_user en interface entre get_current_user et get_user pour avoir un cache Redis et limiter les requesters SQL relative à l'utilisateur
# import redis
# import pickle
#
# redis_client = redis.Redis(host="localhost", port=6379, db=0)
# _CACHE_TTL = 300
#
#
# def get_user_cached(user_login: str, method: str = "byMail") -> UserInDB | None:
#     cache_key = f"user:{method}:{user_login}"
#
#     cached = redis_client.get(cache_key)
#     if cached:
#         return pickle.loads(cached)
#
#     user = get_user(user_login, method)
#     if user:
#         redis_client.setex(cache_key, _CACHE_TTL, pickle.dumps(user))
#     return user

# def invalidate_user_cache(user_login: str):
#     for method in ["byMail", "byLogin"]:
#         redis_client.delete(f"user:{method}:{user_login}")
# # À appeler dans vos endpoints de modification d'utilisateur, logout, voire périodiquement "timeout".

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #print(token, flush=True)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_login = payload.get("login")
        #print("userlogin", userlogin, flush=True)
        if user_login is None:
            logger.error(f"Login error with payload: {payload}")
            raise credentials_exception
        token_data = TokenData(login=user_login)
        #print("token_data", token_data, flush=True)
    except InvalidTokenError as e:
        logger.error(f"Invalid token : {e}")
        raise credentials_exception
    user = get_user(token_data.login)
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


#######################
# Permissions

# def has_role(role_required: str):
#     async def check_role(
#         current_user: Annotated[User, Depends(get_current_user)],
#     ):
#         if role_required not in current_user.roles:
#             logger.error(f"User {current_user.id} has no role {role_required}")
#             raise HTTPException(status_code=403, detail="Unauthorized access")
#
#     return check_role
#
#
# def has_responsabilite(user, type_objet: str, scope: dict) -> bool:
#     """
#     scope = dict de dimensions requises, ex: {"filiere": "IDU", "niveau": "FI4"}
#
#     Logique de subsomption :
#       - type_objet 'all' couvre tout
#       - une dimension absente en BD = wildcard (couvre toutes les valeurs)
#       - une dimension présente en BD doit matcher exactement le scope demandé
#       - une responsabilité avec MOINS de dimensions que le scope est plus large → couvre
#     """
#     for responsability in user.responsabilites:
#
#         # type_objet doit matcher ou être 'all'
#         if responsability["type_objet"] not in (type_objet, "all"):
#             continue
#
#         # Chaque dimension définie en BD doit être satisfaite par le scope
#         # (les dimensions absentes en BD sont des wildcards)
#         match = all(
#             scope.get(dim) == val
#             for dim, val in responsability["dimensions"].items()
#         )
#
#         if match:
#             return True
#
#     return False


##############################
# Request API

def db_request(requester: User, request: SQLRequest):
    # vérification via le système de règles
    check_access(
        request=request,
        user=requester,
    )

    if requester:
        logger.info(f"User {requester.id} has role {requester.roles} requests {request}")
    else:
        logger.info(f"Anonymous user requests {request}")

    rows = []
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_connexion())
        cursor = connection.cursor(dictionary=True)

        if request.params:
            cursor.execute(request.request, request.params)
            #cursor.execute(sqlalchemy.text(request.request), request.params)
        else:
            cursor.execute(request.request)
            #cursor.execute(sqlalchemy.text(request.request))

        if getattr(cursor, "with_rows", False):
            rows = cursor.fetchall()
        else:
            rows = []
        #logger.info(f"User {requester.id} has {rows}")
        connection.commit()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Database request failed: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
    #return json.dumps([dict(ix) for ix in rows]) # return string
    return [dict(ix) for ix in rows] # return list that will be converted to json


###################################

def main():
    return True

if __name__ == '__main__':
    main()