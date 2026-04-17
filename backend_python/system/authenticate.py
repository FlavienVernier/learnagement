import os
import dotenv

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import logger, get_user, Token
import system.authenticate_lnm as authenticate_lnm
#import system.authenticate_ldap
#import system.authenticate_proxy_cas

from typing import Annotated

dotenv.load_dotenv(".env")

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("SESSION_TIMEOUT"))

router = APIRouter()


#password_hash = PasswordHash((BcryptHasher(),))


@router.post("/token",
    tags=["Auth"],
    summary="Token",
    description="Authenticate user and return JWT token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return await authenticate_lnm.login_for_access_token(form_data)




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