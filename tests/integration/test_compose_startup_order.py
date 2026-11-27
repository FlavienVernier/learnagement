"""Check generated Compose services, health dependencies, ports, and mounts."""

import sys
from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))
try:
    import docker_compose
finally:
    sys.path.remove(str(REPOSITORY_ROOT))


def test_generated_compose_waits_for_mysql_and_backend_health(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docker").mkdir()
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")

    environment = {
        "INSTANCE_NAME": "ci-order",
        "MYSQL_DB": "repro_only",
        "MYSQL_USER_LOGIN": "repro_only",
        "MYSQL_USER_PASSWORD": "REPRO_ONLY",
        "MYSQL_ROOT_PASSWORD": "REPRO_ONLY",
        "PHPMYADMIN_PORT": "48080",
        "PHPMYADMIN_DOCKER_PORT": "80",
        "BACKEND_PYTHON_PORT": "44000",
        "BACKEND_PYTHON_DOCKER_PORT": "4000",
        "ENV": "dev",
        "SSL_INTERNAL_DIR": "certs/internal",
        "DOCKER_SSL_INTERNAL_DIR": "/certs/internal",
        "INSTANCE_PROTOCOL": "http",
        "FRONT_PHP_PORT": "40080",
        "FRONT_PHP_DOCKER_PORT": "80",
        "FRONT_PHP_PROTOCOL": "http",
        "SSL_EXTERNAL_DIR": "certs/external",
        "DOCKER_SSL_EXTERNAL_DIR": "/certs/external",
        "FRONT_NEXTAUTH_PORT": "43000",
        "FRONT_NEXTAUTH_DOCKER_PORT": "3000",
        "FRONT_DASH_PORT": "48050",
        "FRONT_DASH_DOCKER_PORT": "8050",
    }
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    docker_compose.gen_docker_compose_yml(
        [
            "data_mysql",
            "phpmyadmin",
            "backend_python",
            "front_php",
            "front_nextjs",
            "front_dashplotly",
        ]
    )

    compose_path = tmp_path / "docker" / "docker-compose.yml"
    compose = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    services = compose["services"]
    mysql = "data_mysql_ci-order"
    backend = "backend_python_ci-order"
    phpmyadmin = "phpmyadmin_ci-order"

    assert services[mysql]["container_name"] == "learnagement_data_mysql_ci-order"
    assert services[mysql]["volumes"][0] == (
        "../db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d:ro"
    )
    assert "ports" not in services[mysql]
    assert "learnagement_back_ci-order" in services[mysql]["networks"]
    assert "learnagement_persistent_db_ci-order" in compose["volumes"]
    assert services[backend]["depends_on"][mysql]["condition"] == "service_healthy"
    assert (REPOSITORY_ROOT / "docker" / "phpmyadmin" / "config.inc.php").is_file()
    assert services[phpmyadmin]["volumes"] == [
        "./phpmyadmin/config.inc.php:/etc/phpmyadmin/config.inc.php:ro"
    ]
    for frontend in ("front_php", "front_nextjs", "front_dashplotly"):
        service = f"{frontend}_ci-order"
        assert services[service]["depends_on"][backend]["condition"] == "service_healthy"

    docker_compose.gen_docker_compose_yml(["data_mysql"])
    mysql_compose = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    assert set(mysql_compose["services"]) == {mysql}

    docker_compose.gen_docker_compose_yml(["data_mysql", "backend_python"])
    core_compose = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    assert set(core_compose["services"]) == {mysql, backend}
