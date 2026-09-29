import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/metier_ac/{id_metier:int}",
    tags=["apc"],
    summary="Get AC, semester and competence by metier",
    description="Return the list of AC, semester and competence for a metier",
)
def get_metier_ac(
    id_metier: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": f"""
            SELECT DISTINCT
                metier.libelle_situation,
                metier.id_situation_professionnelle,
                semestre.id_semestre,
                semestre.semestre,
                ac.id_apprentissage_critique,
                ac.libelle_apprentissage,
                competence.id_competence,
                competence.code_competence
            FROM APC_situation_professionnelle metier
            JOIN APC_competence competence
                ON metier.id_competence = competence.id_competence
            JOIN APC_niveau niveau
                ON niveau.id_competence = competence.id_competence
            JOIN APC_apprentissage_critique ac
                ON ac.id_niveau = niveau.id_niveau
            JOIN APC_apprentissage_critique_as_module acmodule
                ON acmodule.id_apprentissage_critique = ac.id_apprentissage_critique
            JOIN MAQUETTE_module module
                ON module.id_module = acmodule.id_module
            JOIN LNM_semestre semestre
                ON semestre.id_semestre = module.id_semestre
            WHERE metier.id_situation_professionnelle = {id_metier}
        """,
        "allowedRolesRequester": ["connected_user"],
    }

    return db_request(current_user, SQLRequest(**request))

@router.get("/metier/",
            tags=["apc"],
            summary="Students",
            description="Return the list of situation_professionnelle ",)
def get_metier(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                    SELECT metier.id_situation_professionnelle,metier.libelle_situation 
                    FROM APC_situation_professionnelle metier
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))

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
        "allowedRolesRequester" : ["connected_user"],
    }
    requestmodule = {
        "request": """
    SELECT COUNT(DISTINCT id_module) AS nb_module
    FROM APC_apprentissage_critique_as_module
""",
        "allowedRolesRequester" : ["connected_user"],
    }

    request_ac = {
        "request": """
            SELECT COUNT(DISTINCT id_apprentissage_critique) AS nb_ac
            FROM APC_apprentissage_critique
        """,
        "allowedRolesRequester": ["connected_user"],
    }

    request_composante = {
        "request": """
            SELECT COUNT(DISTINCT id_composante_essentielle) AS nb_composante_essentielle
            FROM APC_composante_essentielle
        """,
        "allowedRolesRequester": ["connected_user"],
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