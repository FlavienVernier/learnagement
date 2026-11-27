# Learnagement integration test plan

This plan separates executable isolated tests from runtime tests that require
Docker and real services. It does not turn a mock or static check into proof
that the deployed services communicate.

## Matrix

| Integration | Isolated tests | Runtime test | Real status |
|---|---|---|---|
| Backend / MySQL | Configuration URL and missing/invalid settings | MySQL isolated, SQL read query, schema check | To qualify |
| PHP / Backend | Static proxy contract plus HTTP simulator target | PHP container, session/JWT, `/api.php` | Blocked |
| Next.js / Backend | Static route contract | NextAuth `/token` and `/api/proxy` flows | Blocked |
| Dash / Backend | HTTP mock for methods, auth, errors, timeout, invalid JSON | Dash container against real Backend | Existing mock result |
| IA / Backend | None until the owner provides a contract | Future provider/Backend integration | Not confirmed |

## Commands

```powershell
py -3.13 -m pytest -q tests\integration\test_compose_startup_order.py
py -3.13 -m pytest -q tests\integration\test_backend_mysql_contract.py
py -3.13 -m pytest -q tests\integration\test_http_contract_sources.py
py -3.13 -m pytest -q tests\integration\test_dash_backend_http_contract.py
```

The suite must not need Docker, MySQL, service DEV, real secrets, or private
data. The integration requirement file reuses the repository's dependency
manifests and adds PyYAML for parsing generated Compose YAML. The transferred
suite contains 27 collected cases across four pytest files. They validate
static sources, Compose generation, or local HTTP/engine simulations; they do
not prove runtime Docker or MySQL communication.

Use Python 3.13 or newer for the full suite: the current Dash source imports
`warnings.deprecated`, which is unavailable in Python 3.11. The latest local
re-execution in the `feature/orchestration` worktree passed 27 cases with
Python 3.13; pytest emitted one Dash-plugin deprecation warning. The suite
includes local HTTP simulation, not calls to a real Backend, Docker, or MySQL.

## Compose bind-mount source caveat

Static inspection found that the isolated MySQL procedure must prepare both
`db\docker-entrypoint-initdb.d` and `docker\data_mysql\conf.d`; the first-start
runbook creates them explicitly. The phpMyAdmin configuration and PHP ini
mount sources exist in this checkout. Full-stack sources
`front_NextJS\node_modules`, `front_DashPlotly\data`, `docker\log\php`, and
the configured certificate directories are absent here. In particular, an
empty `node_modules` bind mount could hide dependencies already present in a
container image. Resolve these sources and review the resulting Compose
configuration before any full-stack runtime test. This is a static path check;
Docker was not run.

The Windows CLI test is not transferred: the approved base still imports
`termios` from `tools.py`, and changing that functional module is outside this
transfer.

## INT-001 — Backend / MySQL configuration

- **Objective:** verify that the engine URL uses documented environment names
  and pool settings without opening a database connection.
- **Preconditions:** Python and the integration requirements.
- **Action:** import `db.connection`, set fake environment values, and replace
  `create_engine` with a capturing stub.
- **Expected:** driver, host, port, database, pool size, overflow, pool timeout,
  pre-ping and recycle settings match code; missing port fails locally.
- **Execution:** `test_backend_mysql_contract.py`.
- **Proof:** pytest assertions on the captured SQLAlchemy URL and engine
  keyword arguments.
- **Status:** executable isolated test; not runtime.

## INT-002 — Backend / MySQL unavailable

- **Objective:** distinguish engine construction from a real availability check.
- **Preconditions:** separate runtime MySQL instance and real credentials;
  Backend startup also runs `init.init()` and creates/replaces secondary-key
  views.
- **Action:** start MySQL with no Backend, then add Backend and call a read-only
  query.
- **Expected:** known 503 behavior for unavailable/busy database in the
  implemented paths; no silent fallback.
- **Proof:** logs, HTTP status, health state and read-only SQL result.
- **Status:** not executed; requires an isolated MySQL/Backend runtime and
  approved test credentials.

## INT-003 — PHP / Backend proxy

- **Objective:** verify proxy URL variables, HTTP methods, Authorization
  propagation, 30-second timeout and response/error handling.
- **Preconditions:** source contract and a local Backend simulator.
- **Action:** static source checks; optionally execute PHP only against an HTTP
  simulator if a PHP runtime is approved.
- **Expected:** source permits GET/POST/PATCH/PUT/DELETE; Bearer is forwarded;
  cURL timeout is 30 seconds; unavailable Backend returns status 0.
- **Proof:** pytest static assertions or PHP runtime capture.
- **Status:** static test executable; PHP runtime not executed.

## INT-004 — PHP login / CAS

- **Objective:** verify `/token` and `/token-cas` authentication contracts.
- **Preconditions:** test account and CAS token from an owner; no real secret.
- **Action:** POST factored form data or CAS data through a Backend simulator.
- **Expected:** valid credentials return JWT-shaped response; invalid login
  returns 401; CAS service token policy is enforced.
- **Proof:** HTTP status, redacted response shape and headers.
- **Status:** not executed; requires an approved test account and owner
  confirmation for the CAS flow.

## INT-005 — Next.js proxy

- **Objective:** verify GET/POST support, URL construction, cookie forwarding,
  500 handling and absent timeout/retry behavior.
- **Preconditions:** Next.js dependencies and a local Backend simulator.
- **Action:** execute only route unit tests or the existing Next test harness
  once present.
- **Expected:** path and variables are built as documented; cookie is forwarded;
  unavailable Backend follows the implemented 500 behavior.
- **Proof:** captured `axios` call and `Response`.
- **Status:** static source test executable; runtime Next.js test not executed.

## INT-006 — NextAuth login

- **Objective:** verify form-urlencoded `/token` login and JWT session storage.
- **Preconditions:** Backend simulator returning a syntactically valid test JWT.
- **Action:** call the credentials provider and NextAuth callbacks.
- **Expected:** valid JWT sets user/session; absent/invalid/expired JWT follows
  the implemented errors.
- **Proof:** mocked Axios call, decoded test token and session payload.
- **Status:** to create after confirming the Next.js test convention.

## INT-007 — Dash / Backend

- **Objective:** verify GET/POST/PATCH/DELETE, Bearer, formats, empty data,
  503, timeout, invalid JSON and 401/403.
- **Preconditions:** integration requirements and no Docker.
- **Action:** run the existing in-process HTTP mock.
- **Expected:** bearer and payload content match; HTTP and network failures
  propagate; invalid JSON does not become empty or fallback data.
- **Proof:** pytest observations from the mock HTTP server.
- **Status:** 10 simulated HTTP cases passed in the transfer; runtime
  real-Backend test not executed.

## INT-008 — IA / Backend

- **Objective:** generic provider contract only.
- **Preconditions:** owner-provided service URL, endpoint, method, payload,
  authentication, timeout, retry and error contract.
- **Action:** once supplied, add provider-independent HTTP tests.
- **Expected:** success, invalid payload, 401, 429, timeout and unavailable
  provider are distinguishable and logged.
- **Proof:** captured HTTP and redacted contract payload.
- **Status:** blocked/non-implemented; do not add fake endpoints.

## Stop and rollback criteria

Stop a runtime scenario if:

- a test depends on DEV credentials or data;
- MySQL would use or alter an existing volume;
- an HTTP call targets an undocumented endpoint;
- a response contains an unexpected secret or personal data;
- a test requires Docker startup beyond the approved MySQL-only progression.

Runtime failures must not be repaired by changing application contracts or
mocking results. Preserve the isolated volume for diagnosis and do not use
destructive Compose commands.
