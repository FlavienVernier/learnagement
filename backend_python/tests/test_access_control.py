# tests/test_access_control.py

import pytest
from unittest.mock import MagicMock
from access_control.types import Responsibility
from access_control.responsibilities import (
    _responsibility_covers,
    has_all_responsibilities,
    has_hierarchy_responsibilities,
    has_any_of_responsibilities,
)
from access_control.rules import evaluate_rule
from access_control.checker import check_access
from models.request import SQLRequest
from fastapi import HTTPException


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def make_user(type_role: str = "enseignant", responsibilities: list[dict] = None):
    user = MagicMock()
    user.type = type_role
    user.roles = [type_role]
    user.id = 99
    user.responsibilities = responsibilities or []
    return user


def make_stored(type_objet: str, dimensions: dict) -> dict:
    return {"type_objet": type_objet, "dimensions": dimensions}


def make_required(type_objet: str, **dims) -> Responsibility:
    return Responsibility(type_objet=type_objet, dimensions=dims)


# ─────────────────────────────────────────────
# _responsabilite_covers
# ─────────────────────────────────────────────

class TestResponsibilityCovers:

    def test_wildcard_vide(self):
        """
        {} en BD couvre un scope quelconque.
        """
        stored = make_stored("stage", {})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is True

    def test_filiere_couvre_filiere_et_niveau(self):
        """
        {"filiere":"IDU"} couvre {"filiere":"IDU","niveau":"FI4"}.
        """
        stored = make_stored("stage", {"filiere": "IDU"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is True

    def test_exact_match(self):
        """
        {"filiere":"IDU","niveau":"FI4"} couvre {"filiere":"IDU","niveau":"FI4"}.
        """
        stored = make_stored("stage", {"filiere": "IDU", "niveau": "FI4"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is True

    def test_une_mauvaise_valeur_ne_couvre_pas(self):
        """
        {"filiere":"IDU","niveau":"FI4"} ne couvre PAS {"filiere":"IDU","niveau":"FI3"}.
        """
        stored = make_stored("stage", {"filiere": "IDU", "niveau": "FI4"})
        required = make_required("stage", filiere="IDU", niveau="FI3")
        assert _responsibility_covers(stored, required) is False

    def test_trop_precis_ne_couvre_pas(self):
        """
        {"filiere":"IDU","niveau":"FI4"} ne couvre PAS {"filiere":"IDU"} seul.
        """
        stored = make_stored("stage", {"filiere": "IDU", "niveau": "FI4"})
        required = make_required("stage", filiere="IDU")
        assert _responsibility_covers(stored, required) is False

    def test_mauvaise_valeur_ne_couvre_pas(self):
        """
        {"filiere":"SEA"} ne couvre PAS {"filiere":"IDU","niveau":"FI4"}.
        """
        stored = make_stored("stage", {"filiere": "SEA"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is False

    def test_dimension_differente_ne_couvre_pas(self):
        """
        {"filiere":"IDU","semestre":"S8"} ne couvre PAS {"filiere":"IDU","niveau":"FI4"}.
        """
        stored = make_stored("stage", {"filiere": "IDU", "semestre": "S8"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is False

    def test_type_objet_all_couvre_tout(self):
        """
        type_objet="all" couvre n'importe quel type_objet si dimensions ok.
        """
        stored = make_stored("all", {"filiere": "IDU"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is True

    def test_type_objet_all_ne_couvre_pas_valeur_differente(self):
        """
        type_objet="all" couvre n'importe quel type_objet si dimensions ok.
        """
        stored = make_stored("all", {"filiere": "SEA"})
        required = make_required("stage", filiere="IDU", niveau="FI4")
        assert _responsibility_covers(stored, required) is False

    def test_type_objet_different_ne_couvre_pas(self):
        """
        type_objet différent
        """
        stored = make_stored("semestre", {"filiere": "IDU"})
        required = make_required("stage", filiere="IDU")
        assert _responsibility_covers(stored, required) is False

    def test_dimension_a_valeur_any_couvre_plus_large(self):
        """
        {"filiere":"IDU","niveau":"S8"} couvre {"filiere":"IDU","niveau":"any"}.
        """
        stored = make_stored("stage", {"filiere": "IDU",})
        required = make_required("stage", filiere="any", niveau="FI4")
        assert _responsibility_covers(stored, required) is True

    def test_dimension_a_valeur_any_couvre_exact(self):
        """
        {"filiere":"IDU","niveau":"S8"} couvre {"filiere":"IDU","niveau":"any"}.
        """
        stored = make_stored("stage", {"filiere": "IDU", "niveau": "FI4"})
        required = make_required("stage", filiere="IDU", niveau="any")
        assert _responsibility_covers(stored, required) is True

    def test_dimension_a_valeur_any_ne_couvre_pas_trop_precis(self):
        """
        {"filiere":"IDU","niveau":"S8"} couvre {"filiere":"IDU","niveau":"any"}.
        """
        stored = make_stored("stage", {"filiere": "IDU", "niveau": "FI4"})
        required = make_required("stage", filiere="any")
        assert _responsibility_covers(stored, required) is False

# ─────────────────────────────────────────────
# has_any_of_responsabilites
# ─────────────────────────────────────────────

class TestHasAnyOfResponsabilite:

    def test_user_without_responsibility(self):
        user = make_user(responsibilities=[])
        required = [
            make_required("stage", filiere="IDU")
        ]

        assert has_any_of_responsibilities(user, required) is False

    def test_user_with_responsibility_covering(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "IDU"})
        ])
        required = [
            make_required("stage", filiere="IDU", niveau="FI4")
        ]

        assert has_any_of_responsibilities(user, required) is True

    def test_user_avec_plusieurs_dont_une_couvre(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "SEA"}),
            make_stored("stage", {"filiere": "IDU"}),
        ])
        required = [
            make_required("stage", filiere="IDU", niveau="FI4")
        ]

        assert has_any_of_responsibilities(user, required) is True

    def test_user_with_responsibilities_without_covering(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "SEA"}),
            make_stored("semestre", {"filiere": "IDU", "semestre": "S8"}),
        ])
        required = [
            make_required("stage", filiere="IDU")
        ]

        assert has_any_of_responsibilities(user, required) is False

    def test_user_couvre_au_moins_une_parmi_plusieurs_required(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "SEA"}),
            make_stored("stage", {"filiere": "IDU"}),
        ])
        required = [
            make_required("stage", filiere="IDU", niveau="FI4"),
            make_required("stage", filiere="MM", niveau="FI4"),
        ]
        assert has_any_of_responsibilities(user, required) is True

