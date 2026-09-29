import copy


def requests(key: str):
    return copy.deepcopy(__requests[key])

__requests = {
    "get_filieres" : {
        "route":   "/filieres/",
        "tags":    ["filiere"],
        "summary": "Filiere",
        "description": "Return the list of filieres",
        "auth":    True,
        "request" : """
                        SELECT LNM_filiere.*, ExplicitSecondaryKs_LNM_filiere.ExplicitSecondaryK
                        FROM LNM_filiere
                        JOIN ExplicitSecondaryKs_LNM_filiere ON ExplicitSecondaryKs_LNM_filiere.id_filiere = LNM_filiere.id_filiere
                    """,
        "allowedRolesRequester" : ["connected_user"],
    },
    "get_statuts" : {
        "route":   "/statuts/",
        "tags":    ["filiere"],
        "summary": "Status",
        "description": "Return the list of statuts",
        "auth":    True,
        "request" : """
                        SELECT LNM_statut.*, ExplicitSecondaryKs_LNM_statut.ExplicitSecondaryK
                        FROM LNM_statut
                        JOIN ExplicitSecondaryKs_LNM_statut ON ExplicitSecondaryKs_LNM_statut.id_statut = LNM_statut.id_statut
                    """,
        "allowedRolesRequester" : ["connected_user"],
    },
    "get_groupe_types" : {
        "route":   "/groupe_types/",
        "tags":    ["filiere"],
        "summary": "Groupe types",
        "description": "Return the list of groupe types",
        "auth":    True,
        "request" : """
                        SELECT LNM_groupe_type.*, ExplicitSecondaryKs_LNM_groupe_type.ExplicitSecondaryK
                        FROM LNM_groupe_type
                        JOIN ExplicitSecondaryKs_LNM_groupe_type ON ExplicitSecondaryKs_LNM_groupe_type.id_groupe_type = LNM_groupe_type.id_groupe_type;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    },
    "get_seance_types" : {
        "route":   "/seance_types/",
        "tags":    ["filiere"],
        "summary": "Seance types",
        "description": "Return the list of seance types",
        "auth":    True,
        "request" : """
                        SELECT LNM_seance_type.*, ExplicitSecondaryKs_LNM_seance_type.ExplicitSecondaryK
                        FROM LNM_seance_type
                        JOIN ExplicitSecondaryKs_LNM_seance_type ON ExplicitSecondaryKs_LNM_seance_type.id_seance_type = LNM_seance_type.id_seance_type;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    },
    "get_dags" : {
        "route":   "/filieres/dags",
        "tags":    ["anonymous", "filiere"],
        "summary": "DAGs",
        "description": "Return the DAGs",
        "auth":    False,   # ← endpoint anonyme
        "request" : """
                        SELECT 
                            LNM_filiere.nom_filiere, 
                            LNM_filiere.nom_long, 
                            LNM_promo.annee, 
                            LNM_statut.nom_statut, 
                            MAQUETTE_learning_unit.learning_unit_code, 
                            MAQUETTE_learning_unit.learning_unit_name, 
                            MAQUETTE_module.code_module, 
                            MAQUETTE_module.nom, 
                            APC_apprentissage_critique.libelle_apprentissage, 
                            APC_niveau.niveau, APC_niveau.libelle_niveau, 
                            APC_competence.code_competence, 
                            APC_competence.libelle_competence
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
                    """,
        "allowedRolesRequester" : ["anonymous"],
    },
    "get_promos" : {
        "route":   "/promos/",
        "tags":    ["filiere"],
        "summary": "Promos",
        "description": "Return the list of promos",
        "auth":    True,
        "request" : """
                        SELECT LNM_promo.`id_promo`, ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS promo
                        FROM `LNM_promo`
                        JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    },
    "get_stages" : {
        "route":   "/filieres/stages",
        "tags":    ["filiere", "internship"],
        "summary": "Stages",
        "description": "Return the list of stages",
        "auth":    True,
        "auto":    False,   # ← exclu de la génération automatique
        "request" : """
            SELECT 
                LNM_stage.id_stage,
                LNM_stage.`entreprise`, 
                LNM_stage.`intitulé`, 
                LNM_stage.`description`, 
                LNM_stage.`ville`, 
                DATE_FORMAT(LNM_stage.`date_debut`, '%Y-%m-%d') AS date_debut, 
                DATE_FORMAT(LNM_stage.`date_fin`, '%Y-%m-%d') AS date_fin, 
                LNM_stage.`nature`,
                ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK AS student_fullname,
                LNM_etudiant.mail,
                LNM_etudiant.id_etudiant,
                ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS filiere,
                ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK AS teacher_fullname,
                LNM_enseignant.id_enseignant,
                LNM_enseignant.mail AS teacher_mail,
                CASE
                    WHEN LNM_stage.id_stage IS NULL THEN 'no-internship'
                    WHEN LNM_enseignant.id_enseignant IS NULL THEN 'pending'
                    ELSE 'completed'
                END AS status
            FROM LNM_etudiant
            JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
            JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
            JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
            JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            LEFT JOIN LNM_stage ON LNM_stage.id_etudiant = LNM_etudiant.id_etudiant
            LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
            LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
            WHERE LNM_filiere.nom_filiere LIKE %(nom_filiere)s AND LNM_promo.annee LIKE %(annee)s;
                    """,
        "params": lambda nom_filiere, annee: {"nom_filiere": nom_filiere, "annee": annee},
        "allowedRolesRequester": {
            "roles": ["responsable_etudes"],
            "any": [{"type_objet": "stage", "filiere": "any", "annee": "any"}],
        }
    },
}
