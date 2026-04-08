import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any
from pydantic import BaseModel
from dependencies import db_request, get_current_active_user, User, SQLRequest
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/acp_kpi/",
            tags=["apc"],
            summary="nb competence",
            description="nombre de competence:")
def get_competence(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request_com= {
        "request": """
    SELECT COUNT(DISTINCT id_competence) AS nb_competences
    FROM APC_competence
""",
        "allowedRolesRequester" : ["user"],
    }
    requestmodule = {
        "request": """
    SELECT COUNT(DISTINCT id_module) AS nb_module
    FROM APC_apprentissage_critique_as_module
""",
        "allowedRolesRequester" : ["user"],
    }

    request_ac = {
        "request": """
            SELECT COUNT(DISTINCT id_apprentissage_critique) AS nb_ac
            FROM APC_apprentissage_critique
        """,
        "allowedRolesRequester": ["user"],
    }

    request_composante = {
        "request": """
            SELECT COUNT(DISTINCT id_composante_essentielle) AS nb_composante_essentielle
            FROM APC_composante_essentielle
        """,
        "allowedRolesRequester": ["user"],
    }
    resulat_comp= db_request(current_user, SQLRequest(**request_com))
    resulat_module= db_request(current_user, SQLRequest(**requestmodule))
    result_ac = db_request(current_user, SQLRequest(**request_ac))
    result_composante = db_request(current_user, SQLRequest(**request_composante))
   
    return {
        "nb_competences": resulat_comp,
        "nb_module": resulat_module,
        "nb_ac": result_ac,
        "nb_composante_essentielle": result_composante,
    }