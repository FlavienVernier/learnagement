from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_php_proxy_contract_uses_backend_variables_and_bearer():
    source = (
        REPOSITORY_ROOT / "front_PHP" / "utils" / "apiProxy.php"
    ).read_text(encoding="utf-8")

    assert "BACKEND_PYTHON_DOCKER_URL" in source
    assert "BACKEND_PYTHON_DOCKER_PORT" in source
    assert "INSTANCE_PROTOCOL" in source
    assert "CURLOPT_TIMEOUT => 30" in source
    assert "CURLOPT_HTTPHEADER" in source
    assert "Content-Type" in source


def test_php_api_proxy_transmits_methods_and_http_errors():
    source = (
        REPOSITORY_ROOT / "front_PHP" / "api.php"
    ).read_text(encoding="utf-8")

    assert "['GET', 'POST', 'PATCH', 'PUT', 'DELETE']" in source
    assert "Authorization: Bearer" in source
    assert "Backend unavailable" in source
    assert "http_response_code($status)" in source


def test_next_proxy_contract_supports_get_post_and_cookie():
    route = (
        REPOSITORY_ROOT
        / "front_NextJS"
        / "app"
        / "api"
        / "proxy"
        / "[...phpPath]"
        / "route.ts"
    )
    text = route.read_text(encoding="utf-8")

    assert "export async function POST" in text
    assert "export async function GET" in text
    assert "BACKEND_PYTHON_DOCKER_URL" in text
    assert "BACKEND_PYTHON_DOCKER_PORT" in text
    assert 'req.headers.get("cookie")' in text
    assert "status: 500" in text


def test_php_login_contract_uses_password_token_endpoint():
    login = (
        REPOSITORY_ROOT
        / "front_PHP"
        / "views"
        / "base"
        / "@post"
        / "login.php"
    ).read_text(encoding="utf-8")

    assert "grant_type" in login
    assert '"password"' in login
    assert "forwardToBackend" in login
    assert "path: 'token'" in login
    assert "application/x-www-form-urlencoded" in login
    assert "JWT_SIGNING_KEY" in login


def test_php_cas_contract_uses_service_header_and_backend_payload():
    cas = (
        REPOSITORY_ROOT / "front_PHP" / "utils" / "cas.php"
    ).read_text(encoding="utf-8")
    endpoint = (
        REPOSITORY_ROOT / "front_PHP" / "utils" / "endpoint.php"
    ).read_text(encoding="utf-8")

    assert "get_python_backend_url" in cas
    assert "token-cas/" in cas
    assert "'members'" in cas
    assert "CAS_SERVICE_TOKEN" in endpoint
    assert "X-Cas-Token" in endpoint
    assert "application/json" in endpoint


def test_nextauth_contract_uses_password_token_and_jwt_expiry():
    route = (
        REPOSITORY_ROOT
        / "front_NextJS"
        / "app"
        / "api"
        / "auth"
        / "[...nextauth]"
        / "route.ts"
    ).read_text(encoding="utf-8")

    assert "/token" in route
    assert "grant_type" in route
    assert '"password"' in route
    assert "application/x-www-form-urlencoded" in route
    assert "jwtDecode" in route
    assert "decoded.exp" in route
    assert "JWT_SIGNING_KEY" in route


def test_next_proxy_contract_has_no_declared_timeout_or_retry():
    route = (
        REPOSITORY_ROOT
        / "front_NextJS"
        / "app"
        / "api"
        / "proxy"
        / "[...phpPath]"
        / "route.ts"
    ).read_text(encoding="utf-8")

    assert "export async function POST" in route
    assert "export async function GET" in route
    assert "timeout" not in route.lower()
    assert "retry" not in route.lower()
    assert "status: 500" in route


def test_backend_cas_contract_uses_x_cas_token_and_http_errors():
    auth = (
        REPOSITORY_ROOT / "backend_python" / "auth" / "authenticate.py"
    ).read_text(encoding="utf-8")
    cas = (
        REPOSITORY_ROOT / "backend_python" / "auth" / "authenticate_cas.py"
    ).read_text(encoding="utf-8")

    assert '@router.post("/token-cas"' in auth
    assert "X-Cas-Token" in auth or "x_cas_token" in auth
    assert "CAS_SERVICE_TOKEN" in cas
    assert "status.HTTP_401_UNAUTHORIZED" in cas
    assert "status.HTTP_403_FORBIDDEN" in cas
    assert "status.HTTP_500_INTERNAL_SERVER_ERROR" in cas


def test_groq_contract_is_direct_dash_integration_not_autonomous_service():
    chat = (
        REPOSITORY_ROOT
        / "front_DashPlotly"
        / "apc_dash"
        / "apc20_chatbot_backend.py"
    ).read_text(encoding="utf-8")
    tools = (
        REPOSITORY_ROOT
        / "front_DashPlotly"
        / "apc_dash"
        / "apc20_chatbot_tools.py"
    ).read_text(encoding="utf-8")

    assert "https://api.groq.com/openai/v1/chat/completions" in chat
    assert "GROQ_API_KEY" in chat
    assert "timeout=60" in chat
    assert "429" in chat
    assert "401" in chat
    assert "execute_tool" in chat
    assert "get_apc_" in tools or "def execute_tool" in tools
