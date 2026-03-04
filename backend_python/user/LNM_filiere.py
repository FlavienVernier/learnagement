import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/filieres/",
            tags=["user", "filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def filieres(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT * FROM LNM_filiere
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/statuts/",
            tags=["user", "filiere"],
            summary="Status",
            description="Return the list of statuts")
def statuts(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT * FROM LNM_statut
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/filieres/dags",
            tags=["user", "filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def dags(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT 
                            LNM_filiere.nom_filiere, 
                            LNM_filiere.nom_long, 
                            LNM_promo.annee, 
                            LNM_statut.nom_statut, 
                            MAQUETTE_learning_unit.learning_unit_code, 
                            MAQUETTE_learning_unit.learning_unit_name, 
                            MAQUETTE_module.code_module, 
                            MAQUETTE_module.nom, 
                            APC_apprentissage_critique.libelle_apprentissage, 
                            APC_niveau.niveau, APC_niveau.libelle_niveau, 
                            APC_competence.code_competence, 
                            APC_competence.libelle_competence
                        FROM LNM_filiere
                                 JOIN LNM_promo ON LNM_promo.id_filiere = LNM_filiere.id_filiere
                                 JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
                                 JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
                                 JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_learning_unit = MAQUETTE_learning_unit.id_learning_unit
                                 JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_as_learning_unit.id_module
                                 JOIN APC_apprentissage_critique_as_module ON APC_apprentissage_critique_as_module.id_module = MAQUETTE_module.id_module
                                 JOIN APC_apprentissage_critique ON APC_apprentissage_critique.id_apprentissage_critique = APC_apprentissage_critique_as_module.id_apprentissage_critique
                                 JOIN APC_niveau ON APC_niveau.id_niveau = APC_apprentissage_critique.id_niveau
                                 JOIN APC_competence ON APC_competence.id_competence = APC_niveau.id_competence
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))