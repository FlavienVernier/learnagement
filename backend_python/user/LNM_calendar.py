from typing import Annotated, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependencies import SQLRequest, db_request, get_current_active_user, User

router = APIRouter()

# Modèle pour l'insertion/mise à jour
class CalendarUpdate(BaseModel):
    url: str
    url_name: str = "Planning des cours"

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
    request = {
        "request": """
            SELECT url_name, url 
            FROM LNM_calendar 
            WHERE id_enseignant = %(user_id)s 
               OR id_etudiant = %(user_id)s 
               OR id_administratif = %(user_id)s
            ORDER BY url_name ASC;
        """,
        "params": {
            "user_id": current_user.id,
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
    user_type = getattr(current_user, 'ExplicitSecondaryK', 'etudiant')
    
    role_col = "id_etudiant"
    if user_type == "enseignant":
        role_col = "id_enseignant"
    elif user_type == "administratif":
        role_col = "id_administratif"
        
    print(f"Updating calendar for user {current_user.id} with role {user_type} in column {role_col}")

    request = {
        "request": f"""
            INSERT INTO LNM_calendar (url_name, {role_col}, url) 
            VALUES (%(url_name)s, %(user_id)s, %(url)s)
            ON DUPLICATE KEY UPDATE url = %(url)s;
        """,
        "params": {
            "url_name": data.url_name,
            "user_id": current_user.id,
            "url": data.url,
        },
        "allowedRolesRequester": ["user"],
    }
    return db_request(current_user, SQLRequest(**request))