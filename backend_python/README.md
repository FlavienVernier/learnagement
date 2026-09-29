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




# Architecture du projet

```
project/
│
├── app/                          # package principal
│   ├── __init__.py
│   ├── main.py                   # création de l'app FastAPI, inclusion des routers
│   │
│   ├── core/                     # configuration transversale
│   │   ├── __init__.py
│   │   ├── config.py             # settings (pydantic BaseSettings, .env)
│   │   ├── security.py           # JWT, hashing, tokens
│   │   └── logging.py            # configuration du logger
│   │
│   ├── db/                       # couche base de données
│   │   ├── __init__.py
│   │   ├── connection.py         # pool de connexions
│   │   └── migrations/           # alembic ou scripts SQL
│   │
│   ├── models/                   # modèles de données
│   │   ├── __init__.py
│   │   ├── user.py               # UserInDB, User, UserCreate...
│   │   └── ...
│   │
│   ├── schemas/                  # modèles Pydantic entrée/sortie API
│   │   ├── __init__.py
│   │   ├── user.py               # UserResponse, UserCreate...
│   │   └── ...
│   │
│   ├── repositories/             # accès aux données (requêtes SQL/ORM)
│   │   ├── __init__.py
│   │   ├── user.py               # get_user_by_id, create_user...
│   │   └── ...
│   │
│   ├── services/                 # logique métier
│   │   ├── __init__.py
│   │   ├── auth.py               # login, logout, token
│   │   └── ...
│   │
│   ├── api/                      # endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Depends() partagés (get_current_user...)
│   │   └── v1/                   # versioning
│   │       ├── __init__.py
│   │       ├── router.py         # agrège tous les routers v1
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── ...
│   │
│   └── access_control/           # module de contrôle d'accès
│       ├── __init__.py
│       ├── types.py
│       ├── responsabilites.py
│       ├── rules.py
│       └── checker.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # fixtures partagées (user mock, db test...)
│   ├── test_access_control/
│   │   └── test_rules.py
│   ├── test_api/
│   │   └── test_auth.py
│   └── test_services/
│       └── test_auth.py
│
├── .env
├── .env.example
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── docker-compose.yml
```