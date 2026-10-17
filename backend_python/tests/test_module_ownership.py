import re
import sqlite3

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from access_control.checker import check_access
from api.dependencies import get_current_active_user
from models.user import User
from user import MAQUETTE_module

# ─────────────────────────────────────────────
# Jeu de données : 2 modules, 2 responsables
#   module 1 (resp. enseignant 1)  →  sequencage 10, sequence 100, session 1000
#   module 2 (resp. enseignant 2)  →  sequencage 20, sequence 200, session 2000
# ─────────────────────────────────────────────

SCHEMA = """
CREATE TABLE MAQUETTE_module (
    id_module INTEGER PRIMARY KEY, id_responsable INTEGER);
CREATE TABLE MAQUETTE_module_sequencage (
    id_module_sequencage INTEGER PRIMARY KEY, id_module INTEGER,
    id_intervenant_principal INTEGER);
CREATE TABLE MAQUETTE_module_sequence (
    id_module_sequence INTEGER PRIMARY KEY, id_module_sequencage INTEGER,
    id_intervenant_principal INTEGER);
CREATE TABLE CLASS_session (
    id_session INTEGER PRIMARY KEY, id_module_sequence INTEGER,
    id_enseignant INTEGER);

INSERT INTO MAQUETTE_module VALUES (1, 1), (2, 2);
INSERT INTO MAQUETTE_module_sequencage VALUES (10, 1, NULL), (20, 2, NULL);
INSERT INTO MAQUETTE_module_sequence   VALUES (100, 10, NULL), (200, 20, NULL);
INSERT INTO CLASS_session              VALUES (1000, 100, NULL), (2000, 200, 2);
"""


def make_user(id_: int, role: str, name: str) -> User:
    return User(
        id=id_, prenom=name, nom=name, ExplicitSecondaryK=name,
        main_role=role, roles=["connected_user", role, name],
    )


TEACHER_1 = make_user(1, "enseignant", "Alice Responsable1")   # responsable du module 1
STUDENT_1 = make_user(1, "etudiant", "Etienne Etudiant")       # même id que TEACHER_1, autre table


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def db(monkeypatch):
    conn = sqlite3.connect(":memory:", check_same_thread=False)  # TestClient = autre thread
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)

    def fake_db_request(requester, request):
        check_access(request=request, user=requester)             # vraie règle d'accès
        sql = re.sub(r"%\((\w+)\)s", r":\1", request.request)     # style pyformat → nommé
        cur = conn.execute(sql, request.params or {})
        rows = [dict(r) for r in cur.fetchall()] if cur.description else []
        conn.commit()
        return rows

    monkeypatch.setattr(MAQUETTE_module, "db_request", fake_db_request)
    monkeypatch.setattr("api.dependencies.db_request", fake_db_request)  # pour les prédicats
    yield conn
    conn.close()


@pytest.fixture
def call_as(db):
    app = FastAPI()
    app.include_router(MAQUETTE_module.router)
    client = TestClient(app, raise_server_exceptions=False)

    def _call(user, method, url, **kwargs):
        app.dependency_overrides[get_current_active_user] = lambda: user
        return client.request(method, url, **kwargs)

    return _call


def scalar(db, sql):
    row = db.execute(sql).fetchone()
    return None if row is None else row[0]


# (url, body, requête de contrôle, id du module 1, id du module 2)
PATCH_CASES = [
    pytest.param(
        "/modules/{m}/sequencages/{r}", {"id_intervenant_principal": 99},
        "SELECT id_intervenant_principal FROM MAQUETTE_module_sequencage WHERE id_module_sequencage={r}",
        10, 20, id="sequencage"),
    pytest.param(
        "/modules/{m}/sequences/{r}", {"id_intervenant_principal": 99},
        "SELECT id_intervenant_principal FROM MAQUETTE_module_sequence WHERE id_module_sequence={r}",
        100, 200, id="sequence"),
    pytest.param(
        "/modules/{m}/sessions/{r}", {"id_enseignant": 99},
        "SELECT id_enseignant FROM CLASS_session WHERE id_session={r}",
        1000, 2000, id="session"),
]


