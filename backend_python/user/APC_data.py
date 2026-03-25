import logging

from fastapi import APIRouter, Depends
from typing import Annotated

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/apc/competences/",
            tags=["apc"],
            summary="APC Compétences",
            description="Retourne la liste des compétences APC")
def get_competences(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_competence, libelle_competence, code_competence, description
            FROM APC_competence
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/niveaux/",
            tags=["apc"],
            summary="APC Niveaux",
            description="Retourne la liste des niveaux de compétences")
def get_niveaux(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_niveau, id_competence, niveau, libelle_niveau
            FROM APC_niveau
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/apprentissages/",
            tags=["apc"],
            summary="APC Apprentissages critiques",
            description="Retourne la liste des apprentissages critiques")
def get_apprentissages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_apprentissage_critique, id_niveau, libelle_apprentissage
            FROM APC_apprentissage_critique
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/ac_modules/",
            tags=["apc"],
            summary="APC AC-Modules",
            description="Retourne les associations apprentissages critiques / modules")
def get_ac_modules(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_apprentissage_critique, id_module, type_lien
            FROM APC_apprentissage_critique_as_module
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/modules/",
            tags=["apc"],
            summary="APC Modules",
            description="Retourne la liste des modules de la maquette")
def get_apc_modules(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_module, code_module, nom, ECTS, id_discipline, id_semestre,
                   hCM, hTD, hTP, hTPTD, hPROJ, hPersonnelle, id_responsable, commentaire
            FROM MAQUETTE_module
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/composantes/",
            tags=["apc"],
            summary="APC Composantes essentielles",
            description="Retourne la liste des composantes essentielles")
def get_composantes(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_composante_essentielle, id_competence, libelle_composante_essentielle
            FROM APC_composante_essentielle
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/apc/situations/",
            tags=["apc"],
            summary="APC Situations professionnelles",
            description="Retourne la liste des situations professionnelles / métiers")
def get_situations(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
            SELECT id_situation_professionnelle, id_competence, libelle_situation
            FROM APC_situation_professionnelle
        """,
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))
