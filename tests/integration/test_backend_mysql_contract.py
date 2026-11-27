import importlib
import sys
import warnings
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend_python"


@pytest.fixture
def backend_connection(monkeypatch):
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    if not hasattr(warnings, "deprecated"):
        monkeypatch.setattr(
            warnings,
            "deprecated",
            lambda _message=None: lambda value: value,
            raising=False,
        )
    sys.path.insert(0, str(BACKEND_ROOT))
    try:
        sys.modules.pop("db.connection", None)
        sys.modules.pop("db", None)
        module = importlib.import_module("db.connection")
        module._engine = None
        yield module
    finally:
        sys.path.remove(str(BACKEND_ROOT))


def test_mysql_engine_uses_documented_environment_names(
    monkeypatch, backend_connection
):
    environment = {
        "DB_DRIVER": "mysql+mysqlconnector",
        "MYSQL_USER_LOGIN": "contract-user",
        "MYSQL_USER_PASSWORD": "contract-password",
        "MYSQL_SERVER": "learnagement_data_mysql_contract",
        "MYSQL_PORT": "3306",
        "MYSQL_DB": "learnagement_contract",
        "DB_POOL_SIZE": "7",
        "DB_MAX_OVERFLOW": "9",
    }
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    captured = {}

    def fake_create_engine(url, **kwargs):
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(backend_connection, "create_engine", fake_create_engine)

    engine = backend_connection.get_engine()

    assert engine is not None
    assert captured["url"].drivername == "mysql+mysqlconnector"
    assert captured["url"].username == "contract-user"
    assert captured["url"].host == "learnagement_data_mysql_contract"
    assert captured["url"].port == 3306
    assert captured["url"].database == "learnagement_contract"
    assert captured["kwargs"]["pool_size"] == 7
    assert captured["kwargs"]["max_overflow"] == 9
    assert captured["kwargs"]["pool_timeout"] == 10
    assert captured["kwargs"]["pool_pre_ping"] is True
    assert captured["kwargs"]["pool_recycle"] == 1800


@pytest.mark.parametrize(
    "missing_name",
    [
        "MYSQL_SERVER",
        "MYSQL_PORT",
        "MYSQL_DB",
        "MYSQL_USER_LOGIN",
        "MYSQL_USER_PASSWORD",
    ],
)
def test_missing_mysql_configuration_is_not_silently_defaulted(
    monkeypatch, backend_connection, missing_name
):
    values = {
        "DB_DRIVER": "mysql+mysqlconnector",
        "MYSQL_USER_LOGIN": "contract-user",
        "MYSQL_USER_PASSWORD": "contract-password",
        "MYSQL_SERVER": "learnagement_data_mysql_contract",
        "MYSQL_PORT": "3306",
        "MYSQL_DB": "learnagement_contract",
    }
    values.pop(missing_name)

    for name in values:
        monkeypatch.setenv(name, values[name])
    monkeypatch.delenv(missing_name, raising=False)
    if missing_name == "MYSQL_PORT":
        monkeypatch.setattr(
            backend_connection,
            "create_engine",
            lambda _url, **_kwargs: object(),
        )
        with pytest.raises((TypeError, ValueError)):
            backend_connection.get_engine()
    else:
        captured = {}

        def fake_create_engine(url, **kwargs):
            captured["url"] = url
            captured["kwargs"] = kwargs
            return object()

        monkeypatch.setattr(
            backend_connection,
            "create_engine",
            fake_create_engine,
        )
        backend_connection.get_engine()

        url = captured["url"]
        expected_field = {
            "MYSQL_SERVER": "host",
            "MYSQL_DB": "database",
            "MYSQL_USER_LOGIN": "username",
            "MYSQL_USER_PASSWORD": "password",
        }[missing_name]
        assert getattr(url, expected_field) is None


def test_invalid_mysql_port_does_not_connect(
    monkeypatch, backend_connection
):
    monkeypatch.setenv("MYSQL_USER_LOGIN", "contract-user")
    monkeypatch.setenv("MYSQL_USER_PASSWORD", "contract-password")
    monkeypatch.setenv("MYSQL_SERVER", "learnagement_data_mysql_contract")
    monkeypatch.setenv("MYSQL_PORT", "not-a-port")
    monkeypatch.setenv("MYSQL_DB", "learnagement_contract")
    monkeypatch.setattr(
        backend_connection,
        "create_engine",
        lambda _url, **_kwargs: object(),
    )

    with pytest.raises((TypeError, ValueError)):
        backend_connection.get_engine()