# ─────────────────────────────────────────────
# Témoin : le cas légitime doit continuer à marcher
# ─────────────────────────────────────────────

@pytest.mark.parametrize("url, body, check, own, foreign", PATCH_CASES)
def test_responsable_can_patch_resource_of_own_module(call_as, db, url, body, check, own, foreign):
    r = call_as(TEACHER_1, "PATCH", url.format(m=1, r=own), json=body)
    assert r.status_code == 200
    assert scalar(db, check.format(r=own)) == 99


# ─────────────────────────────────────────────
# Faille : ressource d'un autre module via son propre id_module
# ─────────────────────────────────────────────

@pytest.mark.parametrize("url, body, check, own, foreign", PATCH_CASES)
def test_responsable_cannot_patch_resource_of_other_module(call_as, db, url, body, check, own, foreign):
    before = scalar(db, check.format(r=foreign))

    # TEACHER_1 est responsable du module 1 mais cible une ressource du module 2
    call_as(TEACHER_1, "PATCH", url.format(m=1, r=foreign), json=body)

    assert scalar(db, check.format(r=foreign)) == before, \
        "La ressource du module 2 a été modifiée par le responsable du module 1"


def test_responsable_cannot_delete_sequencage_of_other_module(call_as, db):
    call_as(TEACHER_1, "DELETE", "/modules/1/sequencages/20")

    assert scalar(db, "SELECT COUNT(*) FROM MAQUETTE_module_sequencage WHERE id_module_sequencage=20") == 1, \
        "Le séquençage du module 2 a été supprimé par le responsable du module 1"


# ─────────────────────────────────────────────
# Collision d'ids entre tables (autre défaut du même contrôle)
# ─────────────────────────────────────────────

def test_student_with_same_id_as_responsable_is_denied(call_as, db):
    r = call_as(STUDENT_1, "PATCH", "/modules/1/sequences/100", json={"id_intervenant_principal": 99})

    assert r.status_code == 403
    assert scalar(db, "SELECT id_intervenant_principal FROM MAQUETTE_module_sequence WHERE id_module_sequence=100") is None


# ─────────────────────────────────────────────
# Robustesse : module inexistant
# ─────────────────────────────────────────────

def test_unknown_module_is_denied_not_500(call_as, db):
    r = call_as(TEACHER_1, "PATCH", "/modules/999/sequences/100", json={"id_intervenant_principal": 99})

    assert r.status_code in (403, 404)   # aujourd'hui : IndexError → 500


#─────────────────────────────────────────────
# Interaction entre 2 enseignants
# ─────────────────────────────────────────────

TEACHER_2 = make_user(2, "enseignant", "Bernard Responsable2")  # responsable du module 2

# (utilisateur, module dans l'URL, module propriétaire de la ressource, attendu)
OWNERSHIP_MATRIX = [
    pytest.param(TEACHER_1, 1, 1, True,  id="T1-url1-res1-legitime"),
    pytest.param(TEACHER_2, 2, 2, True,  id="T2-url2-res2-legitime"),
    # URL de son module, ressource de l'autre : la faille
    pytest.param(TEACHER_1, 1, 2, False, id="T1-url1-res2-ressource-etrangere"),
    pytest.param(TEACHER_2, 2, 1, False, id="T2-url2-res1-ressource-etrangere"),
    # URL du module de l'autre : il n'est pas responsable de ce module
    pytest.param(TEACHER_1, 2, 2, False, id="T1-url2-res2-module-etranger"),
    pytest.param(TEACHER_2, 1, 1, False, id="T2-url1-res1-module-etranger"),
    # URL du module de l'autre, ressource de son propre module
    pytest.param(TEACHER_1, 2, 1, False, id="T1-url2-res1-croise"),
    pytest.param(TEACHER_2, 1, 2, False, id="T2-url1-res2-croise"),
]


