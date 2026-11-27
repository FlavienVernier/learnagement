# Runbook de validation Backend / MySQL

Ce runbook prépare uniquement la validation future de MySQL puis du Backend.
Aucune instruction ci-dessous ne doit être exécutée pendant cette préparation.
Il ne transforme pas les contrôles statiques ou simulés en validation runtime.

## 1. Prérequis GO/NO-GO

Avant toute action, exécuter le préflight immédiatement avant le démarrage :

```powershell
$os = Get-CimInstance Win32_OperatingSystem
"TotalGiB=$([math]::Round($os.TotalVisibleMemorySize/1MB,2)); FreeGiB=$([math]::Round($os.FreePhysicalMemory/1MB,2)); UsedGiB=$([math]::Round(($os.TotalVisibleMemorySize-$os.FreePhysicalMemory)/1MB,2))"

docker info --format 'OSType={{.OSType}};CPUs={{.NCPU}};MemoryBytes={{.MemTotal}}'
docker image inspect mysql:8.4 --format 'mysql:8.4 {{.Id}}'
git branch --show-current
git rev-parse HEAD
git status --short
```

GO seulement si toutes les conditions suivantes sont vraies :

- mémoire Windows libre supérieure ou égale à 1,5 Gio ;
- Docker Engine Linux disponible ;
- image locale `mysql:8.4` présente ;
- espace disque suffisant ;
- neuf conteneurs DEV laissés intacts ;
- instance Compose, conteneur, réseau et volume uniques ;
- aucun conteneur ou réseau DEV du même nom ;
- aucun volume MySQL DEV ou ancien réutilisé ;
- aucun port MySQL publié ;
- aucune donnée privée non autorisée dans les scripts ;
- `.env` complet, sans secret affiché ;
- `MYSQL_SERVER=learnagement_data_mysql_<INSTANCE_NAME>`.

Une différence entre un projet Compose et les ressources DEV ne suffit pas à
prouver l'isolation : les noms explicites de conteneurs/réseaux et le volume
effectif doivent tous être absents avant la création.

## 2. Architecture confirmée

La séquence attendue est :

```text
Backend SQLAlchemy
  -> TCP MySQL 3306
  -> Conteneur data_mysql_<INSTANCE_NAME>
  -> Réseau learnagement_back_<INSTANCE_NAME>
  -> Volume learnagement_persistent_db_<INSTANCE_NAME>
```

SQLAlchemy est construit paresseusement dans
[backend_python/db/connection.py](../backend_python/db/connection.py). Une
connexion réelle n'est ouverte que lorsqu'une fonction appelle
`get_connection()` ou `get_read_connection()`.

Le démarrage normal du Backend ne doit pas appeler
[backend_python/init.py](../backend_python/init.py). Ce module initialise des
vues secondaires uniquement avec `python init.py --apply`; cette commande ne
doit pas être exécutée dans le premier démarrage sans autorisation du propriétaire
des données.

L'état `/health` confirme uniquement qu'une réponse HTTP est disponible :
[backend_python/app.py](../backend_python/app.py). Il ne vérifie ni
MySQL, ni les identifiants, ni les tables.

## 3. Phase A — MySQL seul

Utiliser un projet Compose unique `--project-name <PROJECT>` et remplacer
`<INSTANCE_NAME>` uniquement après vérification des collisions. Ne jamais
afficher les secrets.

### A1 — Démarrage contrôlé

Après génération externe autorisée du fichier MySQL-only Compose :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  up -d --no-build --pull never data_mysql_<INSTANCE_NAME>
```

Résultat attendu : un seul conteneur de test démarre, sans port MySQL publié.

Erreur possible : image absente, collision de nom, volume déjà occupé,
permission de montage ou erreur SQL d'initialisation.

Arrêt : stopper immédiatement toute collision, toute erreur critique SQL ou
toute tentative d'utiliser un volume DEV. Conserver les ressources pour
diagnostic.

### A2 — Conteneur démarré

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml ps
docker inspect --format '{{.State.Status}} {{.State.Health.Status}}' `
  learnagement_data_mysql_<INSTANCE_NAME>
