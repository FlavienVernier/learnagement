import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

######################################################
#
# Get relative to all teachers : /enseignants/[fields]
#
######################################################

@router.get("/enseignants/",
            tags=["enseignant"],
            summary="Teachers",
            description="Return the list of teachers")
def enseignants(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_enseignant.`id_enseignant`, 
                               LNM_enseignant.`prenom`, 
                               LNM_enseignant.`nom`, 
                               LNM_enseignant.`mail`, 
                               LNM_enseignant.`statut`, 
                               ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK
                        FROM LNM_enseignant 
                        JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
                        ORDER BY ExplicitSecondaryK;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/enseignant_responsabilite/",
             tags=["enseignant"],
             summary="Teachers responsibilities",
             description="Return the list of teachers' responsibilities")
def enseignants_responsabilities(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT
                            CONCAT(`LNM_enseignant`.`prenom`,' ',`LNM_enseignant`.`nom`) AS `responsable`,
                            COUNT(`MAQUETTE_module`.`id_module`) AS `responsabilite`,
                            GROUP_CONCAT(distinct `MAQUETTE_module`.`code_module` separator ', ') AS `modules`
                        FROM `LNM_enseignant`
                        JOIN `MAQUETTE_module` ON `MAQUETTE_module`.`id_responsable` = `LNM_enseignant`.`id_enseignant`
                        GROUP BY `LNM_enseignant`.`nom`, `LNM_enseignant`.`prenom`;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/enseignants/charge/",
             tags=["administratif", "enseignant"],
             summary="Teachers load",
             description="Return the list of teachers load")
def enseignants_load(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_enseignant.prenom, LNM_enseignant.nom, sum(MAQUETTE_module_sequencage.duree_h)
                        FROM CLASS_session
                        JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
                        JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                        JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                        GROUP BY LNM_enseignant.prenom, LNM_enseignant.nom;
                    """,

        "allowedRolesRequester": ["administratif"],
    }
    return db_request(current_user, SQLRequest(**request))



######################################################
#
# Get specific to 1 teacher : /enseignants/{id_enseignant:int}/[fields]
#
######################################################

@router.get("/enseignants/{id_enseignant:int}/charge/",
             tags=["administratif", "enseignant"],
             summary="Teachers load",
             description="Return the list of teachers load")
def enseignants_load(
    id_enseignant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        # ToDo convert parameters to be SQLAlchemy Core compatible when it is up
        "request" : f"""SELECT 
                            DATE_FORMAT(CLASS_session.schedule, '%Y-%m-%dT%H:%i') AS schedule, 
                            CAST(MAQUETTE_module_sequencage.duree_h AS FLOAT) AS duree_h, 
                            MAQUETTE_module.code_module,
                            MAQUETTE_module.nom, 
                            MAQUETTE_module.id_semestre, 
                            LNM_seance_type.type
            FROM CLASS_session
                JOIN LNM_enseignant ON LNM_enseignant.id_enseignant=CLASS_session.id_enseignant 
                JOIN MAQUETTE_module_sequence ON CLASS_session.id_module_sequence=MAQUETTE_module_sequence.id_module_sequence 
                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequence.id_module_sequencage=MAQUETTE_module_sequencage.id_module_sequencage 
                JOIN MAQUETTE_module ON MAQUETTE_module_sequencage.id_module=MAQUETTE_module.id_module 
                JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
            WHERE LNM_enseignant.id_enseignant = %(id_enseignant)s""",
        "params": {
            "id_enseignant": id_enseignant,
        },
        "allowedRolesRequester": ["administratif"],
    }
    if(current_user.id == id_enseignant):
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))

@router.get("/enseignants/{id_enseignant:int}/stages",
            tags=["administratif", "enseignant",  "internship",],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
        id_enseignant: int,
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
                     LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
            WHERE LNM_stage.id_enseignant = %(id_enseignant)s;
                    """,
        "params": {
            "id_enseignant": id_enseignant,
        },
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages"],
    }
    if(current_user.id == id_enseignant):
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))