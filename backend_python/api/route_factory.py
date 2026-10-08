import re
import logging
from fastapi import APIRouter, Depends
from typing import Annotated
import inspect

from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User

logger = logging.getLogger(__name__)

# Clés de métadonnées à exclure du SQLRequest
_META_KEYS = {"route", "tags", "summary", "description", "auth", "auto"}

# Extrait les noms de paramètres de route, ex: "{nom_filiere:str}" → "nom_filiere"
_PATH_PARAM_RE = re.compile(r"\{(\w+)(?::\w+)?\}")

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

        # Noms des paramètres attendus par la route (ex: ["nom_filiere"])
        path_param_names = _PATH_PARAM_RE.findall(route)

        # Capture des variables pour la closure
        def make_handler(k: str, d: dict, requires_auth: bool, param_names: list[str]):
            params_def = d.get("params")

            def resolve_params(path_values: dict):
                if params_def is None:
                    return None
                if callable(params_def):
                    return params_def(**path_values)
                return params_def  # déjà un dict statique

            if requires_auth:
                if param_names:
                    def handler(current_user: Annotated[User, Depends(get_current_active_user)], **path_values):
                        resolved = {**d, "params": resolve_params(path_values)}
                        return db_request(current_user, SQLRequest(**resolved))
                else:
                    def handler(current_user: Annotated[User, Depends(get_current_active_user)]):
                        return db_request(current_user, SQLRequest(**d))
            else:
                if param_names:
                    def handler(**path_values):
                        resolved = {**d, "params": resolve_params(path_values)}
                        return db_request(None, SQLRequest(**resolved))
                else:
                    def handler():
                        return db_request(None, SQLRequest(**d))


            # Construit dynamiquement la signature pour que FastAPI détecte
            # les paramètres de route (sinon ils restent invisibles, comme actuellement)
            if param_names:
                extra_params = [
                    inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
                    for name in param_names
                ]
                existing_params = list(inspect.signature(handler).parameters.values())
                # Retire le **path_values générique, le remplace par les vrais params typés
                base_params = [p for p in existing_params if p.kind != inspect.Parameter.VAR_KEYWORD]
                handler.__signature__ = inspect.Signature(base_params + extra_params)

            return handler

        handler = make_handler(key, sql_def, auth, path_param_names)

        router.add_api_route(
            path=route,
            endpoint=handler,
            methods=["GET"],
            tags=tags,
            summary=summary,
            description=desc,
        )
        logger.info(f"Route générée : GET {route} ({key}) — params de route: {path_param_names}")