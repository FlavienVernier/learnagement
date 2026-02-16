import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/competence/",
            tags=["user", "request", "university"],
            summary="Universities",
            description="Return the list of partner universities")
def tree_competence(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT APC_competence.code_competence, 
                               APC_competence.libelle_competence, 
                               CONCAT(APC_competence.code_competence,"_N",APC_niveau.niveau) AS 'code_niveau', 
                               APC_niveau.niveau, 
                               CONCAT(APC_competence.code_competence,"_N", APC_niveau.niveau,"_AC",APC_apprentissage_critique.id_apprentissage_critique)  AS 'code_ac', 
                               APC_apprentissage_critique.libelle_apprentissage, MAQUETTE_module.code_module, MAQUETTE_module.nom, 
                               CAST(MAQUETTE_module.ECTS AS DOUBLE) AS 'ects',
                               IFNULL(MAQUETTE_module.hCM,0) AS 'hCM', 
                               IFNULL(MAQUETTE_module.hTD,0) AS 'hTD', 
                               IFNULL(MAQUETTE_module.hTP,0) AS 'hTP', 
                               IFNULL(MAQUETTE_module.hPROJ,0)
                        FROM `APC_competence` 
                        JOIN APC_niveau ON APC_niveau.id_competence = APC_competence.id_competence
                        JOIN APC_apprentissage_critique ON APC_apprentissage_critique.id_niveau = APC_niveau.id_niveau
                        JOIN APC_apprentissage_critique_as_module ON APC_apprentissage_critique_as_module.id_apprentissage_critique = APC_apprentissage_critique.id_apprentissage_critique
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = APC_apprentissage_critique_as_module.id_module
                        WHERE 1;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))
