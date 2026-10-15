import os
from warnings import deprecated
from core.logging import logger

from contextlib import contextmanager

from sqlalchemy import create_engine, URL

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        url = URL.create(  # gère les caractères spéciaux du mot de passe
            drivername=os.getenv("DB_DRIVER", "mysql+mysqlconnector"),
            username=os.getenv("MYSQL_USER_LOGIN"),
            password=os.getenv("MYSQL_USER_PASSWORD"),
            host=os.getenv("MYSQL_SERVER"),
            port=int(os.getenv("MYSQL_PORT")),
            database=os.getenv("MYSQL_DB"),
        )
        _engine = create_engine(
            url,
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            pool_timeout=10,
            pool_pre_ping=True,   # teste la connexion avant usage
            pool_recycle=1800,    # évite les "MySQL server has gone away"
        )
    return _engine

@contextmanager
def get_connection():
    """Connexion + transaction : commit à la sortie, rollback sur exception."""
    with get_engine().begin() as conn:
        yield conn
        
@contextmanager
def get_read_connection():
    with get_engine().connect() as conn:
        yield conn  # fermeture = rollback implicite, retour au pool

@deprecated("Migration to sqlalchemy, use get_connection() instead")
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
