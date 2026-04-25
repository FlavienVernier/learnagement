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


@router.get("/university/etudiant/{id_etudiant:int}/wishes",
            tags=["user", "mobility"],
            summary="Wishes for student",
            description="Return the student's current mobility wishes")
def list_university_wishes_etudiant(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.id != id_etudiant:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    request = {
        "request": """
                        SELECT w.priority, u.*
                        FROM MOB_wishes w
                        JOIN MOB_partner_university u ON u.id_partner_university = w.id_partner_university
                        WHERE w.id_etudiant = %(id_etudiant)s
                        ORDER BY w.priority ASC
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["etudiant"],
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
    if current_user.id != id_etudiant:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    check_request = {
        "request": """
                        SELECT
                            COUNT(*) AS wishes_count,
                            COALESCE(MAX(priority), 0) AS max_priority,
                            COALESCE(SUM(CASE WHEN id_partner_university = %(id_partner_university)s THEN 1 ELSE 0 END), 0) AS already_exists
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
    wishes_count = int((check_rows[0].get("wishes_count") or 0)) if check_rows else 0
    max_priority = int((check_rows[0].get("max_priority") or 0)) if check_rows else 0
    already_exists = int((check_rows[0].get("already_exists") or 0)) if check_rows else 0

    if wishes_count >= 5:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas ajouter plus de 5 voeux.")

    if already_exists > 0:
        raise HTTPException(status_code=400, detail="Cette universite est deja dans vos voeux.")

    next_priority = max_priority + 1

    request = {
        "request": """
                        INSERT INTO MOB_wishes (id_etudiant, id_partner_university, priority)
                        VALUES (%(id_etudiant)s, %(id_partner_university)s, %(priority)s)
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
            "priority": next_priority,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.delete("/university/etudiant/{id_etudiant:int}/wish/{id_partner_university:int}",
            tags=["user", "mobility"],
            summary="Delete university from wishes",
            description="Delete a partner university from the student's mobility wishes")
def delete_university_from_wishes(
    id_etudiant: int,
    id_partner_university: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.id != id_etudiant:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    check_request = {
        "request": """
                        SELECT priority
                        FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    check_rows = db_request(current_user, SQLRequest(**check_request))
    if not check_rows:
        raise HTTPException(status_code=404, detail="Voeu introuvable.")

    removed_priority = int(check_rows[0]["priority"])

    delete_request = {
        "request": """
                        DELETE FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**delete_request))

    shift_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET priority = priority - 1
                        WHERE id_etudiant = %(id_etudiant)s
                          AND priority > %(removed_priority)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "removed_priority": removed_priority,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**shift_request))

    return {"message": "Voeu supprime."}


@router.post("/university/etudiant/{id_etudiant:int}/wish/{id_partner_university:int}/move/{direction}",
            tags=["user", "mobility"],
            summary="Move university wish",
            description="Move a wish up or down in the student's priority list")
def move_university_wish(
    id_etudiant: int,
    id_partner_university: int,
    direction: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.id != id_etudiant:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    if direction not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Direction invalide. Utilisez 'up' ou 'down'.")

    current_request = {
        "request": """
                        SELECT priority
                        FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    current_rows = db_request(current_user, SQLRequest(**current_request))
    if not current_rows:
        raise HTTPException(status_code=404, detail="Voeu introuvable.")

    current_priority = int(current_rows[0]["priority"])
    target_priority = current_priority - 1 if direction == "up" else current_priority + 1

    target_request = {
        "request": """
                        SELECT id_partner_university
                        FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                          AND priority = %(target_priority)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "target_priority": target_priority,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    target_rows = db_request(current_user, SQLRequest(**target_request))
    if not target_rows:
        raise HTTPException(status_code=400, detail="Impossible de deplacer ce voeu plus loin.")

    target_id_partner_university = int(target_rows[0]["id_partner_university"])

    # Step 1: move current wish to a temporary priority to avoid unique collisions.
    temp_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET priority = 0
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(current_id_partner_university)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "current_id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**temp_request))

    # Step 2: move target wish into current position.
    target_to_current_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET priority = %(current_priority)s
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(target_id_partner_university)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "target_id_partner_university": target_id_partner_university,
            "current_priority": current_priority,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**target_to_current_request))

    # Step 3: move current wish from temporary value to target position.
    current_to_target_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET priority = %(target_priority)s
                        WHERE id_etudiant = %(id_etudiant)s
                          AND id_partner_university = %(current_id_partner_university)s
                          AND priority = 0
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "current_id_partner_university": id_partner_university,
            "target_priority": target_priority,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**current_to_target_request))

    return {"message": "Voeu deplace.", "direction": direction}

@router.post("/university/etudiant/{id_etudiant:int}/wishes/submit",
            tags=["user", "mobility"],
            summary="Submit university wishes",
            description="Submit the student's mobility wishes for processing")
def submit_university_wishes(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.id != id_etudiant:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    check_request = {
        "request": """
                        SELECT COUNT(*) AS wishes_count
                        FROM MOB_wishes
                        WHERE id_etudiant = %(id_etudiant)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    check_rows = db_request(current_user, SQLRequest(**check_request))
    wishes_count = int((check_rows[0].get("wishes_count") or 0)) if check_rows else 0

    if wishes_count < 5:
        raise HTTPException(status_code=400, detail="Vous devez avoir au moins 5 voeux pour les soumettre.")

    # Update the submission date for all submitted wishes
    update_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET submission_date = NOW()
                        WHERE id_etudiant = %(id_etudiant)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    db_request(current_user, SQLRequest(**update_request))

    # ToDo : 
    #    - Bloquer les modifications des voeux après soumission (côté front et back)
    #    - Interface côté admin (RI)

    return {"message": "Voeux soumis avec succes."}