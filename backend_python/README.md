requests = {

    # Accès anonyme
    "get_public_info": {
        "requete": "SELECT * FROM info_publiques",
        "params": [],
        "allowedRolesRequester": "anonymous",
    },

    # Utilisateur connecté uniquement
    "get_mon_profil": {
        "requete": "SELECT * FROM users WHERE id = :id",
        "params": ["id"],
        "allowedRolesRequester": "connected_user",
    },

    # Liste de rôles
    "get_all_etudiants": {
        "requete": "SELECT * FROM etudiants",
        "params": [],
        "allowedRolesRequester": ["administratif", "responsable_etudes"],
    },

    # Dictionnaire — satisfaire AU MOINS UNE condition
    "get_stages_filiere": {
        "requete": "SELECT * FROM stages WHERE filiere = :filiere",
        "params": ["filiere"],
        "allowedRolesRequester": {
            "roles": ["administratif"],
            "one": {"type_objet": "stage", "filiere": "IDU"},
        },
    },

    # Dictionnaire — toutes les responsabilités requises
    "get_rapport_complet": {
        "requete": "SELECT * FROM rapports WHERE filiere=:filiere AND semestre=:semestre",
        "params": ["filiere", "semestre"],
        "allowedRolesRequester": {
            "roles": ["administratif"],
            "all": [
                {"type_objet": "filiere", "filiere": "IDU"},
                {"type_objet": "semestre", "semestre": "S8"},
            ],
        },
    },

    # Hiérarchie
    "get_module_details": {
        "requete": "SELECT * FROM modules WHERE id = :id_module",
        "params": ["id_module"],
        "allowedRolesRequester": {
            "hierarchy": [
                {"type_objet": "filiere",  "filiere": "IDU"},
                {"type_objet": "semestre", "filiere": "IDU", "semestre": "S8"},
                {"type_objet": "module",   "filiere": "IDU", "semestre": "S8", "niveau": "FI4"},
            ],
        },
    },

    # Lambda — règle calculée dynamiquement depuis les params
    "get_stages_etudiant": {
        "requete": "SELECT * FROM stages WHERE id_etudiant = :id_etudiant",
        "params": ["id_etudiant"],
        "allowedRolesRequester": lambda params, user: (
            "connected_user"
            if user and user.id == params.get("id_etudiant")
            else ["administratif", "responsable_etudes"]
        ),
    },
}