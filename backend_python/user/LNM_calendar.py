from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dependencies import SQLRequest, db_request, get_current_active_user, User

router = APIRouter()

# Modèle pour l'insertion/mise à jour
class CalendarUpdate(BaseModel):
    url: str
    url_name: str = "Planning des cours"

######################################################
#
# Helper : Obtenir le rôle et le vrai ID depuis la vue
#
######################################################
def get_user_role_and_id(current_user: User):
    """
    Interroge la vue SQL pour récupérer le vrai ID et le rôle 
    basé sur l'mail de l'utilisateur connecté.
    """
    req = {
        "request": "SELECT id, role FROM VIEW_users_default_role WHERE mail = %(mail)s LIMIT 1;",
        # Assure-toi que l'attribut s'appelle bien "mail" dans ton modèle User.
        # Si c'est "mail" ou "username", modifie la ligne ci-dessous.
        "params": {"mail": current_user.mail}, 
        "allowedRolesRequester": ["user"],
    }
    
    response = db_request(current_user, SQLRequest(**req))
    
    if not isinstance(response, list) or len(response) == 0:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable dans la vue des rôles.")
        
    user_data = response[0]
    user_type = user_data.get("role", "etudiant").lower()
    role_id = user_data.get("id")
    
    # Détermination de la bonne colonne
    role_col = "id_etudiant"
    if user_type == "enseignant":
        role_col = "id_enseignant"
    elif user_type == "administratif":
        role_col = "id_administratif"
        
    return role_id, role_col, user_type


######################################################
#
# Get Calendars : /user/calendar/
#
######################################################

@router.get("/user/calendar/",
            tags=["user", "calendar"],
            summary="Get User Calendar URLs",
            description="Returns all ADE iCal URLs for the currently logged-in user")
def get_user_calendar_urls(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    # 1. On récupère le bon ID et la bonne colonne via notre Helper
    role_id, role_col, _ = get_user_role_and_id(current_user)
    
    # 2. On cherche le calendrier en utilisant spécifiquement cette colonne
    request = {
        "request": f"""
            SELECT url_name, url 
            FROM LNM_calendar 
            WHERE {role_col} = %(role_id)s 
            ORDER BY url_name ASC;
        """,
        "params": {
            "role_id": role_id,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))


######################################################
#
# Update/Insert Calendar : /user/calendar/update/
#
######################################################

@router.post("/user/calendar/update/",
             tags=["user", "calendar"],
             summary="Update User Calendar URL",
             description="Saves or updates a specific ADE iCal URL")
def update_user_calendar_url(
    data: CalendarUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    # 1. On récupère le bon ID et la bonne colonne via notre Helper
    role_id, role_col, user_type = get_user_role_and_id(current_user)
        
    print(f"DEBUG: Email {current_user.mail} | Rôle: {user_type} | Vrai ID: {role_id} | Colonne: {role_col}")

    # 2. Requête finale d'insertion / mise à jour avec le vrai role_id
    insert_req = {
        "request": f"""
            INSERT INTO LNM_calendar (url_name, {role_col}, url) 
            VALUES (%(url_name)s, %(role_id)s, %(url)s)
            ON DUPLICATE KEY UPDATE url = %(url)s, url_name = %(url_name)s;
        """,
        "params": {
            "url_name": data.url_name,
            "role_id": role_id, 
            "url": data.url,
        },
        "allowedRolesRequester": ["user"],
    }
    
    return db_request(current_user, SQLRequest(**insert_req))