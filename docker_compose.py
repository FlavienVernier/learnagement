import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

import dotenv

TRAEFIK_MODES = ("none", "local", "domain")
TRAEFIK_SERVICE = "reverse_proxy_traefik"
SOCKET_PROXY = "socket_proxy_tecnativa"

########################################
# Configuration (lue une seule fois)
########################################

@dataclass(frozen=True)
class ComposeConfig:
    instance: str
    env: str
    mode: str          # none | local | domain
    traefik: bool      # Traefik effectivement présent dans le compose
    traefik_api_port: str
    domain: str
    acme_email: str
    acme_staging: bool
    pma_basicauth: str
    pma_port: str
    pma_docker_port: str
    backend_port: str
    backend_docker_port: str
    instance_protocol: str
    ssl_internal_dir: str
    docker_ssl_internal_dir: str
    ssl_external_dir: str
    docker_ssl_external_dir: str
    php_port: str
    php_docker_port: str
    php_protocol: str
    nextauth_port: str
    nextauth_docker_port: str
    dash_port: str
    dash_docker_port: str

    @classmethod
    def from_env(cls, containers: list) -> "ComposeConfig":
        envs = os.getenv
        env = envs("ENV", "dev")
        # Par défaut : dev -> pas de Traefik, sinon prod en test local
        mode = (envs("TRAEFIK_MODE") or ("none" if env == "dev" else "local")).strip().lower()

        if mode != "none" and TRAEFIK_SERVICE not in containers:
            logging.warning(f"TRAEFIK_MODE={mode} mais '{TRAEFIK_SERVICE}' absent de la liste des conteneurs : mode 'none' appliqué")

        if envs("ACME_STAGING") and envs("TRAEFIK_MODE") == "domain":
            logging.warning(f"TRAEFIK_MODE={mode} and ACME_STAGING={envs('ACME_STAGING')}")

        cfg = cls(
            instance=envs("INSTANCE_NAME"),
            env=env,
            mode=mode,
            traefik=(mode != "none" and TRAEFIK_SERVICE in containers),
            traefik_api_port=envs("TRAEFIK_API_PORT", 8080),
            domain=envs("DOMAIN", "localhost"),
            acme_email=envs("ACME_EMAIL", ""),
            acme_staging=envs("ACME_STAGING", "false").strip().lower() in ("1", "true", "yes", "on"),
            pma_basicauth=envs("PMA_BASICAUTH", ""),
            pma_port=envs("PHPMYADMIN_PORT"),
            pma_docker_port=envs("PHPMYADMIN_DOCKER_PORT"),
            backend_port=envs("BACKEND_PYTHON_PORT"),
            backend_docker_port=envs("BACKEND_PYTHON_DOCKER_PORT"),
            instance_protocol=envs("INSTANCE_PROTOCOL"),
            ssl_internal_dir=envs("SSL_INTERNAL_DIR"),
            docker_ssl_internal_dir=envs("DOCKER_SSL_INTERNAL_DIR"),
            ssl_external_dir=envs("SSL_EXTERNAL_DIR"),
            docker_ssl_external_dir=envs("DOCKER_SSL_EXTERNAL_DIR"),
            php_port=envs("FRONT_PHP_PORT"),
            php_docker_port=envs("FRONT_PHP_DOCKER_PORT"),
            php_protocol=envs("FRONT_PHP_PROTOCOL"),
            nextauth_port=envs("FRONT_NEXTAUTH_PORT"),
            nextauth_docker_port=envs("FRONT_NEXTAUTH_DOCKER_PORT"),
            dash_port=envs("FRONT_DASH_PORT"),
            dash_docker_port=envs("FRONT_DASH_DOCKER_PORT"),
        )
        cfg.validate(containers)
        return cfg

    def validate(self, containers: list) -> None:
        if self.mode not in TRAEFIK_MODES:
            raise ValueError(f"TRAEFIK_MODE='{self.mode}' invalide, valeurs possibles : {TRAEFIK_MODES}")
        if self.mode == "domain":
            if self.domain in ("", "localhost") or self.domain.endswith(".localhost"):
                raise ValueError("TRAEFIK_MODE=domain nécessite un vrai DOMAIN (pas localhost)")
            if not self.acme_email:
                raise ValueError("TRAEFIK_MODE=domain nécessite ACME_EMAIL")
        if self.traefik and "phpmyadmin" in containers and not self.pma_basicauth:
            raise ValueError("PMA_BASICAUTH est requis quand Traefik protège phpMyAdmin")


