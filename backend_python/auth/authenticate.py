import os
import dotenv

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import logger
from models.token import Token
import auth.authenticate_lnm as authenticate_lnm
import auth.authenticate_cas as authenticate_cas
#import auth.authenticate_ldap
#import auth.authenticate_proxy_cas

from typing import Annotated

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("SESSION_TIMEOUT"))

router = APIRouter()

@router.post("/token",
    tags=["Auth"],
    summary="Token",
    description="Authenticate user and return JWT token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await authenticate_lnm.login_for_access_token(form_data)


@router.post("/token-cas/",
    tags=["Auth"],
    summary="CAS login or provision",
    description="Internal endpoint — login or create user from CAS, returns JWT token")
async def cas_login(
    #data: authenticate_cas.CasUserProvision,
    data,
    x_cas_token: Annotated[str | None , Header()] = None
) -> Token:
    logger.info(f"CAS login {data}")
    authenticate_cas.verify_cas_service_token(x_cas_token)
    return await authenticate_cas.login_or_provision_from_cas(data)

@router.post("/logout",
    tags=["Auth"],
    summary="User logout",
    description="...")
def logout():
    return authenticate_lnm.logout()

# ToDo check usefully => comment or remove
def permission(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ToDo check usefully => comment or remove
def main():
    return {"message": "authenticate module"}

# ToDo check usefully => comment or remove
if __name__ == '__main__':
    main()