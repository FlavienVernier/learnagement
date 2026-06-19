import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
import openpyxl
from datetime import datetime
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
                        )
                        UNION
                        SELECT u.*, 999 as number_of_places, 4 as annee
                        FROM MOB_partner_university u
                        WHERE u.type = 'stage'
                        UNION
                        SELECT u.*, 999 as number_of_places, 5 as annee
                        FROM MOB_partner_university u
                        WHERE u.type = 'stage';
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
                        VALUES (%(id_etudiant)s, %(id_partner_university)s, %(priority)s, %(id_semestre)s)
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

@router.post("/university/admin/wishes/force-submit",
            tags=["admin", "mobility"],
            summary="Force submit all incomplete wishes",
            description="Force the submission of all existing student wishes that have not been submitted yet.")
def force_submit_wishes(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    update_request = {
        "request": """
                        UPDATE MOB_wishes
                        SET submission_date = NOW()
                        WHERE submission_date IS NULL
                    """,
        "params": None,
        "allowedRolesRequester": ["relations_internationales"],
    }
    db_request(current_user, SQLRequest(**update_request))
    return {"message": "Tous les voeux incomplets ont ete clotures avec succes."}


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

@router.get("/university/admin/wishes/export",
            tags=["admin", "mobility"],
            summary="Export student mobility wishes to Excel")
def export_admin_wishes(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT
                e.nom AS Nom,
                e.prenom AS Prenom,
                e.mail AS Email,
                f.nom_filiere AS Filiere,
                p.annee AS Annee,
                s.nom_statut AS Statut,
                IFNULL(e.mobility_note, 'N/A') AS Note,
                w.priority AS Priorite,
                u.name AS Universite_Partenaire,
                u.country AS Pays,
                sem.semestre AS Semestre_Demande,
                w.submission_date AS Date_Soumission
            FROM MOB_wishes w
            JOIN LNM_etudiant e ON e.id_etudiant = w.id_etudiant
            JOIN LNM_promo p ON p.id_promo = e.id_promo
            JOIN LNM_filiere f ON f.id_filiere = p.id_filiere
            JOIN LNM_statut s ON s.id_statut = p.id_statut
            JOIN MOB_partner_university u ON u.id_partner_university = w.id_partner_university
            JOIN LNM_semestre sem ON sem.id_semestre = w.id_semestre
            ORDER BY e.nom ASC, e.prenom ASC, w.priority ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Voeux Etudiants"
    
    headers = [
        "Nom", "Prénom", "Email", "Filière", "Année", "Statut", 
        "Note de Mobilité", "Priorité", "Université Partenaire", 
        "Pays", "Semestre Demandé", "Date de Soumission"
    ]
    ws.append(headers)
    
    for row in result:
        ws.append([
            row.get("Nom", ""), row.get("Prenom", ""), row.get("Email", ""),
            row.get("Filiere", ""), row.get("Annee", ""), row.get("Statut", ""),
            row.get("Note", ""), row.get("Priorite", ""), row.get("Universite_Partenaire", ""),
            row.get("Pays", ""), row.get("Semestre_Demande", ""),
            str(row.get("Date_Soumission", "")) if row.get("Date_Soumission") else "Non Soumis"
        ])
        
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"Export_Voeux_Mobilite_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    headers_dict = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return StreamingResponse(
        stream, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers_dict
    )

@router.get("/university/admin/assignments/export",
            tags=["admin", "mobility"],
            summary="Export student mobility assignments to Excel")
def export_admin_assignments(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT
                e.nom AS Nom,
                e.prenom AS Prenom,
                e.mail AS Email,
                f.nom_filiere AS Filiere,
                p.annee AS Annee,
                s.nom_statut AS Statut,
                IFNULL(e.mobility_note, 'N/A') AS Note,
                u.name AS Universite_Affectee,
                u.country AS Pays,
                sem.semestre AS Semestre_Affecte,
                a.status AS Statut_Affectation
            FROM MOB_assignment a
            JOIN LNM_etudiant e ON e.id_etudiant = a.id_etudiant
            JOIN LNM_promo p ON p.id_promo = e.id_promo
            JOIN LNM_filiere f ON f.id_filiere = p.id_filiere
            JOIN LNM_statut s ON s.id_statut = p.id_statut
            JOIN MOB_partner_university u ON u.id_partner_university = a.id_partner_university
            JOIN LNM_semestre sem ON sem.id_semestre = a.id_semestre
            ORDER BY e.nom ASC, e.prenom ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Affectations Etudiants"
    
    headers = [
        "Nom", "Prénom", "Email", "Filière", "Année", "Statut", 
        "Note de Mobilité", "Université Affectée", "Pays", 
        "Semestre Affecté", "Statut de l'affectation"
    ]
    ws.append(headers)
    
    for row in result:
        ws.append([
            row.get("Nom", ""), row.get("Prenom", ""), row.get("Email", ""),
            row.get("Filiere", ""), row.get("Annee", ""), row.get("Statut", ""),
            row.get("Note", ""), row.get("Universite_Affectee", ""),
            row.get("Pays", ""), row.get("Semestre_Affecte", ""), row.get("Statut_Affectation", "")
        ])
        
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"Export_Affectations_Mobilite_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    headers_dict = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return StreamingResponse(
        stream, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers_dict
    )

@router.get("/university/admin/mobility/submitted-students",
            tags=["admin", "mobility"],
            summary="Get list of students who have submitted wishes")
def get_submitted_students(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT e.id_etudiant, e.nom, e.prenom, e.mail, f.nom_filiere
            FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            WHERE p.annee IN (4, 5)
              AND e.mobility_completed = 0
              AND EXISTS (
                  SELECT 1 FROM MOB_wishes w 
                  WHERE w.id_etudiant = e.id_etudiant 
                    AND w.submission_date IS NOT NULL
              )
            ORDER BY e.nom ASC, e.prenom ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    return result if result else []

@router.post("/university/admin/mobility/reset-wishes/{id_etudiant}",
             tags=["admin", "mobility"],
             summary="Reset submission date for a student's wishes")
def reset_student_wishes(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    check_request = SQLRequest(
        request='''
            SELECT 1 FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            WHERE e.id_etudiant = %(id)s AND p.annee IN (4, 5) AND e.mobility_completed = 0
        ''',
        params={"id": id_etudiant},
        allowedRolesRequester=["relations_internationales"]
    )
    if not db_request(current_user, check_request):
        raise HTTPException(status_code=400, detail="Étudiant invalide ou non éligible.")

    sql_request = SQLRequest(
        request='''
            UPDATE MOB_wishes
            SET submission_date = NULL
            WHERE id_etudiant = %(id)s
        ''',
        params={"id": id_etudiant},
        allowedRolesRequester=["relations_internationales"]
    )
    db_request(current_user, sql_request)
    return {"message": "La soumission a été annulée avec succès."}

class UpdateAssignmentStatusPayload(BaseModel):
    id_assignment: int
    new_status: str

@router.get("/university/admin/mobility/assigned-students",
            tags=["admin", "mobility"],
            summary="Get list of students who have an assignment")
def get_assigned_students(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT a.id_assignment, a.id_etudiant, a.status, e.nom, e.prenom, e.mail, 
                   f.nom_filiere, u.name as university_name
            FROM MOB_assignment a
            JOIN LNM_etudiant e ON a.id_etudiant = e.id_etudiant
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            JOIN MOB_partner_university u ON a.id_partner_university = u.id_partner_university
            ORDER BY e.nom ASC, e.prenom ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    return result if result else []

@router.get("/university/admin/mobility/assigned-students/export/{status}",
            tags=["admin", "mobility"],
            summary="Export assigned students by status")
def export_assigned_students_status(
    status: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if status not in ['accepted', 'pending', 'declined']:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    sql_request = SQLRequest(
        request='''
            SELECT a.id_etudiant, a.status, e.nom, e.prenom, e.mail, 
                   f.nom_filiere, u.name as university_name, u.country
            FROM MOB_assignment a
            JOIN LNM_etudiant e ON e.id_etudiant = a.id_etudiant
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            JOIN MOB_partner_university u ON a.id_partner_university = u.id_partner_university
            WHERE a.status = %(status)s
            ORDER BY e.nom ASC, e.prenom ASC
        ''',
        params={"status": status},
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    
    import openpyxl
    import io
    from fastapi.responses import StreamingResponse
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Affectations {status.capitalize()}"
    
    headers = ["ID Etudiant", "Nom", "Prénom", "Email", "Filière", "Université Attribuée", "Pays", "Statut"]
    ws.append(headers)
    
    if result:
        for row in result:
            ws.append([
                row.get("id_etudiant", ""),
                row.get("nom", ""),
                row.get("prenom", ""),
                row.get("mail", ""),
                row.get("nom_filiere", ""),
                row.get("university_name", ""),
                row.get("country", ""),
                row.get("status", "")
            ])
            
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"Export_Affectations_{status}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    headers_res = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return StreamingResponse(iter([stream.getvalue()]), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers_res)

@router.post("/university/admin/mobility/update-assignment-status",
             tags=["admin", "mobility"],
             summary="Update assignment status")
def update_assignment_status(
    payload: UpdateAssignmentStatusPayload,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if payload.new_status not in ['pending', 'accepted', 'declined']:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    sql_request = SQLRequest(
        request='UPDATE MOB_assignment SET status = %(status)s WHERE id_assignment = %(id)s',
        params={"status": payload.new_status, "id": payload.id_assignment},
        allowedRolesRequester=["relations_internationales"]
    )
    db_request(current_user, sql_request)
    return {"message": "Assignment status updated successfully"}

@router.get("/university/admin/mobility/diagnostics",
            tags=["admin", "mobility"],
            summary="Get statistics and diagnostics for mobility procedure")
def get_mobility_diagnostics(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT 
                e.id_etudiant,
                e.mobility_completed,
                (SELECT COUNT(w.id_partner_university) FROM MOB_wishes w WHERE w.id_etudiant = e.id_etudiant) as wish_count,
                (SELECT MAX(w.submission_date) FROM MOB_wishes w WHERE w.id_etudiant = e.id_etudiant) as last_submission_date
            FROM LNM_etudiant e 
            JOIN LNM_promo p ON e.id_promo = p.id_promo 
            WHERE p.annee IN (4, 5)
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    
    validated_mobility = 0
    remaining_students = 0
    
    wishes_submitted = 0
    wishes_in_progress = 0
    retardataires = 0
    
    wishes_distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}

    if result:
        for row in result:
            if row.get("mobility_completed") == 1:
                validated_mobility += 1
            else:
                remaining_students += 1
                wish_count = row.get("wish_count", 0)
                last_sub = row.get("last_submission_date")
                
                # Distribution of wishes (only for remaining students)
                if wish_count == 0:
                    retardataires += 1
                else:
                    last_sub_str = str(last_sub).strip().lower() if last_sub is not None else ""
                    if last_sub_str and last_sub_str not in ["none", "null", "0000-00-00 00:00:00", "0000-00-00", "0"]:
                        wishes_submitted += 1
                    else:
                        wishes_in_progress += 1
                    
                    # Update distribution (clamp to max 5)
                    w_key = str(min(wish_count, 5))
                    wishes_distribution[w_key] = wishes_distribution.get(w_key, 0) + 1

    return {
        "validated_mobility": validated_mobility,
        "remaining_students": remaining_students,
        "wishes_submitted": wishes_submitted,
        "wishes_in_progress": wishes_in_progress,
        "retardataires": retardataires,
        "wishes_distribution": wishes_distribution
    }

@router.get("/university/admin/mobility/diagnostics/export/{category}",
            tags=["admin", "mobility"],
            summary="Export specific diagnostic category to Excel")
def export_mobility_diagnostics(
    category: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT 
                e.id_etudiant,
                e.nom,
                e.prenom,
                e.mail,
                f.nom_filiere,
                e.mobility_note,
                e.mobility_completed,
                (SELECT COUNT(w.id_partner_university) FROM MOB_wishes w WHERE w.id_etudiant = e.id_etudiant) as wish_count,
                (SELECT MAX(w.submission_date) FROM MOB_wishes w WHERE w.id_etudiant = e.id_etudiant) as last_submission_date
            FROM LNM_etudiant e 
            JOIN LNM_promo p ON e.id_promo = p.id_promo 
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            WHERE p.annee IN (4, 5)
            ORDER BY e.nom ASC, e.prenom ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    
    filtered_students = []
    
    if result:
        for row in result:
            wish_count = row.get("wish_count", 0)
            last_sub = row.get("last_submission_date")
            is_completed = row.get("mobility_completed") == 1
            
            last_sub_str = str(last_sub).strip().lower() if last_sub is not None else ""
            is_submitted = last_sub_str and last_sub_str not in ["none", "null", "0000-00-00 00:00:00", "0000-00-00", "0"]
            
            match = False
            if category == "validated" and is_completed:
                match = True
            elif category == "remaining" and not is_completed:
                match = True
            elif category == "submitted" and not is_completed and wish_count > 0 and is_submitted:
                match = True
            elif category == "in_progress" and not is_completed and wish_count > 0 and not is_submitted:
                match = True
            elif category == "retardataires" and not is_completed and wish_count == 0:
                match = True
                
            if match:
                filtered_students.append(row)
                
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Export {category.capitalize()}"
    
    headers = [
        "ID Etudiant", "Nom", "Prénom", "Email", "Filière", "Note de Mobilité"
    ]
    if category not in ["retardataires", "validated"]:
        headers.append("Nombre de vœux enregistrés")
        
    ws.append(headers)
    
    for student in filtered_students:
        row_data = [
            student.get("id_etudiant", ""),
            student.get("nom", ""),
            student.get("prenom", ""),
            student.get("mail", ""),
            student.get("nom_filiere", ""),
            student.get("mobility_note", "")
        ]
        if category not in ["retardataires", "validated"]:
            row_data.append(student.get("wish_count", 0))
            
        ws.append(row_data)
        
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"Export_{category}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    headers_dict = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return StreamingResponse(
        stream, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers_dict
    )

@router.get("/university/admin/places/export",
            tags=["admin", "mobility"],
            summary="Export partner university places status to Excel")
def export_admin_places(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # Requête pour récupérer les universités, leurs places globales (S8/S9) et le détail par filière.
    sql_request = SQLRequest(
        request='''
            SELECT 
                u.id_partner_university,
                u.name AS university_name,
                u.country,
                IFNULL(u.S8_total_places, 0) AS S8_total,
                IFNULL(u.S9_total_places, 0) AS S9_total,
                IFNULL(u.S8_remaining_places, IFNULL(u.S8_total_places, 0)) AS S8_restant,
                IFNULL(u.S9_remaining_places, IFNULL(u.S9_total_places, 0)) AS S9_restant,
                f.nom_filiere,
                pr.annee,
                pl.number_of_places AS filiere_total,
                IFNULL(pl.remaining_places, pl.number_of_places) AS filiere_restant
            FROM MOB_partner_university u
            LEFT JOIN MOB_partner_university_places pl ON u.id_partner_university = pl.id_partner_university
            LEFT JOIN LNM_promo pr ON pl.id_promo = pr.id_promo
            LEFT JOIN LNM_filiere f ON pr.id_filiere = f.id_filiere
            WHERE u.type != 'stage'
            ORDER BY u.name ASC, f.nom_filiere ASC, pr.annee ASC
        ''',
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    result = db_request(current_user, sql_request)
    # Récupérer la liste des filières pour construire les colonnes
    filiere_req = SQLRequest(request='SELECT nom_filiere FROM LNM_filiere ORDER BY nom_filiere ASC', allowedRolesRequester=["relations_internationales"])
    filieres_result = db_request(current_user, filiere_req)
    filieres = [f['nom_filiere'] for f in filieres_result] if filieres_result else []

    # Récupérer les affectations actives (acceptées ou en attente) pour calculer le vrai reste
    assign_req = SQLRequest(request='''
        SELECT a.id_partner_university, a.id_semestre, f.nom_filiere
        FROM MOB_assignment a
        JOIN LNM_etudiant e ON a.id_etudiant = e.id_etudiant
        JOIN LNM_promo p ON e.id_promo = p.id_promo
        JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
        WHERE a.status = 'accepted'
    ''', allowedRolesRequester=["relations_internationales"])
    assign_result = db_request(current_user, assign_req)
    
    taken_global = {}
    taken_filiere = {}
    if assign_result:
        for a in assign_result:
            u_id = a.get('id_partner_university')
            sem = a.get('id_semestre')
            f_nom = a.get('nom_filiere')
            
            taken_global[(u_id, sem)] = taken_global.get((u_id, sem), 0) + 1
            taken_filiere[(u_id, sem, f_nom)] = taken_filiere.get((u_id, sem, f_nom), 0) + 1
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Etat des Places"
    
    headers = [
        "Université", "Pays", 
        "Total S8 Initial", "Total S8 Restant",
        "Total S9 Initial", "Total S9 Restant"
    ]
    
    for f in filieres:
        headers.append(f"S8 {f} Initial")
        headers.append(f"S8 {f} Restant")
        
    for f in filieres:
        headers.append(f"S9 {f} Initial")
        headers.append(f"S9 {f} Restant")
        
    ws.append(headers)
    
    if result:
        uni_map = {}
        for row in result:
            u_name = row.get("university_name", "")
            u_id = row.get("id_partner_university")
            
            if u_name not in uni_map:
                s8_tot = row.get("S8_total", 0)
                s9_tot = row.get("S9_total", 0)
                uni_map[u_name] = {
                    "pays": row.get("country", ""),
                    "S8_total": s8_tot,
                    "S9_total": s9_tot,
                    "S8_restant": max(0, s8_tot - taken_global.get((u_id, 8), 0)),
                    "S9_restant": max(0, s9_tot - taken_global.get((u_id, 9), 0)),
                    "filieres": {}
                }
            
            annee = row.get('annee')
            nom_filiere = row.get("nom_filiere")
            if annee and nom_filiere:
                sem_num = 8 if annee == 4 else (9 if annee == 5 else annee * 2)
                sem = f"S{sem_num}"
                key = f"{sem}_{nom_filiere}"
                fil_tot = row.get("filiere_total", 0)
                uni_map[u_name]["filieres"][key] = {
                    "total": fil_tot,
                    "restant": max(0, fil_tot - taken_filiere.get((u_id, sem_num, nom_filiere), 0))
                }
                
        for u_name, data in uni_map.items():
            row_data = [
                u_name,
                data["pays"],
                data["S8_total"],
                data["S8_restant"],
                data["S9_total"],
                data["S9_restant"]
            ]
            
            for f in filieres:
                key_s8 = f"S8_{f}"
                if key_s8 in data["filieres"]:
                    row_data.append(data["filieres"][key_s8]["total"])
                    row_data.append(data["filieres"][key_s8]["restant"])
                else:
                    row_data.append("")
                    row_data.append("")
                    
            for f in filieres:
                key_s9 = f"S9_{f}"
                if key_s9 in data["filieres"]:
                    row_data.append(data["filieres"][key_s9]["total"])
                    row_data.append(data["filieres"][key_s9]["restant"])
                else:
                    row_data.append("")
                    row_data.append("")
                    
            ws.append(row_data)
            
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    
    filename = f"Export_Etat_Places_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    headers_dict = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return StreamingResponse(
        stream, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers_dict
    )

class StudentDecisionPayload(BaseModel):
    decision: str

@router.get("/university/etudiant/{id_etudiant}/assignment",
            tags=["etudiant", "mobility"],
            summary="Get the assigned university for a student")
def get_student_assignment(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request='''
            SELECT a.id_assignment, a.status, u.id_partner_university, u.name, u.code, u.country, u.address
            FROM MOB_assignment a
            JOIN MOB_partner_university u ON a.id_partner_university = u.id_partner_university
            WHERE a.id_etudiant = %(id)s
        ''',
        params={"id": id_etudiant},
        allowedRolesRequester=["etudiant"]
    )
    result = db_request(current_user, sql_request)
    if result and len(result) > 0:
        return result[0]
    return None

@router.post("/university/etudiant/{id_etudiant}/assignment/decision",
             tags=["etudiant", "mobility"],
             summary="Submit student decision for assignment")
def submit_student_decision(
    id_etudiant: int,
    payload: StudentDecisionPayload,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if payload.decision not in ['accepted', 'declined']:
        raise HTTPException(status_code=400, detail="Invalid decision. Must be 'accepted' or 'declined'.")

    # Vérifier que l'affectation existe et est "pending"
    check_request = SQLRequest(
        request='SELECT id_assignment, status FROM MOB_assignment WHERE id_etudiant = %(id)s',
        params={"id": id_etudiant},
        allowedRolesRequester=["etudiant"]
    )
    assignment = db_request(current_user, check_request)
    
    if not assignment or len(assignment) == 0:
        raise HTTPException(status_code=404, detail="Aucune affectation trouvée pour cet étudiant.")
        
    if assignment[0]["status"] != 'pending':
        raise HTTPException(status_code=400, detail="La décision a déjà été prise pour cette affectation.")

    # Mettre à jour le statut
    update_request = SQLRequest(
        request='UPDATE MOB_assignment SET status = %(status)s WHERE id_etudiant = %(id)s',
        params={"status": payload.decision, "id": id_etudiant},
        allowedRolesRequester=["etudiant"]
    )
    db_request(current_user, update_request)
    
    return {"message": "Décision enregistrée avec succès"}

@router.post("/university/admin/mobility/assignment/close",
             tags=["admin", "mobility"],
             summary="Decline all pending assignments to close the acceptance phase")
def close_assignment_phase(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    sql_request = SQLRequest(
        request="UPDATE MOB_assignment SET status = 'declined' WHERE status = 'pending'",
        params=None,
        allowedRolesRequester=["relations_internationales"]
    )
    db_request(current_user, sql_request)
    return {"message": "Toutes les affectations en attente ont été refusées."}