```

Résultat attendu : état `running` et santé `healthy`.

Preuve : sortie exacte des deux commandes.

Condition d'arrêt : `exited`, `restarting`, `unhealthy`, journal SQL critique
ou absence de healthcheck.

### A3 — Journaux d'initialisation

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  logs --no-color data_mysql_<INSTANCE_NAME>
```

Résultat attendu : initialisation terminée, aucune erreur SQL critique.

Erreur possible : scripts incompatibles avec MySQL 8.4, redéclaration,
définisseur invalide, erreur `DELIMITER`, erreur de migration ou volume non
vierge.

Arrêt : ne pas rejouer les scripts et ne pas utiliser `down -v`.

### A4 — Résolution DNS depuis le réseau Backend

Ne lancer cette vérification qu'après ajout autorisé du conteneur Backend :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec backend_python_<INSTANCE_NAME> python -c `
  "import os,socket; print(socket.getaddrinfo(os.getenv('MYSQL_SERVER'), int(os.getenv('MYSQL_PORT')))[0][4][0])"
```

Résultat attendu : résolution vers une adresse du réseau
`learnagement_back_<INSTANCE_NAME>`.

Preuve : adresse résolue sans secret.

Arrêt : nom non résolu, adresse externe inattendue ou résolution vers une
instance DEV.

### A5 — TCP MySQL 3306

Depuis le Backend :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec backend_python_<INSTANCE_NAME> python -c `
  "import os,socket; s=socket.create_connection((os.getenv('MYSQL_SERVER'), int(os.getenv('MYSQL_PORT')), 2)); s.close(); print('TCP_OK')"
```

Résultat attendu : `TCP_OK`.

Erreur possible : DNS absent, port fermé, firewall réseau ou MySQL arrêté.

Arrêt : aucune nouvelle étape tant que la connexion TCP n'est pas confirmée.

### A6 — Authentification applicative

Utiliser les variables internes du conteneur, sans écrire le mot de passe dans
la ligne de commande :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec data_mysql_<INSTANCE_NAME> sh -c `
  'mysql --protocol=socket -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e "SELECT 1;"'
```

Résultat attendu : `1`.

Erreur possible : compte absent, mot de passe incorrect, hôte interdit ou base
absente.

Arrêt : ne pas continuer si l'authentification échoue.

### A7 — Base attendue

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec data_mysql_<INSTANCE_NAME> sh -c `
  'mysql --protocol=socket -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -N -e "SELECT DATABASE();" "$MYSQL_DATABASE"'
```

Résultat attendu : nom de `MYSQL_DB` sans secret affiché.

Erreurs possibles : base absente ou mauvaise variable injectée.

### A8 — Tables attendues

La liste exacte des tables ne doit pas être supposée. Obtenir uniquement
d'abord un compte réel, puis confirmer les tables nécessaires auprès du
propriétaire Backend :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec data_mysql_<INSTANCE_NAME> sh -c `
  'mysql --protocol=socket -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE();" "$MYSQL_DATABASE"'
```

Résultat attendu : nombre de tables supérieur à zéro et liste approuvée.

Arrêt : base vide ou table nécessaire absente.

### A9 — Lecture non destructive

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec data_mysql_<INSTANCE_NAME> sh -c `
  'mysql --protocol=socket -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -N -e "SELECT 1 AS probe;" "$MYSQL_DATABASE"'
