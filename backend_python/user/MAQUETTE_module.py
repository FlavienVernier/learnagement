import json
import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/m2c3/",
            tags=["user", "module"],
            summary="M2c3",
            description="Return maquette et modalités de contrôle de connaissances et compétences")
def m2c3(
    current_user: Annotated[User, Depends(get_current_active_user)],
    id_filiere: int,
    id_statut: int
):
    request = {
        # ToDo convert parameters to be SQLAlchemy Core compatible when it is up
        "request" : f"""SELECT MAQUETTE_module.id_module, 
                            MAQUETTE_module.code_module, 
                            MAQUETTE_module.nom, 
                            CAST(MAQUETTE_module.ECTS AS FLOAT) AS ECTS, 
                            MAQUETTE_module.hCM, 
                            MAQUETTE_module.hTD, 
                            MAQUETTE_module.hTP, 
                            MAQUETTE_module.hPROJ, 
                            MAQUETTE_module.hPersonnelle, 
                            MAQUETTE_learning_unit.learning_unit_code,
                            LNM_filiere.nom_filiere, 
                            LNM_promo.annee, 
                            LNM_statut.nom_statut, 
                            ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK AS "Responsable"
                        FROM `MAQUETTE_module` 
                        JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                        JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
                        JOIN LNM_promo ON LNM_promo.id_promo = MAQUETTE_learning_unit.id_promo
                        JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                        JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
                        JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = MAQUETTE_module.id_responsable
                        WHERE LNM_filiere.id_filiere = %(id_filiere)s AND LNM_statut.id_statut= %(id_statut)s;
                """,
        "params": {
            "id_filiere": id_filiere,
            "id_statut": id_statut,
        },
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.patch("/module/{id_module}",
            tags=["module"],
            summary="Update module",
            description="Update module according to parameters")
def update_module(
    id_module: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):

    if 'id_responsable' in data.keys():
        request = {
            # ToDo use following with SQLAlchemy
            # "request" : f"""
            #     UPDATE MAQUETTE_module
            #     SET id_responsable = :id_responsable
            #     WHERE id_module = :id_module
            # """,
            # ToDo remove next when SQLAlchemy Core is up
            "request" : f"""
                UPDATE MAQUETTE_module
                SET id_responsable = %(id_responsable)s
                WHERE id_module = %(id_module)s
            """,
            "params": {
                "id_responsable": data['id_responsable'],
                "id_module": id_module,
            },
            "allowedRolesRequester" : ["user"],
        }
    return db_request(current_user, SQLRequest(**request))