# ─────────────────────────────────────────────
# has_all_responsabilites
# ─────────────────────────────────────────────

class TestHasAllResponsabilites:

    def test_satisfait_toutes(self):
        user = make_user(responsibilities=[
            make_stored("filiere",  {"filiere": "IDU"}),
            make_stored("semestre", {"filiere": "IDU", "semestre": "S8"}),
        ])
        required = [
            make_required("filiere",  filiere="IDU"),
            make_required("semestre", filiere="IDU", semestre="S8"),
        ]
        assert has_all_responsibilities(user, required) is True

    def test_satisfait_une_seule(self):
        user = make_user(responsibilities=[
            make_stored("filiere", {"filiere": "IDU"}),
        ])
        required = [
            make_required("filiere",  filiere="IDU"),
            make_required("semestre", filiere="IDU", semestre="S8"),
        ]
        assert has_all_responsibilities(user, required) is False

    def test_liste_vide(self):
        user = make_user(responsibilities=[])
        assert has_all_responsibilities(user, []) is True  # all([]) vacuité


# ─────────────────────────────────────────────
# has_hierarchy_responsabilites
# ─────────────────────────────────────────────

class TestHasHierarchyResponsabilites:

    def setup_method(self):
        self.hierarchy = [
            make_required("filiere",  filiere="IDU"),
            make_required("semestre", filiere="IDU", semestre="S8"),
            make_required("module",   filiere="IDU", semestre="S8", niveau="FI4"),
        ]

    def test_satisfait_premier_uniquement(self):
        user = make_user(responsibilities=[
            make_stored("filiere", {"filiere": "IDU"}),
        ])
        assert has_hierarchy_responsibilities(user, self.hierarchy) is True

    def test_satisfait_deux_premiers(self):
        user = make_user(responsibilities=[
            make_stored("filiere",  {"filiere": "IDU"}),
            make_stored("semestre", {"filiere": "IDU", "semestre": "S8"}),
        ])
        assert has_hierarchy_responsibilities(user, self.hierarchy) is True

    def test_satisfait_toute_la_hierarchie(self):
        user = make_user(responsibilities=[
            make_stored("filiere",  {"filiere": "IDU"}),
            make_stored("semestre", {"filiere": "IDU", "semestre": "S8"}),
            make_stored("module",   {"filiere": "IDU", "semestre": "S8", "niveau": "FI4"}),
        ])
        assert has_hierarchy_responsibilities(user, self.hierarchy) is True

    def test_ne_satisfait_pas_le_premier(self):
        user = make_user(responsibilities=[
            make_stored("semestre", {"filiere": "IDU", "semestre": "S8"}),
        ])
        assert has_hierarchy_responsibilities(user, self.hierarchy) is False

    def test_hierarchie_vide(self):
        user = make_user(responsibilities=[])
        assert has_hierarchy_responsibilities(user, []) is False


