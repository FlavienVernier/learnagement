import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/etudiants/",
            tags=["user", "request", "university"],
            summary="Students",
            description="Return the list of students")
def get_etudiants(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT 
                            LNM_etudiant.`id_etudiant`,
                            LNM_etudiant.`nom`,
                            LNM_etudiant.`prenom`,
                            LNM_etudiant.`mail`,
                            LNM_etudiant.`password_updated`,
                            ExplicitSecondaryK
                        FROM LNM_etudiant
                        JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                        ORDER BY ExplicitSecondaryK;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/absences",
            tags=["user", "request", "university"],
            summary="Students",
            description="Return the list of students")
def get_etudiants_absences(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """SELECT ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK as etudiant, 
                              ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK as promo, 
                              MAQUETTE_module.code_module, 
                              DATE_FORMAT(CLASS_session.schedule, '%Y-%m-%dT%H:%i') AS schedule
                       FROM `CLASS_absence` 
                                JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
                                JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                                JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
                                JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
                                JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                                JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
                                JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                                JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
                    """,
        "allowedRolesRequester": ["responsable_etudes"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant:int}",
            tags=["user", "request", "university"],
            summary="Students",
            description="Return the list of students")
def get_etudiant(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT 
                            LNM_etudiant.`id_etudiant`,
                            LNM_etudiant.`nom`,
                            LNM_etudiant.`prenom`,
                            LNM_etudiant.`mail`,
                            LNM_etudiant.`password_updated`,
                            ExplicitSecondaryK
                        FROM LNM_etudiant
                                 JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                        WHERE LNM_etudiant.id_etudiant = %(id_etudiant)s;
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant:int}/absences",
            tags=["user", "request", "university"],
            summary="Students",
            description="Return the list of students")
def get_etudiant_absences(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request" : """SELECT MAQUETTE_module.code_module, 
                              DATE_FORMAT(CLASS_session.schedule, '%Y-%m-%dT%H:%i') AS schedule
                       FROM `CLASS_absence` 
                                JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
                                JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                                JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
                       WHERE LNM_etudiant.`id_etudiant` = %(id_etudiant)s
        """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["responsable_etudes"],
    }
    if current_user.id == id_etudiant:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))
