import logging
from fastapi import APIRouter

from api.dependencies import db_request
from models.request import SQLRequest

logger = logging.getLogger(__name__)
router = APIRouter()

SEP = "__"

# label (= nom de table) -> (clé primaire, [propriétés exposées])
NODE_SPECS = {
    "LNM_filiere":                ("id_filiere", ["nom_filiere", "nom_long"]),
    "LNM_promo":                  ("id_promo", ["annee"]),
    "LNM_statut":                 ("id_statut", ["nom_statut"]),
    "MAQUETTE_learning_unit":     ("id_learning_unit", ["learning_unit_code", "learning_unit_name"]),
    "MAQUETTE_module":            ("id_module", ["code_module", "nom"]),
    "APC_apprentissage_critique": ("id_apprentissage_critique", ["libelle_apprentissage"]),
    "APC_niveau":                 ("id_niveau", ["niveau", "libelle_niveau"]),
    "APC_competence":             ("id_competence", ["code_competence", "libelle_competence"]),
    "APC_composante_essentielle": ("id_composante_essentielle", ["libelle_composante_essentielle"]),
}

# (table source, TYPE, table cible) : suit les JOIN de la requête
RELATIONSHIPS = [
    ("LNM_filiere",                "HAS_PROMO",           "LNM_promo"),
    ("LNM_promo",                  "HAS_STATUT",          "LNM_statut"),
    ("LNM_promo",                  "HAS_LEARNING_UNIT",   "MAQUETTE_learning_unit"),
    ("MAQUETTE_learning_unit",     "HAS_MODULE",          "MAQUETTE_module"),
    ("MAQUETTE_module",            "HAS_AC",              "APC_apprentissage_critique"),
    ("APC_apprentissage_critique", "IN_NIVEAU",           "APC_niveau"),
    ("APC_niveau",                 "IN_COMPETENCE",       "APC_competence"),
    ("APC_competence",             "HAS_COMPOSANTE",      "APC_composante_essentielle"),
]


def _build_select() -> str:
    cols = []
    for table, (pk, props) in NODE_SPECS.items():
        for col in [pk] + props:
            cols.append(f"{table}.{col} AS {table}{SEP}{col}")
    return ",\n".join(cols)


GRAPH_QUERY = f"""
    SELECT
        {_build_select()}
    FROM LNM_filiere
        JOIN LNM_promo ON LNM_promo.id_filiere = LNM_filiere.id_filiere
        JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
        JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
        JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_learning_unit = MAQUETTE_learning_unit.id_learning_unit
        JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_as_learning_unit.id_module
        JOIN APC_apprentissage_critique_as_module ON APC_apprentissage_critique_as_module.id_module = MAQUETTE_module.id_module
        JOIN APC_apprentissage_critique ON APC_apprentissage_critique.id_apprentissage_critique = APC_apprentissage_critique_as_module.id_apprentissage_critique
        JOIN APC_niveau ON APC_niveau.id_niveau = APC_apprentissage_critique.id_niveau
        JOIN APC_competence ON APC_competence.id_competence = APC_niveau.id_competence
        JOIN APC_composante_essentielle ON APC_composante_essentielle.id_competence = APC_competence.id_competence
"""


def rows_to_graph(rows: list[dict]) -> dict:
    nodes: dict[str, dict] = {}
    rels: dict[str, dict] = {}

    for row in rows:
        # 1. nœuds de la ligne
        row_node_ids: dict[str, str] = {}
        for label, (pk, props) in NODE_SPECS.items():
            pk_value = row.get(f"{label}{SEP}{pk}")
            if pk_value is None:
                continue
            node_id = f"{label}:{pk_value}"
            row_node_ids[label] = node_id
            if node_id not in nodes:
                properties = {pk: pk_value}
                for p in props:
                    properties[p] = row.get(f"{label}{SEP}{p}")
                nodes[node_id] = {
                    "id": node_id,
                    "labels": [label],
                    "properties": properties,
                }

        # 2. relations de la ligne
        for src, rel_type, dst in RELATIONSHIPS:
            if src in row_node_ids and dst in row_node_ids:
                rel_id = f"{row_node_ids[src]}-{rel_type}->{row_node_ids[dst]}"
                if rel_id not in rels:
                    rels[rel_id] = {
                        "id": rel_id,
                        "type": rel_type,
                        "startNode": row_node_ids[src],
                        "endNode": row_node_ids[dst],
                        "properties": {},
                    }

    return {"nodes": list(nodes.values()), "relationships": list(rels.values())}


@router.get("/filieres/dags/graph",
            tags=["anonymous", "filiere", "graph"],
            summary="DAGs graph",
            description="Return the DAGs as a Neo4j-compatible graph (nodes + relationships)")
def get_dags_graph():
    request = {
        "request": GRAPH_QUERY,
        "allowedRolesRequester": "anonymous",
    }
    rows = db_request(None, SQLRequest(**request))
    return rows_to_graph(rows)