```

Résultat attendu : une seule ligne contenant `1`.

Cette lecture ne valide pas seule le schéma métier.

## 4. Phase B — Backend

Le Backend ne doit être ajouté qu'après validation réelle des contrôles A1 à
A9.

### B1 — Démarrage Backend seul

Générer ou modifier uniquement l'environnement isolé approuvé, puis démarrer
MySQL et Backend sans PHP, Next.js, Dash ou phpMyAdmin :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  up -d --no-build --pull never data_mysql_<INSTANCE_NAME> backend_python_<INSTANCE_NAME>
```

Résultat attendu : les deux conteneurs démarrent et respectent
`service_healthy`.

### B2 — Healthcheck HTTP

Depuis l'hôte :

```powershell
curl --fail --silent --show-error `
  http://127.0.0.1:<BACKEND_PYTHON_PORT>/health
```

Résultat attendu : HTTP 200 avec `{"status":"ok"}`.

Preuve : code HTTP et corps.

Limite : ce contrôle ne prouve ni MySQL, ni l'authentification, ni le schéma.

### B3 — Résolution SQL

La commande Python suivante lit les variables injectées et résout uniquement
le nom configuré :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml `
  exec backend_python_<INSTANCE_NAME> python -c `
  "import os,socket; print(os.getenv('MYSQL_SERVER')); print(socket.gethostbyname(os.getenv('MYSQL_SERVER')))"
```

Résultat attendu : `MYSQL_SERVER=learnagement_data_mysql_<INSTANCE_NAME>` et
une adresse du réseau Back. Ne pas afficher les identifiants.

### B4 — Connexion SQLAlchemy

Une première connexion réelle doit être déclenchée par un endpoint ou un
script approuvé utilisant `get_read_connection()`. Ne pas considérer l'import
de SQLAlchemy comme une preuve.

Résultats possibles :

- succès : SELECT/résultat réel ;
- indisponibilité : erreur SQLAlchemy convertie en 503 dans les chemins protégés ;
- erreur d'identifiant : échec d'authentification ;
- base absente : erreur SQLAlchemy ;
- tables absentes : SQL/exception sur la requête.

Preuve : journal redacted, code HTTP, requête SQL de lecture approuvée.

### B5 — Endpoint GET sans effet de bord

Choisir uniquement un endpoint GET approuvé utilisant réellement MySQL.
Exemples possibles uniquement après confirmation du propriétaire :

```text
/filieres
/apc/competences
/enseignants
/etudiants
```

La validation doit utiliser un JWT de test généré pour l'environnement, jamais
un compte réel.

Résultat attendu : 200 avec format réel, ou 401/403 si le test vérifie
séparément l'authentification.

Preuve : code HTTP, corps redacted, journal Backend sans secret.

### B6 — Authentification

Le cas `/token` nécessite un compte de test et des variables JWT/CAS approuvées.
Ne pas utiliser de données personnelles.

Résultat attendu : JWT valide d'un compte isolé, ou 401/403 attendu pour
des identifiants invalides.

Ne pas déclarer validée une authentification fondée uniquement sur la route
`/health`.

## 5. Scénarios de résilience

| Scénario | Action future | Résultat attendu | Preuve |
|---|---|---|---|
| MySQL indisponible au démarrage | Démarrer Backend après MySQL arrêté dans l'environnement isolé | Backend peut démarrer; `health` reste HTTP OK; premier endpoint DB échoue sans fallback | état conteneurs, `/health`, 503/erreur documentée, journaux |
| Identifiants incorrects | Modifier temporairement uniquement l'environnement isolé | échec SQLAlchemy; aucun fallback ni ouverture silencieuse | erreur d'authentification redacted, code endpoint |
| Base absente | Variable `MYSQL_DB` vers une base inexistante approuvée | échec SQLAlchemy lors de la première vraie connexion | erreur MySQL redacted, code endpoint |
| Tables absentes | Utiliser une base vide non destructive | endpoint échoue clairement ou retourne selon le contrat réel | nom absent, code HTTP, absence de données fictives |
| Interruption temporaire | Arrêter MySQL puis le redémarrer dans le même environnement | endpoint échoue pendant l'interruption puis peut retrouver l'accès après reprise | chronologie, logs, lecture avant/après |
| Redémarrage Backend | Redémarrer uniquement le Backend après rétablissement MySQL | nouvelle connexion SQLAlchemy réussie sur les mêmes volumes | `/health`, lecture réelle, logs |

