import copy


def requests(key: str):
    return copy.deepcopy(__requests[key])

# Convention : chaque colonne est aliasée en  <TABLE>__<colonne>
#  - la TABLE devient le label du nœud
#  - la clé primaire (id_<nom de table sans préfixe>) identifie le nœud
#  - les autres colonnes deviennent ses propriétés
# "relationships" : (nœud source, TYPE, nœud cible) produits par la requête
__requests = {

    "get_graph_filiere_promo_statut": {
        "tags": ["filiere", "graph"],
        "summary": "Graph filiere/promo/statut",
        "description": "Nodes and relationships between filieres, promos and statuts",
        "auth": False,
        "auto": False,
        "request": """
            SELECT
                LNM_filiere.id_filiere   AS LNM_filiere__id_filiere,
                LNM_filiere.nom_filiere  AS LNM_filiere__nom_filiere,
                LNM_filiere.nom_long     AS LNM_filiere__nom_long,
                LNM_promo.id_promo       AS LNM_promo__id_promo,
                LNM_promo.annee          AS LNM_promo__annee,
                LNM_statut.id_statut     AS LNM_statut__id_statut,
                LNM_statut.nom_statut    AS LNM_statut__nom_statut
            FROM LNM_filiere
                JOIN LNM_promo ON LNM_promo.id_filiere = LNM_filiere.id_filiere
                JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
        """,
        "relationships": [
            ("LNM_filiere", "HAS_PROMO",  "LNM_promo"),
            ("LNM_promo",   "HAS_STATUT", "LNM_statut"),
        ],
        "allowedRolesRequester": "anonymous",
    },

    "get_graph_promo_learning_unit_module": {
        "tags": ["filiere", "graph"],
        "summary": "Graph promo/learning unit/module",
        "description": "Nodes and relationships between promos, learning units and modules",
        "auth": False,
        "auto": False,
        "request": """
            SELECT
                LNM_promo.id_promo                          AS LNM_promo__id_promo,
                MAQUETTE_learning_unit.id_learning_unit     AS MAQUETTE_learning_unit__id_learning_unit,
                MAQUETTE_learning_unit.learning_unit_code   AS MAQUETTE_learning_unit__learning_unit_code,
                MAQUETTE_learning_unit.learning_unit_name   AS MAQUETTE_learning_unit__learning_unit_name,
                MAQUETTE_module.id_module                   AS MAQUETTE_module__id_module,
                MAQUETTE_module.code_module                 AS MAQUETTE_module__code_module,
                MAQUETTE_module.nom                         AS MAQUETTE_module__nom
            FROM LNM_promo
                JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
                JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_learning_unit = MAQUETTE_learning_unit.id_learning_unit
                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_as_learning_unit.id_module
        """,
        "relationships": [
            ("LNM_promo",              "HAS_LEARNING_UNIT", "MAQUETTE_learning_unit"),
            ("MAQUETTE_learning_unit", "HAS_MODULE",        "MAQUETTE_module"),
        ],
        "allowedRolesRequester": "anonymous",
    },

    "get_graph_module_ac_niveau_competence": {
        "tags": ["filiere", "graph", "apc"],
        "summary": "Graph module/AC/niveau/competence",
        "description": "Nodes and relationships between modules, apprentissages critiques, niveaux and competences",
        "auth": False,
        "auto": False,
        "request": """
            SELECT
                MAQUETTE_module.id_module                                   AS MAQUETTE_module__id_module,
                APC_apprentissage_critique.id_apprentissage_critique        AS APC_apprentissage_critique__id_apprentissage_critique,
                APC_apprentissage_critique.libelle_apprentissage            AS APC_apprentissage_critique__libelle_apprentissage,
                APC_niveau.id_niveau                                        AS APC_niveau__id_niveau,
                APC_niveau.niveau                                           AS APC_niveau__niveau,
                APC_niveau.libelle_niveau                                   AS APC_niveau__libelle_niveau,
                APC_competence.id_competence                                AS APC_competence__id_competence,
                APC_competence.code_competence                              AS APC_competence__code_competence,
                APC_competence.libelle_competence                           AS APC_competence__libelle_competence
            FROM MAQUETTE_module
                JOIN APC_apprentissage_critique_as_module ON APC_apprentissage_critique_as_module.id_module = MAQUETTE_module.id_module
                JOIN APC_apprentissage_critique ON APC_apprentissage_critique.id_apprentissage_critique = APC_apprentissage_critique_as_module.id_apprentissage_critique
                JOIN APC_niveau ON APC_niveau.id_niveau = APC_apprentissage_critique.id_niveau
                JOIN APC_competence ON APC_competence.id_competence = APC_niveau.id_competence
        """,
        "relationships": [
            ("MAQUETTE_module",            "HAS_AC",        "APC_apprentissage_critique"),
            ("APC_apprentissage_critique", "IN_NIVEAU",     "APC_niveau"),
            ("APC_niveau",                 "IN_COMPETENCE", "APC_competence"),
        ],
        "allowedRolesRequester": "anonymous",
    },

    "get_graph_competence_composante": {
        "tags": ["filiere", "graph", "apc"],
        "summary": "Graph competence/composante essentielle",
        "description": "Nodes and relationships between competences and composantes essentielles",
        "auth": False,
        "auto": False,
        "request": """
            SELECT
                APC_competence.id_competence                                    AS APC_competence__id_competence,
                APC_composante_essentielle.id_composante_essentielle            AS APC_composante_essentielle__id_composante_essentielle,
                APC_composante_essentielle.libelle_composante_essentielle       AS APC_composante_essentielle__libelle_composante_essentielle
            FROM APC_competence
                JOIN APC_composante_essentielle ON APC_composante_essentielle.id_competence = APC_competence.id_competence
        """,
        "relationships": [
            ("APC_competence", "HAS_COMPOSANTE", "APC_composante_essentielle"),
        ],
        "allowedRolesRequester": "anonymous",
    },

    "get_graph_module_sequencage_sequence": {
        "tags": ["filiere", "graph", "module"],
        "summary": "Graph module/sequencage/seance type/sequence",
        "description": "Nodes and relationships between modules, sequencages, seance types and sequences",
        "auth": False,
        "auto": False,
        "request": """
            SELECT
                MAQUETTE_module.id_module                           AS MAQUETTE_module__id_module,
                MAQUETTE_module_sequencage.id_module_sequencage     AS MAQUETTE_module_sequencage__id_module_sequencage,
                LNM_seance_type.id_seance_type                      AS LNM_seance_type__id_seance_type,
                LNM_seance_type.type                                AS LNM_seance_type__type,
                MAQUETTE_module_sequence.id_module_sequence         AS MAQUETTE_module_sequence__id_module_sequence,
                MAQUETTE_module_sequence.numero_ordre               AS MAQUETTE_module_sequence__numero_ordre,
                MAQUETTE_module_sequence.commentaire                AS MAQUETTE_module_sequence__commentaire
            FROM MAQUETTE_module
                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module = MAQUETTE_module.id_module
                JOIN LNM_seance_type ON LNM_seance_type.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage
        """,
        "relationships": [
            ("MAQUETTE_module",            "HAS_SEQUENCAGE",  "MAQUETTE_module_sequencage"),
            ("MAQUETTE_module_sequencage", "HAS_SEANCE_TYPE", "LNM_seance_type"),
            ("MAQUETTE_module_sequencage", "HAS_SEQUENCE",    "MAQUETTE_module_sequence"),
        ],
        "allowedRolesRequester": "anonymous",
    },
}