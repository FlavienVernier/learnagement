import logging

from fastapi import APIRouter, Depends
from typing import Annotated
from pydantic import BaseModel

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/university/",
            tags=["user", "mobility"],
            summary="Universities",
            description="Return the list of partner universities")
def list_universities(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT * FROM MOB_partner_university
                    """,
        "allowedRolesRequester" : ["user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/university/etudiant/{id_etudiant:int}",
            tags=["user", "mobility"],
            summary="Universities for student",
            description="Return the list of partner universities with the number of places for the student")
def list_universities_etudiant(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT u.*, pl.number_of_places, pr.annee
                        FROM MOB_partner_university_places pl
                        JOIN MOB_partner_university u ON u.id_partner_university = pl.id_partner_university 
                        JOIN LNM_promo pr ON pr.id_promo = pl.id_promo
                        WHERE id_filiere = (
                            SELECT e_pr.id_filiere
                            FROM LNM_etudiant e 
                            JOIN LNM_promo e_pr ON e_pr.id_promo = e.id_promo 
                            WHERE e.id_etudiant = %(id_etudiant)s
                        );
                    """,
        "params": {
            "id_etudiant": id_etudiant
        },
        "allowedRolesRequester" : ["etudiant"],
    }
    return db_request(current_user, SQLRequest(**request))