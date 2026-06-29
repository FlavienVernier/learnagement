import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Annotated, Any, Dict, List, Optional
import time

assignment_progress = {
    "is_running": False,
    "progress": 0,
    "step": "",
    "error": None
}

from dependencies import db_request, get_current_active_user, User, SQLRequest

logger = logging.getLogger(__name__)

# Création du routeur FastAPI pour ce module
router = APIRouter()

from pydantic import BaseModel

class MobilityQuota(BaseModel):
    id_filiere: int
    id_semestre: int
    places: int

class AssignmentRunPayload(BaseModel):
    annee_eligible: int = 4
    mobility_quotas: List[MobilityQuota] = []

def get_eligible_students(current_user: User) -> List[dict]:
    """
    Étape 1: Récupérer les étudiants éligibles (4ème et 5ème année).
    Retourne une liste de dictionnaires avec id_etudiant, mobility_note, id_promo, id_filiere et submission_date.
    """
    query = """
        SELECT e.id_etudiant, e.mobility_z_score as z_score, e.id_promo, p.id_filiere, p.annee, MAX(w.submission_date) as submission_date
        FROM LNM_etudiant e
        JOIN LNM_promo p ON e.id_promo = p.id_promo
        JOIN MOB_wishes w ON e.id_etudiant = w.id_etudiant
        WHERE p.annee = 4
          AND w.submission_date IS NOT NULL
          AND e.mobility_z_score IS NOT NULL
        GROUP BY e.id_etudiant, e.mobility_z_score, e.id_promo, p.id_filiere, p.annee
    """
    request = {
        "request": query,
        "params": {},
        "allowedRolesRequester": ["relations_internationales"]
    }
    sql_request = SQLRequest(**request)
    result = db_request(current_user, sql_request)
    return result if result else []

