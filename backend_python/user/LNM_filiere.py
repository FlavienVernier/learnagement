import logging
import inspect

from fastapi import APIRouter, Depends
from typing import Annotated

from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User
from repositories.LNM_filiere_requests import requests

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/filieres/",
            tags=["filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def filieres(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/statuts/",
            tags=["filiere"],
            summary="Status",
            description="Return the list of statuts")
def statuts(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request =  requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/groupe_types/",
            tags=["filiere"],
            summary="Status",
            description="Return the list of groupe types")
def groupe_types(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/seance_types/",
            tags=["filiere"],
            summary="Status",
            description="Return the list of seance types")
def seance_types(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))

@router.get("/filieres/dags",
            tags=["anonymous", "filiere"],
            summary="Filiere",
            description="Return the list of filieres")
def dags(
        #current_user = None,  #current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(None, SQLRequest(**request))


@router.get("/filieres/stages",
            tags=["filiere", "internship"],
            summary="Filiere",
            description="Return the list of filieres")
def stages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]

    # Résolution de id_filiere :
    # 1. Si l'user a une responsabilité stage avec une dimension filiere → on l'utilise
    # 2. Sinon on utilise "id_filiere"
    stage_resp = next(
        (r for r in current_user.responsibilities if r["type_objet"] in ("stage", "all") and "filiere" in r["dimensions"]),
        None
    )
    id_filiere = stage_resp["dimensions"]["filiere"] \
                    if stage_resp \
                    else "id_filiere"

    request["params"] = request["params"](id_filiere) \
                            if callable(request["params"]) \
                            else request["params"]
    request["allowedRolesRequester"] = request["allowedRolesRequester"](id_filiere) \
                                        if callable(request["allowedRolesRequester"]) \
                                        else request["allowedRolesRequester"]
    print(request, flush=True)
    return db_request(current_user, SQLRequest(**request))

@router.get("/promos/",
            tags=["filiere"],
            summary="promos",
            description="Return the list of promos")
def promos(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = requests["get_" + inspect.currentframe().f_code.co_name]
    return db_request(current_user, SQLRequest(**request))