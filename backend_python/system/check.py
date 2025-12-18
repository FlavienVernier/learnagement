import os
import dotenv
import logging
import json

from fastapi import APIRouter, Depends, HTTPException, status
import mysql.connector
from dependencies import db_request


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/enseignant_sans_cours/", tags=["check"])
def checkLNM_enseignant_sans_cours():
    return db_request("""SELECT `prenom`, `nom`, `mail`, `statut`, `composante`
            FROM LNM_enseignant
            WHERE LNM_enseignant.id_enseignant
                      NOT IN (  SELECT CLASS_session.id_enseignant
                                FROM CLASS_session
                                WHERE CLASS_session.id_enseignant IS NOT null);""")