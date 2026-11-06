import os
import dotenv
import logging
import asyncio

def gen_docker_compose_yml(containers: list):
    dotenv.load_dotenv()
    try:
        INSTANCE_NAME = os.getenv("INSTANCE_NAME")
        MYSQL_DB = os.getenv("MYSQL_DB")
        MYSQL_USER_LOGIN =  os.getenv("MYSQL_USER_LOGIN")
        MYSQL_USER_PASSWORD = os.getenv("MYSQL_USER_PASSWORD")
        MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
        PHPMYADMIN_PORT = os.getenv("PHPMYADMIN_PORT")
        PHPMYADMIN_DOCKER_PORT = os.getenv("PHPMYADMIN_DOCKER_PORT")
        BACKEND_PYTHON_PORT = os.getenv("BACKEND_PYTHON_PORT")
        BACKEND_PYTHON_DOCKER_PORT = os.getenv("BACKEND_PYTHON_DOCKER_PORT")
        ENV = os.getenv("ENV")
        SSL_INTERNAL_DIR = os.getenv("SSL_INTERNAL_DIR")
        DOCKER_SSL_INTERNAL_DIR = os.getenv("DOCKER_SSL_INTERNAL_DIR")
        INSTANCE_PROTOCOL = os.getenv("INSTANCE_PROTOCOL")
        FRONT_PHP_PORT = os.getenv("FRONT_PHP_PORT")
        FRONT_PHP_DOCKER_PORT = os.getenv("FRONT_PHP_DOCKER_PORT")
        FRONT_PHP_PROTOCOL = os.getenv("FRONT_PHP_PROTOCOL")
        SSL_EXTERNAL_DIR = os.getenv("SSL_EXTERNAL_DIR")
        DOCKER_SSL_EXTERNAL_DIR = os.getenv("DOCKER_SSL_EXTERNAL_DIR")
        FRONT_NEXTAUTH_PORT = os.getenv("FRONT_NEXTAUTH_PORT")
        FRONT_NEXTAUTH_DOCKER_PORT = os.getenv("FRONT_NEXTAUTH_DOCKER_PORT")
        FRONT_DASH_PORT = os.getenv("FRONT_DASH_PORT")
        FRONT_DASH_DOCKER_PORT = os.getenv("FRONT_DASH_DOCKER_PORT")
    except Exception as e:
        logging.error(e)

    docker_compose_parts = {
    "head": """
services:
    """,
    "data_mysql": f"""
    data_mysql_{INSTANCE_NAME}:
        container_name: learnagement_data_mysql_{INSTANCE_NAME}
        image: mysql:8.4
        restart: always
        networks:
            - learnagement_back_{INSTANCE_NAME}
        # ports
            # NEVER SET PORTS FOR DB
        command: --mysql-native-password=ON
        environment:
            - MYSQL_DATABASE={MYSQL_DB}
            - MYSQL_USER={MYSQL_USER_LOGIN}
            - MYSQL_PASSWORD={MYSQL_USER_PASSWORD}
            - MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}
        volumes:
            - ../db/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d
            - ./data_mysql/conf.d:/etc/mysql/conf.d
            - learnagement_persistent_db_{INSTANCE_NAME}:/var/lib/mysql
        healthcheck:
            test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-u$MYSQL_USER_LOGIN", "-p$MYSQL_USER_PASSWORD"]
            start_period: 5s
            interval: 5s
            timeout: 5s
            retries: 55
    """,
    "phpmyadmin": f"""
    phpmyadmin_{INSTANCE_NAME}:
        container_name: learnagement_phpmyadmin_{INSTANCE_NAME}
        image: phpmyadmin
        restart: always
        networks:
            - learnagement_back_{INSTANCE_NAME}
        ports:
            - {PHPMYADMIN_PORT}:{PHPMYADMIN_DOCKER_PORT}
        environment:
            - PMA_HOST=data_mysql_{INSTANCE_NAME}
            - RELATIONA_DISPLAY=D
            - APACHE_HTTP_PORT_NUMBER={PHPMYADMIN_DOCKER_PORT}
        volumes:
            - ./phpmyadmin/config.user.inc.php:/etc/phpmyadmin/config.user.inc.php:ro
        depends_on:
            data_mysql_{INSTANCE_NAME}:
                condition: service_healthy
    """,
    "backend_python": f"""
    backend_python_{INSTANCE_NAME}:
        container_name: learnagement_backend_python_{INSTANCE_NAME}
        build: ./backend_python/
        restart: no
        networks:
            - learnagement_back_{INSTANCE_NAME}
            - learnagement_front_{INSTANCE_NAME}
        ports:
            - {BACKEND_PYTHON_PORT}:{BACKEND_PYTHON_DOCKER_PORT}
        environment:
            - INSTANCE_NAME={INSTANCE_NAME}
            - ENV={ENV}
        volumes:
            - ../backend_python/:/app/
            - ../{SSL_INTERNAL_DIR}:{DOCKER_SSL_INTERNAL_DIR}:ro
        depends_on:
            data_mysql_{INSTANCE_NAME}:
                condition: service_healthy
        healthcheck:
            test: ["CMD", "curl", "-fk", "{INSTANCE_PROTOCOL}://127.0.0.1:{BACKEND_PYTHON_DOCKER_PORT}/health"]
            start_period: 10s
            interval: 5s
            timeout: 5s
            retries: 55
    """,
    "front_php": f"""
    front_php_{INSTANCE_NAME}:
        container_name: learnagement_php_{INSTANCE_NAME}
        build: ./front_PHP/
        restart: always
        networks:
              - learnagement_front_{INSTANCE_NAME}
        ports:
            - "{FRONT_PHP_PORT}:{FRONT_PHP_DOCKER_PORT}"
        environment:
            - INSTANCE_NAME={INSTANCE_NAME}
            - ENV={ENV}
        volumes:
            - ../front_PHP:/var/www/html
            - ./log/php:/var/log/apache2
            - ./front_PHP/lnm-php.ini:/usr/local/etc/php/conf.d/lnm-php.ini
            - ../{SSL_INTERNAL_DIR}:{DOCKER_SSL_INTERNAL_DIR}:ro
            - ../{SSL_EXTERNAL_DIR}:{DOCKER_SSL_EXTERNAL_DIR}:ro
        depends_on:
            backend_python_{INSTANCE_NAME}:
                condition: service_healthy
        healthcheck:
            test: ["CMD", "curl", "-fk", "{FRONT_PHP_PROTOCOL}://127.0.0.1:{FRONT_PHP_DOCKER_PORT}/health"]
            start_period: 10s
            interval: 5s
            timeout: 5s
            retries: 55
    """,
    "front_nextjs": f"""
    front_nextjs_{INSTANCE_NAME}:
        container_name: learnagement_nextjs_{INSTANCE_NAME}
        build: ./front_NextJS
        restart: always
        networks:
              - learnagement_front_{INSTANCE_NAME}
        ports:
            - "{FRONT_NEXTAUTH_PORT}:{FRONT_NEXTAUTH_DOCKER_PORT}"
        environment:
            - INSTANCE_NAME={INSTANCE_NAME}
            - ENV={ENV}
        volumes:
            - ../front_NextJS:/app
            - ../front_NextJS/node_modules:/app/node_modules
            - ../{SSL_INTERNAL_DIR}:{DOCKER_SSL_INTERNAL_DIR}:ro
            - ../{SSL_EXTERNAL_DIR}:{DOCKER_SSL_EXTERNAL_DIR}:ro
        depends_on:
            backend_python_{INSTANCE_NAME}:
                condition: service_healthy
        healthcheck:
            test: ["CMD", "node", "-e", "fetch('http://127.0.0.1:{FRONT_NEXTAUTH_DOCKER_PORT}/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
            start_period: 30s
            interval: 5s
            timeout: 5s
            retries: 55
    """,
    "front_dashplotly": f"""
    front_dashplotly_{INSTANCE_NAME}:
        container_name: learnagement_python_web_server_{INSTANCE_NAME}
        build: ./front_DashPlotly/
        restart: always
        networks:
              - learnagement_front_{INSTANCE_NAME}
        ports:
            - "{FRONT_DASH_PORT}:{FRONT_DASH_DOCKER_PORT}"
        environment:
            - INSTANCE_NAME={INSTANCE_NAME}
            - ENV={ENV}
        volumes:
            - ../front_DashPlotly/:/app/
            - ../front_DashPlotly/data/:/data/
            - ../{SSL_INTERNAL_DIR}:{DOCKER_SSL_INTERNAL_DIR}:ro
            - ../{SSL_EXTERNAL_DIR}:{DOCKER_SSL_EXTERNAL_DIR}:ro
        depends_on:
            backend_python_{INSTANCE_NAME}:
                condition: service_healthy
        healthcheck:
            test: ["CMD", "curl", "-fk", "{FRONT_PHP_PROTOCOL}://127.0.0.1:{FRONT_DASH_DOCKER_PORT}/health"]
            start_period: 10s
            interval: 5s
            timeout: 5s
            retries: 55
    """,
    "volumes": f"""
volumes:
    learnagement_persistent_db_{INSTANCE_NAME}:
    """,
    "networks": f"""
networks:
    # network to access to fronts (only fronts and backends on this network)
    learnagement_front_{INSTANCE_NAME}:
        name: learnagement_front_{INSTANCE_NAME}
        driver: bridge
    # network to access to back (only backends and data storages on this network)
    learnagement_back_{INSTANCE_NAME}:
        name: learnagement_back_{INSTANCE_NAME}
        driver: bridge
    
    """,
    }
    os.chdir("docker")

    docker_compose_file = "docker-compose.yml"
    with open(docker_compose_file, 'w') as file:
        file.write(docker_compose_parts["head"])
        for container in containers:
            file.write(docker_compose_parts[container])
        file.write(docker_compose_parts["volumes"])
        file.write(docker_compose_parts["networks"])

    os.chdir("..")

import json

async def __wait_for_all_dockers_ready__(timeout: int = 60, poll_interval: int = 3):
    """Attend que tous les conteneurs du projet soient 'running' (et 'healthy' s'ils ont un healthcheck)."""
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
        #logging.info(containers_state)
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