########################################
# Helpers de génération YAML
########################################

def _svc(*lines: str) -> str:
    """Assemble les lignes d'un service en ignorant les blocs vides."""
    return "\n" + "\n".join(l for l in lines if l) + "\n"


def _list(items: list, indent: int = 12) -> str:
    pad = " " * indent
    return "\n".join(f'{pad}- "{item}"' for item in items)


def _block(key: str, items: list) -> str:
    """'        key:' suivi de la liste, ou chaîne vide si la liste est vide."""
    return f"        {key}:\n{_list(items)}" if items else ""


def _networks(cfg: ComposeConfig, *names: str) -> str:
    return _block("networks", [f"learnagement_{n}_{cfg.instance}" for n in names])


def _environment(cfg: ComposeConfig, *extra: str) -> str:
    return _block("environment", [f"INSTANCE_NAME={cfg.instance}", f"ENV={cfg.env}", *extra])


def _ssl_volumes(cfg: ComposeConfig, internal=True, external=True) -> list:
    vols = []
    if internal:
        vols.append(f"../{cfg.ssl_internal_dir}:{cfg.docker_ssl_internal_dir}:ro")
    if external:
        vols.append(f"../{cfg.ssl_external_dir}:{cfg.docker_ssl_external_dir}:ro")
    return vols


def _healthcheck(test: list, start_period: str | None = None, retries: int = 55) -> str:
    lines = ["        healthcheck:", f"            test: {json.dumps(test)}"]
    if start_period:
        lines.append(f"            start_period: {start_period}")
    lines += ["            interval: 5s", "            timeout: 5s", f"            retries: {retries}"]
    return "\n".join(lines)


def _depends_on(cfg: ComposeConfig, *services: str, traefik: bool = False) -> str:
    deps = []
    if traefik and cfg.traefik:
        deps.append(f"{TRAEFIK_SERVICE}_{cfg.instance}")
    deps += [f"{s}_{cfg.instance}" for s in services]
    if not deps:
        return ""
    body = "\n".join(f"            {d}:\n                condition: service_healthy" for d in deps)
    return "        depends_on:\n" + body


def _ports(cfg: ComposeConfig, mapping: str, only_without_traefik: bool = False) -> str:
    """Publie un port. Si only_without_traefik, le service n'est joignable que via Traefik quand il est actif."""
    if only_without_traefik and cfg.traefik:
        return ""
    return _block("ports", [mapping])


def _traefik_labels(cfg: ComposeConfig, name: str, subdomain: str, port: str,
                    scheme: str, auth: bool = False) -> str:
    if not cfg.traefik:
        return ""
    router = f"{name}_{cfg.instance}"
    labels = [
        "traefik.enable=true",
        f"traefik.http.routers.{router}.rule=Host(`{subdomain}.{cfg.domain}`)",
        f"traefik.http.routers.{router}.entrypoints=websecure",
        f"traefik.http.routers.{router}.tls=true",
        f"traefik.http.services.{router}.loadbalancer.server.port={port}",
        f"traefik.http.services.{router}.loadbalancer.server.scheme={scheme}",
    ]
    if scheme == "https":
        # certificat interne du conteneur : défini dans traefik/dynamic.yml
        labels.append(f"traefik.http.services.{router}.loadbalancer.serversTransport=insecure@file")
    if cfg.mode == "domain":
        labels.append(f"traefik.http.routers.{router}.tls.certresolver=myresolver")
    if auth:
        mw = f"auth_{cfg.instance}"
        labels.append(f"traefik.http.routers.{router}.middlewares={mw}")
        labels.append(f"traefik.http.middlewares.{mw}.basicauth.users=${{PMA_BASICAUTH}}")
    return _block("labels", labels)


