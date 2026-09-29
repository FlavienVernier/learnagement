import os

from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("INSTANCE_SECRET")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