def sort_students_by_z_score(students: List[dict]) -> List[dict]:
    """
    Étape 2: Trier les étudiants par Z-score (lu en BDD) décroissant 
    (et date de soumission des vœux en cas d'égalité).
    """
    sorted_students = sorted(
        students,
        key=lambda x: (-float(x["z_score"] or 0), x["submission_date"])
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

    Récupère en priorité les capacités de référence nécessaires à l'exécution
    de l'algorithme :
      - number_of_places : capacité initiale par spécialité/promo (MOB_partner_university_places)
      - S8_total_places  : capacité globale S8 par université (MOB_partner_university)
      - S9_total_places  : capacité globale S9 par université (MOB_partner_university)

    Les colonnes de suivi des places restantes (S8_remaining_places,
    S9_remaining_places, remaining_places) sont des sorties de l'algorithme ;
    elles sont mises à jour via save_assignments après le calcul.

    Gère la spécificité des stages (places illimitées).
    """
    # 1. Capacités de référence par spécialité/promo
    query_places = """
        SELECT id_partner_university, id_promo, number_of_places
        FROM MOB_partner_university_places
    """
    sql_places = SQLRequest(request=query_places, params={}, allowedRolesRequester=["relations_internationales"])
    places_rows = db_request(current_user, sql_places) or []

    # 2. Capacités globales de référence par semestre (S8 / S9)
    query_global = """
        SELECT id_partner_university, S8_total_places, S9_total_places
        FROM MOB_partner_university
        WHERE type != 'stage'
          AND (S8_total_places IS NOT NULL OR S9_total_places IS NOT NULL)
    """
    sql_global = SQLRequest(request=query_global, params={}, allowedRolesRequester=["relations_internationales"])
    global_rows = db_request(current_user, sql_global) or []

    # 3. Identifier les stages (places illimitées)
    query_stages = """
        SELECT id_partner_university
        FROM MOB_partner_university
        WHERE type = 'stage'
    """
    sql_stages = SQLRequest(request=query_stages, params={}, allowedRolesRequester=["relations_internationales"])
    stage_rows = db_request(current_user, sql_stages) or []

    # Formatage : specialty_places[str(id_university)][str(id_promo)] = nombre_de_places
    specialty_places = {}
    for row in places_rows:
        id_univ = str(row["id_partner_university"])
        id_promo = str(row["id_promo"])
        if id_univ not in specialty_places:
            specialty_places[id_univ] = {}
        specialty_places[id_univ][id_promo] = int(row["number_of_places"])

    # Formatage : global_places[str(id_university)] = {"S8": n, "S9": n}
    global_places = {}
    for row in global_rows:
        id_univ = str(row["id_partner_university"])
        global_places[id_univ] = {
            "S8": int(row["S8_total_places"]) if row["S8_total_places"] is not None else 0,
            "S9": int(row["S9_total_places"]) if row["S9_total_places"] is not None else 0,
        }

    stages_list = [row["id_partner_university"] for row in stage_rows]

    return {
        "specialty_places": specialty_places,  # capacités de référence par spécialité
        "global_places": global_places,         # capacités de référence globales S8/S9
        "stages": stages_list
    }

def run_round_robin_assignment(
    students: List[dict],
    wishes: List[dict],
    places: dict,
    mobility_quotas: List[MobilityQuota] = None
) -> Dict[str, Any]:
    """
    Étape 5: Logique d'affectation Round-Robin.

    Parcourt la liste des étudiants triés par Z-score décroissant.
    Pour chaque étudiant, examine ses vœux par ordre de priorité (1 à 5) :
      - Condition 1 : places globales S8 ou S9 restantes > 0 (toujours vrai si stage)
      - Condition 2 : places spécialité restantes > 0 (toujours vrai si stage)
      - Condition 3 : quota de départ restant (filière × semestre) > 0 (toujours vrai si stage)

    Si les 3 conditions sont satisfaites → affectation validée.
    Si aucun vœu n'est accepté → l'étudiant n'est pas inséré dans MOB_assignment.

    Retourne un dict :
      {
        "assignments"      : List[dict],  affectations validées
        "final_places"     : dict,        état des places restantes en mémoire
        "remaining_quotas" : dict          état des quotas restants par filière×semestre
      }
    Les quotas restants sont retournés en mémoire uniquement (pas persistés en base).
    """
    # --- Initialisation des places restantes (copie des capacités de référence) ---
    # global_places_left[str(id_university)]["S8"|"S9"] = places restantes
    global_places_left: Dict[str, Dict[str, int]] = {}
    for id_univ, semesters in (places.get("global_places") or {}).items():
        global_places_left[id_univ] = dict(semesters)  # copie

    # specialty_places_left[str(id_university)][str(id_promo)] = places restantes
    specialty_places_left: Dict[str, Dict[str, int]] = {}
    for id_univ, promos in (places.get("specialty_places") or {}).items():
        specialty_places_left[id_univ] = dict(promos)  # copie

    stages_set = set(places.get("stages") or [])

    # --- Initialisation des quotas restants (fournis par l'utilisateur) ---
    # remaining_quotas[id_filiere][id_semestre] = quota restant
    remaining_quotas: Dict[int, Dict[int, int]] = {}
    for q in (mobility_quotas or []):
        if q.id_filiere not in remaining_quotas:
            remaining_quotas[q.id_filiere] = {}
        remaining_quotas[q.id_filiere][q.id_semestre] = q.places

    # --- Index des vœux par étudiant ---
    wishes_by_student: Dict[int, List[dict]] = {}
    for w in wishes:
        student_id = w["id_etudiant"]
        if student_id not in wishes_by_student:
            wishes_by_student[student_id] = []
        wishes_by_student[student_id].append(w)
    # Les vœux sont déjà triés par priorité ASC depuis get_student_wishes

    # --- Boucle principale : parcours des étudiants par Z-score décroissant ---
    assignments = []
    for student in students:
        id_etudiant  = student["id_etudiant"]
        id_promo     = str(student["id_promo"])
        id_filiere   = student["id_filiere"]
        student_wishes = wishes_by_student.get(id_etudiant, [])

        assigned = False
        for wish in student_wishes:
            id_university = wish["id_partner_university"]
            id_univ_str   = str(id_university)
            id_semestre   = wish["id_semestre"]
            sem_key       = "S8" if id_semestre == 8 else "S9"
            is_stage      = id_university in stages_set

            # --- Condition 1 : places globales disponibles ---
            if is_stage:
                cond1 = True
            else:
                univ_global = global_places_left.get(id_univ_str, {})
                cond1 = univ_global.get(sem_key, 0) > 0

            if not cond1:
                logger.debug(
                    "Étudiant %s — vœu université %s sem %s refusé : places globales épuisées",
                    id_etudiant, id_university, id_semestre
                )
                continue

            # --- Condition 2 : places spécialité disponibles ---
            if is_stage:
                cond2 = True
            else:
                univ_specialty = specialty_places_left.get(id_univ_str, {})
                cond2 = univ_specialty.get(id_promo, 0) > 0

            if not cond2:
                logger.debug(
                    "Étudiant %s — vœu université %s sem %s refusé : places spécialité épuisées",
                    id_etudiant, id_university, id_semestre
                )
                continue

            # --- Condition 3 : quota de départ restant ---
            if is_stage:
                cond3 = True
            else:
                quota_sem = remaining_quotas.get(id_filiere, {}).get(id_semestre, 0)
                cond3 = quota_sem > 0

            if not cond3:
                logger.debug(
                    "Étudiant %s — vœu université %s sem %s refusé : quota filière épuisé",
                    id_etudiant, id_university, id_semestre
                )
                continue

            # --- Les 3 conditions sont satisfaites : affectation validée ---
            assignments.append({
                "id_etudiant":           id_etudiant,
                "id_partner_university": id_university,
                "id_semestre":           id_semestre,
                "status":                "accepted" if is_stage else "pending"
            })

            # Décrémentation des stocks (sauf stage)
            if not is_stage:
                global_places_left[id_univ_str][sem_key] -= 1
                specialty_places_left[id_univ_str][id_promo] -= 1
                remaining_quotas[id_filiere][id_semestre] -= 1

            assigned = True
            break  # passer à l'étudiant suivant

        if not assigned:
            logger.debug("Étudiant %s — aucun vœu accepté, non inséré dans MOB_assignment.", id_etudiant)
            # SUPPRESSION À LA DEMANDE DE L'UTILISATEUR :
            # Il n'y a plus d'affectation par défaut au stage pour les étudiants non affectés
            # (ni pour les retardataires, ni pour ceux dont les vœux ont tous été refusés).

    # --- Construction de l'état final des places restantes (pour persistance) ---
    final_places = {
        "global_places":    global_places_left,
        "specialty_places": specialty_places_left,
    }

    return {
        "assignments":      assignments,
        "final_places":     final_places,
        "remaining_quotas": remaining_quotas,
    }

def save_assignments(assignments: List[dict], final_places: dict, current_user: User) -> None:
    """
    Étape 6: Sauvegarder les affectations (statut 'pending') dans MOB_assignment
    et mettre à jour les places restantes en base de données.

    Met à jour :
      - S8_remaining_places / S9_remaining_places dans MOB_partner_university
      - remaining_places dans MOB_partner_university_places
    """
    # --- 6a. Supprimer les affectations précédentes non validées pour éviter les fantômes ---
    delete_pending = SQLRequest(
        request="DELETE FROM MOB_assignment WHERE status = 'pending'",
        params={},
        allowedRolesRequester=["relations_internationales"]
    )
    db_request(current_user, delete_pending)

    # --- 6b. Insérer les nouvelles affectations dans MOB_assignment ---
    if assignments:
        values_clause = []
        params = {}
        for i, assign in enumerate(assignments):
            status = assign.get("status", "pending")
            values_clause.append(f"(%(e{i})s, %(u{i})s, %(s{i})s, %(st{i})s)")
            params[f"e{i}"] = assign["id_etudiant"]
            params[f"u{i}"] = assign["id_partner_university"]
            params[f"s{i}"] = assign["id_semestre"]
            params[f"st{i}"] = status

        query = f"""
            INSERT INTO MOB_assignment (id_etudiant, id_partner_university, id_semestre, status)
            VALUES {", ".join(values_clause)}
            ON DUPLICATE KEY UPDATE
                id_partner_university = VALUES(id_partner_university),
                id_semestre           = VALUES(id_semestre),
                status                = VALUES(status)
        """
        sql_request = SQLRequest(
            request=query,
            params=params,
            allowedRolesRequester=["relations_internationales"]
        )
        db_request(current_user, sql_request)

    # --- 6b. Mettre à jour les places globales restantes (S8 / S9) ---
    global_remaining = (final_places or {}).get("global_places") or {}
    for id_univ_str, semesters in global_remaining.items():
        params_g = {
            "s8": semesters.get("S8"),
            "s9": semesters.get("S9"),
            "id_university": int(id_univ_str),
        }
        query_g = """
            UPDATE MOB_partner_university
            SET S8_remaining_places = %(s8)s,
                S9_remaining_places = %(s9)s
            WHERE id_partner_university = %(id_university)s
        """
        sql_g = SQLRequest(request=query_g, params=params_g, allowedRolesRequester=["relations_internationales"])
        db_request(current_user, sql_g)

    # --- 6c. Mettre à jour les places restantes par spécialité ---
    specialty_remaining = (final_places or {}).get("specialty_places") or {}
    for id_univ_str, promos in specialty_remaining.items():
        for id_promo_str, remaining in promos.items():
            params_sp = {
                "remaining": remaining,
                "id_university": int(id_univ_str),
                "id_promo": int(id_promo_str),
            }
            query_sp = """
                UPDATE MOB_partner_university_places
                SET remaining_places = %(remaining)s
                WHERE id_partner_university = %(id_university)s
                  AND id_promo              = %(id_promo)s
            """
            sql_sp = SQLRequest(request=query_sp, params=params_sp, allowedRolesRequester=["relations_internationales"])
            db_request(current_user, sql_sp)

@router.get("/university/admin/assignment/status", tags=["admin", "mobility"], summary="Get assignment progress")
def get_assignment_status():
    return assignment_progress

def execute_assignment_task(payload: AssignmentRunPayload, current_user: User):
    global assignment_progress
    assignment_progress = {
        "is_running": True,
        "progress": 0,
        "step": "Démarrage...",
        "error": None
    }
    try:
        time.sleep(0.5)
        assignment_progress["progress"] = 10
        assignment_progress["step"] = "Étape 1 : Récupération des étudiants éligibles..."
        students = get_eligible_students(current_user=current_user)
        
        time.sleep(0.5)
        assignment_progress["progress"] = 30
        assignment_progress["step"] = "Étape 2 : Tri des étudiants..."
        sorted_students = sort_students_by_z_score(students)
        
        time.sleep(0.5)
        assignment_progress["progress"] = 50
        assignment_progress["step"] = "Étape 3 : Récupération des vœux et places disponibles..."
        wishes = get_student_wishes(current_user)
        places = get_available_places(current_user)
        
        time.sleep(0.5)
        assignment_progress["progress"] = 70
        assignment_progress["step"] = "Étape 4 : Exécution de l'algorithme Round-Robin..."
        result = run_round_robin_assignment(sorted_students, wishes, places, payload.mobility_quotas)
        assignments = result["assignments"]
        final_places = result["final_places"]
        
        time.sleep(0.5)
        assignment_progress["progress"] = 90
        assignment_progress["step"] = "Étape 5 : Sauvegarde des affectations..."
        save_assignments(assignments, final_places, current_user)
        
        time.sleep(0.5)
        assignment_progress["progress"] = 100
        assignment_progress["step"] = "Terminé !"
        assignment_progress["is_running"] = False
    except Exception as e:
        logger.error(f"Erreur algorithme affectation: {e}")
        assignment_progress["error"] = str(e)
        assignment_progress["is_running"] = False

@router.post("/university/admin/assignment/run",
            tags=["admin", "mobility"],
            summary="Run assignment algorithm",
            description="Lancer l'algorithme d'affectation automatique pour la mobilité internationale")
def run_mobility_assignment(
    payload: AssignmentRunPayload,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Route principale de l'algorithme (asynchrone).
    Seuls les administrateurs RI pourront lancer cette route.
    """
    if assignment_progress["is_running"]:
        raise HTTPException(status_code=400, detail="Une affectation est déjà en cours.")
        
    background_tasks.add_task(execute_assignment_task, payload, current_user)
    return {"message": "Algorithme d'affectation démarré en arrière-plan."}

