"""Read-only HTTP health checks for Learnagement service URLs."""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener


_OPENER = build_opener(ProxyHandler({}))


def _url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def _check(
    name: str, url: str, timeout: float, extra_headers: dict[str, str] | None = None
) -> bool:
    headers = {"Accept": "application/json", **(extra_headers or {})}
    request = Request(url, headers=headers, method="GET")
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            status = response.status
            body = response.read()
    except HTTPError as error:
        print(f"FAIL {name}: HTTP {error.code}")
        return False
    except (TimeoutError, URLError, OSError) as error:
        reason = "timeout" if isinstance(error, TimeoutError) else type(error).__name__
        print(f"FAIL {name}: {reason}")
        return False

    if status != 200:
        print(f"FAIL {name}: HTTP {status}")
        return False

    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(f"FAIL {name}: response is not JSON")
        return False

    if not isinstance(payload, dict) or payload.get("status") != "ok":
        print(f"FAIL {name}: unexpected health response")
        return False

    print(f"PASS {name}: HTTP 200, status=ok")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check health GET routes and optionally the Next.js proxy when a "
            "session cookie is supplied. No database or write endpoint is used."
        )
    )
    parser.add_argument("--backend", default=os.getenv("LEARNAGEMENT_BACKEND_URL"))
    parser.add_argument("--php", default=os.getenv("LEARNAGEMENT_PHP_URL"))
    parser.add_argument("--next", default=os.getenv("LEARNAGEMENT_NEXT_URL"))
    parser.add_argument("--dash", default=os.getenv("LEARNAGEMENT_DASH_URL"))
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    bases = {
        "Backend": args.backend,
        "PHP": args.php,
        "Next.js": args.next,
        "Dash": args.dash,
    }
    missing = [name for name, value in bases.items() if not value]
    if missing:
        parser.error(
            "provide URLs for all services with --backend/--php/--next/--dash "
            "or LEARNAGEMENT_BACKEND_URL/LEARNAGEMENT_PHP_URL/"
            "LEARNAGEMENT_NEXT_URL/LEARNAGEMENT_DASH_URL"
        )
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    checks = [
        ("Backend health", _url(args.backend, "/health")),
        ("PHP health", _url(args.php, "/health")),
        ("Next.js health", _url(args.next, "/health")),
        ("Dash health", _url(args.dash, "/health")),
        ("PHP to Backend health", _url(args.php, "/api.php?path=%2Fhealth")),
    ]
    results = [_check(name, url, args.timeout) for name, url in checks]

    next_cookie = os.getenv("LEARNAGEMENT_NEXTAUTH_COOKIE")
    if next_cookie:
        results.append(
            _check(
                "Next.js to Backend health",
                _url(args.next, "/api/proxy/health"),
                args.timeout,
                {"Cookie": next_cookie},
            )
        )
    else:
        print(
            "SKIP Next.js to Backend health: "
            "LEARNAGEMENT_NEXTAUTH_COOKIE is not set"
        )

    print(f"Result: {sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
