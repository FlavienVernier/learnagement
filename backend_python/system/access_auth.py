import logging
import re
import inspect

import sqlglot
import sqlglot.expressions as exp

from fastapi import APIRouter, Depends
from system.tools import get_all_requests, get_all_local_requests
from typing import Annotated
from api.dependencies import get_current_active_user
from models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/access_auth/",
            tags=["check", "table"],
            summary="Teacher without session",
            description="Check teacher without session.")
def get_access_auth(
    current_user: Annotated[User, Depends(get_current_active_user)],
):

    if "administratif" in current_user.roles:
        all_requests = get_all_requests(package_name="user") | get_all_local_requests()

        result = []
        for fichier, module_requests in all_requests.items():
            for endpoint_name, req in module_requests.items():

                # Extraire les champs SELECT de la requête SQL
                sql = req.get("request", "")
                select_match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
                if select_match:
                    # fields = [f.strip().split(".")[-1].split(" AS ")[-1].strip()
                    #           for f in select_match.group(1).split(",")]

                    fields = [f.strip().split(" AS ")[0].strip()
                              for f in select_match.group(1).split(",")]
                else:
                    fields = []

                # Un tuple par rôle autorisé
                allowed = req.get("allowedRolesRequester", [])
                if callable(allowed):
                    # C'est un lambda : on récupère son code source
                    source = inspect.getsource(allowed).strip()
                    #match = re.search(r'lambda\s.*', source)
                    #roles = [match.group(0).strip() if match else source]
                    roles = ["".join(source.split(":")[1:]).strip()]
                else:
                    roles = allowed

                for role in roles:
                    result.append({
                        "fichier": fichier,
                        "data_access": endpoint_name,
                        "data": ", ".join(fields),
                        "allowed_access": role
                    })
        return result
    else:
        return {"response" : "User not allowed"}



def parse_select_fields(sql: str) -> list[dict]:
    """Extrait les champs d'un SELECT sous forme {table, field}."""
    match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []

    raw_fields = match.group(1).split(',')
    fields = []

    for raw in raw_fields:
        raw = raw.strip()
        if '.' in raw:
            table, field = raw.split('.', 1)
            fields.append({"table": table.strip(), "field": field.strip()})
        else:
            fields.append({"table": "_unknown", "field": raw})

    return fields


def build_tree(config: dict) -> dict:
    """Construit l'arbre de droits d'accès depuis la config JSON."""

    root = {
        "id": "root",
        "name": "root",
        "type": "root",
        "children": []
    }

    for file_name, functions in config.items():

        # Niveau 1 — fichier
        file_node = {
            "id": file_name,
            "name": file_name,
            "type": "file",
            "children": []
        }

        for func_name, func_def in functions.items():

            # Niveau 2 — fonction
            func_node = {
                "id": f"{file_name}.{func_name}",
                "name": func_name,
                "type": "function",
                "children": []
            }

            sql            = func_def.get("request", "")
            allowed_roles  = func_def.get("allowedRolesRequester", [])
            fields         = parse_select_fields(sql)

            # Regroupement des champs par table
            tables: dict[str, list[str]] = {}
            for f in fields:
                tables.setdefault(f["table"], []).append(f["field"])

            for table_name, field_list in tables.items():

                # Niveau 3 — table
                table_node = {
                    "id": f"{file_name}.{func_name}.{table_name}",
                    "name": table_name,
                    "type": "table",
                    "children": []
                }

                for field_name in field_list:

                    # Niveau 4 — champ
                    field_node = {
                        "id": f"{file_name}.{func_name}.{table_name}.{field_name}",
                        "name": field_name,
                        "type": "field",
                        "children": []
                    }
                    if callable(allowed_roles):
                        source = inspect.getsource(allowed_roles).strip()
                        name = "".join(source.split(":")[1:]).strip()
                        id = "".join(name.split("[")[0]).strip()
                        # Niveau 5 — lambda rôle
                        role_node = {
                            "id": f"{file_name}.{func_name}.{table_name}.{field_name}.{id}",
                            "name": name,
                            "type": "role",
                            "children": []
                        }
                        field_node["children"].append(role_node)
                    else:
                        for role in allowed_roles:

                            # Niveau 5 — static rôle
                            role_node = {
                                "id": f"{file_name}.{func_name}.{table_name}.{field_name}.{role}",
                                "name": role,
                                "type": "role",
                                "children": []
                            }
                            field_node["children"].append(role_node)

                    table_node["children"].append(field_node)

                func_node["children"].append(table_node)

            file_node["children"].append(func_node)

        root["children"].append(file_node)

    return root


