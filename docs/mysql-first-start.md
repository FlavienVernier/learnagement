# First isolated MySQL start

> Purpose: prepare a guarded first MySQL start in a dedicated checkout without touching DEV data.

This procedure is for the first controlled MySQL start only. It must be run
from a dedicated checkout, never from a checkout used by DEV. It does not
initialize a previously used volume or include private SQL data.

## Preconditions

Do not continue unless all of these conditions are met:

- Windows has at least 1.5 GiB of free physical memory.
- Docker Desktop is healthy and the existing DEV containers are left untouched.
- The dedicated checkout contains the reviewed orchestration changes.
- The instance name, Compose project name, container name, network name, and
  volume name are unique and do not match any existing Docker resource.
- The four MySQL settings are available locally: `MYSQL_DB`,
  `MYSQL_USER_LOGIN`, `MYSQL_USER_PASSWORD`, and `MYSQL_ROOT_PASSWORD`.
- The local `.env` has the matching `INSTANCE_NAME` and
  `COMPOSE_PROJECT_NAME`. Never print or share its contents.

The CLI command `Learnagement.py start` is not suitable for this procedure: it
prepares initial data and starts the environment's configured service list.
Use the Compose generator with an explicit one-service selection instead.

## Prepare the isolated checkout

Choose a unique, lowercase `INSTANCE_NAME` and use it in the local `.env`.
The generator derives these names from it:

| Resource | Generated name |
|---|---|
| Compose service | `data_mysql_<INSTANCE_NAME>` |
| Container | `learnagement_data_mysql_<INSTANCE_NAME>` |
| Back network | `learnagement_back_<INSTANCE_NAME>` |
| Declared volume key | `learnagement_persistent_db_<INSTANCE_NAME>` |

Set a separate `COMPOSE_PROJECT_NAME` in `.env`. Compose combines that project
name with the declared volume key to determine the effective Docker volume
name. The network and container have explicit names, so verify all three
resource names against Docker before continuing. MySQL must have no published
host port.

Create `db\docker-entrypoint-initdb.d` in this checkout and copy only the ten
versioned scripts from `db\sql`:

```powershell
New-Item -ItemType Directory -Force db\docker-entrypoint-initdb.d
Copy-Item db\sql\*.sql db\docker-entrypoint-initdb.d\
```

Compare the source and staged files by name, size, and SHA-256 before
generating Compose:

```powershell
$source = Get-ChildItem db\sql -File -Filter '*.sql' | Sort-Object Name
$staged = Get-ChildItem db\docker-entrypoint-initdb.d -File -Filter '*.sql' |
    Sort-Object Name
if ($source.Count -ne 10 -or $staged.Count -ne 10) {
    throw 'Expected exactly ten SQL scripts in both source and staging folders.'
}
for ($i = 0; $i -lt $source.Count; $i++) {
    $srcHash = (Get-FileHash $source[$i].FullName -Algorithm SHA256).Hash
    $dstHash = (Get-FileHash $staged[$i].FullName -Algorithm SHA256).Hash
    if ($source[$i].Name -ne $staged[$i].Name -or
        $source[$i].Length -ne $staged[$i].Length -or
        $srcHash -ne $dstHash) {
        throw "SQL staging mismatch at index $i."
    }
}
```

Do not add files from `db\data` without approval from their data owner. Several
versioned scripts perform schema changes, deletes, or drops. They are intended
for first initialization of a new database volume and must not be manually
replayed against a volume that may contain data.

## Generate and inspect MySQL-only Compose

From the isolated checkout root, after preparing `.env` and the SQL staging
folder, generate Compose with only MySQL selected:

```powershell
python -c "import docker_compose; docker_compose.gen_docker_compose_yml(['data_mysql'])"
```

This writes the ignored file `docker\docker-compose.yml`. Do not display it
without redacting the MySQL credentials. Validate its effective Compose
configuration without starting a service:

```powershell
$project = (Get-Content .env | Where-Object { $_ -match '^COMPOSE_PROJECT_NAME=' } |
    Select-Object -First 1).Split('=', 2)[1]
docker compose --project-name $project -f docker\docker-compose.yml config --format json
```

Inspect the rendered JSON locally and confirm all of the following before
proceeding:

- the only service is `data_mysql_<INSTANCE_NAME>`;
- image is `mysql:8.4`;
- `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, and
  `MYSQL_ROOT_PASSWORD` are present, without copying their values into logs;
- container name is `learnagement_data_mysql_<INSTANCE_NAME>`;
- the only network is `learnagement_back_<INSTANCE_NAME>`;
- the declared persistent volume resolves to a new, unique project-scoped
  volume name;
- the SQL staging bind mount ends in `:/docker-entrypoint-initdb.d:ro`;
- there is no `ports` mapping and no Backend, PHP, Next.js, Dash, or phpMyAdmin
  service.

Before any start, verify that the effective container, network, and volume
names are absent from Docker's existing resource listings. If a collision
exists, stop and choose another instance/project name. Do not remove or reuse
the colliding resource.

## Controlled start and validation (next step only)

This section is a procedure, not authorization to run it during preparation.
Recheck the 1.5 GiB memory threshold immediately before starting. Start only
the service shown in the generated Compose:

```powershell
docker compose --project-name $project -f docker\docker-compose.yml `
    up -d --no-build --pull never data_mysql_<INSTANCE_NAME>
```

Replace `<INSTANCE_NAME>` with the chosen identifier. `--pull never` prevents
an implicit image pull; if `mysql:8.4` is not already available locally, stop
and request a separately approved image-provisioning step.

Check the service and health state:

```powershell
docker compose --project-name $project -f docker\docker-compose.yml ps
docker inspect --format '{{.State.Status}} {{.State.Health.Status}}' `
    learnagement_data_mysql_<INSTANCE_NAME>
docker compose --project-name $project -f docker\docker-compose.yml `
    logs --no-color data_mysql_<INSTANCE_NAME>
```

Proceed only when the container is `running`, health is `healthy`, and logs
show no critical initialization error. Then use an approved local MySQL client
with the application account to select `MYSQL_DB` and execute `SELECT 1`.
Keep credentials out of the command line, terminal history, and logs. A
successful connection and `SELECT 1` establish accessibility only; separately
inspect the expected tables and initialization logs to establish schema
initialization.

Stop and preserve the volume if health does not become healthy, the logs show
SQL errors, or the schema is incomplete. Do not rerun initialization scripts
against that volume and do not use `down -v`, volume removal, or cleanup as a
recovery step. Keep the isolated Compose project and volume for diagnosis.

## Scope of validation

The Compose-selection test validates generated YAML contracts without
starting Docker services. This document describes the guarded runtime
procedure. Neither is evidence that MySQL has started or that the SQL scripts
are compatible with MySQL 8.4; those claims require the controlled runtime
validation above.
