import asyncio
import json
import logging
import os
import re
import urllib.request
import urllib.error


def _http_get(url: str, timeout: float = 2.0) -> tuple[int, str] | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        return None


def __traefik_api_url() -> str:
    port = os.environ.get("TRAEFIK_API_PORT", "8080")
    return f"http://127.0.0.1:{port}"


def __is_traefik_up() -> bool:
    """Healthcheck Traefik via /ping (renvoie 200 'OK')."""
    res = _http_get(f"{__traefik_api_url()}/ping")
    return res is not None and res[0] == 200


_HOST_RE = re.compile(r"Host\(\s*((?:`[^`]+`\s*,?\s*)+)\)")


def __extract_hosts(rule: str) -> list[str]:
    """Extrait les hôtes d'une règle : Host(`a.fr`) || Host(`b.fr`, `c.fr`)"""
    hosts = []
    for group in _HOST_RE.findall(rule):
        hosts += re.findall(r"`([^`]+)`", group)
    return hosts


def __get_traefik_urls() -> list[str]:
    """Interroge l'API Traefik et retourne les URLs publiées par les routers actifs."""
    res = _http_get(f"{__traefik_api_url()}/api/http/routers")
    if res is None or res[0] != 200:
        return []
    try:
        routers = json.loads(res[1])
    except json.JSONDecodeError:
        return []

    urls = set()
    for r in routers:
        # on ignore les routers internes (api@internal, dashboard@internal, ping@internal)
        if r.get("provider") == "internal" or r.get("status") != "enabled":
            continue
        tls = "tls" in r
        scheme = "https" if tls else "http"
        for host in __extract_hosts(r.get("rule", "")):
            urls.add(f"{scheme}://{host}")
    return sorted(urls)


# __wait_for_all_dockers_ready__ et __wait_for_mysql_healthy__ : inchangées


async def __wait_for_all_dockers_ready__():
    """Attend que tous les conteneurs du projet soient 'running' (et 'healthy' s'ils ont un healthcheck)."""
    timeout: int = int(os.environ["DOCKER_STARTING_TIMEOUT"])
    poll_interval: int = 3
    cmd = os.environ["DOCKER_COMPOSE_COMMAND"].split(" ") + [
        "-p", os.environ["COMPOSE_PROJECT_NAME"], "ps", "--all", "--format", "json"
    ]
    elapsed = 0
    while elapsed < timeout:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()

        containers_state = []
        for line in stdout.decode().splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            containers_state.extend(data if isinstance(data, list) else [data])

        def ok(c):
            if c.get("State") == "exited" and c.get("ExitCode") == 0:
                return True  # conteneur ponctuel terminé normalement
            return c.get("State") == "running" and c.get("Health", "") in ("", "healthy")

        if containers_state and all(ok(c) for c in containers_state):
            return True

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"Tous les conteneurs ne sont pas prêts après {timeout}s")


async def __wait_for_mysql_healthy__(container_name: str, timeout: int = 300, poll_interval: int = 2):
    """Attend que le conteneur MySQL soit 'healthy' selon son healthcheck Docker."""
    elapsed = 0
    while elapsed < timeout:
        cmd = os.environ["DOCKER_COMMAND"].split(" ") + [
            "inspect", "--format={{.State.Health.Status}}", container_name
        ]
        # result = subprocess.run(cmd, capture_output=True, text=True)
        # status = result.stdout.strip()
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            #text=True
        )
        stdout, _ = await proc.communicate()
        #status = stdout.strip()
        status = stdout.decode().strip()
        logging.info(f"{container_name} health: {status!r}")

        if status == "healthy":
            return True
        elif status == "unhealthy":
            raise RuntimeError(f"Le conteneur {container_name} est en état 'unhealthy'")

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"Timeout : {container_name} n'est pas devenu 'healthy' après {timeout}s")