@router.get("/access_auth_tree/",
            tags=["check", "tree"],
            summary="Teacher without session",
            description="Check teacher without session.")
def get_access_auth_tree(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    response = {
        "success": None,
        "meta": {
            "version": "1",
            "type": "tree",
        },
        "data": None,
        "errors": None,
    }

    if "administratif" in current_user.roles:
        all_requests = get_all_requests(package_name="user") | get_all_local_requests()

        response["success"] = True
        response["data"] = build_tree(all_requests)
    else:
        response["success"] = False
        response ["errors"] = [
                {
                  "code": "ACCESS_DENIED",
                  "message": "You are not authorized to access this resource.",
                }
            ]

    return response





# ─────────────────────────────────────────────
# Helpers de classification
# ─────────────────────────────────────────────

def is_direct_wrapper(node) -> bool:
    """
    Retourne True si le nœud est une simple transformation
    qui expose directement le champ sous-jacent :
    CAST, ROUND, FLOOR, CEIL, COALESCE à 1 arg, alias simple...
    """
    DIRECT_WRAPPERS = {
        exp.Cast, exp.Round, exp.Floor, exp.Ceil,
        exp.Upper, exp.Lower, exp.Trim, exp.Coalesce,
        exp.TryCast,
    }
    return type(node) in DIRECT_WRAPPERS


def classify_column_in_expression(col: exp.Column, root_expr) -> str:
    """
    Détermine si une colonne dans une expression est accédée
    de manière 'direct' ou 'indirect'.

    Logique :
    - Si la colonne est l'enfant direct (ou via wrapper direct) → 'direct'
    - Si la colonne est imbriquée dans une fonction d'agrégation,
      une sous-requête, ou une expression arithmétique → 'indirect'
    """
    # Remonte l'arbre depuis la colonne vers la racine
    # pour analyser le contexte immédiat
    parent = col.parent

    # Wrapper direct (CAST, ROUND simple, etc.)
    if parent is not None and is_direct_wrapper(parent):
        # Vérifie que c'est le seul argument significatif
        col_siblings = [c for c in parent.args.values()
                        if isinstance(c, (exp.Expression,))
                        and not isinstance(c, exp.DataType)]
        if len(col_siblings) == 1:
            return "direct"

    # Colonne directe sans transformation
    if isinstance(parent, exp.Alias) or parent is root_expr:
        return "direct"

    # Fonctions d'agrégation → indirect
    AGGREGATE_FUNCTIONS = {
        exp.Sum, exp.Avg, exp.Max, exp.Min, exp.Count,
        exp.StddevPop, exp.VariancePop,
    }
    for ancestor in col.walk():
        pass  # on va utiliser find_ancestor à la place

    # Remontée manuelle vers la racine
    node = col.parent
    while node is not None and node is not root_expr:
        if type(node) in AGGREGATE_FUNCTIONS:
            return "indirect"
        if isinstance(node, exp.Subquery):
            return "indirect"
        if isinstance(node, (exp.Add, exp.Sub, exp.Mul, exp.Div)):
            return "indirect"
        if isinstance(node, exp.Anonymous):  # fonctions inconnues ex: IFNULL
            return "indirect"
        if isinstance(node, exp.If) or isinstance(node, exp.Case):
            return "indirect"
        node = node.parent

    return "direct"


# ─────────────────────────────────────────────
# Extraction des accès depuis un SELECT
# ─────────────────────────────────────────────

def extract_accesses(sql: str, dialect: str = "mysql") -> list[dict]:
    """
    Retourne la liste de tous les accès champ/table avec leur type
    (direct / indirect) et l'alias exposé le cas échéant.

    Format retourné :
    [
      {
        "table": "MAQUETTE_module",
        "column": "hCM",
        "access": "direct",       # ou "indirect"
        "exposed_as": "hCM",      # alias dans le SELECT (None si indirect)
      },
      ...
    ]
    """
    statement = sqlglot.parse_one(sql, dialect=dialect)

    if not isinstance(statement, exp.Select):
        raise ValueError("La requête fournie n'est pas un SELECT.")

    accesses: list[dict] = []
    seen: set[tuple] = set()  # dédoublonnage

    for select_expr in statement.selects:

        # Alias exposé dans le résultat
        if isinstance(select_expr, exp.Alias):
            exposed_as = select_expr.alias
            inner      = select_expr.this
        else:
            exposed_as = None
            inner      = select_expr

        # Toutes les colonnes dans cette expression SELECT
        for col in inner.find_all(exp.Column):
            if not col.table:
                continue  # on ignore les colonnes sans table explicite

            access_type = classify_column_in_expression(col, inner)

            key = (col.table, col.name, access_type, exposed_as)
            if key in seen:
                continue
            seen.add(key)

            accesses.append({
                "table":      col.table,
                "column":     col.name,
                "access":     access_type,
                "exposed_as": exposed_as if access_type == "direct" else None,
            })

    return accesses


# ─────────────────────────────────────────────
# Construction de l'arbre de data lineage
# ─────────────────────────────────────────────

def build_lineage_tree(config: dict) -> dict:

    root = {"id": "root", "name": "root", "type": "root", "children": []}

    for file_name, functions in config.items():

        file_node = {"id": file_name, "name": file_name, "type": "file", "children": []}

        for func_name, func_def in functions.items():

            func_node = {
                #"id":       f"{file_name}.{func_name}",
                "id":       f"function.{func_name}",
                "name":     func_name,
                "type":     "function",
                "children": []
            }

            sql           = func_def.get("request", "")
            allowed_roles = func_def.get("allowedRolesRequester", [])

            try:
                accesses = extract_accesses(sql)
            except Exception as e:
                print(f"⚠️  [{file_name}.{func_name}] : {e}")
                accesses = []

            # Regroupement par table
            tables: dict[str, list[dict]] = {}
            for a in accesses:
                tables.setdefault(a["table"], []).append(a)

            for table_name, field_accesses in tables.items():

                table_node = {
                    #"id":       f"{file_name}.{func_name}.{table_name}",
                    "id":       f"table.{table_name}",
                    "name":     table_name,
                    "type":     "table",
                    "children": []
                }

                for access in field_accesses:
                    col_name    = access["column"]
                    access_type = access["access"]
                    exposed_as  = access["exposed_as"]

                    field_node = {
                        #"id":          f"{file_name}.{func_name}.{table_name}.{col_name}",
                        "id":          f"field.{table_name}.{col_name}",
                        "name":        col_name,
                        "type":        "field",
                        "access":      access_type,   # "direct" | "indirect"
                        "exposed_as":  exposed_as,    # alias retourné, None si indirect
                        "children":    []
                    }

                    for role in allowed_roles:
                        role_node = {
                            #"id":       f"{file_name}.{func_name}.{table_name}.{col_name}.{role}",
                            "id":       f"role.{role}",
                            "name":     role,
                            "type":     "role",
                            "children": []
                        }
                        field_node["children"].append(role_node)

                    table_node["children"].append(field_node)

                func_node["children"].append(table_node)

            file_node["children"].append(func_node)

        root["children"].append(file_node)

    return root


@router.get("/access_auth_tree_sqlglot/",
            tags=["check", "tree"],
            summary="Teacher without session",
            description="Check teacher without session.")
def get_access_auth_tree_sqlglot(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    response = {
        "success": None,
        "meta": {
            "version": "1",
            "type": "tree",
        },
        "data": None,
        "errors": None,
    }

    if "administratif" in current_user.roles:
        all_requests = get_all_requests(package_name="user") | get_all_local_requests()

        response["success"] = True
        response["data"] = build_lineage_tree(all_requests)
    else:
        response["success"] = False
        response ["errors"] = [
                {
                  "code": "ACCESS_DENIED",
                  "message": "You are not authorized to access this resource.",
                }
            ]

    return response