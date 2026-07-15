import logging
import inspect

from fastapi import APIRouter, Depends
from typing import Annotated
from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()

requests = {
    "get_checkLNM_enseignant_sans_cours" : {
        "request" : """SELECT LNM_enseignant.`prenom`, LNM_enseignant.`nom`, LNM_enseignant.`mail`, LNM_enseignant.`statut`, LNM_enseignant.`composante`
            FROM LNM_enseignant
            WHERE LNM_enseignant.id_enseignant
                      NOT IN (  SELECT CLASS_session.id_enseignant
                                FROM CLASS_session
                                WHERE CLASS_session.id_enseignant IS NOT null);""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_checkMAQUETTE_moduleWithoutLearningUnit" : {
        "request" : """SELECT MAQUETTE_module.`code_module`, MAQUETTE_module.`nom`
            FROM `MAQUETTE_module`
            WHERE `id_module` NOT IN (SELECT `id_module` FROM MAQUETTE_module_as_learning_unit);""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_module_sans_apprentissage_critique" : {
        "request" : """SELECT MAQUETTE_module.`code_module`, MAQUETTE_module.`nom`
            FROM `MAQUETTE_module`
            WHERE `id_module` NOT IN (SELECT id_module FROM APC_apprentissage_critique_as_module);""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_module_detail_ects" : {
        "request" : """SELECT
                `MAQUETTE_module`.`code_module` AS `code_module`,
                `MAQUETTE_module`.`nom` AS `nom`,
                CAST(`MAQUETTE_module`.`ECTS` AS FLOAT) AS `ECTS`,
                `MAQUETTE_module`.`hCM` AS `hCM`,
                `MAQUETTE_module`.`hTD` AS `hTD`,
                `MAQUETTE_module`.`hTP` AS `hTP`,
                `MAQUETTE_module`.`hPROJ` AS `hPROJ`,
                `MAQUETTE_module`.`hPersonnelle` AS `hPersonnelle`,
                ROUND((ifnull(`MAQUETTE_module`.`hCM`, 0) + ifnull(`MAQUETTE_module`.`hTD`, 0) + ifnull(`MAQUETTE_module`.`hTP`, 0)) / `MAQUETTE_module`.`ECTS`, 2) AS `h/ECTS`,
                ROUND(`MAQUETTE_module`.`ECTS` / (ifnull(`MAQUETTE_module`.`hCM`, 0) + ifnull(`MAQUETTE_module`.`hTD`, 0) + ifnull(`MAQUETTE_module`.`hTP`, 0)), 3) AS `ECTS/h`
                FROM `MAQUETTE_module`
                GROUP BY `MAQUETTE_module`.`id_module`
                ORDER BY `MAQUETTE_module`.`code_module`;""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_session_sans_intervenant" : {
        "request" : """SELECT
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
            WHERE CLASS_session.id_enseignant IS NULL;""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_session_reference_corruption" : {
        "request": """
            SELECT
                CLASS_session.`id_session`,
                CLASS_session.`id_module_sequence`,
                MAQUETTE_module_sequence.id_module_sequence
            FROM CLASS_session
            LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            WHERE MAQUETTE_module_sequence.id_module_sequence IS NULL;""",
        "allowedRolesRequester" : ["administratif"],
    },
    "get_maquette_vs_sequencage" : {
        "request" : """
                        SELECT hMaquette.ExplicitSecondaryK, 
                               hMaquette.code_module,
                               hMaquette.hCM - hSession.hCM AS hCM_maquette_vs_sequencage,
                            hMaquette.hTD - hSession.hTD AS hTD_maquette_vs_sequencage,
                            hMaquette.hTP - hSession.hTP AS hTP_maquette_vs_sequencage,
                            hMaquette.hProj - hSession.hProj AS hProj_maquette_vs_sequencage
                        FROM
                            (SELECT ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK, 
                                   MAQUETTE_module.code_module, 
                                   SUM(LNM_promo.nbGroupeCM * IFNULL(MAQUETTE_module.hCM, 0)) AS hCM, 
                                   SUM(LNM_promo.nbGroupeTD * IFNULL(MAQUETTE_module.hTD, 0)) AS hTD, 
                                   SUM(LNM_promo.nbGroupeTP * IFNULL(MAQUETTE_module.hTP, 0)) AS hTP,
                                   SUM(LNM_promo.nbGroupeCM * IFNULL(MAQUETTE_module.hProj, 0)) AS hProj
                            FROM `MAQUETTE_module` 
                            JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                            JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
                            JOIN LNM_promo ON LNM_promo.id_promo = MAQUETTE_learning_unit.id_promo
                            JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
                            GROUP BY ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK, 
                                     MAQUETTE_module.code_module
                            ) AS hMaquette
                        LEFT JOIN    
                            (SELECT ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK, 
                                    MAQUETTE_module.code_module,
                                    LNM_seance_type.type,
                                    SUM(CASE WHEN type = 'CM' THEN MAQUETTE_module_sequencage.duree_h ELSE 0 END) AS hCM,
                                    SUM(CASE WHEN type = 'TD' THEN MAQUETTE_module_sequencage.duree_h ELSE 0 END) AS hTD,
                                    SUM(CASE WHEN type = 'TP' THEN MAQUETTE_module_sequencage.duree_h ELSE 0 END) AS hTP,
                                    SUM(CASE WHEN type = 'PROJ' THEN MAQUETTE_module_sequencage.duree_h ELSE 0 END) AS hPROJ
                            FROM `MAQUETTE_module` 
                            JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                            JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
                            JOIN LNM_promo ON LNM_promo.id_promo = MAQUETTE_learning_unit.id_promo
                            JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
                            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module = MAQUETTE_module.id_module
                            JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage
                            JOIN CLASS_session ON CLASS_session.id_module_sequence = MAQUETTE_module_sequence.id_module_sequence
                            JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                            GROUP BY ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK, 
                                    MAQUETTE_module.code_module,
                                    LNM_seance_type.type
                            ) AS hSession
                        ON hMaquette.code_module = hSession.code_module AND hMaquette.ExplicitSecondaryK = hSession.ExplicitSecondaryK
                    """,
        "allowedRolesRequester" : ["administratif", "responsable_etudes"],
    },
    "get_maquette_vs_sequencage_by_idResp" : {
        "request": """
                    SELECT DISTINCT
                        MAQUETTE_module.id_module,
                        MAQUETTE_module.code_module,
                        CONCAT(IFNULL(hCM,0) - IFNULL(hCMCequenced,0), " / ", IFNULL(hCM,0))  AS 'CM_to_plan',
                        CONCAT(IFNULL(hTD,0)  - IFNULL(hTDCequenced,0), " / ", IFNULL(hTD,0)) AS 'TD_to_plan',
                        CONCAT(IFNULL(hTP,0)  - IFNULL(hTPCequenced,0), " / ", IFNULL(hTP,0)) AS 'TP_to_plan',
                        CONCAT(IFNULL(hPROJ,0)  - IFNULL(hPROJCequenced,0), " / ", IFNULL(hPROJ,0)) AS 'Proj_to_plan'
                    FROM MAQUETTE_module
                    LEFT JOIN (
                        SELECT code_module, SUM(nombre * duree_h) as hCMCequenced
                        FROM MAQUETTE_module_sequencage
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                        JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                        JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                        WHERE LNM_seance_type.type = 'CM' AND LNM_groupe_type.groupe_type = 'PROMO' OR LNM_seance_type.type = 'Exam' AND LNM_groupe_type.groupe_type = 'PROMO'
                        GROUP BY code_module) CMsequenced ON  CMsequenced.code_module = MAQUETTE_module.code_module
                    LEFT JOIN (
                        SELECT code_module, SUM(nombre * duree_h) as hTDCequenced
                        FROM MAQUETTE_module_sequencage
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                        JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                        JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                        WHERE LNM_seance_type.type = 'TD' AND LNM_groupe_type.groupe_type = 'TD'
                        GROUP BY code_module) TDsequenced ON  TDsequenced.code_module = MAQUETTE_module.code_module
                    LEFT JOIN (
                        SELECT code_module, SUM(nombre * duree_h) as hTPCequenced
                        FROM MAQUETTE_module_sequencage
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                        JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                        JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                        WHERE LNM_seance_type.type = 'TP' AND LNM_groupe_type.groupe_type = 'TP'
                        GROUP BY code_module) TPsequenced ON  TPsequenced.code_module = MAQUETTE_module.code_module
                    LEFT JOIN (
                        SELECT code_module, SUM(nombre * duree_h) as hPROJCequenced
                        FROM MAQUETTE_module_sequencage
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                        JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                        JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                        WHERE LNM_seance_type.type = 'PROJ' AND LNM_groupe_type.groupe_type = 'Promo'
                        GROUP BY code_module) PROJsequenced ON  PROJsequenced.code_module = MAQUETTE_module.code_module
                    WHERE MAQUETTE_module.id_responsable = %(id_responsable)s
                    """,
        # I don't know why I set lambda params
        "params":
            lambda id_responsable: {"id_responsable": id_responsable},
        #"allowedRolesRequester": ["administratif", "responsable_etudes"],
        # request allowed if the user is reponsible of the module, or an administratif, or has "responsable_etudes" role
        "allowedRolesRequester": lambda id_responsable, current_user: [current_user.ExplicitSecondaryK] if id_responsable and current_user.id == id_responsable else ["administratif", "responsable_etudes"],

    },
}

##################
# Enseignant
##################
@router.get("/enseignant_sans_cours/",
             tags=["check"],
            summary="Teacher without session",
            description="Check teacher without session.")
def checkLNM_enseignant_sans_cours(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

#########################
# Module
#########################
@router.get("/module_sans_unite_d_enseignement/",
             tags=["check"],
            summary="Module without learning unit",
            description="Check module not link to a learning unit.")
def  checkMAQUETTE_moduleWithoutLearningUnit(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/module_sans_apprentissage_critique/",
             tags=["check"],
            summary="Module without apprentissage critique",
            description="Check module without apprentissage critique.")
def module_sans_apprentissage_critique(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/module_detail_ects/",
             tags=["check"],
            summary="ECTs weight",
            description="Check ratio hours ECTs.")
def  module_detail_ects(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

########################
# Class
########################

@router.get("/session_sans_intervenant/",
             tags=["check"],
            summary="Session without teacher",
            description="Check session without teacher.")
def  session_sans_intervenant(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))


@router.get("/session_reference_corruption/",
             tags=["check"],
            summary="Session foreign K coruption",
            description="Check session not linked to module.")
def session_reference_corruption(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

# ToDo to finished
@router.get("/maquette_vs_sequencage/",
            tags=["check"],
            summary="Session hours Vs Program",
            description="Check whether the number of sequencage hours corresponds to the program.")
def maquette_vs_sequencage(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))


@router.get("/maquette_vs_sequencage/{id_responsable}/",
            tags=["check"],
            summary="Session hours Vs Program",
            description="Check whether the number of sequencage hours corresponds to the program.")
def maquette_vs_sequencage_by_idResp(
        id_responsable: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    request["params"] = request["params"](id_responsable) if callable(request["params"]) else request["params"]
    request["allowedRolesRequester"] = request["allowedRolesRequester"](id_responsable, current_user) if callable(request["allowedRolesRequester"]) else request["allowedRolesRequester"]
    # if id_responsable and current_user.id == id_responsable:
    #     request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


