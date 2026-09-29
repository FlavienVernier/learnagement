import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from auth.authenticate_cas import (
    authenticate_cas,
    _determine_role_from_cas_groups,
    _determine_promo_from_cas_groups,
    _create_cas_user,
    CasUserProvision,
)


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

def make_cas_data(login="tartampion", role="enseignant") -> CasUserProvision:
    members_by_role = {
        "enseignant": [
            "cn=personnels-enseignants.polytech,ou=groups,dc=uds,dc=fr",
            "cn=permanents,ou=groups,dc=uds,dc=fr",
        ],
        "etudiant": [
            "cn=etudiants-ige4-idu,ou=groups,dc=uds,dc=fr",
            "cn=usmb-etudiants-polytech,ou=groups,dc=uds,dc=fr",
        ],
        "administratif": [
            "cn=personnels.polytech,ou=groups,dc=uds,dc=fr",
        ],
        "inconnu": [
            "cn=groupe-inconnu,ou=groups,dc=uds,dc=fr",
        ],
    }
    return CasUserProvision(
        login=login,
        email=f"{login}@lnm.fr",
        nom="Tartampion",
        prenom="Pierre",
        members=members_by_role[role],
    )


# ─────────────────────────────────────────────
# _determine_role_from_cas_groups
# ─────────────────────────────────────────────

class TestDetermineRole:

    @pytest.fixture(autouse=True)
    def set_env(self, monkeypatch):
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ADMINISTRATIF", "administratif-polytech")
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ENSEIGNANT", "personnels-enseignants.polytech")
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ETUDIANT", "usmb-etudiants-polytech etudiants-polytech")

    def test_enseignant(self):
        data = make_cas_data(role="enseignant")
        assert _determine_role_from_cas_groups(data.members) == "enseignant"

    def test_etudiant(self):
        data = make_cas_data(role="etudiant")
        assert _determine_role_from_cas_groups(data.members) == "etudiant"

    def test_administratif(self):
        data = make_cas_data(role="administratif")
        assert _determine_role_from_cas_groups(data.members) == "administratif"

    def test_groupe_inconnu(self):
        data = make_cas_data(role="inconnu")
        assert _determine_role_from_cas_groups(data.members) is None

    def test_priorite_administratif_sur_enseignant(self):
        """Un user dans les deux groupes → administratif prioritaire."""
        members = [
            "cn=administratif-polytech,ou=groups,dc=uds,dc=fr",
            "cn=personnels-enseignants.polytech,ou=groups,dc=uds,dc=fr",
        ]
        assert _determine_role_from_cas_groups(members) == "administratif"

    def test_env_vide_retourne_none(self, monkeypatch):
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ENSEIGNANT", "")
        data = make_cas_data(role="enseignant")
        assert _determine_role_from_cas_groups(data.members) is None


# ─────────────────────────────────────────────
# _determine_promo_from_cas_groups
# ─────────────────────────────────────────────

class TestDeterminePromo:

    @pytest.fixture(autouse=True)
    def set_env(self, monkeypatch):
        monkeypatch.setenv(
            "CAS_ETUDIANTS_2_PROMO",
            '[{"groupe":"etudiants-ige4-idu","promo":"IDU FISE 4 Annecy"},'
            ' {"groupe":"etudiants-ige3-sea","promo":"SEA FISE 3 Annecy"}]'
        )

    def test_promo_trouvee(self):
        members = ["cn=etudiants-ige4-idu,ou=groups,dc=uds,dc=fr"]
        with patch("auth.authenticate_cas.mysql.connector.connect") as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id_promo": 42}
            mock_conn.return_value.cursor.return_value = mock_cursor

            result = _determine_promo_from_cas_groups(members)
            assert result == 42

    def test_groupe_inconnu(self):
        members = ["cn=groupe-inconnu,ou=groups,dc=uds,dc=fr"]
        result = _determine_promo_from_cas_groups(members)
        assert result is None

    def test_promo_non_trouvee_en_bd(self):
        members = ["cn=etudiants-ige4-idu,ou=groups,dc=uds,dc=fr"]
        with patch("auth.authenticate_cas.mysql.connector.connect") as mock_conn:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None  # promo absente de la BD
            mock_conn.return_value.cursor.return_value = mock_cursor

            result = _determine_promo_from_cas_groups(members)
            assert result is None

    def test_env_mal_forme(self, monkeypatch):
        monkeypatch.setenv("CAS_ETUDIANTS_2_PROMO", "pas_du_json")
        members = ["cn=etudiants-ige4-idu,ou=groups,dc=uds,dc=fr"]
        result = _determine_promo_from_cas_groups(members)
        assert result is None


# ─────────────────────────────────────────────
# authenticate_cas — flux complet mocké
# ─────────────────────────────────────────────

class TestAuthenticateCas:

    @pytest.fixture(autouse=True)
    def set_env(self, monkeypatch):
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ADMINISTRATIF", "")
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ENSEIGNANT", "personnels-enseignants.polytech")
        monkeypatch.setenv("CAS_ALLOWED_GROUPS_4_ETUDIANT", "usmb-etudiants-polytech etudiants-polytech")
        monkeypatch.setenv("INSTANCE_SECRET", "secret")
        monkeypatch.setenv("SESSION_TIMEOUT", "900")

    @pytest.mark.asyncio
    async def test_user_existant_retourne_token(self):
        """User déjà en BD → pas de provisionnement, retourne un JWT."""
        data = make_cas_data(role="enseignant")
        mock_user = MagicMock()
        mock_user.email = data.email
        mock_user.type = "enseignant"
        mock_user.id = 1

        with patch("auth.authenticate_cas.get_user", return_value=mock_user):
            token = await authenticate_cas(data)
            assert token.token_type == "bearer"
            assert token.access_token != ""

    @pytest.mark.asyncio
    async def test_premier_login_enseignant(self):
        """Premier login → provisionnement → JWT."""
        data = make_cas_data(role="enseignant")
        mock_user = MagicMock()
        mock_user.email = data.email
        mock_user.type = "enseignant"
        mock_user.id = 1

        with patch("auth.authenticate_cas.get_user", side_effect=[None, mock_user]), \
             patch("auth.authenticate_cas._create_cas_user", return_value=mock_user):
            token = await authenticate_cas(data)
            assert token.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_groupe_non_autorise_leve_403(self):
        """Groupe CAS non reconnu → 403."""
        data = make_cas_data(role="inconnu")

        with patch("auth.authenticate_cas.get_user", return_value=None):
            with pytest.raises(HTTPException) as exc:
                await authenticate_cas(data)
            assert exc.value.status_code == 403

    @pytest.mark.asyncio
    async def test_echec_provisionnement_leve_500(self):
        """Provisionnement échoue (DB KO) → 500."""
        data = make_cas_data(role="enseignant")

        with patch("auth.authenticate_cas.get_user", return_value=None), \
             patch("auth.authenticate_cas._create_cas_user", return_value=None):
            with pytest.raises(HTTPException) as exc:
                await authenticate_cas(data)
            assert exc.value.status_code == 500