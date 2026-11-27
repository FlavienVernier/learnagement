from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_UIDS = {
    "backend": 10001,
    "front-php": 33,
    "front-nextjs": 1000,
    "front-dash": 10001,
}
IMAGE_CONTRACTS = {
    "backend": ("backend", 4000, "USER 10001:10001", 'CMD ["python", "app.py"]'),
    "front-php": (
        "front-php",
        8080,
        "USER www-data:www-data",
        'CMD ["apache2-foreground"]',
    ),
    "front-nextjs": (
        "front-nextjs",
        3000,
        "USER node",
        'CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]',
    ),
    "front-dash": (
        "front-dash",
        8050,
        "USER 10001:10001",
        'CMD ["gunicorn", "--bind", "0.0.0.0:8050"',
    ),
}
IMAGE_REPOSITORIES = {
    "backend": "learnagement/backend-k8s",
    "front-php": "learnagement/front-php-k8s",
    "front-nextjs": "learnagement/front-nextjs",
    "front-dash": "learnagement/front-dash",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def pod_labels(workload: dict[str, Any]) -> dict[str, str]:
    return workload["spec"]["template"]["metadata"]["labels"]


def policy_allows(
    policy: dict[str, Any], source_name: str, protocol: str, port: int
) -> bool:
    return any(
        any(
            source.get("podSelector", {})
            .get("matchLabels", {})
            .get("app.kubernetes.io/name")
            == source_name
            for source in rule.get("from", [])
        )
        and any(
            allowed.get("protocol") == protocol and allowed.get("port") == port
            for allowed in rule.get("ports", [])
        )
        for rule in policy["spec"].get("ingress", [])
    )


def main() -> None:
    rendered = subprocess.run(
        ["kubectl", "kustomize", "kubernetes/base"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    resources = [item for item in yaml.safe_load_all(rendered.stdout) if item]
    require(len(resources) == 15, f"expected 15 rendered resources, got {len(resources)}")

    by_key = {(item["kind"], item["metadata"]["name"]): item for item in resources}
    require(len(by_key) == len(resources), "duplicate resource kind/name")
    workloads = [
        item for item in resources if item["kind"] in {"Deployment", "StatefulSet"}
    ]

    for service in (item for item in resources if item["kind"] == "Service"):
        selector = service["spec"]["selector"]
        owner = next(
            (
                item
                for item in workloads
                if all(pod_labels(item).get(key) == value for key, value in selector.items())
            ),
            None,
        )
        require(owner is not None, f"{service['metadata']['name']}: no workload matches Service selector")
        containers = owner["spec"]["template"]["spec"]["containers"]
        for service_port in service["spec"]["ports"]:
            target = service_port["targetPort"]
            declared_port = next(
                (
                    port
                    for container in containers
                    for port in container.get("ports", [])
                    if port.get("name") == target or port.get("containerPort") == target
                ),
                None,
            )
            require(
                declared_port is not None,
                f"{service['metadata']['name']}: targetPort {target} is not declared",
            )
            require(
                declared_port.get("protocol", "TCP") == service_port.get("protocol", "TCP"),
                f"{service['metadata']['name']}: Service/container protocol mismatch",
            )

    for workload in workloads:
        pod_spec = workload["spec"]["template"]["spec"]
        for container in pod_spec["containers"]:
            for probe_name in ("startupProbe", "readinessProbe", "livenessProbe"):
                probe = container.get(probe_name)
                if probe and "httpGet" in probe:
                    port = probe["httpGet"]["port"]
                    require(
                        any(
                            declared.get("name") == port
                            or declared.get("containerPort") == port
                            for declared in container.get("ports", [])
                        ),
                        f"{container['name']} {probe_name}: unknown port {port}",
                    )

            expected_uid = EXPECTED_UIDS.get(container["name"])
            if expected_uid is not None:
                security = container.get("securityContext", {})
                require(security.get("runAsNonRoot") is True, f"{container['name']}: runAsNonRoot missing")
                require(
                    security.get("runAsUser") == expected_uid,
                    f"{container['name']}: unexpected runAsUser",
                )
                require(
                    security.get("runAsGroup") == expected_uid,
                    f"{container['name']}: unexpected runAsGroup",
                )
                require(
                    security.get("allowPrivilegeEscalation") is False,
                    f"{container['name']}: privilege escalation is not disabled",
                )
                require(
                    "ALL" in security.get("capabilities", {}).get("drop", []),
                    f"{container['name']}: capabilities are not fully dropped",
                )

        if workload["metadata"]["name"] in EXPECTED_UIDS:
            require(
                pod_spec.get("securityContext", {}).get("seccompProfile", {}).get("type")
                == "RuntimeDefault",
                f"{workload['metadata']['name']}: RuntimeDefault seccomp missing",
            )

    backend = by_key[("Deployment", "backend")]["spec"]["template"]["spec"]["containers"][0]
    readiness = backend["readinessProbe"]
    readiness_command = readiness.get("exec", {}).get("command", [])
    require(readiness_command and readiness_command[0] == "python", "Backend readiness must use its Python TCP check")
    require(
        "MYSQL_SERVER" in readiness_command[-1] and "MYSQL_PORT" in readiness_command[-1],
        "Backend readiness must use configured MySQL host and port",
    )
    require(
        backend["startupProbe"]["httpGet"]["path"] == "/health"
        and backend["livenessProbe"]["httpGet"]["path"] == "/health",
        "Backend startup/liveness must continue to use /health",
    )

    network_config = by_key[("ConfigMap", "learnagement-network-config")]["data"]
    require(
        network_config.get("MYSQL_SERVER") == "mysql"
        and network_config.get("MYSQL_PORT") == "3306",
        "MySQL DNS/port do not match the Service contract",
    )
    require(
        network_config.get("BACKEND_PYTHON_DOCKER_URL") == "backend"
        and network_config.get("BACKEND_PYTHON_DOCKER_PORT") == "4000",
        "Backend DNS/port do not match the Service contract",
    )

    external_refs: set[tuple[str, str]] = set()
    for workload in workloads:
        for container in workload["spec"]["template"]["spec"]["containers"]:
            for variable in container.get("env", []):
                for source_kind in ("secretKeyRef", "configMapKeyRef"):
                    source = variable.get("valueFrom", {}).get(source_kind)
                    if source:
                        external_refs.add(
                            ("Secret" if source_kind == "secretKeyRef" else "ConfigMap", source["name"])
                        )
            for source_kind in ("secretRef", "configMapRef"):
                source = container.get("envFrom", [{}])[0].get(source_kind)
                if source:
                    external_refs.add(
                        ("Secret" if source_kind == "secretRef" else "ConfigMap", source["name"])
                    )
        for volume in workload["spec"]["template"]["spec"].get("volumes", []):
            if "secret" in volume:
                external_refs.add(("Secret", volume["secret"]["secretName"]))

    for policy in (item for item in resources if item["kind"] == "NetworkPolicy"):
        selector = policy["spec"]["podSelector"]["matchLabels"]
        selected_workloads = [
            workload
            for workload in workloads
            if all(pod_labels(workload).get(key) == value for key, value in selector.items())
        ]
        require(
            bool(selected_workloads),
            f"{policy['metadata']['name']}: selector matches no workload",
        )
        selected_ports = {
            port.get("name", port["containerPort"])
            for workload in selected_workloads
            for container in workload["spec"]["template"]["spec"]["containers"]
            for port in container.get("ports", [])
        }
        for rule in policy["spec"].get("ingress", []):
            for allowed_port in rule.get("ports", []):
                port = allowed_port["port"]
                require(
                    port in selected_ports
                    or any(
                        item["containerPort"] == port
                        for workload in selected_workloads
                        for container in workload["spec"]["template"]["spec"]["containers"]
                        for item in container.get("ports", [])
                    ),
                    f"{policy['metadata']['name']}: ingress port {port} is not served by selected workload",
                )
            for source in rule.get("from", []):
                source_selector = source.get("podSelector", {}).get("matchLabels")
                if source_selector is not None:
                    require(
                        any(
                            all(
                                pod_labels(workload).get(key) == value
                                for key, value in source_selector.items()
                            )
                            for workload in workloads
                        ),
                        f"{policy['metadata']['name']}: ingress source matches no workload",
                    )

    mysql_ingress = by_key.get(("NetworkPolicy", "mysql-ingress"))
    backend_ingress = by_key.get(("NetworkPolicy", "backend-ingress"))
    require(mysql_ingress is not None, "MySQL ingress policy is missing")
    require(backend_ingress is not None, "Backend ingress policy is missing")
    require(
        policy_allows(mysql_ingress, "backend", "TCP", 3306),
        "MySQL ingress must allow Backend TCP/3306",
    )
    for frontend in ("front-php", "front-nextjs", "front-dash"):
        require(
            policy_allows(backend_ingress, frontend, "TCP", 4000),
            f"Backend ingress must allow {frontend} TCP/4000",
        )
        require(
            not any(
                frontend
                in policy["spec"].get("podSelector", {})
                .get("matchLabels", {})
                .get("app.kubernetes.io/name", "")
                for policy in resources
                if policy["kind"] == "NetworkPolicy"
                and "Egress" in policy["spec"].get("policyTypes", [])
            ),
            f"{frontend} egress must not be restricted before external endpoints are confirmed",
        )

    backend_egress = by_key.get(("NetworkPolicy", "backend-egress"))
    require(backend_egress is not None, "Backend egress policy is missing")
    require(
        backend_egress["spec"].get("policyTypes") == ["Egress"],
        "Backend egress policy must isolate only egress",
    )
    backend_egress_rules = backend_egress["spec"].get("egress", [])
    mysql_rules = [
        rule
        for rule in backend_egress_rules
        if any(
            source.get("podSelector", {}).get("matchLabels", {}).get("app.kubernetes.io/name")
            == "mysql"
            for source in rule.get("to", [])
        )
    ]
    require(
        any(
            any(port.get("protocol") == "TCP" and port.get("port") == 3306 for port in rule.get("ports", []))
            for rule in mysql_rules
        ),
        "Backend egress must allow TCP/3306 to MySQL",
    )
    dns_ports = {
        (port.get("protocol"), port.get("port"))
        for rule in backend_egress_rules
        if not rule.get("to")
        for port in rule.get("ports", [])
    }
    require(
        {("UDP", 53), ("TCP", 53)} <= dns_ports,
        "Backend egress must allow UDP/TCP DNS",
    )
    require(
        all(
            (
                rule.get("to")
                and all(
                    source.get("podSelector", {}).get("matchLabels", {}).get(
                        "app.kubernetes.io/name"
                    )
                    == "mysql"
                    for source in rule["to"]
                )
                and all(
                    port.get("protocol") == "TCP" and port.get("port") == 3306
                    for port in rule.get("ports", [])
                )
            )
            or (
                not rule.get("to")
                and rule.get("ports")
                and all(
                    port.get("protocol") in {"TCP", "UDP"} and port.get("port") == 53
                    for port in rule["ports"]
                )
            )
            for rule in backend_egress_rules
        ),
        "Backend egress contains a destination or port outside MySQL/DNS",
    )

    local_objects = {(item["kind"], item["metadata"]["name"]) for item in resources}
    require(
        external_refs - local_objects
        == {
            ("Secret", "learnagement-database-credentials"),
            ("Secret", "learnagement-auth-secrets"),
            ("Secret", "learnagement-php-runtime"),
            ("ConfigMap", "learnagement-app-config"),
        },
        "external Secret/ConfigMap references differ from the documented runtime prerequisites",
    )

    for name, repository in IMAGE_REPOSITORIES.items():
        deployment = by_key[("Deployment", name)]
        container = deployment["spec"]["template"]["spec"]["containers"][0]
        require(
            container["image"] == f"{repository}:REPLACE_WITH_BUILT_IMAGE",
            f"{name}: image must remain an explicit pre-release placeholder",
        )
        for probe_name in ("startupProbe", "readinessProbe", "livenessProbe"):
            probe = container.get(probe_name, {}).get("httpGet")
            if probe is not None:
                require(
                    probe.get("path") == "/health",
                    f"{name} {probe_name}: expected the application /health endpoint",
                )
    require(not any(item["kind"] == "Secret" for item in resources), "secret data must remain external")
    for name in ("backend", "front-php", "front-nextjs", "front-dash"):
        require(
            by_key[("Deployment", name)]["spec"].get("strategy", {}).get("type") == "Recreate",
            f"{name}: rollout strategy changed without an approved availability gate",
        )
        dockerfile_name, port, user_line, command_prefix = IMAGE_CONTRACTS[name]
        dockerfile = ROOT / "docker" / "kubernetes" / dockerfile_name / "Dockerfile"
        require(dockerfile.is_file(), f"{name}: Kubernetes Dockerfile is missing")
        dockerfile_lines = [line.strip() for line in dockerfile.read_text(encoding="utf-8").splitlines()]
        require(f"EXPOSE {port}" in dockerfile_lines, f"{name}: Dockerfile EXPOSE does not match the manifest")
        require(user_line in dockerfile_lines, f"{name}: Dockerfile runtime user changed")
        require(
            any(line.startswith(command_prefix) for line in dockerfile_lines),
            f"{name}: Dockerfile startup command changed",
        )
        if name == "front-php":
            dockerfile_text = "\n".join(dockerfile_lines)
            require(
                "docker-php-ext-install" in dockerfile_text
                and all(
                    extension in dockerfile_text
                    for extension in ("curl", "dom", "mysqli", "simplexml")
                ),
                "front-php: Dockerfile must install the Composer/runtime PHP extensions",
            )
        container = by_key[("Deployment", name)]["spec"]["template"]["spec"]["containers"][0]
        require(
            any(item["containerPort"] == port for item in container.get("ports", [])),
            f"{name}: container port does not match Dockerfile EXPOSE",
        )
    require(
        by_key[("StatefulSet", "mysql")]["spec"].get("updateStrategy", {}).get("type")
        == "OnDelete",
        "MySQL update strategy must remain explicitly controlled",
    )
    next_ignore = ROOT / "docker" / "kubernetes" / "front-nextjs" / "Dockerfile.dockerignore"
    next_ignore_lines = next_ignore.read_text(encoding="utf-8").splitlines()
    next_dockerfile = ROOT / "docker" / "kubernetes" / "front-nextjs" / "Dockerfile"
    next_dockerfile_lines = next_dockerfile.read_text(encoding="utf-8").splitlines()
    health_route = ROOT / "front_NextJS" / "app" / "health" / "route.tsx"
    require(health_route.is_file(), "tracked Next.js /health Route Handler is missing")
    health_route_source = health_route.read_text(encoding="utf-8")
    require(
        "export async function GET" in health_route_source
        and "Response.json({ status: \"ok\" })" in health_route_source,
        "Next.js /health Route Handler must expose the expected GET response",
    )
    require(
        "COPY front_NextJS/ ./" in next_dockerfile_lines,
        "Next.js Dockerfile must copy the application source into the build stage",
    )
    require(
        "!front_NextJS/**" in next_ignore_lines
        and "front_NextJS/app/health/route.tsx" not in next_ignore_lines,
        "Next.js Docker context must include the tracked /health route.tsx",
    )
    require(
        "front_NextJS/app/health/route.ts" in next_ignore_lines,
        "Next.js Docker context must exclude the duplicate untracked /health route",
    )

    print(
        "PASS: 15 resources; Service selectors/ports, HTTP probes, Backend MySQL "
        "readiness, NetworkPolicy selectors, application security contexts, "
        "external Secrets, image placeholders, and rollout gates verified."
    )
    print("PASS: Backend egress allows only MySQL TCP/3306 and DNS TCP/UDP 53.")
    print("NOTE: PHP, Next.js and Dash egress remain open pending endpoint inventory.")


if __name__ == "__main__":
    main()
