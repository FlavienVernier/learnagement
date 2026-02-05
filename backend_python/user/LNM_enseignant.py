import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/enseignant/",
            tags=["user", "request", "enseignant"],
            summary="Teachers",
            description="Return the list of teachers")
def list_enseignant(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT * FROM LNM_enseignant ORDER BY nom, prenom
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.post("/enseignant_responsabilite/",
             tags=["user", "request", "enseignant"],
             summary="Teachers responsibilities",
             description="Return the list of teachers' responsibilities")
def listLNM_enseignant_responsabilite(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT
                            CONCAT(`LNM_enseignant`.`prenom`,' ',`LNM_enseignant`.`nom`) AS `responsable`,
                            COUNT(`MAQUETTE_module`.`id_module`) AS `responsabilite`,
                            GROUP_CONCAT(distinct `MAQUETTE_module`.`code_module` separator ', ') AS `modules`
                        FROM `LNM_enseignant`
                        JOIN `MAQUETTE_module` ON `MAQUETTE_module`.`id_responsable` = `LNM_enseignant`.`id_enseignant`
                        GROUP BY `LNM_enseignant`.`nom`, `LNM_enseignant`.`prenom`;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.post("/charge_enseignants/",
             tags=["user", "request", "enseignant"],
             summary="Teachers responsibilities",
             description="Return the list of teachers' responsibilities")
def listLNM_enseignant_responsabilite(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_enseignant.prenom, LNM_enseignant.nom, sum(MAQUETTE_module_sequencage.duree_h)
                        FROM CLASS_session
                        JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
                        JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                        JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                        GROUP BY LNM_enseignant.prenom, LNM_enseignant.nom;
                    """,
        "allowedRolesRequester": ["administratif"],
    }
    return db_request(current_user, SQLRequest(**request))