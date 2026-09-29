from models.request import SQLRequest
from models.user import User
from fastapi import HTTPException, status
from access_control.rules import evaluate_rule


def check_access(
                 request: SQLRequest,
                 user: User | None = None,
            ) -> None:
    """
    Vérifie que user a le droit d'exécuter la requête query_key.
    Lève HTTPException si refusé.
    """

    granted = evaluate_rule(request.allowedRolesRequester, user, request.params)
    if not granted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )