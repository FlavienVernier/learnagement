def is_current_user_module_participant(user, params) -> bool:
    """L'étudiant connecté suit-il ce module ?"""
    if user.main_role != "etudiant":
        return False

    # import local pour éviter l'import circulaire
    # (dependencies -> checker -> rules -> predicates -> dependencies)
    from api.dependencies import db_request
    from models.request import SQLRequest

    rows = db_request(user, SQLRequest(
        request="""
            SELECT 1
            FROM MAQUETTE_module_as_learning_unit malu
            JOIN MAQUETTE_learning_unit lu ON lu.id_learning_unit = malu.id_learning_unit
            JOIN LNM_etudiant e ON e.id_promo = lu.id_promo
            WHERE malu.id_module = %(id_module)s
              AND e.id_etudiant  = %(id_etudiant)s
            LIMIT 1
        """,
        params={"id_module": params["id_module"], "id_etudiant": user.id},
        allowedRolesRequester="connected_user",   # règle string : pas de récursion
    ))
    return bool(rows)

def is_current_user_module_responsible(user, params) -> bool:
    """L'enseignant connecté est-il responsable de ce module ?"""
    if user is None or user.main_role != "enseignant":
        return False

    id_module = (params or {}).get("id_module")
    if id_module is None:
        return False

    # imports locaux : dependencies -> checker -> rules -> predicates -> dependencies
    from api.dependencies import db_request
    from models.request import SQLRequest

    rows = db_request(user, SQLRequest(
        request="""
            SELECT 1
            FROM MAQUETTE_module
            WHERE id_module = %(id_module)s
              AND id_responsable = %(id_user)s
            LIMIT 1
        """,
        params={"id_module": id_module, "id_user": user.id},
        allowedRolesRequester="connected_user",   # règle string : pas de récursion
    ))
    return bool(rows)