def _traefik_command(cfg: ComposeConfig) -> list:
    cmd = [
        "--ping=true",
        "--api.insecure=true",
        "--entrypoints.traefik.address=:8080",
        "--providers.docker=true",
        f"--providers.docker.endpoint=tcp://socket_proxy_{cfg.instance}:2375",
        "--providers.docker.exposedbydefault=false",
        "--providers.file.directory=/etc/traefik/dynamic",
        "--providers.file.watch=true",
        "--entrypoints.web.address=:80",
        "--entrypoints.websecure.address=:443",
        "--entrypoints.web.http.redirections.entrypoint.to=websecure",
        "--entrypoints.web.http.redirections.entrypoint.scheme=https",
    ]
    if cfg.mode == "domain":
        cmd += [
            f"--certificatesresolvers.myresolver.acme.email={cfg.acme_email}",
            "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json",
            "--certificatesresolvers.myresolver.acme.httpchallenge.entrypoint=web",
        ]
        if cfg.acme_staging:
            cmd.append("--certificatesresolvers.myresolver.acme.caserver="
                       "https://acme-staging-v02.api.letsencrypt.org/directory")
    return cmd


########################################
# Générateurs : un par partie du compose
########################################

def _gen_head(cfg: ComposeConfig) -> str:
    return _svc(
        "# NEVER EDIT THIS FILE, IT IS SELF GENERATED",
        "",
        "services:",
        "",
    )

# --- socket proxy :
def _gen_socket_proxy_tecnativa(cfg: ComposeConfig) -> str:
    image = getattr(cfg, "socket_proxy_image", "tecnativa/docker-socket-proxy:latest")
    swarm = getattr(cfg, "swarm", False)

    envs = ["CONTAINERS=1"]                      # KEY=value, pas "KEY: value"
    if swarm:
        envs += ["SERVICES=1", "TASKS=1", "NETWORKS=1", "SWARM=1"]
    envs += ["POST=0"]

    return _svc(
        f"    socket_proxy_{cfg.instance}:",
        f"        image: {image}",
        f"        container_name: socket_proxy_tecnativa_{cfg.instance}",
        "        restart: unless-stopped",
        _block("environment", envs),
        "        volumes:",
        "            - /var/run/docker.sock:/var/run/docker.sock:ro",
        _networks(cfg, "socket_proxy"),
        "        read_only: true",
        "        tmpfs:",
        "            - /run",
        "            - /tmp",
        "        security_opt:",
        "            - no-new-privileges:true",
        # /_ping est autorisé par défaut par le proxy ; wget est fourni par busybox (alpine) mais gène du bruit dans les logs
        _healthcheck(["CMD", "wget", "-q", "--spider", "http://127.0.0.1:2375/_ping"], retries=20),
        #_healthcheck(["CMD", "nc", "-z", "127.0.0.1", "2375"], retries=20),
    )

# --- Traefik :
def _gen_reverse_proxy_traefik(cfg: ComposeConfig) -> str:
    volumes = ["./traefik:/etc/traefik/dynamic:ro"]      # docker.sock retiré
    if cfg.mode == "domain":
        volumes.append("./letsencrypt:/letsencrypt")
    if cfg.mode == "local":
        volumes.append("../certs/traefik:/certs:ro")
    return _svc(
        f"    {TRAEFIK_SERVICE}_{cfg.instance}:",
        "        image: traefik:v3.7",
        f"        container_name: learnagement_{TRAEFIK_SERVICE}_{cfg.instance}",
        _block("command", _traefik_command(cfg)),
        _block("ports", ["80:80", "443:443", f"127.0.0.1:{cfg.traefik_api_port}:8080"]),
        _block("volumes", volumes),
        _networks(cfg, "front", "back", "socket_proxy"),
        "        restart: unless-stopped",
        _depends_on(cfg, "socket_proxy"),               # ni traefik=True, ni data_mysql
        _healthcheck(["CMD", "traefik", "healthcheck", "--ping"], retries=20),
    )


def _gen_data_mysql(cfg: ComposeConfig) -> str:
    return _svc(
        f"    data_mysql_{cfg.instance}:",
        f"        container_name: learnagement_data_mysql_{cfg.instance}",
        "        image: mysql:8.4",
        "        restart: always",
        _networks(cfg, "back"),
        "        # NEVER SET PORTS FOR DB",
        "        command: --mysql-native-password=ON",
        _block("environment", [
            "MYSQL_DATABASE=${MYSQL_DB}",
            "MYSQL_USER=${MYSQL_USER_LOGIN}",
            "MYSQL_PASSWORD=${MYSQL_USER_PASSWORD}",
            "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}",
        ]),
        _block("volumes", [
            "../db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d",
            "./data_mysql/conf.d:/etc/mysql/conf.d",
            f"learnagement_persistent_db_{cfg.instance}:/var/lib/mysql",
        ]),
        _healthcheck(["CMD", "mysqladmin", "ping", "-h", "127.0.0.1",
                      "-u${MYSQL_USER_LOGIN}", "-p${MYSQL_USER_PASSWORD}"], start_period="5s"),
    )