Ces scénarios ne sont pas autorisés sur les services DEV. Chaque arrêt MySQL
doit utiliser uniquement le projet isolé.

## 6. Arrêt sans destruction

Après validation ou incident :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml stop
```

Pour redémarrer :

```powershell
docker compose --project-name <PROJECT> -f docker\docker-compose.yml start
```

Interdit pour ces validations :

- `docker compose down -v`;
- suppression ou nettoyage de volume ;
- `docker system prune`;
- suppression de conteneur DEV ;
- réinitialisation `--from_scratch`;
- réexécution SQL sur un volume interrompu ;
- arrêt ou redémarrage des services DEV.

## 7. Matrice de validation

| Contrôle | Commande | Résultat attendu | Preuve | Statut |
|---|---|---|---|---|
| Mémoire/ressources | préflight PowerShell | >= 1,5 Gio libre | valeurs exactes | NON EXÉCUTÉ |
| Docker/image | `docker info`, `docker image inspect` | Docker Linux actif, image locale présente | sortie Docker | NON EXÉCUTÉ |
| Isolation | listings Docker des conteneurs/réseaux/volumes | aucune collision DEV | résultats redacted | NON EXÉCUTÉ |
| MySQL démarré | `docker compose up` MySQL seul | conteneur running | sortie `ps` | NON EXÉCUTÉ |
| MySQL health | `docker inspect` | `healthy` | état Health.Status | NON EXÉCUTÉ |
| Journaux init | `docker compose logs` | aucune erreur critique | extrait de logs | NON EXÉCUTÉ |
| DNS Back | Python `getaddrinfo` depuis Backend | hôte MySQL résolu | adresse résolue | NON EXÉCUTÉ |
| TCP 3306 | Python `create_connection` depuis Backend | TCP_OK | sortie Python | NON EXÉCUTÉ |
| Authentification SQL | mysql avec compte applicatif | SELECT 1 | ligne `1` | NON EXÉCUTÉ |
| Base attendue | mysql `SELECT DATABASE()` | base configurée | nom approuvé | NON EXÉCUTÉ |
| Tables | information_schema | tables attendues présentes | compte + liste approuvée | NON EXÉCUTÉ |
| Lecture non destructive | SELECT 1 | résultat `1` | sortie mysql | NON EXÉCUTÉ |
| Backend démarré | Compose MySQL + Backend | deux services en état sain | sortie `ps` | NON EXÉCUTÉ |
| HTTP health | `curl /health` | HTTP 200, JSON attendu | code + corps | NON EXÉCUTÉ |
| SQLAlchemy | endpoint GET nécessitant DB | connexion réelle réussie | réponse et logs redacted | NON EXÉCUTÉ |
| Endpoint applicatif | GET approuvé | données autorisées ou 401/403 | code HTTP et résultat redacted | NON EXÉCUTÉ |
| Authentification | `/token` avec compte test | JWT test ou erreur attendue | réponse redacted | NON EXÉCUTÉ |
| Résilience MySQL | scénarios isolés | comportement attendu | chronologie et journaux | NON EXÉCUTÉ |

## 8. Limites

- Ce runbook ne prouve aucune intégration tant que ses commandes ne sont pas
  exécutées dans l'environnement isolé.
- Le statut reste `NON EXÉCUTÉ` après la préparation documentaire.
- Les réponses HTTP du Backend ne prouveront pas MySQL si elles viennent
  uniquement de `/health`.
- PHP, Next.js, Dash, CAS, IA et Kubernetes restent hors de la première
  validation MySQL → Backend.
