import logging
from fastapi import APIRouter, Depends
from typing import Annotated

from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User

logger = logging.getLogger(__name__)

# Clés de métadonnées à exclure du SQLRequest
_META_KEYS = {"route", "tags", "summary", "description", "auth", "auto"}


def register_auto_routes(router: APIRouter, all_requests: dict) -> None:
    """
    Génère automatiquement les endpoints GET pour toutes les entrées
    dont "auto" != False.
    """
    for key, definition in all_requests.items():
        if not definition.get("auto", True):
            continue  # endpoint défini manuellement → on saute

        route    = definition.get("route")
        tags     = definition.get("tags", [])
        summary  = definition.get("summary", key)
        desc     = definition.get("description", "")
        auth     = definition.get("auth", True)

        if route is None:
            logger.warning(f"Entrée '{key}' sans 'route' — ignorée")
            continue

        # Construit le dict SQLRequest sans les métadonnées
        sql_def = {k: v for k, v in definition.items() if k not in _META_KEYS}

        # Capture des variables pour la closure
        def make_handler(k: str, d: dict, requires_auth: bool):
            if requires_auth:
                def handler(current_user: Annotated[User, Depends(get_current_active_user)]):
                    return db_request(current_user, SQLRequest(**d))
            else:
                def handler():
                    return db_request(None, SQLRequest(**d))
            return handler

        handler = make_handler(key, sql_def, auth)

        router.add_api_route(
            path=route,
            endpoint=handler,
            methods=["GET"],
            tags=tags,
            summary=summary,
            description=desc,
        )
        logger.info(f"Route générée : GET {route} ({key})")