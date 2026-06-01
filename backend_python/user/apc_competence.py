import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest


logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/competence_ac/",
            tags=["apc"],
            summary="Students",
            description="Return the list of competences and apprentissages for the students",)
def get_competence_ac(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                    SELECT 
                    C.id_competence,C.libelle_competence , C.code_competence ,AC.id_apprentissage_critique, AC.libelle_apprentissage 
                    FROM APC_competence C join APC_niveau N ON C.id_competence=N.id_competence JOIN APC_apprentissage_critique AC ON AC.id_niveau=N.id_niveau;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/competence_ce/",
            tags=["apc"],
            summary="Students",
            description="Return the list of competences and essentiel composant",)
def get_competence_ce(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                     SELECT
                        C.id_competence,
                        C.code_competence,
                        C.libelle_competence,
                        CE.id_composante_essentielle,
                        CE.libelle_composante_essentielle
                    FROM APC_competence C
                    JOIN APC_composante_essentielle CE
                        ON C.id_competence = CE.id_competence;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))