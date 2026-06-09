import logging

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

router = APIRouter()


class UniversityPlacePayload(BaseModel):
    id_filiere: int
    annee: int
    number_of_places: int = Field(ge=0)


class UniversityAdminPayload(BaseModel):
    name: str
    country: str
    code: Optional[str] = None
    address: Optional[str] = None
    latitude: float = 0.0
    longitude: float = 0.0
    website: Optional[str] = None
    languages: Optional[str] = None
    note_min: Optional[float] = None
    type: Optional[str] = "ERASMUS"
    places: List[UniversityPlacePayload] = []


def _resolve_promo_id(
    current_user: User,
    id_filiere: int,
    annee: int,
) -> int:
    promo_request = {
        "request": """
                        SELECT id_promo
                        FROM LNM_promo
                        WHERE id_filiere = %(id_filiere)s
                          AND annee = %(annee)s
                        ORDER BY id_promo ASC
                        LIMIT 1
                    """,
        "params": {
            "id_filiere": id_filiere,
            "annee": annee,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }
    promo_rows = db_request(current_user, SQLRequest(**promo_request))
    if not promo_rows:
        raise HTTPException(
            status_code=400,
            detail=f"Aucune promo trouvee pour la filiere {id_filiere} en annee {annee}.",
        )

    return int(promo_rows[0]["id_promo"])


def _sync_university_places(
    current_user: User,
    id_partner_university: int,
    places: List[UniversityPlacePayload],
) -> None:
    normalized_places: Dict[Tuple[int, int], int] = {}
    for place in places:
        if place.number_of_places <= 0:
            continue
        normalized_places[(place.id_filiere, place.annee)] = int(place.number_of_places)

    resolved_places: List[Dict[str, int]] = []
    for (id_filiere, annee), number_of_places in normalized_places.items():
        id_promo = _resolve_promo_id(current_user, id_filiere, annee)
        resolved_places.append(
            {
                "id_promo": id_promo,
                "number_of_places": number_of_places,
            }
        )

    delete_places_request = {
        "request": """
                        DELETE FROM MOB_partner_university_places
                        WHERE id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }
    db_request(current_user, SQLRequest(**delete_places_request))

    for place in resolved_places:
        insert_place_request = {
            "request": """
                            INSERT INTO MOB_partner_university_places (id_partner_university, id_promo, number_of_places)
                            VALUES (%(id_partner_university)s, %(id_promo)s, %(number_of_places)s)
                        """,
            "params": {
                "id_partner_university": id_partner_university,
                "id_promo": place["id_promo"],
                "number_of_places": place["number_of_places"],
            },
            "allowedRolesRequester": ["relations_internationales"],
        }
        db_request(current_user, SQLRequest(**insert_place_request))


@router.get("/university/",
            tags=["mobility"],
            summary="Universities",
            description="Return the list of partner universities")
def list_universities(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT * FROM MOB_partner_university
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/university/etudiant/{id_etudiant:int}",
            tags=["mobility"],
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
            tags=["mobility"],
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
                        SELECT w.priority, w.submission_date, u.*
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
            tags=["mobility"],
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
                            COALESCE(SUM(CASE WHEN id_partner_university = %(id_partner_university)s THEN 1 ELSE 0 END), 0) AS already_exists,
                            MAX(CASE WHEN submission_date IS NOT NULL THEN 1 ELSE 0 END) AS is_submitted
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
    is_submitted = int((check_rows[0].get("is_submitted") or 0)) if check_rows else 0

    if is_submitted > 0:
        raise HTTPException(status_code=400, detail="Vos voeux ont déjà été soumis et ne peuvent plus être modifiés.")

    if wishes_count >= 5:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas ajouter plus de 5 voeux.")

    if already_exists > 0:
        raise HTTPException(status_code=400, detail="Cette universite est deja dans vos voeux.")

    next_priority = max_priority + 1

    # ToDo manage semester !!! default stub set as 8
    request = {
        "request": """
                        INSERT INTO MOB_wishes (id_etudiant, id_partner_university, priority, id_semestre)
                        VALUES (%(id_etudiant)s, %(id_partner_university)s, %(priority)s, %(id_semestre)s
                    """,
        "params": {
            "id_etudiant": id_etudiant,
            "id_partner_university": id_partner_university,
            "priority": next_priority,
            "id_semestre": 8,
        },
        "allowedRolesRequester": ["etudiant"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.delete("/university/etudiant/{id_etudiant:int}/wish/{id_partner_university:int}",
            tags=["mobility"],
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
                        SELECT priority, submission_date
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

    if check_rows[0].get("submission_date") is not None:
        raise HTTPException(status_code=400, detail="Vos voeux ont déjà été soumis et ne peuvent plus être modifiés.")

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
            tags=["mobility"],
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
                        SELECT priority, submission_date
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

    if current_rows[0].get("submission_date") is not None:
        raise HTTPException(status_code=400, detail="Vos voeux ont déjà été soumis et ne peuvent plus être modifiés.")

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
            tags=["mobility"],
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
                        SELECT 
                            COUNT(*) AS wishes_count,
                            MAX(CASE WHEN submission_date IS NOT NULL THEN 1 ELSE 0 END) AS is_submitted
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
    is_submitted = int((check_rows[0].get("is_submitted") or 0)) if check_rows else 0

    if is_submitted > 0:
        raise HTTPException(status_code=400, detail="Vos voeux ont déjà été soumis.")

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

    return {"message": "Voeux soumis avec succes."}



@router.get("/university/admin/wishes",
            tags=["mobility"],
            summary="All wishes for RI",
            description="Return all student wishes (submitted and in progress) for International Relations admins")
def list_all_wishes_ri(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
                        SELECT
                            e.id_etudiant,
                            e.nom AS etudiant_nom,
                            e.prenom AS etudiant_prenom,
                            e.mail AS etudiant_mail,
                            w.priority,
                            w.submission_date,
                            u.id_partner_university,
                            u.name AS university_name,
                            u.country AS university_country,
                            u.code AS university_code
                        FROM MOB_wishes w
                        JOIN LNM_etudiant e ON e.id_etudiant = w.id_etudiant
                        JOIN MOB_partner_university u ON u.id_partner_university = w.id_partner_university
                        ORDER BY e.nom ASC, e.prenom ASC, w.priority ASC
                    """,
        "allowedRolesRequester": ["relations_internationales"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/university/admin/catalog",
            tags=["mobility"],
            summary="University catalog for RI",
            description="Return partner universities enriched with their available filieres for International Relations admins")
def list_university_catalog_ri(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request": """
                        SELECT
                            u.*,
                            pl.number_of_places,
                            pr.annee,
                            pr.id_filiere,
                            f.nom_filiere,
                            f.nom_long
                        FROM MOB_partner_university_places pl
                        JOIN MOB_partner_university u ON u.id_partner_university = pl.id_partner_university
                        JOIN LNM_promo pr ON pr.id_promo = pl.id_promo
                        JOIN LNM_filiere f ON f.id_filiere = pr.id_filiere
                        ORDER BY u.name ASC, f.nom_filiere ASC, pr.annee ASC
                    """,
        "allowedRolesRequester": ["relations_internationales"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.post("/university/admin",
            tags=["mobility"],
            summary="Create partner university for RI",
            description="Create a partner university and its places by filiere/semester for International Relations admins")
def create_university_ri(
    payload: UniversityAdminPayload,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    name = payload.name.strip()
    country = payload.country.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Le nom de l'universite est obligatoire.")
    if not country:
        raise HTTPException(status_code=400, detail="Le pays est obligatoire.")

    insert_request = {
        "request": """
                        INSERT INTO MOB_partner_university (
                            name, code, country, address, latitude, longitude, website, 
                            languages, note_min, type
                        ) VALUES (
                            %(name)s, %(code)s, %(country)s, %(address)s, %(latitude)s, 
                            %(longitude)s, %(website)s, %(languages)s, %(note_min)s, %(type)s
                        )
                    """,
        "params": {
            "name": name,
            "code": payload.code,
            "country": country,
            "address": payload.address,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "website": payload.website,
            "languages": payload.languages,
            "note_min": payload.note_min,
            "type": payload.type,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }

    try:
        db_request(current_user, SQLRequest(**insert_request))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Creation impossible: {exc}")

    select_request = {
        "request": """
                        SELECT id_partner_university
                        FROM MOB_partner_university
                        WHERE name = %(name)s
                          AND country = %(country)s
                        ORDER BY id_partner_university DESC
                        LIMIT 1
                    """,
        "params": {
            "name": name,
            "country": country,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }
    rows = db_request(current_user, SQLRequest(**select_request))
    if not rows:
        raise HTTPException(status_code=500, detail="Universite creee mais identifiant introuvable.")

    id_partner_university = int(rows[0]["id_partner_university"])
    _sync_university_places(current_user, id_partner_university, payload.places)

    return {
        "message": "Universite creee.",
        "id_partner_university": id_partner_university,
    }


@router.put("/university/admin/{id_partner_university:int}",
            tags=["mobility"],
            summary="Update partner university for RI",
            description="Update a partner university and its places by filiere/semester for International Relations admins")
def update_university_ri(
    id_partner_university: int,
    payload: UniversityAdminPayload,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    exists_request = {
        "request": """
                        SELECT id_partner_university
                        FROM MOB_partner_university
                        WHERE id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_partner_university": id_partner_university,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }
    rows = db_request(current_user, SQLRequest(**exists_request))
    if not rows:
        raise HTTPException(status_code=404, detail="Universite introuvable.")

    name = payload.name.strip()
    country = payload.country.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Le nom de l'universite est obligatoire.")
    if not country:
        raise HTTPException(status_code=400, detail="Le pays est obligatoire.")

    update_request = {
        "request": """
                        UPDATE MOB_partner_university
                        SET
                            name = %(name)s,
                            code = %(code)s,
                            country = %(country)s,
                            address = %(address)s,
                            latitude = %(latitude)s,
                            longitude = %(longitude)s,
                            website = %(website)s,
                            languages = %(languages)s,
                            note_min = %(note_min)s,
                            type = %(type)s
                        WHERE id_partner_university = %(id_partner_university)s
                    """,
        "params": {
            "id_partner_university": id_partner_university,
            "name": name,
            "code": payload.code,
            "country": country,
            "address": payload.address,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "website": payload.website,
            "languages": payload.languages,
            "note_min": payload.note_min,
            "type": payload.type,
        },
        "allowedRolesRequester": ["relations_internationales"],
    }

    try:
        db_request(current_user, SQLRequest(**update_request))
        _sync_university_places(current_user, id_partner_university, payload.places)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Mise a jour impossible: {exc}")

    return {
        "message": "Universite mise a jour.",
        "id_partner_university": id_partner_university,
    }