# Contrats interservices Learnagement

## Niveau de preuve

- **Confirmé** : démontré directement par le code ou un test existant.
- **Partiellement confirmé** : certains éléments sont présents, mais le contrat reste incomplet.
- **À confirmer** : information absente, divergente ou non vérifiée en runtime.
- **Non implémenté** : aucune intégration réellement disponible.

Les informations ci-dessous sont des observations statiques ou des tests
automatisés existants. Elles ne constituent pas une validation runtime d'une
stack Docker complète.

## 1. Vue d'ensemble

| Appelant | Destinataire | Transport | État général |
|---|---|---|---|
| Backend Python | MySQL | SQLAlchemy/mysql+mysqlconnector sur port MySQL 3306 | Partiellement confirmé |
| PHP | Backend Python | HTTP(S), proxy `/api.php`, JWT Bearer | Confirmé dans le code; runtime non validé |
| Next.js | Backend Python | HTTP(S), Axios, cookies puis endpoint `/token` ou `/api/proxy/<path>` | Partiellement confirmé |
| Dash/Plotly | Backend Python | HTTPS HTTP requests, JWT Bearer | Confirmé dans le code et test HTTP simulé |
| Dash/Plotly | API Groq externe | HTTPS OpenAI-compatible; appels de fonctions locaux vers le Backend | Partiellement confirmé; le service IA interne futur reste non implémenté |

Le backend est placé sur les réseaux Compose Back et Front. MySQL est sur Back
avec le Backend; les interfaces sont sur Front avec le Backend. Dans le Compose
actuel, MySQL n'est pas publié sur un port hôte.

## 2. Tableau synthétique des contrats

| Contrat | Adresse | Méthodes | Authentification | Format | Timeout/retry | Preuve |
|---|---|---|---|---|---|---|
| Backend ↔ MySQL | `MYSQL_SERVER:<MYSQL_PORT>/<MYSQL_DB>` | SQL/transactions | compte applicatif MySQL | SQLAlchemy | pool: 10; timeout pool 10 s; pre_ping; recycle 1800 s | Partiel |
| PHP ↔ Backend | `<INSTANCE_PROTOCOL>://<BACKEND_PYTHON_DOCKER_URL>:<BACKEND_PYTHON_DOCKER_PORT>/<path>` | GET, POST, PUT, PATCH, DELETE par `/api.php` | JWT Bearer dans `Authorization`; session PHP locale | JSON pour écriture, form pour auth | cURL 30 s; pas de retry | Confirmé |
| Next.js ↔ Backend | même construction d'URL; `/token`; `/api/proxy/<path>` | POST/GET sur le proxy; POST credentials sur `/token` | NextAuth JWT en session/cookie; proxy transmet aussi le cookie | form-urlencoded pour `/token`; JSON en réponse | Aucun timeout Axios explicite; aucun retry | Partiel |
| Dash ↔ Backend | même variables Docker; chemin `/...` | GET, POST, PATCH, DELETE | JWT Bearer | GET/query ou JSON; retour JSON puis DataFrame | 30 s; pas de retry | Confirmé statiquement + test HTTP simulé |
| Dash ↔ Groq | `https://api.groq.com/openai/v1/chat/completions` | POST | clé `GROQ_API_KEY` | JSON OpenAI-compatible | 60 s; 429/401/HTTP gérés; pas de retry HTTP | Partiel |

## 3. Détail des intégrations

### 3.1 Backend Python ↔ MySQL

**Appelant/destinataire**

Le Backend Python ouvre une connexion SQLAlchemy vers MySQL. C'est un contrat
database, pas HTTP.

**Configuration confirmée**

- `MYSQL_SERVER` : hôte Docker.
- `MYSQL_PORT` : port interne du serveur, `3306` dans le squelette.
- `MYSQL_DB` : base.
- `MYSQL_USER_LOGIN` : utilisateur applicatif.
- `MYSQL_USER_PASSWORD` : mot de passe applicatif.
- `MYSQL_ROOT_PASSWORD` : provisionnement du conteneur; non consommé directement
  par le Backend.