@pytest.mark.parametrize("url, body, check, res_m1, res_m2", PATCH_CASES)
@pytest.mark.parametrize("user, url_module, res_module, allowed", OWNERSHIP_MATRIX)
def test_two_teachers_ownership_matrix(
    call_as, db, url, body, check, res_m1, res_m2,
    user, url_module, res_module, allowed,
):
    resource = res_m1 if res_module == 1 else res_m2
    before = scalar(db, check.format(r=resource))

    call_as(user, "PATCH", url.format(m=url_module, r=resource), json=body)

    after = scalar(db, check.format(r=resource))
    if allowed:
        assert after == 99, "Le responsable légitime n'a pas pu modifier sa ressource"
    else:
        assert after == before, (
            f"{user.prenom} (module {url_module} dans l'URL) a modifié "
            f"une ressource du module {res_module}"
        )


@pytest.mark.parametrize("user, url_module, res_module, allowed", [
    pytest.param(TEACHER_1, 1, 1, True,  id="T1-legitime"),
    pytest.param(TEACHER_1, 1, 2, False, id="T1-url1-res2"),
    pytest.param(TEACHER_2, 2, 1, False, id="T2-url2-res1"),
    pytest.param(TEACHER_2, 1, 1, False, id="T2-url1-res1"),
])
def test_two_teachers_delete_sequencage(call_as, db, user, url_module, res_module, allowed):
    resource = 10 if res_module == 1 else 20

    call_as(user, "DELETE", f"/modules/{url_module}/sequencages/{resource}")

    remaining = scalar(db, f"SELECT COUNT(*) FROM MAQUETTE_module_sequencage WHERE id_module_sequencage={resource}")
    assert remaining == (0 if allowed else 1)


# ─────────────────────────────────────────────
# Dépendances entre séquences
#   séquences : 100, 101 → module 1   |   200, 201 → module 2
#   dépendances initiales :
#       (100, 101)  interne au module 1
#       (200, 201)  interne au module 2
#       (101, 200)  inter-modules (101 ∈ module 1, 200 ∈ module 2)
# ─────────────────────────────────────────────

DEPS_SCHEMA = """
CREATE TABLE MAQUETTE_dependance_sequence (
    id_sequence_prev INTEGER, id_sequence_next INTEGER,
    PRIMARY KEY (id_sequence_prev, id_sequence_next));

INSERT INTO MAQUETTE_module_sequencage VALUES (11, 1, NULL), (21, 2, NULL);
INSERT INTO MAQUETTE_module_sequence   VALUES (101, 11, NULL), (201, 21, NULL);
INSERT INTO MAQUETTE_dependance_sequence VALUES (100, 101), (200, 201), (101, 200);
"""


@pytest.fixture
def db_deps(db):
    db.executescript(DEPS_SCHEMA)
    return db


def dep_count(db, prev=None, nxt=None):
    sql = "SELECT COUNT(*) FROM MAQUETTE_dependance_sequence"
    if prev is not None:
        sql += f" WHERE id_sequence_prev={prev} AND id_sequence_next={nxt}"
    return scalar(db, sql)


# ─────────────────────────────────────────────
# POST /modules/{id_module}/dependencies/
# ─────────────────────────────────────────────

# (utilisateur, module dans l'URL, (prev, next), autorisé)
# Les paires sont absentes du jeu initial (la PK ferait échouer l'INSERT).
# (101, 100) est l'inverse de (100, 101) : l'API ne détecte pas les cycles,
# on s'en sert ici uniquement pour obtenir une paire interne libre.
ADD_MATRIX = [
    pytest.param(TEACHER_1, 1, (101, 100), True,  id="T1-url1-interne-legitime"),
    pytest.param(TEACHER_2, 2, (201, 200), True,  id="T2-url2-interne-legitime"),
    pytest.param(TEACHER_1, 1, (100, 200), True,  id="T1-url1-croise-une-extremite-a-lui"),
    # URL de son module, mais aucune des deux séquences ne lui appartient : la faille
    pytest.param(TEACHER_1, 1, (201, 200), False, id="T1-url1-sequences-etrangeres"),
    pytest.param(TEACHER_2, 2, (101, 100), False, id="T2-url2-sequences-etrangeres"),
    # URL du module de l'autre : il n'en est pas responsable
    pytest.param(TEACHER_1, 2, (201, 200), False, id="T1-url2-module-etranger"),
    pytest.param(TEACHER_2, 1, (101, 100), False, id="T2-url1-module-etranger"),
]


