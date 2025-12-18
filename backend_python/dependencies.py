import os
import dotenv
import logging

import mysql.connector

from typing import Annotated

from fastapi import Header, HTTPException

logger = logging.getLogger(__name__)

dotenv.load_dotenv(".env")

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
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_SERVER"),
            user=os.getenv("MYSQL_USER_LOGIN"),
            port=int(os.getenv("MYSQL_PORT")),
            password=os.getenv("MYSQL_USER_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )
        # OR ADD THIS TO THAT SAME STRING ABOVE IN PLACE OF

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM LNM_enseignant")

        return cursor
    except Exception as e:
        logger.exception(e)
        raise e

def main():
    return True

if __name__ == '__main__':
    main()