- `DB_DRIVER` : `mysql+mysqlconnector` par défaut.
- `DB_POOL_SIZE` : `10` par défaut.
- `DB_MAX_OVERFLOW` : `10` par défaut.

**Comportement confirmé**

- Driver SQLAlchemy avec `pool_pre_ping=True`.
- `pool_recycle=1800`.
- Timeout du pool : 10 secondes.
- Le Backend retourne HTTP 503 pour une base indisponible ou un pool saturé
  dans les chemins où l'erreur est interceptée.

**Incohérence à résoudre**

Le squelette d'environnement déclare
`MYSQL_SERVER=learnagement_mysql_<INSTANCE_NAME>`, mais `env.py` produit
`learnagement_data_mysql_<INSTANCE_NAME>`. Le générateur Compose crée réellement
`learnagement_data_mysql_<INSTANCE_NAME>`. Le contrat applicable à un lancement
Compose est donc le nom produit par `env.py`, à confirmer auprès du responsable
de configuration avant la prochaine génération.

**Non démontré**

- Compatibilité de tous les scripts SQL avec MySQL 8.4.
- Runtime de la connexion.
- Initialisation fonctionnelle du schéma.
- Résolution DNS depuis un nouveau checkout isolé.

Références : [connection.py](../backend_python/db/connection.py),
[docker_compose.py](../docker_compose.py),
[env.py](../env.py), [__env_skeleton.env](../__env_skeleton.env).

### 3.2 PHP ↔ Backend Python

**Contrat local PHP → Backend**

PHP construit l'URL avec `INSTANCE_PROTOCOL`,
`BACKEND_PYTHON_DOCKER_URL`, `BACKEND_PYTHON_DOCKER_PORT` puis ajoute le chemin
sans duplication des slashs. Le port doit correspondre au port interne `4000`,
pas nécessairement au port hôte publié.

Le proxy PHP limité aux méthodes GET, POST, PATCH, PUT et DELETE valide :

- méthode autorisée;
- chemin strictement limité à des caractères sûrs;
- taille maximale déclarée et streaming limitée à 1 Mo;
- session PHP locale;
- JWT porté à la requête sous `Authorization: Bearer <token>`.

**Authentification**

La connexion locale POST `/login` envoie `username`, `password` et
`grant_type=password` sous form-urlencoded vers `/token`. Le Backend répond avec
`access_token` et `token_type`. PHP vérifie le JWT HS256 avec
`JWT_SIGNING_KEY`, la date d'expiration et stocke le JWT en session.

CAS est géré par un chemin distinct prévu via `/token-cas` avec le header
`X-Cas-Token` et `CAS_SERVICE_TOKEN`. Sa disponibilité runtime reste à
vérifier.

**Erreurs**

- cURL utilise un timeout de 30 secondes.
- une absence de réponse produit `status=0` côté proxy.
- PHP renvoie 502 avec `Backend unavailable` en cas d'exception;
- PHP normalise les codes hors intervalle à 502;
- les autres codes HTTP du Backend sont propagés.
- aucun retry n'est implémenté.

**Test existant**

Le script `smoke_services.py` vérifie un proxy PHP vers `/health`, mais cette
vérification suppose des services externes et une URL configurée. Elle n'a pas
été exécutée dans cette mission.

Références : [api.php](../front_PHP/api.php),
[apiProxy.php](../front_PHP/utils/apiProxy.php),
[endpoint.php](../front_PHP/utils/endpoint.php),
[login.php](../front_PHP/views/base/@post/login.php).

### 3.3 Next.js ↔ Backend Python

**Authentification**

NextAuth utilise les identifiants locaux pour POST `/token` sous
`application/x-www-form-urlencoded`. Il vérifie `access_token`, décode le JWT,
contrôle `exp`, puis conserve l'utilisateur et le JWT dans sa session NextAuth.

**Proxy**

`app/api/proxy/[...phpPath]/route.ts` accepte GET et POST, reconstruit
l'appel vers le Backend avec les variables Docker, transmet le cookie entrant,
le `Content-Type` et le corps pour POST. Il ne transmet pas explicitement
`Authorization: Bearer`; il délègue au cookie entrant. Son format de réponse
est JSON.