# ─────────────────────────────────────────────
# evaluate_rule
# ─────────────────────────────────────────────

class TestEvaluateRule:

    def test_anonymous_autorise_toujours(self):
        assert evaluate_rule("anonymous", None, {}) is True

    def test_connected_user_avec_user(self):
        assert evaluate_rule("connected_user", make_user(), {}) is True

    def test_connected_user_sans_user(self):
        assert evaluate_rule("connected_user", None, {}) is False

    def test_string_inconnue_leve_erreur(self):
        with pytest.raises(ValueError):
            evaluate_rule("superadmin", make_user(), {})

    def test_liste_roles_role_present(self):
        user = make_user(type_role="administratif")
        assert evaluate_rule(["administratif", "enseignant"], user, {}) is True

    def test_liste_roles_role_absent(self):
        user = make_user(type_role="etudiant")
        assert evaluate_rule(["administratif", "enseignant"], user, {}) is False

    def test_liste_roles_vide_leve_erreur(self):
        with pytest.raises(ValueError):
            evaluate_rule([], make_user(), {})

    def test_liste_roles_user_none(self):
        assert evaluate_rule(["administratif"], None, {}) is False

    def test_dict_roles_satisfait(self):
        user = make_user(type_role="administratif")
        assert evaluate_rule({"roles": ["administratif"]}, user, {}) is True

    def test_dict_any_satisfait(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "IDU"})
        ])
        rule = {"any": [{"type_objet": "stage", "filiere": "IDU"}]}
        assert evaluate_rule(rule, user, {}) is True

    def test_dict_any_non_satisfait(self):
        user = make_user(responsibilities=[
            make_stored("stage", {"filiere": "SEA"})
        ])
        rule = {"any": [{"type_objet": "stage", "filiere": "IDU"}]}
        assert evaluate_rule(rule, user, {}) is False

    def test_dict_all_satisfait(self):
        user = make_user(responsibilities=[
            make_stored("filiere",  {"filiere": "IDU"}),
            make_stored("semestre", {"semestre": "S8"}),
        ])
        rule = {"all": [
            {"type_objet": "filiere",  "filiere": "IDU"},
            {"type_objet": "semestre", "semestre": "S8"},
        ]}
        assert evaluate_rule(rule, user, {}) is True

    def test_dict_au_moins_une_condition_suffit(self):
        """roles échoue mais one réussit → True"""
        user = make_user(type_role="enseignant", responsibilities=[
            make_stored("stage", {"filiere": "IDU"})
        ])
        rule = {
            "roles": ["administratif"],
            "any":   [{"type_objet": "stage", "filiere": "IDU"}],
        }
        assert evaluate_rule(rule, user, {}) is True

    def test_dict_cle_inconnue_leve_erreur(self):
        with pytest.raises(ValueError):
            evaluate_rule({"superpower": ["x"]}, make_user(), {})

    def test_lambda_retourne_string(self):
        rule = lambda params, user: "anonymous"
        assert evaluate_rule(rule, None, {}) is True

    def test_lambda_retourne_liste_roles(self):
        user = make_user(type_role="administratif")
        rule = lambda params, user: ["administratif"] if params.get("secret") else ["etudiant"]
        assert evaluate_rule(rule, user, {"secret": True}) is True

    def test_lambda_utilise_params(self):
        user = make_user(type_role="etudiant")
        user.id = 42
        rule = lambda params, u: "connected_user" if u.id == params.get("id_etudiant") else ["administratif"]
        assert evaluate_rule(rule, user, {"id_etudiant": 42}) is True
        assert evaluate_rule(rule, user, {"id_etudiant": 99}) is False


# ─────────────────────────────────────────────
# check_access
# ─────────────────────────────────────────────

class TestCheckAccess:

    def setup_method(self):
        self.requests = {
            "get_public": {
                "request": "SELECT 1",
                "params": {},
                "allowedRolesRequester": "anonymous",
            },
            "get_admin_only": {
                "request": "SELECT 1",
                "params": {},
                "allowedRolesRequester": ["administratif"],
            },
        }

    def test_acces_autorise(self):
        request = SQLRequest.model_validate(self.requests["get_public"])
        check_access(request, None)  # ne lève pas d'exception

    def test_acces_refuse_leve_403(self):
        request = SQLRequest.model_validate(self.requests["get_admin_only"])
        user = make_user(type_role="etudiant")
        with pytest.raises(HTTPException) as exc:
            check_access(request, user)
        assert exc.value.status_code == 403