@pytest.mark.parametrize("user, url_module, pair, allowed", ADD_MATRIX)
def test_add_dependency_ownership(call_as, db_deps, user, url_module, pair, allowed):
    prev, nxt = pair
    total_before = dep_count(db_deps)

    call_as(user, "POST", f"/modules/{url_module}/dependencies",
            json={"id_sequence_prev": prev, "id_sequence_next": nxt})

    if allowed:
        assert dep_count(db_deps, prev, nxt) == 1, "Le responsable légitime n'a pas pu créer la dépendance"
    else:
        assert dep_count(db_deps, prev, nxt) == 0, (
            f"{user.prenom} (module {url_module} dans l'URL) a créé la dépendance {pair} "
            f"entre des séquences qui ne lui appartiennent pas"
        )
        assert dep_count(db_deps) == total_before


# ─────────────────────────────────────────────
# DELETE /modules/{id_module}/dependencies/{prev}/{next}
# ─────────────────────────────────────────────

DELETE_MATRIX = [
    pytest.param(TEACHER_1, 1, (100, 101), True,  id="T1-url1-interne-legitime"),
    pytest.param(TEACHER_2, 2, (200, 201), True,  id="T2-url2-interne-legitime"),
    # dépendance inter-modules : chaque responsable peut la supprimer
    pytest.param(TEACHER_1, 1, (101, 200), True,  id="T1-url1-croise"),
    pytest.param(TEACHER_2, 2, (101, 200), True,  id="T2-url2-croise"),
    # URL de son module, dépendance qui ne le concerne pas : la faille
    pytest.param(TEACHER_1, 1, (200, 201), False, id="T1-url1-dependance-etrangere"),
    pytest.param(TEACHER_2, 2, (100, 101), False, id="T2-url2-dependance-etrangere"),
    # URL du module de l'autre
    pytest.param(TEACHER_1, 2, (200, 201), False, id="T1-url2-module-etranger"),
    pytest.param(TEACHER_2, 1, (100, 101), False, id="T2-url1-module-etranger"),
    pytest.param(TEACHER_2, 1, (101, 200), False, id="T2-url1-croise-module-etranger"),
]


@pytest.mark.parametrize("user, url_module, pair, allowed", DELETE_MATRIX)
def test_delete_dependency_ownership(call_as, db_deps, user, url_module, pair, allowed):
    prev, nxt = pair
    assert dep_count(db_deps, prev, nxt) == 1  # garde-fou sur le jeu de données

    call_as(user, "DELETE", f"/modules/{url_module}/dependencies/{prev}/{nxt}")

    assert dep_count(db_deps, prev, nxt) == (0 if allowed else 1), (
        f"{user.prenom} (module {url_module} dans l'URL) : résultat inattendu sur la dépendance {pair}"
    )
    # Détecte un DELETE au WHERE trop large : seule la ligne visée peut disparaître
    assert dep_count(db_deps) == (2 if allowed else 3)


# ─────────────────────────────────────────────
# Collision d'ids entre tables et module inexistant
# ─────────────────────────────────────────────

def test_student_with_same_id_as_responsable_cannot_add_dependency(call_as, db_deps):
    r = call_as(STUDENT_1, "POST", "/modules/1/dependencies",
                json={"id_sequence_prev": 101, "id_sequence_next": 100})

    assert r.status_code == 403
    assert dep_count(db_deps, 101, 100) == 0


def test_student_with_same_id_as_responsable_cannot_delete_dependency(call_as, db_deps):
    call_as(STUDENT_1, "DELETE", "/modules/1/dependencies/100/101")

    assert dep_count(db_deps, 100, 101) == 1


def test_add_dependency_unknown_module_is_denied_not_500(call_as, db_deps):
    r = call_as(TEACHER_1, "POST", "/modules/999/dependencies",
                json={"id_sequence_prev": 101, "id_sequence_next": 100})

    assert r.status_code in (403, 404)   # aujourd'hui : IndexError → 500
    assert dep_count(db_deps, 101, 100) == 0