**Erreurs**

- un échec est converti en HTTP 500 avec un message contenant l'URL Backend;
- aucun timeout Axios explicite n'est configuré;
- aucun retry n'est configuré;
- les méthodes PUT/PATCH/DELETE ne sont pas exposées par cette route;
- le proxy ne conserve pas le code HTTP Backend en cas d'erreur : il utilise
  actuellement 500.

**À confirmer**

- la transmission effective du cookie et du JWT NextAuth aux routes Backend;
- le comportement attendu des codes non 200;
- le timeout réseau runtime;
- l'usage réel du handler côté Next.js dépendant de sa configuration Docker.

Références : [NextAuth](../front_NextJS/app/api/auth/[...nextauth]/route.ts),
[proxy Next.js](../front_NextJS/app/api/proxy/[...phpPath]/route.ts).

### 3.4 Dash/Plotly ↔ Backend Python

**Contrat confirmé dans le code**

Dash construit les URLs avec `INSTANCE_PROTOCOL`,
`BACKEND_PYTHON_DOCKER_URL` et `BACKEND_PYTHON_DOCKER_PORT`. Il envoie
`Authorization: Bearer <jwt>`.

- GET : paramètres en query, form-urlencoded.
- POST/PATCH : JSON.
- DELETE : sans corps, form-urlencoded.
- succès JSON listés : conversion en `pandas.DataFrame`.
- un objet JSON avec `{"success": true, "data": ...}` est converti en `data`.
- un retour vide devient un DataFrame vide.

**Erreurs**

- timeout fixe de 30 secondes.
- vérification TLS avec le certificat interne `cert.pem`.
- 401 : `Token invalide ou expiré`.
- 403 : `Accès refusé - l'utilisateur n'a pas le rôle requis`.
- `raise_for_status()` pour les autres erreurs HTTP.
- `Timeout` et `RequestException` sont propagés.
- aucun retry.

**Authentification Dash**

Dash utilise une session Flask et un JWT. Il vérifie l'expiration avec une
marge de leeway de 30 secondes et stocke le token dans la session.

**Test existant**

`tests/integration/test_dash_backend_http_contract.py` vérifie un serveur HTTP
simulé pour GET/POST/PATCH/DELETE, le header Bearer, les formats, les réponses
vides, 503 et timeout. Le test a été exécuté dans une mission antérieure mais
n'a pas été relancé dans cette mission; il ne remplace pas un appel runtime au
Backend réel.

Références : [app_tools.py](../front_DashPlotly/app_tools.py),
[auth Dash](../front_DashPlotly/auth.py),
[test Dash/Backend](../tests/integration/test_dash_backend_http_contract.py).

### 3.5 Préparation du futur service IA

**État actuel**

Un chatbot APC existe dans le module Dash. Il appelle directement l'API Groq
avec `GROQ_API_KEY`, puis ses fonctions locales interrogent les APIs Backend
via Dash `app_tools`. Ce n'est pas une intégration par un service IA autonome
discutant directement avec FastAPI.

**Contrat actuellement partiellement confirmé**

- destination Groq : `https://api.groq.com/openai/v1/chat/completions`;
- méthode POST;
- modèle fixe `llama-3.3-70b-versatile`;
- payload JSON avec historique, modèle, outils et `max_tokens=1500`;
- timeout 60 secondes;
- gestion des statuts 429, 401 et autres HTTP;
- jusqu'à huit itérations pour résoudre des appels d'outils;
- les outils exécutent ensuite les appels Dash/Backend avec le JWT utilisateur.

**Non implémenté**

- aucun endpoint Learnagement/Backend dédié au futur service IA n'est confirmé;
- aucun contrat d'orchestration IA ↔ Backend autre que les outils locaux
  Dash n'est disponible;
- aucun service IA indépendant, déployable séparément, ni contrat réseau propre
  n'est confirmé;
- aucun endpoint ou format centralisé ne doit être inventé.

Le responsable IA devra fournir : URL/service réseau, endpoint, méthode,
payload, authentification, format des réponses, erreurs, timeout, retry,
modèle/provider, taille maximale des messages, et gestion des données
pédagogiques.

