from access_control.types import AccessRule
from access_control.responsabilites import (
    has_any_of_responsabilites,
    has_all_responsabilites,
    has_hierarchy_responsabilites,
    parse_responsabilite,
)


def evaluate_rule(rule: AccessRule, user, params: dict | None) -> bool:
    """
    Point d'entrée principal. Évalue si user satisfait la règle d'accès.
    Résout d'abord les lambdas, puis dispatche selon le type de règle.
    """
    # Résolution du lambda → valeur concrète
    if callable(rule):
        rule = rule(params, user)

    if isinstance(rule, str):
        return _evaluate_string(rule, user)

    if isinstance(rule, list):
        return _evaluate_role_list(rule, user)

    if isinstance(rule, dict):
        return _evaluate_dict(rule, user, params)

    raise ValueError(f"Type de règle non supporté : {type(rule)}")


# --- Évaluateurs par type ---

def _evaluate_string(rule: str, user) -> bool:
    """
    "anonymous"      → toujours autorisé
    "connected_user" → autorisé si authentifié
    """
    if rule == "anonymous":
        return True

    if rule == "connected_user":
        return user is not None

    raise ValueError(f"Valeur de règle string inconnue : '{rule}'")


def _evaluate_role_list(roles: list[str], user) -> bool:
    """
    L'utilisateur doit avoir AU MOINS UN des rôles listés.
    """
    if not roles:
        raise ValueError("La liste de rôles ne peut pas être vide")

    if user is None:
        return False

    return user.type in roles


def _evaluate_dict(rule: dict, user, params: dict) -> bool:
    """
    Dictionnaire de conditions — l'utilisateur doit satisfaire AU MOINS UNE entrée.

    Clés supportées :
      "roles"     → list[str]  : au moins un rôle
      "any"       → list[dict] : au moins une des responsabilités
      "all"       → list[dict] : toutes les responsabilités
      "hierarchy" → list[dict] : préfixe valide de la hiérarchie
    """
    if user is None:
        return False

    evaluators = {
        "roles":     lambda v: _evaluate_role_list(v, user),
        "any":       lambda v: has_any_of_responsabilites(
                                   user,
                                   [parse_responsabilite(r) for r in v]
                               ),
        "all":       lambda v: has_all_responsabilites(
                                   user,
                                   [parse_responsabilite(r) for r in v]
                               ),
        "hierarchy": lambda v: has_hierarchy_responsabilites(
                                   user,
                                   [parse_responsabilite(r) for r in v]
                               ),
    }

    for key, value in rule.items():
        evaluator = evaluators.get(key)
        if evaluator is None:
            raise ValueError(f"Clé de règle inconnue dans le dictionnaire : '{key}'")
        if evaluator(value):
            return True  # AU MOINS UNE condition satisfaite

    return False