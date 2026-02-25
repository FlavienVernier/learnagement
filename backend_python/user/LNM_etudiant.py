import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest


logger = logging.getLogger(__name__)

router = APIRouter()


######################################################
#
# spécific to all students : /etudiants/[spécific data]
#
######################################################

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
            tags=["user"],
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


@router.get("/etudiants/stages",
            tags=["user"],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
            SELECT LNM_stage.`id_stage`, 
                   ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK AS "étudiant", 
                   ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo", 
                   LNM_stage.`entreprise`, 
                   LNM_stage.`intitulé`, 
                   LNM_stage.`description`, 
                   LNM_stage.`ville`, 
                   DATE_FORMAT(LNM_stage.`date_debut`, '%Y-%m-%dT%H:%i') AS date_debut, 
                   DATE_FORMAT(LNM_stage.`date_fin`, '%Y-%m-%dT%H:%i') AS date_fin, 
                   LNM_stage.`nature`, 
                   ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK AS "enseignant"
            FROM `LNM_stage` 
                     JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
                     LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
                     JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
                     JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                     LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant;
                    """,
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/without_stage",
            tags=["user"],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
            SELECT `LNM_etudiant`.`id_etudiant`, 
                   `LNM_etudiant`.`nom`,
                   `LNM_etudiant`.`prenom`,
                   ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo"
            FROM `LNM_etudiant` 
                     JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
            WHERE `LNM_etudiant`.`id_etudiant` 
                      NOT IN ( SELECT `LNM_stage`.`id_etudiant` FROM `LNM_stage` WHERE 1)
                    """,
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


######################################################
#
# spécific to 1 student : /etudiants/{id_etudiant:int}
#
######################################################

@router.get("/etudiants/{id_etudiant:int}",
            tags=["user"],
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
            tags=["user"],
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

@router.post("/etudiants/{id_etudiant:int}/stage",
            tags=["user"],
            summary="Students",
            description="Return the list of students")
def post_etudiant_stage(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request" : """ 
                    INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`, `id_enseignant`) 
                    VALUES (%(entreprise)s, %(intitule)s, %(description)s, %(ville)s, %(date_debut)s, %(date_fin)s, %(nature)s, %(id_etudiant)s, %(id_enseignant)s)
        """,
        "params": {
            "entreprise": data['entreprise'],
            "intitule": data[intitule],
            "description": data['description'],
            "ville": data['ville'],
            "date_debut": data['date_debut'],
            "date_fin": data['date_fin'],
            "nature": data['nature'],
            "id_etudiant": id_etudiant,
            "id_enseignant": data['id_enseignant'],
        },
        "allowedRolesRequester": ["responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.patch("/etudiants/{id_etudiant:int}/stage",
             tags=["user"],
             summary="Students",
             description="Return the list of students")
def patch_etudiant_stage(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        data: Dict[str, Any],
):
    # ToDo il pourrait être intéressant de vérifier que le stage est bien à l'étudiant
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": """"
                   UPDATE LNM_stage
            SET id_enseignant = '%(id_enseignant)s'
            WHERE id_stage = '%(d_stage)s'
        """,
        "params": {
            "id_enseignant": data['id_enseignant'],
            "id_stage": data['id_stage'],
        },
        "allowedRolesRequester": ["responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.delete("/etudiants/{id_etudiant:int}/stage",
              tags=["user"],
              summary="Students",
              description="Return the list of students")
def delete_etudiant_stage(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        data: Dict[str, Any],
):
    # ToDo il pourrait être intéressant de vérifier que le stage est bien à l'étudiant
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": """
                   DELETE FROM `LNM_stage` WHERE `id_stage`= %(id_stage)s)
                   """,
        "params": {
            "id_stage": data['id_stage'],
        },
        "allowedRolesRequester": ["responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))