Références : [chatbot Groq](../front_DashPlotly/apc_dash/apc20_chatbot_backend.py),
[outils chatbot](../front_DashPlotly/apc_dash/apc20_chatbot_tools.py).

## 4. Incohérences et risques identifiés

1. **MySQL** : le nom `learnagement_mysql_<INSTANCE_NAME>` du squelette diffère
   du nom `learnagement_data_mysql_<INSTANCE_NAME>` produit par `env.py` et le
   générateur. Ce point doit être fermé avant l'intégration Backend.
2. **Next.js** : le proxy capture toutes les erreurs en HTTP 500 et expose
   actuellement l'URL Backend dans le corps d'erreur. Les responsables Next.js
   doivent fournir le traitement attendu.
3. **Next.js** : aucune gestion explicite de timeout/retry n'est visible.
4. **PHP/CAS** : le flux local est confirmé dans le code, tandis que
   `/token-cas` dépend de variables CAS et d'un token de service interne dont
   la configuration locale effective n'est pas démontrée.
5. **Sécurité** : plusieurs contrats transportent ou acceptent des JWT dans
   des sessions/cookies/URLs. Les besoins exacts de sécurité doivent être
   testés; Dash contient des liens avec `jwt_token` en query, à valider avant
   de le considérer comme stable.
6. **HTTPS** : PHP et Dash vérifient ou peuvent vérifier un certificat interne;
   le mode et les chemins réels doivent être validés en environnement isolé.
7. **Backend** : les tests unitaires couvrent 401/403/500/503 sur différents
   chemins, mais aucun test runtime global ne vérifie les communications.

## 5. Informations à confirmer auprès des responsables

- **Responsable Backend/MySQL** : nom canonique `MYSQL_SERVER`, état du schéma,
  migrations obligatoires avant démarrage, comportement 503/500 et timeout réel.
- **Responsable PHP** : contrats HTTP complets exposés au proxy, traitement CAS,
  CSRF, taille maximale et codes d'erreur attendus.
- **Responsable Next.js** : politique des codes d'erreur, timeout/retry,
  méthodes proxy exposées et transmission du JWT/cookie.
- **Responsable Dash** : durée de session, transport du JWT, disponibilité du
  certificat, formats JSON/DataFrame et comportement hors ligne du Backend.
- **Responsable IA** : service, URL réseau, endpoint, contrat JSON, sécurité,
  timeout, retry, limites, dépendances et propriétaire de `GROQ_API_KEY`.

## 6. Matrice de préparation des tests d'intégration

| Test | Préconditions | Action | Résultat attendu | Preuve à collecter | Statut |
|---|---|---|---|---|---|
| Backend ↔ MySQL | MySQL neuf isolé, `.env` local, scripts disponibles | Ajouter puis démarrer le Backend seulement après MySQL healthy | Connexion applicative, lecture simple réussie, pool disponible | logs Backend, état SQLAlchemy, requête de lecture autorisée | Bloqué par ressources/runtime |
| PHP vers `/token` | MySQL + Backend démarrés | Soumettre des identifiants factices validés par données de test | 200 + `access_token`; mauvais mot de passe = 401 | réponse HTTP redacted, logs, header WWW-Authenticate | À créer; données réelles nécessaires |
| PHP vers `/api.php` | session PHP avec JWT factice/valide | GET `/health` puis route protégée avec/sans JWT | santé propagée; JWT valide autorisé; absent/expiré = 401/403 | status, corps, headers Bearer observés | Test statique possible; runtime bloqué |
| Next.js `/token` | Backend disponible | POST form-urlencoded avec compte factice | 200, JWT décodé, NextAuth session créée | status NextAuth, payload redacted, cookie | À créer; runtime bloqué |
| Next.js proxy | session NextAuth valide | GET `/api/proxy/health` puis route Backend protégée | Backend status conservé en succès/erreur | status, cookie, logs proxy | À créer; runtime bloqué |
| Dash vers Backend | JWT valide, certificat interne disponible | GET/POST/PATCH/DELETE vers endpoints factices | formats corrects, Bearer propagé, DataFrame attendu | log HTTP serveur simulé ou réel; réponse | Test simulé existant; réel bloqué |
| Dashboard indisponible | arrêter uniquement la simulation, pas DEV | appeler les fonctions Dash avec Backend injoignable | Timeout/RequestException propagé sans données trompeuses | test timeout, durée, exception | Test simulé existant |
| Erreur Backend 503 | mock ou instance contrôlée | appeler une route avec base indisponible | 503 reconnu; aucune donnée fallback silencieuse | status, détail, logs | Test Dash simulé existant; global à créer |
| Backend MySQL pool saturé | base réelle isolée | dépasser le pool par chargement contrôlé | 503 "Database busy" ou indisponibilité explicite | status/log/error | À créer; bloqué dépendance DB |
| IA disponible | contrat du responsable fourni | demander une réponse normale puis une indisponibilité provider | contrat stabilisé, erreur 429/401/timeout exploitable | payload, status, traces redacted | Bloqué: service/contrat non implémenté |

