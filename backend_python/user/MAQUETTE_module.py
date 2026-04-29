import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Dict, Any
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()


#####################################
# Private functions
#####################################

def __get_module_responsible_id(id_module: int,
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
    return db_request(current_user, SQLRequest(**request))

def __participate(id_module: int, id_etudiant: int, current_user: Annotated[User, Depends(get_current_active_user)], ):
    request = {
        "request" : f"""
            SELECT  MAQUETTE_module.id_module, LNM_etudiant.id_etudiant
            FROM MAQUETTE_module
            JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
            JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
            JOIN LNM_promo ON LNM_promo.id_promo = MAQUETTE_learning_unit.id_promo
            JOIN LNM_etudiant ON LNM_etudiant.id_promo = LNM_promo.id_promo
            WHERE MAQUETTE_module.id_module = %(id_module)s
            AND LNM_etudiant.id_etudiant = %(id_etudiant)s;
        """,
        "params": {
            "id_module": id_module,
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["user"],
    }
    res = db_request(current_user, SQLRequest(**request))
    print(("res", res), flush=True)
    return True


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
                    LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = CLASS_session.id_enseignant""",
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
def get_modules_intervenants(
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
def get_modules_etudiant(
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
def get_sequencages_responsable(
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


@router.get("/modules/sequences/{id_responsable}/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_sequences_responsable(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
            SELECT  MAQUETTE_module_sequence.id_module_sequence AS id_sequence, 
                    MAQUETTE_module_sequence.numero_ordre, 
                    MAQUETTE_module_sequence.id_intervenant_principal, 
                    MAQUETTE_module_sequence.commentaire,
                    MAQUETTE_module_sequencage.id_module, 
                    MAQUETTE_module_sequencage.id_seance_type, 
                    MAQUETTE_module_sequencage.id_groupe_type, 
                    CAST(MAQUETTE_module_sequencage.duree_h AS FLOAT) AS duree_h,
                    MAQUETTE_module.code_module, 
                    LNM_seance_type.type, 
                    LNM_groupe_type.groupe_type, 
                    ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant_principal
            FROM MAQUETTE_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = MAQUETTE_module_sequence.id_intervenant_principal
            WHERE MAQUETTE_module.id_responsable = %(id_responsable)s
        """,
        "params": {
            "id_responsable": id_responsable,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/sessions/{id_responsable}/",
            tags=["module"],
            summary="Get modules by responsible",
            description="Get all modules of a responsible")
def get_sessions_responsable(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
            SELECT
	            CLASS_session.id_session,
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
                LNM_seance_type.type,
                ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant
			FROM CLASS_session
            	LEFT JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session.id_groupe
                LEFT JOIN LNM_promo ON LNM_promo.id_promo = LNM_groupe.id_promo
                LEFT JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            	LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
            WHERE MAQUETTE_module.id_responsable = %(id_responsable)s
        """,
        "params": {
            "id_responsable": id_responsable,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/{id_module}/dependencies/",
            tags=["module"],
            summary="Get modules dependencies",
            description="Get all modules dependencies")
def get_module_dependencies(
        id_module: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
            SELECT `id_sequence_prev`, `id_sequence_next`
            FROM `MAQUETTE_dependance_sequence` 
                LEFT JOIN MAQUETTE_module_sequence on MAQUETTE_module_sequence.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_prev 
                LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module.id_module = %(id_module_prev)s
            UNION
            SELECT `id_sequence_prev`, `id_sequence_next`
            FROM `MAQUETTE_dependance_sequence` 
                LEFT JOIN MAQUETTE_module_sequence on MAQUETTE_module_sequence.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_next 
                LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
                LEFT JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module.id_module = %(id_module_next)s
        """,
        "params": {
            "id_module_prev": id_module,
            "id_module_next": id_module,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/modules/{id_module}/sequence_dependencies/",
            tags=["module"],
            summary="Get sequence dependencies",
            description="Get all modules sequence dependencies")
def get_module_sequence_dependencies(
        id_module: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": f"""
            SELECT MAQUETTE_module_sequence.id_module_sequence, LNM_seance_type.type, MAQUETTE_module.code_module, MAQUETTE_module.nom, MAQUETTE_module_sequence.commentaire 
			FROM MAQUETTE_module_sequence 
                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
                JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module_sequence.id_module_sequence IN (
                    SELECT MAQUETTE_module_sequence.id_module_sequence
                    FROM MAQUETTE_module_sequence
                        JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
                    WHERE MAQUETTE_module.id_module = %(id_module)s)
            OR MAQUETTE_module_sequence.id_module_sequence IN (
                    SELECT `id_sequence_next` 
                    FROM `MAQUETTE_dependance_sequence` 
                        JOIN MAQUETTE_module_sequence as sequence_prev on sequence_prev.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_prev 
                        JOIN MAQUETTE_module_sequencage  as sequencage_prev ON sequencage_prev.id_module_sequencage = sequence_prev.id_module_sequencage 
                        JOIN MAQUETTE_module as module_prev ON module_prev.id_module = sequencage_prev.id_module 
                    WHERE module_prev.id_module = %(id_module_prev)s)
            OR MAQUETTE_module_sequence.id_module_sequence IN (
                    SELECT `id_sequence_prev`
                    FROM `MAQUETTE_dependance_sequence` 
                        JOIN MAQUETTE_module_sequence as sequence_next on sequence_next.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_next
                        JOIN MAQUETTE_module_sequencage  as sequencage_next ON sequencage_next.id_module_sequencage = sequence_next.id_module_sequencage 
                        JOIN MAQUETTE_module as module_next ON module_next.id_module = sequencage_next.id_module 
                    WHERE module_next.id_module = %(id_module_next)s)
        """,
        "params": {
            "id_module": id_module,
            "id_module_prev": id_module,
            "id_module_next": id_module,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/modules/gantt/{id_responsable}/",
            tags=["module"],
            summary="Get sequence dependencies for Gantt",
            description="Get all modules sequence dependencies formatted for a Gantt chart")
def get_data_gantt_endpoint(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": f"""
            SELECT
	            pmms.id_module_sequence AS "prv_id",
	            pmm.code_module AS "prv_code_module",
                pmm.nom AS "prv_nom",
                pmd.nom AS "prv_discipline",
                pls.semestre AS "prv_semestre",
                pmmsg.duree_h AS "prv_duree_h",
                CONCAT(plst.type, pmms.numero_ordre) AS "prv_type",
                nmms.id_module_sequence AS "nxt_id",
                nmm.code_module AS "nxt_code_module",
                nmd.nom AS "prv_discipline",
                nls.semestre AS "nxt_semestre",
                nmm.nom AS "nxt_nom",
                nmmsg.duree_h AS "nxt_duree_h",
                CONCAT(nlst.type, nmms.numero_ordre) AS "nxt_type"
            FROM MAQUETTE_dependance_sequence mds
                # PREVIOUS
                LEFT JOIN MAQUETTE_module_sequence pmms on pmms.id_module_sequence = mds.id_sequence_prev
                JOIN MAQUETTE_module_sequencage pmmsg on pmmsg.id_module_sequencage = pmms.id_module_sequencage
                JOIN LNM_seance_type plst on plst.id_seance_type = pmmsg.id_seance_type
                JOIN MAQUETTE_module pmm on pmm.id_module = pmmsg.id_module
                JOIN MAQUETTE_discipline pmd on pmd.id_discipline = pmm.id_discipline
                JOIN LNM_semestre pls on pls.id_semestre = pmm.id_semestre
                # NEXT
                LEFT JOIN MAQUETTE_module_sequence nmms on nmms.id_module_sequence = mds.id_sequence_next
                JOIN MAQUETTE_module_sequencage nmmsg on nmmsg.id_module_sequencage = nmms.id_module_sequencage
                JOIN LNM_seance_type nlst on nlst.id_seance_type = nmmsg.id_seance_type
                JOIN MAQUETTE_module nmm on nmm.id_module = nmmsg.id_module
                JOIN MAQUETTE_discipline nmd on nmd.id_discipline = nmm.id_discipline
                JOIN LNM_semestre nls on nls.id_semestre = nmm.id_semestre
                # FILTER BY RESPONSABLE
            WHERE pmm.id_responsable = %(id_responsable_prv)s or nmm.id_responsable = %(id_responsable_nxt)s;
        """,
        "params": {
            "id_responsable_prv": id_responsable,
            "id_responsable_nxt": id_responsable,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/modules/gantt/etudiant/{id_etudiant}/",
            tags=["module"],
            summary="Get sequence dependencies for Gantt",
            description="Get all modules sequence dependencies formatted for a Gantt chart for an etudiant")
def get_data_gantt_endpoint_etudiant(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": f"""
            SELECT
                pmms.id_module_sequence AS "prv_id",
                pmm.code_module        AS "prv_code_module",
                pmm.nom                AS "prv_nom",
                pmd.nom                AS "prv_discipline",
                pls.semestre           AS "prv_semestre",
                pmmsg.duree_h          AS "prv_duree_h",
                CONCAT(plst.type, pmms.numero_ordre) AS "prv_type",
                nmms.id_module_sequence AS "nxt_id",
                nmm.code_module        AS "nxt_code_module",
                nmm.nom                AS "nxt_nom",
                nmd.nom                AS "nxt_discipline",
                nls.semestre           AS "nxt_semestre",
                nmmsg.duree_h          AS "nxt_duree_h",
                CONCAT(nlst.type, nmms.numero_ordre) AS "nxt_type"

            FROM LNM_etudiant lnm_e

            -- Résolution de la promo de l'étudiant
            JOIN MAQUETTE_learning_unit etu_lu ON etu_lu.id_promo = lnm_e.id_promo
            
            JOIN MAQUETTE_module_as_learning_unit etu_malu ON etu_malu.id_learning_unit = etu_lu.id_learning_unit
            
            -- Point d'entrée dans les séquences via la promo
            JOIN MAQUETTE_module_sequence etu_mms ON etu_mms.id_module_sequencage IN (SELECT id_module_sequencage
                    FROM MAQUETTE_module_sequencage
                    WHERE id_module = etu_malu.id_module)
            
            JOIN MAQUETTE_dependance_sequence mds
                ON mds.id_sequence_prev = etu_mms.id_module_sequence
                OR mds.id_sequence_next = etu_mms.id_module_sequence
            
            -- === PREVIOUS ===
            LEFT JOIN MAQUETTE_module_sequence pmms ON pmms.id_module_sequence = mds.id_sequence_prev
            LEFT JOIN MAQUETTE_module_sequencage pmmsg ON pmmsg.id_module_sequencage = pmms.id_module_sequencage
            LEFT JOIN LNM_seance_type plst ON plst.id_seance_type = pmmsg.id_seance_type
            LEFT JOIN MAQUETTE_module pmm ON pmm.id_module = pmmsg.id_module
            LEFT JOIN MAQUETTE_module_as_learning_unit pmmalu ON pmmalu.id_module = pmm.id_module
            LEFT JOIN MAQUETTE_learning_unit pmlu ON pmlu.id_learning_unit = pmmalu.id_learning_unit
            LEFT JOIN MAQUETTE_discipline pmd ON pmd.id_discipline = pmm.id_discipline
            LEFT JOIN LNM_semestre pls ON pls.id_semestre = pmm.id_semestre
            
            -- === NEXT ===
            LEFT JOIN MAQUETTE_module_sequence nmms ON nmms.id_module_sequence = mds.id_sequence_next
            LEFT JOIN MAQUETTE_module_sequencage nmmsg ON nmmsg.id_module_sequencage = nmms.id_module_sequencage
            LEFT JOIN LNM_seance_type nlst ON nlst.id_seance_type = nmmsg.id_seance_type
            LEFT JOIN MAQUETTE_module nmm ON nmm.id_module = nmmsg.id_module
            LEFT JOIN MAQUETTE_module_as_learning_unit nmmalu ON nmmalu.id_module = nmm.id_module
            LEFT JOIN MAQUETTE_learning_unit nmlu ON nmlu.id_learning_unit = nmmalu.id_learning_unit
            LEFT JOIN MAQUETTE_discipline nmd ON nmd.id_discipline = nmm.id_discipline
            LEFT JOIN LNM_semestre nls ON nls.id_semestre = nmm.id_semestre

        WHERE lnm_e.id_etudiant = %(id_etudiant)s AND (pmlu.id_promo = lnm_e.id_promo OR nmlu.id_promo = lnm_e.id_promo)
        GROUP BY pmms.id_module_sequence, nmms.id_module_sequence;
        """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/disciplines/",
            tags=["module"],
            summary="Get disciplines",
            description="Get disciplines")
def get_disciplines(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : f"""
                SELECT
                    * 
                FROM `MAQUETTE_discipline`""",
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


#####################################
#
# Patch
#
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
        if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
            request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))

@router.patch("/modules/{id_module}/sequencages/{id_sequencage}/",
            tags=["module"],
            summary="Update sequencage",
            description="Update sequencage according to parameters")
def update_sequencage(
    id_module: int,
    id_sequencage: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):

    if 'id_intervenant_principal' in data.keys():
        request = {
            # ToDo refactor when SQLAlchemy Core is up
            "request" : f"""
                UPDATE MAQUETTE_module_sequencage
                SET id_intervenant_principal = %(id_intervenant_principal)s
                WHERE id_module_sequencage = %(id_sequencage)s
            """,
            "params": {
                "id_intervenant_principal": data['id_intervenant_principal'],
                "id_sequencage": id_sequencage,
            },
            "allowedRolesRequester" : [],
        }
        if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
            request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


@router.patch("/modules/{id_module}/sequences/{id_sequence}/",
            tags=["module"],
            summary="Update sequencage",
            description="Update sequencage according to parameters")
def update_sequence(
    id_module: int,
    id_sequence: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):
    if 'id_intervenant_principal' in data.keys():
        request = {
            # ToDo refactor when SQLAlchemy Core is up
            "request": f"""
                   UPDATE MAQUETTE_module_sequence
                   SET id_intervenant_principal = %(id_intervenant_principal)s
                   WHERE id_module_sequence = %(id_sequence)s
               """,
            "params": {
                "id_intervenant_principal": data['id_intervenant_principal'],
                "id_sequence": id_sequence,
            },
            "allowedRolesRequester": [],
        }
        if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
            request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


@router.patch("/modules/{id_module}/sessions/{id_session}/",
            tags=["module"],
            summary="Update sequencage",
            description="Update sequencage according to parameters")
def update_session(
    id_module: int,
    id_session: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):
    if 'id_enseignant' in data.keys():
        request = {
            # ToDo refactor when SQLAlchemy Core is up
            "request": f"""
                   UPDATE CLASS_session
                   SET id_enseignant = %(id_enseignant)s
                   WHERE id_session = %(id_session)s
               """,
            "params": {
                "id_enseignant": data['id_enseignant'],
                "id_session": id_session,
            },
            "allowedRolesRequester": [],
        }
        if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
            request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


#####################################
#
# Post
#
#####################################

@router.post("/modules/{id_module}/sequencage",
            tags=["module"],
            summary="Update module",
            description="Update module according to parameters")
def add_sequencage(
    id_module: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],):
    print(data)
    if 'id_intervenant_principal' in data.keys() and data['id_intervenant_principal'] is not None and data['id_intervenant_principal'] != "":
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
    #print(type(__get_module_responsible_id(id_module, current_user)), flush=True)
    if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


@router.post("/modules/create/",
             tags=["module"],
             summary="Create a new module",
             description="Create a module without sequencing")
def create_module(
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],
):
    required = ['code_module', 'nom_module', 'ECTS', 'id_discipline', 'semestre', 'id_responsable']
    missing = [f for f in required if f not in data or data[f] in (None, "")]
    if missing:
        raise HTTPException(status_code=422, detail=f"Champs manquants : {missing}")

    request = {
        "request": """
            INSERT INTO MAQUETTE_module (
                code_module,
                nom_module,
                hCM,
                hTD,
                hTP,
                hProj,
                hPerso,
                ECTS,
                id_semestre,
                id_responsable,
                id_discipline
            ) VALUES (
                %(code_module)s,
                %(nom_module)s,
                %(hCM)s,
                %(hTD)s,
                %(hTP)s,
                %(hProj)s,
                %(hPerso)s,
                %(ECTS)s,
                %(id_semestre)s,
                %(id_responsable)s,
                %(id_discipline)s
            );
        """,
        "params": {
            "code_module":    data['code_module'],
            "nom_module":     data['nom_module'],
            "hCM":            data.get('hCM', 0),
            "hTD":            data.get('hTD', 0),
            "hTP":            data.get('hTP', 0),
            "hProj":          data.get('hProjet', 0),
            "hPerso":         data.get('hPerso', 0),
            "ECTS":           data['ECTS'],
            "id_semestre":    data['semestre'],
            "id_responsable": data['id_responsable'],
            "id_discipline":  data['id_discipline'],
        },
        "allowedRolesRequester": ["responsable_etudes"],
    }


    return db_request(current_user, SQLRequest(**request))


#####################################
#
# Delete
#
#####################################

@router.delete("/modules/{id_module}/sequencages/{id_sequencage}",
            tags=["module"],
            summary="Update module",
            description="Update module according to parameters")
def delete_sequencage(
    id_module: int,
    id_sequencage: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):

    request = {
        # ToDo refactor next when SQLAlchemy Core is up
        "request" : f"""
            DELETE FROM MAQUETTE_module_sequencage
            WHERE id_module_sequencage = %(id_sequencage)s
        """,
        "params": {
            "id_sequencage": id_sequencage,
        },
        "allowedRolesRequester" : [],
    }
    if current_user.id == __get_module_responsible_id(id_module, current_user)[0]["id_responsable"]:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))