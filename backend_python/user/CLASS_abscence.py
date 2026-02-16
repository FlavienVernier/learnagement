import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/abscence/",
            tags=["user", "request"],
            summary="Abscence",
            description="Return abscence")
def list_universities(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = { # ToDo refactor request to use explicit Keys instead concat
        "request" : """
                        SELECT concat(LNM_etudiant.prenom, ' ', LNM_etudiant.nom) as etudiant, 
                               concat(LNM_filiere.nom_filiere, '_', LNM_promo.annee, '_', LNM_statut.nom_statut) as filiere, 
                               MAQUETTE_module.code_module, 
                               CLASS_session.schedule
                        FROM `CLASS_absence` 
                        JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
                        JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                        JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                        JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
                        JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
                        JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                        JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))