## 7. Tests existants

- `tests/integration/test_dash_backend_http_contract.py` : contrat HTTP
  Dash/Backend simulé; confirme méthodes, Bearer, JSON, 503 et timeout.
- `tests/integration/smoke_services.py` : smoke health PHP/Backend/Next/Dash,
  PHP→Backend et Next→Backend lorsque le cookie est fourni.
- Backend : tests unitaires de 401/403/503/500 et ownership.
- Compose : test de sélection MySQL, dépendances et ordre; validation statique.

Ces tests démontrent des comportements locaux ou simulés. Aucun ne prouve
l'ensemble des communications sur une stack Docker démarrée.

## 8. Avancement de l'étape 6

L'étape 6 est **partiellement convergente** :

- PHP ↔ Backend et Dash ↔ Backend ont des contrats suffisamment documentés pour
  préparer des tests d'intégration.
- Next.js ↔ Backend est partiellement confirmé; ses politiques d'erreur et son
  timeout restent incomplets.
- Backend ↔ MySQL est structurellement confirmé mais sa connexion et son
  initialisation restent bloquées par le runtime.
- Le futur service IA reste une préparation technique; aucun contrat entre un
  service IA autonome et Backend n'est actuellement implémenté.

La convergence devient exploitable pour la préparation de l'étape 7, mais
aucune intégration réelle n'est déclarée validée.

## 9. Questions techniques ouvertes par la phase de coordination

Les réponses suivantes ne doivent pas être déduites du code : elles exigent
la confirmation du propriétaire compétent.

### PHP / CAS

- Quel est le statut runtime réel de `/token-cas` et du header
  `X-Cas-Token` dans l'environnement intégré?
- Quel est le jeu de cas de test approuvé pour un utilisateur déjà connu,
  un nouvel utilisateur et un groupe non autorisé?
- La création CAS doit-elle rester approuvée côté propriétaire des données?

### Next.js

- Quel timeout réseau doit être déclaré côté proxy et côté NextAuth?
- Quel comportement est attendu pour 401, 403, 404, 429, 502 et 503?
- Le cookie entrant doit-il être remplacé par une transmission explicite
  `Authorization: Bearer`?
- Une politique de retry est-elle souhaitée ou explicitement interdite?

### Dash

- Quel certificat interne est disponible dans les images et les environnements
  réellement déployés?
- Quels endpoints GET protégés peuvent servir de smoke-tests sans effet de bord?
- Quels comptes ou jetons de test sont approuvés pour 401/403/200?

### IA

- L'intégration Groq existante dans Dash représente-t-elle uniquement un
  connecteur applicatif direct ou existe-t-il un service autonome prévu?
- Si un service autonome est prévu, quel URL, endpoint, méthode, payload,
  authentification, timeout, retry et format d'erreur doivent être fournis?

### Backend / MySQL

- Quel est le nombre et quels sont les noms exacts des tables nécessaires après
  initialisation?
- `/health` doit-il rester limité au processus HTTP ou devenir une readiness
  vérifiant DNS/TCP, authentification ou schéma?
- Quels 401/403/503/500 doivent être testés sur quels endpoints GET?
