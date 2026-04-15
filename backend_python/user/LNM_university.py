import logging

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from typing import Any, Dict

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


@router.post("/university/etudiant/{id_etudiant:int}/wish/{id_partner_university:int}",
            tags=["user", "mobility"],
            summary="Add university to wishes",
            description="Add a partner university to the student's mobility wishes")
def add_university_to_wishes(
    id_etudiant: int,
    id_partner_university: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    check_request = {
        "request": """
                        SELECT
                            COUNT(*) AS wishes_count,
                            SUM(CASE WHEN id_partner_university = %(id_partner_university)s THEN 1 ELSE 0 END) AS already_exists
                        FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    check_rows = db_request(current_user, SQLRequest(**check_request))
    wishes_count = int(check_rows[0].get("wishes_count", 0)) if check_rows else 0
    already_exists = int(check_rows[0].get("already_exists", 0)) if check_rows else 0

    if wishes_count >= 5:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas ajouter plus de 5 voeux.")

    if already_exists > 0:
        raise HTTPException(status_code=400, detail="Cette universite est deja dans vos voeux.")

    request = {
        "request": """
                        INSERT INTO MOB_wishes (id_etudiant, id_partner_university, priority)
                        VALUES (%(id_etudiant)s, %(id_partner_university)s, (
                            SELECT COALESCE(MAX(priority), 0) + 1
                            FROM MOB_wishes
                            WHERE id_etudiant = %(id_etudiant)s
                        ))
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    return db_request(current_user, SQLRequest(**request))