def _gen_phpmyadmin(cfg: ComposeConfig) -> str:
    return _svc(
        f"    phpmyadmin_{cfg.instance}:",
        f"        container_name: learnagement_phpmyadmin_{cfg.instance}",
        "        image: phpmyadmin",
        "        restart: always",
        _networks(cfg, "back"),
        # sans Traefik (dev) : accessible uniquement depuis la machine locale
        _ports(cfg, f"127.0.0.1:{cfg.pma_port}:{cfg.pma_docker_port}", only_without_traefik=True),
        _block("environment", [
            f"PMA_HOST=data_mysql_{cfg.instance}",
            "RELATIONA_DISPLAY=D",
            f"APACHE_HTTP_PORT_NUMBER={cfg.pma_docker_port}",
        ]),
        _traefik_labels(cfg, "phpmyadmin", "phpmyadmin", cfg.pma_docker_port, "http", auth=True),
        _block("volumes", ["./phpmyadmin/config.user.inc.php:/etc/phpmyadmin/config.user.inc.php:ro"]),
        _depends_on(cfg, "data_mysql", traefik=True),
    )


def _gen_backend_python(cfg: ComposeConfig) -> str:
    return _svc(
        f"    backend_python_{cfg.instance}:",
        f"        container_name: learnagement_backend_python_{cfg.instance}",
        "        build: ./backend_python/",
        '        restart: "no"',
        _networks(cfg, "back", "front"),
        _ports(cfg, f"127.0.0.1:{cfg.backend_port}:{cfg.backend_docker_port}"),
        _environment(cfg),
        _block("volumes", ["../backend_python/:/app/", *_ssl_volumes(cfg, external=False)]),
        _depends_on(cfg, "data_mysql"),
        _healthcheck(["CMD", "curl", "-fk",
                      f"{cfg.instance_protocol}://127.0.0.1:{cfg.backend_docker_port}/health"],
                     start_period="10s"),
    )


def _gen_front_php(cfg: ComposeConfig) -> str:
    return _svc(
        f"    front_php_{cfg.instance}:",
        f"        container_name: learnagement_php_{cfg.instance}",
        "        build: ./front_PHP/",
        "        restart: always",
        _networks(cfg, "front"),
        _ports(cfg, f"{cfg.php_port}:{cfg.php_docker_port}", only_without_traefik=True),
        _traefik_labels(cfg, "front_php", "www", cfg.php_docker_port, cfg.php_protocol),
        _environment(cfg),
        _block("volumes", [
            "../front_PHP:/var/www/html",
            "./log/php:/var/log/apache2",
            "./front_PHP/lnm-php.ini:/usr/local/etc/php/conf.d/lnm-php.ini",
            *_ssl_volumes(cfg),
        ]),
        _depends_on(cfg, "backend_python", traefik=True),
        _healthcheck(["CMD", "curl", "-fk",
                      f"{cfg.php_protocol}://127.0.0.1:{cfg.php_docker_port}/health"],
                     start_period="10s"),
    )


def _gen_front_nextjs(cfg: ComposeConfig) -> str:
    js = (f"fetch('http://127.0.0.1:{cfg.nextauth_docker_port}/health')"
          ".then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))")
    return _svc(
        f"    front_nextjs_{cfg.instance}:",
        f"        container_name: learnagement_nextjs_{cfg.instance}",
        "        build: ./front_NextJS",
        "        restart: always",
        _networks(cfg, "front"),
        _ports(cfg, f"{cfg.nextauth_port}:{cfg.nextauth_docker_port}", only_without_traefik=True),
        _environment(cfg),
        _block("volumes", [
            "../front_NextJS:/app/",
            "../front_NextJS/node_modules:/app/node_modules",
            *_ssl_volumes(cfg),
        ]),
        _depends_on(cfg, "backend_python"),
        _healthcheck(["CMD", "node", "-e", js], start_period="30s"),
    )


