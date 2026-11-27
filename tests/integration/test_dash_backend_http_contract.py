import importlib
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pandas as pd
import pytest
import requests


@pytest.fixture
def backend_server(monkeypatch):
    observed = []

    class Handler(BaseHTTPRequestHandler):
        def _respond(self, status, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            observed.append(
                {
                    "method": "GET",
                    "path": self.path,
                    "authorization": self.headers.get("Authorization"),
                }
            )
            if self.path.startswith("/unavailable"):
                self._respond(503, {"detail": "mock unavailable"})
            elif self.path.startswith("/unauthorized"):
                self._respond(401, {"detail": "mock unauthorized"})
            elif self.path.startswith("/forbidden"):
                self._respond(403, {"detail": "mock forbidden"})
            elif self.path.startswith("/empty"):
                self._respond(200, [])
            elif self.path.startswith("/invalid-json"):
                body = b"not-json"
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._respond(200, [{"id": 7, "name": "mock"}])

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            observed.append(
                {
                    "method": "POST",
                    "path": self.path,
                    "authorization": self.headers.get("Authorization"),
                    "content_type": self.headers.get("Content-Type"),
                    "body": json.loads(body),
                }
            )
            self._respond(200, [{"accepted": True}])

        def do_PATCH(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            observed.append(
                {
                    "method": "PATCH",
                    "path": self.path,
                    "authorization": self.headers.get("Authorization"),
                    "content_type": self.headers.get("Content-Type"),
                    "body": json.loads(body),
                }
            )
            self._respond(200, [{"updated": True}])

        def do_DELETE(self):
            observed.append(
                {
                    "method": "DELETE",
                    "path": self.path,
                    "authorization": self.headers.get("Authorization"),
                }
            )
            self._respond(200, [])

        def log_message(self, _format, *_args):
            pass

    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", observed
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.fixture
def dash_client():
    module_path = str(Path(__file__).resolve().parents[2] / "front_DashPlotly")
    sys.path.insert(0, module_path)
    try:
        sys.modules.pop("app_tools", None)
        return importlib.import_module("app_tools")
    finally:
        sys.path.remove(module_path)


def test_get_forwards_bearer_and_query_to_backend(backend_server, dash_client):
    base_url, observed = backend_server

    result = dash_client.get_endpoint(
        f"{base_url}/students", token="test-token", data={"student_id": 42}
    )

    assert isinstance(result, pd.DataFrame)
    assert result.to_dict("records") == [{"id": 7, "name": "mock"}]
    assert observed == [
        {
            "method": "GET",
            "path": "/students?student_id=42",
            "authorization": "Bearer test-token",
        }
    ]


def test_post_sends_json_and_bearer_to_backend(backend_server, dash_client):
    base_url, observed = backend_server

    result = dash_client.post_endpoint(
        f"{base_url}/assignments", {"assignment_id": 12}, token="test-token"
    )

    assert result.to_dict("records") == [{"accepted": True}]
    assert observed == [
        {
            "method": "POST",
            "path": "/assignments",
            "authorization": "Bearer test-token",
            "content_type": "application/json",
            "body": {"assignment_id": 12},
        }
    ]


def test_patch_sends_json_and_bearer_to_backend(backend_server, dash_client):
    base_url, observed = backend_server

    result = dash_client.patch_endpoint(
        f"{base_url}/assignments/12", {"status": "approved"}, token="test-token"
    )

    assert result.to_dict("records") == [{"updated": True}]
    assert observed == [
        {
            "method": "PATCH",
            "path": "/assignments/12",
            "authorization": "Bearer test-token",
            "content_type": "application/json",
            "body": {"status": "approved"},
        }
    ]


def test_delete_forwards_bearer_without_body(backend_server, dash_client):
    base_url, observed = backend_server

    result = dash_client.delete_endpoint(
        f"{base_url}/assignments/12", token="test-token"
    )

    assert result.empty
    assert observed == [
        {
            "method": "DELETE",
            "path": "/assignments/12",
            "authorization": "Bearer test-token",
        }
    ]


def test_empty_backend_result_returns_empty_dataframe(backend_server, dash_client):
    base_url, _observed = backend_server

    result = dash_client.get_endpoint(f"{base_url}/empty", token="test-token")

    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_backend_http_failure_is_propagated(backend_server, dash_client):
    base_url, _observed = backend_server

    with pytest.raises(requests.HTTPError) as error:
        dash_client.get_endpoint(f"{base_url}/unavailable", token="test-token")

    assert error.value.response.status_code == 503


def test_backend_timeout_is_propagated(monkeypatch, dash_client):
    def raise_timeout(*_args, **kwargs):
        assert kwargs["timeout"] == 30
        raise requests.Timeout("mock timeout")

    monkeypatch.setattr(dash_client.requests, "get", raise_timeout)

    with pytest.raises(requests.Timeout):
        dash_client.get_endpoint(
            "http://127.0.0.1:1/unreachable", token="test-token"
        )


def test_invalid_json_response_is_propagated(backend_server, dash_client):
    base_url, _observed = backend_server

    with pytest.raises((requests.JSONDecodeError, ValueError)):
        dash_client.get_endpoint(
            f"{base_url}/invalid-json", token="test-token"
        )


@pytest.mark.parametrize(
    ("path", "status"),
    [
        ("unauthorized", 401),
        ("forbidden", 403),
    ],
)
def test_auth_http_errors_are_propagated(
    backend_server, dash_client, path, status
):
    base_url, _observed = backend_server

    with pytest.raises(requests.HTTPError) as error:
        dash_client.get_endpoint(
            f"{base_url}/{path}", token="test-token"
        )

    assert error.value.response.status_code == status
