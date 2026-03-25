import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, get_current_active_user_optional, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/filieres/",
            tags=["anonymous", "user", "filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def filieres(
    current_user: Annotated[Optional[User], Depends(get_current_active_user_optional)],
    #current_user: Annotated[User, Depends(get_current_active_user)],
):
    print(current_user, flush=True)
    # Comportement différencié selon que l'utilisateur est authentifié ou non
    if current_user:
        # Requête pour utilisateur authentifié
        request = {
            "request" : """
                            SELECT LNM_filiere.*, ExplicitSecondaryKs_LNM_filiere.ExplicitSecondaryK
                            FROM LNM_filiere
                            JOIN ExplicitSecondaryKs_LNM_filiere ON ExplicitSecondaryKs_LNM_filiere.id_filiere = LNM_filiere.id_filiere
                        """,
            "allowedRolesRequester" : ["user"],
        }
    else:
        # Requête pour utilisateur non authentifié
        request = {
            "request" : """
                            SELECT LNM_filiere.id_filiere, 
                                   LNM_filiere.nom_filiere, 
                                   LNM_filiere.nom_long,
                                   ExplicitSecondaryKs_LNM_filiere.ExplicitSecondaryK AS filiere
                            FROM LNM_filiere
                            JOIN ExplicitSecondaryKs_LNM_filiere ON ExplicitSecondaryKs_LNM_filiere.id_filiere = LNM_filiere.id_filiere
                        
                        """,
            "allowedRolesRequester" : ["anonymous"],
        }
    print(request,flush=True)
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
                        SELECT LNM_statut.*, ExplicitSecondaryKs_LNM_statut.ExplicitSecondaryK
                        FROM LNM_statut
                        JOIN ExplicitSecondaryKs_LNM_statut ON ExplicitSecondaryKs_LNM_statut.id_statut = LNM_statut.id_statut
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/groupe_types/",
            tags=["user", "filiere"],
            summary="Status",
            description="Return the list of groupe types")
def groupe_types(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_groupe_type.*, ExplicitSecondaryKs_LNM_groupe_type.ExplicitSecondaryK
                        FROM LNM_groupe_type
                        JOIN ExplicitSecondaryKs_LNM_groupe_type ON ExplicitSecondaryKs_LNM_groupe_type.id_groupe_type = LNM_groupe_type.id_groupe_type;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/seance_types/",
            tags=["user", "filiere"],
            summary="Status",
            description="Return the list of seance types")
def seance_types(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_seance_type.*, ExplicitSecondaryKs_LNM_seance_type.ExplicitSecondaryK
                        FROM LNM_seance_type
                        JOIN ExplicitSecondaryKs_LNM_seance_type ON ExplicitSecondaryKs_LNM_seance_type.id_seance_type = LNM_seance_type.id_seance_type;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/filieres/dags",
            tags=["anonymous", "filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def dags(
        #current_user = None,  #current_user: Annotated[User, Depends(get_current_active_user)],
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
        "allowedRolesRequester" : ["anonymous"],
    }
    return db_request(None, SQLRequest(**request))

@router.get("/promos/",
            tags=["user", "filiere"],
            summary="promos",
            description="Return the list of promos")
def promos(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT LNM_promo.`id_promo`, ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS promo
                        FROM `LNM_promo`
                        JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo;
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/filieres/{id_filiere:int}/competences",
            tags=["anonymous"],
            summary="Filiere",
            description="Return competences of a filiere")
def competence_filiere(
        id_filiere: int,
):
    request = {
        "request" : """
            SELECT
                `APC_competence`.`id_competence` AS `id_competence`,
                `APC_competence`.`code_competence` AS `code_competence`,
                `APC_competence`.`libelle_competence` AS `libelle_competence`,
                `APC_competence`.`description` AS `description_competence`
            FROM `APC_competence_as_filiere_as_statut`
                JOIN `APC_competence` ON `APC_competence_as_filiere_as_statut`.`id_competence` = `APC_competence`.`id_competence`
                JOIN `LNM_filiere` ON `APC_competence_as_filiere_as_statut`.`id_filiere` = `LNM_filiere`.`id_filiere`
            WHERE `LNM_filiere`.`id_filiere` = %(id_filiere)s""",
        "params": {
            "id_filiere": id_filiere,
        },
        "allowedRolesRequester" : ["anonymous"],
    }
    return db_request(None, SQLRequest(**request))


@router.get("/filieres/{id_filiere:int}/competences/{id_competence:int}",
            tags=["anonymous"],
            summary="Filiere",
            description="Return competences of a filiere")
def competence_filiere(
        id_filiere: int,
        id_competence: int,
):
    request = {
        "request": """
                   SELECT * FROM `APC_composante_essentielle` WHERE `id_competence` = %(id_competence)s""",
        "params": {
            "id_competence": id_competence,
        },
        "allowedRolesRequester" : ["anonymous"],
    }
    return db_request(None, SQLRequest(**request))


@router.get("/filieres/{id_filiere:int}/competences/{id_competence:int}/apprentissagesCritiques",
            tags=["anonymous"],
            summary="Filiere",
            description="Return competences of a filiere")
def apprentissagesCritiques_competence_filiere(
        id_filiere: int,
        id_competence: int,
):
    request = { #`APC_niveau`.`id_competence`,`APC_apprentissage_critique`.`id_apprentissage_critique`,
        # "request": """
        #            SELECT
        #
        #                 `APC_niveau`.`niveau`,
        #
        #                 GROUP_CONCAT(`APC_apprentissage_critique`.`libelle_apprentissage` SEPARATOR ' ')
        #            FROM `APC_apprentissage_critique`
        #            JOIN `APC_niveau` ON `APC_apprentissage_critique`.`id_niveau` = `APC_niveau`.`id_niveau`
        #            WHERE `APC_niveau`.`id_competence` = %(id_competence)s
        #            GROUP BY `APC_niveau`.`id_competence`, `APC_niveau`.`niveau`
        #           """,
        "request": """
                   SELECT
                        `APC_niveau`.`id_competence`, 
                        `APC_apprentissage_critique`.`id_apprentissage_critique`,
                        `APC_niveau`.`niveau`,
                        `APC_apprentissage_critique`.`libelle_apprentissage` 
                   FROM `APC_apprentissage_critique`
                   JOIN `APC_niveau` ON `APC_apprentissage_critique`.`id_niveau` = `APC_niveau`.`id_niveau`
                   WHERE `APC_niveau`.`id_competence` = %(id_competence)s
                   """,
        "params": {
            "id_competence": id_competence,
        },
        "allowedRolesRequester" : ["anonymous"],
    }
    return db_request(None, SQLRequest(**request))