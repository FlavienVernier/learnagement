import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter()

class User(BaseModel):
    prenom: str
    nom: str
    mail: str | None = None

@router.post("/enseignant/",
            tags=["user", "request", "enseignant"],
            summary="Teachers",
            description="Return the list of teachers")
def list_enseignant(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return db_request("""
        SELECT * FROM LNM_enseignant ORDER BY nom, prenom
    """)

@router.post("/enseignant_responsabilite/",
             tags=["user", "request", "enseignant"],
             summary="Teachers",
             description="Return the list of teachers' responsibilities")
def listLNM_enseignant_responsabilite(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return db_request("""
        SELECT
            CONCAT(`LNM_enseignant`.`prenom`,' ',`LNM_enseignant`.`nom`) AS `responsable`,
            COUNT(`MAQUETTE_module`.`id_module`) AS `responsabilite`,
            GROUP_CONCAT(distinct `MAQUETTE_module`.`code_module` separator ', ') AS `modules`
        FROM `LNM_enseignant`
        JOIN `MAQUETTE_module` ON `MAQUETTE_module`.`id_responsable` = `LNM_enseignant`.`id_enseignant`
        GROUP BY `LNM_enseignant`.`nom`, `LNM_enseignant`.`prenom`;
    """)
