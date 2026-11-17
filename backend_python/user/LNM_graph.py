import logging
from fastapi import APIRouter

from api.dependencies import db_request
from models.request import SQLRequest
from repositories.LNM_graph_requests import requests, __requests

logger = logging.getLogger(__name__)
router = APIRouter()

SEP = "__"


def _primary_key(label: str) -> str:
    """Convention du framework : table XXXX_name -> clé primaire id_name."""
    return "id_" + label.split("_", 1)[1]


def _group_by_label(row: dict) -> dict[str, dict]:
    """{'LNM_filiere__nom_filiere': 'IDU'} -> {'LNM_filiere': {'nom_filiere': 'IDU'}}"""
    grouped: dict[str, dict] = {}
    for key, value in row.items():
        label, column = key.split(SEP, 1)
        grouped.setdefault(label, {})[column] = value
    return grouped


def add_rows_to_graph(rows: list[dict], relationships: list, nodes: dict, rels: dict) -> None:
    """Fusionne les lignes d'une requête dans les dicts nodes / rels (dédoublonnés par id)."""
    for row in rows:
        node_ids: dict[str, str] = {}

        for label, props in _group_by_label(row).items():
            pk_value = props.get(_primary_key(label))
            if pk_value is None:
                continue
            node_id = f"{label}:{pk_value}"
            node_ids[label] = node_id
            node = nodes.setdefault(
                node_id, {"id": node_id, "labels": [label], "properties": {}}
            )
            node["properties"].update(props)  # fusion si le nœud apparaît dans plusieurs requêtes

        for src, rel_type, dst in relationships:
            if src in node_ids and dst in node_ids:
                rel_id = f"{node_ids[src]}-{rel_type}->{node_ids[dst]}"
                rels.setdefault(rel_id, {
                    "id": rel_id,
                    "type": rel_type,
                    "startNode": node_ids[src],
                    "endNode": node_ids[dst],
                    "properties": {},
                })


@router.get("/filieres/dags/graph",
            tags=["anonymous", "filiere", "graph"],
            summary="DAGs graph",
            description="Return the DAGs as a Neo4j-compatible graph (nodes + relationships)")
def get_dags_graph():
    nodes: dict[str, dict] = {}
    rels: dict[str, dict] = {}

    for key in __requests:
        definition = requests(key)
        rows = db_request(None, SQLRequest(
            request=definition["request"],
            params=definition.get("params"),
            allowedRolesRequester=definition["allowedRolesRequester"],
        ))
        add_rows_to_graph(rows, definition["relationships"], nodes, rels)

    return {"nodes": list(nodes.values()), "relationships": list(rels.values())}