import json
import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()


#####################################
# Get
#####################################

@router.get("/m2c3/",
            tags=["user", "module"],
            summary="M2c3",
            description="Return maquette et modalités de contrôle de connaissances et compétences")
def get_m2c3(
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

@router.get("/modules/responsables/",
            tags=["module"],
            summary="Get responsibles",
            description="Get modules responsibles")
def get_modules_responsables(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
                SELECT
                    MAQUETTE_module.id_module, 
                    MAQUETTE_module.code_module, 
                    MAQUETTE_module.nom as nom_module, 
                    LNM_semestre.semestre, 
                    MAQUETTE_module.hCM, 
                    MAQUETTE_module.hTD, 
                    MAQUETTE_module.hTP, 
                    MAQUETTE_module.hPROJ,
                    MAQUETTE_module.hPersonnelle, 
                    MAQUETTE_module.commentaire, 
                    LNM_enseignant.nom, 
                    LNM_enseignant.prenom
                FROM `MAQUETTE_module`
                    LEFT JOIN LNM_semestre ON LNM_semestre.id_semestre = MAQUETTE_module.id_semestre
                    LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module = MAQUETTE_module.id_module
                    LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage
                    LEFT JOIN CLASS_session ON CLASS_session.id_module_sequence = MAQUETTE_module_sequence.id_module_sequence
                    LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
                WHERE `id_responsable` = %(id_responsable)s""",
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/responsables/{id_responsable}",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_modules_responsable(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
                SELECT
                    MAQUETTE_module.id_module, 
                    MAQUETTE_module.code_module, 
                    MAQUETTE_module.nom as nom_module, 
                    LNM_semestre.semestre, 
                    MAQUETTE_module.hCM, 
                    MAQUETTE_module.hTD, 
                    MAQUETTE_module.hTP, 
                    MAQUETTE_module.hPROJ,
                    MAQUETTE_module.hPersonnelle, 
                    MAQUETTE_module.commentaire, 
                    LNM_enseignant.nom, 
                    LNM_enseignant.prenom
                FROM `MAQUETTE_module`
                    LEFT JOIN LNM_semestre ON LNM_semestre.id_semestre = MAQUETTE_module.id_semestre
                    LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module = MAQUETTE_module.id_module
                    LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage
                    LEFT JOIN CLASS_session ON CLASS_session.id_module_sequence = MAQUETTE_module_sequence.id_module_sequence
                    LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
                WHERE `id_responsable` = %(id_responsable)s""",
        "params": {
            "id_responsable": id_responsable,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/intervenants/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_modules_intervenant(

        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""

SELECT
                CLASS_session.id_groupe,
                LNM_groupe.nom_groupe,
                LNM_promo.id_promo,
                ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK as promo,
                MAQUETTE_module_sequence.numero_ordre,
                MAQUETTE_module_sequence.id_intervenant_principal,
                MAQUETTE_module_sequence.commentaire,
                MAQUETTE_module_sequencage.id_module,
                MAQUETTE_module_sequencage.id_seance_type, 
                CAST(MAQUETTE_module_sequencage.duree_h AS FLOAT) AS duree_h, 
                MAQUETTE_module.code_module, 
                MAQUETTE_module.nom as nom_module,
                LNM_seance_type.type,
                LNM_semestre.semestre
            FROM CLASS_session
            	LEFT JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session.id_groupe
                LEFT JOIN LNM_promo ON LNM_promo.id_promo = LNM_groupe.id_promo
                LEFT JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            	LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                LEFT JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit AND MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
                LEFT JOIN LNM_semestre ON LNM_semestre.id_semestre = MAQUETTE_module.id_semestre
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
            """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/intervenants/{id_intervenant}/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_modules_intervenant(
        id_intervenant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""

SELECT
                CLASS_session.id_groupe,
                LNM_groupe.nom_groupe,
                LNM_promo.id_promo,
                ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK as promo,
                MAQUETTE_module_sequence.numero_ordre,
                MAQUETTE_module_sequence.id_intervenant_principal,
                MAQUETTE_module_sequence.commentaire,
                MAQUETTE_module_sequencage.id_module,
                MAQUETTE_module_sequencage.id_seance_type, 
                CAST(MAQUETTE_module_sequencage.duree_h AS FLOAT) AS duree_h, 
                MAQUETTE_module.code_module, 
                MAQUETTE_module.nom as nom_module,
                LNM_seance_type.type,
                LNM_semestre.semestre
            FROM CLASS_session
            	LEFT JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session.id_groupe
                LEFT JOIN LNM_promo ON LNM_promo.id_promo = LNM_groupe.id_promo
                LEFT JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            	LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                LEFT JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit AND MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
                LEFT JOIN LNM_semestre ON LNM_semestre.id_semestre = MAQUETTE_module.id_semestre
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
            WHERE CLASS_session.id_enseignant = %(id_intervenant)s""",
        "params": {
            "id_intervenant": id_intervenant,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/modules/etudiants/{id_etudiant}/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_modules_intervenant(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
            SELECT MAQUETTE_module.id_module, 
                MAQUETTE_module.code_module, 
                MAQUETTE_module.nom 
            FROM `MAQUETTE_module` 
                JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module 
                JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit 
                JOIN LNM_promo ON LNM_promo.id_promo = MAQUETTE_learning_unit.id_promo 
                JOIN LNM_etudiant ON LNM_etudiant.id_promo = LNM_promo.id_promo 
            WHERE LNM_etudiant.id_etudiant = %(id_etudiant)s
        """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))



@router.get("/modules/sequencages/{id_responsable}/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_modules_intervenant(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
            SELECT  MAQUETTE_module_sequencage.`id_module_sequencage`, 
                    MAQUETTE_module_sequencage.`id_module`,
                    MAQUETTE_module_sequencage.`nombre`,
                    CAST(MAQUETTE_module_sequencage.`duree_h` AS FLOAT) AS duree_h,
                    MAQUETTE_module.code_module, 
                    LNM_seance_type.type, 
                    LNM_groupe_type.groupe_type, 
                    ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant_principal
            FROM MAQUETTE_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = MAQUETTE_module_sequencage.id_intervenant_principal
            WHERE MAQUETTE_module.id_responsable = %(id_responsable)s
        """,
        "params": {
            "id_responsable": id_responsable,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

def get_module_responsible_id(id_module: int,
                           current_user: Annotated[User, Depends(get_current_active_user)], ):
    request = {
        "request" : f"""
            SELECT  MAQUETTE_module.id_responsable
            FROM MAQUETTE_module
            WHERE MAQUETTE_module.id_module = %(id_module)s
        """,
        "params": {
            "id_module": id_module,
        },
        "allowedRolesRequester": ["user"],
    }
    return json.loads(db_request(current_user, SQLRequest(**request)))

#####################################
# Patch
#####################################
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
            "allowedRolesRequester" : ["responsable_etudes"],
        }
        if current_user.id == get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
            request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


#####################################
# Post
#####################################

@router.post("/modules/{id_module}/sequencage",
            tags=["module"],
            summary="Update module",
            description="Update module according to parameters")
def add_sequencage(
    id_module: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):
    if 'id_responsable' in data.keys() and data['id_responsable'] is not None and data['id_responsable'] != "":
        request = {
            "request" : f"""
                INSERT INTO MAQUETTE_module_sequencage ( 
                    id_module, 
                    nombre, 
                    id_seance_type, 
                    id_groupe_type, 
                    duree_h, 
                    id_intervenant_principal)
                VALUES (
                    %(id_module)s, 
                    %(nombre)s, 
                    %(id_seance_type)s, 
                    %(id_groupe_type)s, 
                    %(duree_h)s, 
                    %(id_intervenant_principal)s)
            """,
            "params": {
                "id_module": id_module,
                "nombre": data['nombre'],
                "id_seance_type": data['id_seance_type'],
                "id_groupe_type": data['id_groupe_type'],
                "duree_h": data['duree_h'],
                "id_intervenant_principal": data['id_intervenant_principal'],
            },
        }
    else:
        request = {
            "request" : f"""
                INSERT INTO MAQUETTE_module_sequencage ( 
                    id_module, 
                    nombre, 
                    id_seance_type, 
                    id_groupe_type, 
                    duree_h)
                VALUES (
                    %(id_module)s, 
                    %(nombre)s, 
                    %(id_seance_type)s, 
                    %(id_groupe_type)s, 
                    %(duree_h)s)
            """,
            "params": {
                "id_module": id_module,
                "nombre": data['nombre'],
                "id_seance_type": data['id_seance_type'],
                "id_groupe_type": data['id_groupe_type'],
                "duree_h": data['duree_h'],
            }
        }
    request["allowedRolesRequester"] = ["responsable_etudes"]
    print(type(get_module_responsible_id(id_module, current_user)), flush=True)
    if current_user.id == get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))
