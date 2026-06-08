import logging

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any, Dict, List, Optional

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

# Création du routeur FastAPI pour ce module
router = APIRouter()

from pydantic import BaseModel

class AssignmentRunPayload(BaseModel):
    annee_eligible: int = 4
    filiere_limits: Dict[str, int] = {}

def get_eligible_students(current_user: User, annee: int) -> List[dict]:
    """
    Étape 1: Récupérer les étudiants éligibles.
    Retourne une liste de dictionnaires avec id_etudiant, mobility_note, id_promo, id_filiere et submission_date.
    """
    query = f"""
        SELECT e.id_etudiant, e.mobility_note, e.id_promo, p.id_filiere, MAX(w.submission_date) as submission_date
        FROM LNM_etudiant e
        JOIN LNM_promo p ON e.id_promo = p.id_promo
        JOIN MOB_wishes w ON e.id_etudiant = w.id_etudiant
        WHERE p.annee = %(annee)s
          AND w.submission_date IS NOT NULL
        GROUP BY e.id_etudiant, e.mobility_note, e.id_promo, p.id_filiere
    """
    request = {
        "request": query,
        "params": {
            "annee": annee
        },
        "allowedRolesRequester": ["relations_internationales"]
    }
    sql_request = SQLRequest(**request)
    result = db_request(current_user, sql_request)
    return result if result else []

def calculate_z_scores(students: List[dict]) -> List[dict]:
    """
    Étape 2: Calculer la moyenne centrée réduite (Z-score) par promo.
    Trie les étudiants par Z-score décroissant (et date de soumission des vœux en cas d'égalité).
    """
    import math
    from collections import defaultdict

    # Regrouper les notes par promo
    promo_notes = defaultdict(list)
    for s in students:
        promo_notes[s["id_promo"]].append(float(s["mobility_note"]))
            
    # Calculer la moyenne et l'écart-type par promo
    promo_stats = {}
    for promo, notes in promo_notes.items():
        n = len(notes)
        if n == 0:
            mean, std = 0.0, 0.0
        else:
            mean = sum(notes) / n
            variance = sum((x - mean) ** 2 for x in notes) / n
            std = math.sqrt(variance)
        promo_stats[promo] = {"mean": mean, "std": std}
        
    # Calculer le z-score pour chaque étudiant
    for s in students:
        note = float(s["mobility_note"])
        stats = promo_stats[s["id_promo"]]
        if stats["std"] > 0:
            s["z_score"] = (note - stats["mean"]) / stats["std"]
        else:
            s["z_score"] = 0.0
                
    # Trier par z_score (décroissant), puis par submission_date (croissant)
    # L'utilisation du tuple (-z_score, date) permet ce double tri
    sorted_students = sorted(
        students,
        key=lambda x: (-x["z_score"], x["submission_date"])
    )
    return sorted_students

def get_student_wishes(current_user: User) -> List[dict]:
    """
    Étape 3: Récupérer tous les vœux soumis (submission_date IS NOT NULL).
    Trie par id_etudiant puis par priorité croissante.
    """
    query = """
        SELECT id_etudiant, id_partner_university, id_semestre, priority
        FROM MOB_wishes
        WHERE submission_date IS NOT NULL
        ORDER BY id_etudiant ASC, priority ASC
    """
    request = {
        "request": query,
        "params": {},
        "allowedRolesRequester": ["relations_internationales"]
    }
    sql_request = SQLRequest(**request)
    result = db_request(current_user, sql_request)
    return result if result else []

def get_available_places(current_user: User) -> dict:
    """
    Étape 4: Récupérer les places disponibles par université et promo.
    Gère la spécificité des stages (places illimitées).
    """
    # 1. Récupérer les quotas par filière (promo)
    query_places = """
        SELECT id_partner_university, id_promo, number_of_places
        FROM MOB_partner_university_places
        WHERE number_of_places > 0
    """
    sql_places = SQLRequest(request=query_places, params={}, allowedRolesRequester=["relations_internationales"])
    places_rows = db_request(current_user, sql_places) or []
    
    # 2. Identifier les stages (qui ont des places illimitées)
    query_stages = """
        SELECT id_partner_university
        FROM MOB_partner_university
        WHERE type = 'stage'
    """
    sql_stages = SQLRequest(request=query_stages, params={}, allowedRolesRequester=["relations_internationales"])
    stage_rows = db_request(current_user, sql_stages) or []
    
    # Formatage : places_dict[str(id_university)][str(id_promo)] = nombre_de_places
    places_dict = {}
    for row in places_rows:
        id_univ = str(row["id_partner_university"])
        id_promo = str(row["id_promo"])
        if id_univ not in places_dict:
            places_dict[id_univ] = {}
        places_dict[id_univ][id_promo] = int(row["number_of_places"])
        
    stages_list = [row["id_partner_university"] for row in stage_rows]
    
    return {
        "quotas": places_dict,
        "stages": stages_list
    }

def run_round_robin_assignment(students: List[dict], wishes: List[dict], places: dict, filiere_limits: Dict[str, int] = None) -> List[dict]:
    """
    Étape 5: Logique d'affectation Round-Robin.
    Retourne la liste des affectations validées.
    """
    assignments = []
    return assignments

def save_assignments(assignments: List[dict], current_user: User) -> None:
    """
    Étape 6: Sauvegarder les affectations (statut 'pending') dans MOB_assignment.
    """
    if not assignments:
        return
        
    values_clause = []
    params = {}
    for i, assign in enumerate(assignments):
        values_clause.append(f"(%(e{i})s, %(u{i})s, %(s{i})s, 'pending')")
        params[f"e{i}"] = assign["id_etudiant"]
        params[f"u{i}"] = assign["id_partner_university"]
        params[f"s{i}"] = assign["id_semestre"]
        
    query = f"""
        INSERT INTO MOB_assignment (id_etudiant, id_partner_university, id_semestre, status)
        VALUES {", ".join(values_clause)}
        ON DUPLICATE KEY UPDATE 
            id_partner_university = VALUES(id_partner_university),
            id_semestre = VALUES(id_semestre),
            status = VALUES(status)
    """
    
    sql_request = SQLRequest(
        request=query,
        params=params,
        allowedRolesRequester=["relations_internationales"]
    )
    db_request(current_user, sql_request)

@router.post("/university/admin/assignment/run",
            tags=["admin", "mobility"],
            summary="Run assignment algorithm",
            description="Lancer l'algorithme d'affectation automatique pour la mobilité internationale")
def run_mobility_assignment(
    payload: AssignmentRunPayload,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Route principale de l'algorithme.
    Seuls les administrateurs RI pourront lancer cette route.
    """
    
    # Étape 1 : Récupérer les étudiants
    students = get_eligible_students(
        current_user=current_user,
        annee=payload.annee_eligible
    )
    # return {"eligible_students": students}
    
    # Étape 2 : Calculer les Z-scores et trier
    sorted_students = calculate_z_scores(students)
    
    # Étape 3 : Récupérer les vœux
    wishes = get_student_wishes(current_user)
    
    # Étape 4 : Récupérer les places
    places = get_available_places(current_user)
    
    # Étape 5 : Exécuter l'algorithme Round-Robin
    assignments = run_round_robin_assignment(sorted_students, wishes, places, payload.filiere_limits)
    
    # Étape 6 : Sauvegarder les résultats
    save_assignments(assignments, current_user)
    
    return {"message": "Algorithme d'affectation terminé avec succès !"}
