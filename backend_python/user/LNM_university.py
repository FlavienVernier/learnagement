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
