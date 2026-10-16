# tests/test_university_subscript.py
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from api.dependencies import get_current_active_user
from models.request import SQLRequest
from models.user import User
from user import LNM_university
from user.LNM_university import StudentDecisionPayload

from access_control.rules import evaluate_rule

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

ID_ETUDIANT = 42


def make_student(user_id: int = ID_ETUDIANT) -> User:
    return User(
        id=user_id,
        prenom="Jean",
        nom="Dupont",
        mail="jean.dupont@lnm.fr",
        ExplicitSecondaryK="Dupont Jean",
        main_role="etudiant",
        roles=["connected_user", "etudiant", "Dupont Jean"],
    )


@pytest.fixture
def recorded(monkeypatch):
    """Remplace db_request par un faux qui enregistre les SQLRequest reçues."""
    calls = []

    def fake_db_request(requester, request):
        calls.append(request)
        sql = request.request
        if "mobility_z_score" in sql:
            return [{"mobility_z_score": 1.0}]
        if "wishes_count" in sql:
            return [{"wishes_count": 0, "max_priority": 0,
                     "already_exists": 0, "is_submitted": 0}]
        return [{"id_assignment": 1, "status": "pending"}]

    monkeypatch.setattr(LNM_university, "db_request", fake_db_request)
    return calls


# Un appel par endpoint concerné, avec l'utilisateur courant en paramètre
ENDPOINT_CALLS = {
    "get_campaign_status": lambda user: LNM_university.get_campaign_status(
        id_etudiant=ID_ETUDIANT, current_user=user),
    "add_university_to_wishes": lambda user: LNM_university.add_university_to_wishes(
        id_etudiant=ID_ETUDIANT, id_partner_university=7,
        current_user=user, payload={"id_semestre": 8}),
    "get_student_assignment": lambda user: LNM_university.get_student_assignment(
        id_etudiant=ID_ETUDIANT, current_user=user),
    "submit_student_decision": lambda user: LNM_university.submit_student_decision(
        id_etudiant=ID_ETUDIANT,
        payload=StudentDecisionPayload(decision="accepted"),
        current_user=user),
}


# ─────────────────────────────────────────────
# 0. Cause racine, isolée
# ─────────────────────────────────────────────

class TestRootCause:

    def test_sqlrequest_is_not_subscriptable(self):
        req = SQLRequest(request="SELECT 1", allowedRolesRequester=[])
        with pytest.raises(TypeError):
            req["allowedRolesRequester"] += ["Dupont Jean"]


# ─────────────────────────────────────────────
# 1. L'étudiant légitime ne doit pas provoquer de TypeError
#    (ÉCHOUENT tant que le bug existe)
# ─────────────────────────────────────────────

EXPECTED_OWNER_RULE = {
    "roles": [],
    "owner": {"role": "etudiant", "id": "id_etudiant"},
}

@pytest.mark.parametrize("endpoint", ENDPOINT_CALLS.keys())
class TestLegitStudent:

    def test_no_type_error(self, endpoint, recorded):
        user = make_student(ID_ETUDIANT)
        try:
            ENDPOINT_CALLS[endpoint](user)
        except TypeError as exc:
            pytest.fail(f"{endpoint} : TypeError pour l'étudiant légitime : {exc}")

    def test_first_request_grants_student_secondary_key(self, endpoint, recorded):
        user = make_student(ID_ETUDIANT)
        ENDPOINT_CALLS[endpoint](user)
        assert recorded, "db_request n'a jamais été appelé"
        first = recorded[0]
        assert isinstance(first, SQLRequest)
        assert first.allowedRolesRequester == EXPECTED_OWNER_RULE


    def test_first_request_declares_owner_rule(self, endpoint, recorded):
        user = make_student(ID_ETUDIANT)
        ENDPOINT_CALLS[endpoint](user)
        assert recorded, "db_request n'a jamais été appelé"
        first = recorded[0]
        assert isinstance(first, SQLRequest)
        assert first.allowedRolesRequester == EXPECTED_OWNER_RULE

    def test_owner_rule_grants_student_on_own_data(self, endpoint, recorded):
        user = make_student(ID_ETUDIANT)
        ENDPOINT_CALLS[endpoint](user)
        first = recorded[0]
        assert evaluate_rule(first.allowedRolesRequester, user, first.params) is True


# ─────────────────────────────────────────────
# 2. Témoins : le bug ne touche que le chemin "étudiant légitime"
#    (PASSENT aujourd'hui)
# ─────────────────────────────────────────────

class TestOtherUserControl:

    @pytest.mark.parametrize("endpoint", ["add_university_to_wishes", "submit_student_decision"])
    def test_other_user_gets_403_before_the_bug(self, endpoint, recorded):
        other = make_student(user_id=999)
        with pytest.raises(HTTPException) as exc:
            ENDPOINT_CALLS[endpoint](other)
        assert exc.value.status_code == 403

    @pytest.mark.parametrize("endpoint", ["get_campaign_status", "get_student_assignment"])
    def test_other_user_is_refused_by_owner_rule(self, endpoint, recorded):
        other = make_student(user_id=999)
        ENDPOINT_CALLS[endpoint](other)
        first = recorded[0]
        assert first.params["id_etudiant"] == ID_ETUDIANT   # la ressource visée est celle de 42
        assert evaluate_rule(first.allowedRolesRequester, other, first.params) is False


# ─────────────────────────────────────────────
# 3. Vue HTTP : l'étudiant légitime obtient un 500
#    (ÉCHOUENT tant que le bug existe)
# ─────────────────────────────────────────────

class TestHttpLevel:

    @pytest.fixture
    def client(self, recorded):
        app = FastAPI()
        app.include_router(LNM_university.router)
        app.dependency_overrides[get_current_active_user] = lambda: make_student(ID_ETUDIANT)
        # raise_server_exceptions=False : on veut le code HTTP, pas l'exception
        return TestClient(app, raise_server_exceptions=False)

    def test_campaign_status_returns_200(self, client):
        r = client.get(f"/university/etudiant/{ID_ETUDIANT}/campaign-status")
        assert r.status_code == 200, r.text

    def test_assignment_returns_200(self, client):
        r = client.get(f"/university/etudiant/{ID_ETUDIANT}/assignment")
        assert r.status_code == 200, r.text

    def test_decision_returns_200(self, client):
        r = client.post(f"/university/etudiant/{ID_ETUDIANT}/assignment/decision",
                        json={"decision": "accepted"})
        assert r.status_code == 200, r.text

    def test_add_wish_returns_200(self, client):
        r = client.post(f"/university/etudiant/{ID_ETUDIANT}/wish/7",
                        json={"id_semestre": 8})
        assert r.status_code == 200, r.text