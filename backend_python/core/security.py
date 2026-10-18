import os

from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SIGNING_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
