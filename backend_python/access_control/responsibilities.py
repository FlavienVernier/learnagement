from access_control.types import Responsibility
from models.user import User

def _responsibility_covers(stored: dict, required: Responsibility) -> bool:
    """
    Vérifie qu'une responsabilité stockée en BD couvre la responsabilité requise.

    Règle : chaque dimension définie en BD doit matcher le scope demandé.
            Une dimension absente en BD = wildcard (couvre toutes les valeurs).
    """
    if stored["type_objet"] not in (required.type_objet, "all"):
        return False

    return all(
        required.dimensions.get(dim) == val or required.dimensions.get(dim) == "any"
        for dim, val in stored["dimensions"].items()
    )

def has_any_of_responsibilities(user: User, required_list: list[Responsibility]) -> bool:
    """
    L'utilisateur doit couvrir AU MOINS UNE des responsabilités de la liste.
    """
    return any(
        any(_responsibility_covers(stored, required) for stored in user.responsibilities)
        for required in required_list
    )

def has_all_responsibilities(user: User, required_list: list[Responsibility]) -> bool:
    """
    L'utilisateur doit avoir UNE responsabilité couvrant CHACUNE des entrées.
    """
    return all(
        has_any_of_responsibilities(user, [required])
        for required in required_list
    )


def has_hierarchy_responsibilities(user: User, ordered_list: list[Responsibility]) -> bool:
    """
    L'utilisateur doit satisfaire un préfixe non vide de la hiérarchie :
    [R1] ou [R1, R2] ou [R1, R2, R3] ...

    Autrement dit : il doit avoir R1, et optionnellement R2 si R1 satisfait, etc.
    On retourne True dès qu'au moins R1 est satisfait.
    """
    if not ordered_list:
        return False

    for i, required in enumerate(ordered_list):
        if not has_any_of_responsibilities(user, [required]):
            return i > 0

    return True  # toute la hiérarchie est satisfaite


def parse_responsibility(raw: dict) -> Responsibility:
    """
    Convertit une entrée du dictionnaire requests en objet Responsabilite.
    ex: {"type_objet": "stage", "filiere": "IDU", "niveau": "FI4"}
      → Responsabilite(type_objet="stage", dimensions={"filiere":"IDU","niveau":"FI4"})
    """
    type_objet = raw.get("type_objet", "all")
    dimensions = {k: v for k, v in raw.items() if k != "type_objet"}
    return Responsibility(type_objet=type_objet, dimensions=dimensions)