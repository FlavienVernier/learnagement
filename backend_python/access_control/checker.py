from fastapi import HTTPException, status
from access_control.rules import evaluate_rule
from access_control.types import AccessRule


def check_access(query_key: str, params: dict, user, requests: dict) -> None:
    """
    Vérifie que user a le droit d'exécuter la requête query_key.
    Lève HTTPException si refusé.
    """
    query_def = requests.get(query_key)
    if query_def is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requête '{query_key}' introuvable"
        )

    rule: AccessRule = query_def.get("allowedRolesRequester")
    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Règle d'accès manquante pour '{query_key}'"
        )

    granted = evaluate_rule(rule, user, params)
    if not granted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )