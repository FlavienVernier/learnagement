import os

from core.logging import logger


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