def _gen_front_dashplotly(cfg: ComposeConfig) -> str:
    return _svc(
        f"    front_dashplotly_{cfg.instance}:",
        f"        container_name: learnagement_python_web_server_{cfg.instance}",
        "        build: ./front_DashPlotly/",
        "        restart: always",
        _networks(cfg, "front"),
        _ports(cfg, f"{cfg.dash_port}:{cfg.dash_docker_port}", only_without_traefik=True),
        _environment(cfg),
        _block("volumes", [
            "../front_DashPlotly/:/app/",
            "../front_DashPlotly/data/:/data/",
            *_ssl_volumes(cfg),
        ]),
        _depends_on(cfg, "backend_python"),
        _healthcheck(["CMD", "curl", "-fk",
                      f"{cfg.php_protocol}://127.0.0.1:{cfg.dash_docker_port}/health"],
                     start_period="10s"),
    )


def _gen_volumes(cfg: ComposeConfig) -> str:
    return f"\nvolumes:\n    learnagement_persistent_db_{cfg.instance}:\n"


def _gen_networks(cfg: ComposeConfig) -> str:
    return f"""
networks:
    learnagement_socket_proxy_{cfg.instance}:
        internal: true
    # network to access to fronts (only fronts and backends on this network)
    learnagement_front_{cfg.instance}:
        name: learnagement_front_{cfg.instance}
        driver: bridge
    # network to access to back (only backends and data storages on this network)
    learnagement_back_{cfg.instance}:
        name: learnagement_back_{cfg.instance}
        driver: bridge
"""


# Chaque clé est la fonction génératrice (cfg -> texte) de sa partie du compose
docker_compose_parts = {
    "head":                   _gen_head,
    "socket_proxy_tecnativa": _gen_socket_proxy_tecnativa,
    "reverse_proxy_traefik":  _gen_reverse_proxy_traefik,
    "data_mysql":             _gen_data_mysql,
    "phpmyadmin":             _gen_phpmyadmin,
    "backend_python":         _gen_backend_python,
    "front_php":              _gen_front_php,
    "front_nextjs":           _gen_front_nextjs,
    "front_dashplotly":       _gen_front_dashplotly,
    "volumes":                _gen_volumes,
    "networks":               _gen_networks,
}


########################################
# Fichiers annexes de Traefik
########################################

def _prepare_traefik_files(cfg: ComposeConfig, compose_dir: Path) -> None:
    (compose_dir / "traefik").mkdir(parents=True, exist_ok=True)
    if cfg.mode == "domain":
        (compose_dir / "letsencrypt").mkdir(parents=True, exist_ok=True)
    if cfg.mode == "local":
        Path("certs/traefik").mkdir(parents=True, exist_ok=True)

    content = (
        "http:\n"
        "  serversTransports:\n"
        "    insecure:\n"
        "      insecureSkipVerify: true\n"
    )
    # Certificat de confiance généré avec mkcert (sinon Traefik sert son certificat auto-signé)
    if cfg.mode == "local" and Path("certs/traefik/local.pem").exists() \
            and Path("certs/traefik/local-key.pem").exists():
        content += (
            "tls:\n"
            "  certificates:\n"
            "    - certFile: /certs/local.pem\n"
            "      keyFile: /certs/local-key.pem\n"
        )
    (compose_dir / "traefik" / "dynamic.yml").write_text(content, encoding="utf-8")


########################################
# Point d'entrée
########################################

def gen_docker_compose_yml(containers: list):
    dotenv.load_dotenv()
    cfg = ComposeConfig.from_env(containers)

    unknown = [c for c in containers if c not in docker_compose_parts]
    if unknown:
        raise ValueError(f"Conteneurs inconnus : {unknown}")

    # Pas de Traefik ni tecnativa en mode 'none'
    selected = [c for c in containers if c not in (TRAEFIK_SERVICE, SOCKET_PROXY)]
    if cfg.traefik:
        selected = [SOCKET_PROXY, TRAEFIK_SERVICE] + selected

    compose_dir = Path("docker")   # plus de os.chdir : le script ne dépend plus du dossier courant
    parts = [
        docker_compose_parts["head"](cfg),
        *(docker_compose_parts[c](cfg) for c in selected),
        docker_compose_parts["volumes"](cfg),
        docker_compose_parts["networks"](cfg),
    ]

    if cfg.traefik:
        _prepare_traefik_files(cfg, compose_dir)

    (compose_dir / "docker-compose.yml").write_text("".join(parts), encoding="utf-8")
    logging.info(f"docker-compose.yml généré (env={cfg.env}, traefik_mode={cfg.mode}, traefik={cfg.traefik})")

