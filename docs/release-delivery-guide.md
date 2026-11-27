# Guide de livraison Learnagement

Ce guide consolide les procédures déjà présentes dans le dépôt pour préparer
une livraison. Il ne remplace ni les contrats applicatifs, ni les procédures
isolées, ni les gates Kubernetes. Il ne constitue pas une preuve de validation
runtime.

## Présentation générale

Learnagement est l'application d'intégration pédagogique développée par les
étudiants de Polytech Annecy / USMB. Le dépôt réunit un Backend Python,
plusieurs interfaces web, MySQL, des services de configuration et les bases
préparatoires pour Docker Compose et Kubernetes.

Ce guide couvre l'orchestration technique globale : Docker, Compose, réseaux,
configuration, contrats interservices, fiabilisation, tests d'intégration,
préparation Kubernetes, CI/CD et documentation de livraison.

Les modules Backend, PHP, Next.js, Dash et IA restent sous la responsabilité
de leurs développeurs respectifs. L'orchestrateur ne modifie pas leur logique
métier sans décision coordonnée et preuve d'un défaut d'orchestration.

### Organisation des responsabilités

| Domaine | Responsable logique |
|---|---|
| Docker, Compose, réseaux, volumes et ressources | Orchestration |
| API, SQLAlchemy, authentification Backend | Développeur Backend |
| Proxy PHP, session PHP et CAS | Développeur PHP |
| NextAuth, proxy Next.js et gestion des cookies | Développeur Next.js |
| Dash, Plotly, TLS interne et chatbot | Développeur Dash |
| Service IA autonome ou intégration fournisseur | Développeur IA |
| Manifests, Secrets, stockage et rollout | Orchestration avec propriétaire Kubernetes |
| Livraison finale et registre d'images | Orchestration, après autorisation |

## 1. État actuel de livraison

**Révision de référence :** `dev`, `315d5753fc05464b1ff912e5c36d3b54c33d2c00`.

Le checkout contient des modifications locales préexistantes. Elles doivent
être conservées et distinguées des livrables de cette étape.

Le relevé suivant est **historique** et ne constitue pas une mesure actuelle :

- l'analyse statique, les tests isolés et la préparation Kubernetes sont
  avancés ;
- aucun démarrage runtime MySQL/Backend contrôlé n'a été réalisé ;
- la mémoire Windows libre mesurée alors était de 0,62 Gio, sous le seuil
  prudentiel de 1,5 Gio ;
- les neuf conteneurs DEV doivent rester actifs et inchangés ;
- aucune ressource Docker de l'environnement isolé n'a été créée.

Ces limites sont des faits observés, pas des résultats attendus masqués.

## 2. Sources de vérité

- [Installation locale](../Doc/Installation.md) : préparation Python, `.env`,
  démarrage et arrêt ;
- [Premier démarrage MySQL isolé](mysql-first-start.md) : préparation et
  validation MySQL seule ;
- [Runbook validation Backend/MySQL](backend-mysql-validation-runbook.md) :
  séquence opérationnelle préparée pour MySQL puis le Backend ;
- [Contrats interservices](interservice-contracts.md) : intégrations,
  preuves et informations à confirmer ;
- [Plan de tests d'intégration](integration-test-plan.md) : tests isolés,
  tests simulés et validations runtime bloquées ;
- [Préparation Kubernetes](kubernetes-readiness.md) : état des images,
  manifests, probes et risques ;
- [Checklist Kubernetes](kubernetes-deployment-checklist.md) : gates avant
  déploiement ;
- [Images Kubernetes](../docker/kubernetes/README.md) : Dockerfiles,
  conventions et limites des builds ;
- [Base Kubernetes](../kubernetes/base/README.md) : rendu statique,
  configuration externe et blocages.

## 3. Architecture opérationnelle actuelle

| Composant | Rôle confirmé | Communication | Persistance |
|---|---|---|---|
| MySQL | Schéma, données applicatives et scripts d'initialisation | SQLAlchemy depuis le Backend sur le réseau Docker interne | Volume Docker ou PVC futur |
| Backend Python / FastAPI | API applicative, authentification et accès SQLAlchemy | HTTP interne vers les fronts | Aucun stockage applicatif principal connu |
| PHP | Interface serveur et proxy des requêtes applicatives | HTTP vers le Backend | Session PHP selon l'implémentation existante |
| Next.js | Interface web, NextAuth et proxy API | HTTP et cookie vers le Backend | Aucun stockage applicatif documenté ici |
| Dash / Plotly | Interface d'analyse et chatbot | HTTP vers le Backend; Groq directement depuis le module chatbot | Aucun stockage persistant défini ici |
| phpMyAdmin | Administration manuelle DEV | HTTP vers MySQL | Aucun volume applicatif propre |
| Service IA futur | Intégration non confirmée | Contrat à fournir par le responsable IA | Aucun choix retenu |

Les détails et niveaux de preuve restent définis dans
[Contrats interservices](interservice-contracts.md).

## 4. Configuration sans exposition des secrets

Les fichiers `.env` sont ignorés par Git. Ne copier aucun secret dans le dépôt,
les tickets, les captures ou les journaux.

Variables et groupes à préparer :

- identité d'instance : `INSTANCE_NAME`, `COMPOSE_PROJECT_NAME`,
  `INSTANCE_PROTOCOL`, `INSTANCE_URL`, `INSTANCE_IP` ;
- MySQL : `MYSQL_SERVER`, `MYSQL_PORT`, `MYSQL_DB`, `MYSQL_USER_LOGIN`,
  `MYSQL_USER_PASSWORD`, `MYSQL_ROOT_PASSWORD` ;
- Backend : `BACKEND_PYTHON_DOCKER_URL`, `BACKEND_PYTHON_DOCKER_PORT`,
  `BACKEND_PYTHON_PORT` ;
- sécurité : `JWT_SIGNING_KEY`, `CAS_SERVICE_TOKEN` ;
- CAS : variables `CAS_*` consommées par les modules PHP/Backend ;
- fronts : ports et URLs propres à PHP, Next.js et Dash ;
- IA : `GROQ_API_KEY` pour le chatbot Dash existant. Aucun contrat autonome
  Backend/IA n'est confirmé.

Résolution confirmée :

- [env.py](../env.py) charge le squelette puis remplace
  `MYSQL_SERVER` par `learnagement_data_mysql_<INSTANCE_NAME>`.
- [__env_skeleton.env](../__env_skeleton.env) conserve encore une ancienne
  valeur `learnagement_mysql_<INSTANCE_NAME>`, mais cette valeur est écrasée
  par `env.py` lors de la génération.
- [docker_compose.py](../docker_compose.py) crée le service
  `data_mysql_<INSTANCE_NAME>`, le conteneur
  `learnagement_data_mysql_<INSTANCE_NAME>` et le réseau
  `learnagement_back_<INSTANCE_NAME>`.

La configuration effective doit néanmoins être inspectée avant tout démarrage :
une différence éventuelle entre `.env`, `MYSQL_SERVER`, le service Compose et
le conteneur rendrait l'isolation ou la résolution DNS ambiguë.

### Génération interactive de `.env`

`env.py` propose `Learnagement.py generate-env --env dev|prod`. Son chargement
normal demande `INSTANCE_NAME`, puis génère les secrets CAS/JWT/NextAuth et les
mot de passe MySQL/administrateur via `__generate_base_env()`.

Cette commande écrit `.env.default`, peut créer les fichiers d'environnement
spécifiques, écrit `.env`, puis `propagate_env()` copie `.env` vers les modules
applicatifs configurés. Elle ne doit donc pas être utilisée pour préparer
uniquement MySQL lorsqu'un environnement DEV existe déjà.

Pour l'isolation MySQL, privilégier une configuration locale limitée à un
checkout dédié. Le fichier `.env` reste en clair côté stockage pour être lu par
Python, Docker Compose et les modules; `Read-Host -AsSecureString` masque la
saisie mais ne suffit pas à chiffrer le fichier final. Les permissions Windows
doivent être restreintes et les secrets ne doivent jamais être placés dans
l'historique, les journaux ou un argument de commande.

## 5. Installation reproductible

1. Préparer Python et `.venv` selon
   [Installation locale](../Doc/Installation.md).
2. Vérifier Docker Desktop et le moteur Linux, sans arrêter les environnements
   DEV existants.
3. Générer `.env` avec le CLI uniquement dans le checkout concerné.
4. Vérifier localement les noms, ports, clés de sécurité et paramètres
   MySQL sans afficher les valeurs.
5. Générer Compose avec le mécanisme existant.
6. Utiliser une procédure de démarrage conforme à l'instance choisie.
7. Vérifier les états, healthchecks, journaux et chemins d'accès selon le type
   de validation.

Sous Windows, l'environnement natif n'a pas été validé comme environnement
runtime principal. WSL2 Ubuntu reste la voie Linux recommandée lorsque le
projet doit utiliser les scripts Unix et Docker avec un comportement cohérent.

## 6. Démarrage et arrêt

Pour l'usage DEV normal, les commandes documentées dans
[Installation locale](../Doc/Installation.md) sont :

- démarrage : `python Learnagement.py start --env dev` ;
- arrêt : `python Learnagement.py stop`.

La commande normale doit préserver le volume MySQL. Une option
`--from_scratch` est destructive : elle supprime les données locales et le
volume. Elle exige une sauvegarde vérifiée et une autorisation explicite.

Le premier démarrage runtime MySQL doit suivre
[Premier démarrage MySQL isolé](mysql-first-start.md). Il doit rester séparé
du démarrage complet et utiliser un projet Compose, des conteneurs, réseaux
et volumes uniques. Aucun port MySQL ne doit être publié.

## 7. MySQL, initialisation et persistance

Les dix scripts sous `db/sql` sont destinés à un premier volume neuf. Ils ne
doivent pas être rejoués manuellement sur une base existante :

- `V0.0.0__schema_init.sql` contient de nombreux `DROP TABLE IF EXISTS`;
- `V0.1.8_trim_remove_htdtp_correct_DBbugs.sql` contient des `ALTER`,
  `DROP INDEX`, `DROP COLUMN` et `RENAME TABLE`;
- `V0.2.0_update_mobility.sql` contient notamment des `DROP TABLE IF EXISTS`;
- `V0.2.8_clean_mobility.sql` contient des `ALTER TABLE` et des suppressions
  de colonnes;
- `V0.3.8_clean_CAS_login.sql` contient des changements de colonnes et des
  suppressions de tables;
- `V0.99.0__trigger_init.sql` contient `DELIMITER` et des triggers avec
  `DEFINER`;
- tous les scripts ne sont pas automatiquement destructifs : les scripts
  `ALTER` peuvent être non répétables ou structurants sans supprimer de données
  directement, mais ils restent risqués sur une base existante;
- l'ordre alphabétique progresse du schéma aux migrations puis aux triggers ;
- une initialisation interrompue ne constitue pas une base vierge ;
- le montage d'initialisation doit rester en lecture seule.

Une validation MySQL acceptable exige :

- conteneur `running` ;
- healthcheck `healthy` ;
- absence d'erreur critique dans les journaux ;
- connexion authentifiée avec le compte applicatif ;
- `SELECT 1` ;
- vérification séparée des tables attendues.

La simple présence de l'état `running` ou d'un port TCP ne prouve ni la
connexion authentifiée, ni la présence du schéma.

## 8. Sauvegarde, reprise et incident

### Sauvegarde

`Learnagement.py` expose une commande de sauvegarde de la structure, des données
et des triggers. Le code indique que cette fonction n'est pas implémentée sous
Windows. Ne pas la présenter comme une sauvegarde Windows validée. Dans sa
branche Linux/WSL, son implémentation doit aussi être qualifiée : elle référence
encore `learnagement_mysql_<INSTANCE_NAME>` dans
[Learnagement.py](../Learnagement.py), tandis que le Compose actuel génère
`learnagement_data_mysql_<INSTANCE_NAME>` dans
[docker_compose.py](../docker_compose.py). Cette commande n'a donc pas été
validée comme procédure de sauvegarde réutilisable.

Une nouvelle procédure de sauvegarde ou l'adaptation vérifiée de la commande
existante exige une autorisation, un conteneur de test approuvé hors des volumes
DEV, puis une restauration de preuve. Les données, noms de compte et secrets ne
doivent pas apparaître dans les preuves.

### Arrêt contrôlé

1. préserver les données et les volumes ;
2. arrêter uniquement l'instance ou le service concerné avec sa configuration
   Compose/Kubernetes approuvée ;
3. conserver les journaux et l'état avant modification ;
4. ne pas utiliser `down -v`, le nettoyage Docker ou la suppression de volume
   comme procédure de diagnostic.

### Reprise après incident

- MySQL non sain : ne pas démarrer ou ajouter le Backend; conserver le volume
  isolé pour diagnostic ;
- Backend indisponible : vérifier MySQL, DNS Docker, variables et journaux ;
- Front indisponible : vérifier sa dépendance Backend et ne pas modifier les
  contrats pour masquer l'incident ;
- initialisation SQL interrompue : ne pas rejouer les scripts sur ce volume ;
- conflit de nom Docker : changer l'identifiant d'instance et vérifier les
  ressources; ne pas supprimer une ressource existante.

Toute restauration exige une sauvegarde vérifiée et un propriétaire désigné
pour les données. Ces procédures doivent être testées après autorisation d'un
environnement runtime isolé.

## 9. Preuves et limites actuelles

| Niveau | Résultat réel |
|---|---|
| Statique | CLI, génération Compose, Kubernetes et contrats vérifiés sur les sources |
| Test isolé | Suite ciblée de l'étape 7 exécutée sans Docker réel |
| Simulation HTTP | Dash testé avec un serveur HTTP simulé |
| Docker runtime | Aucun démarrage MySQL/Backend isolé après les préflights |
| Authentification runtime | Non validée |
| Persistance/reprise | Non validée |
| Parcours PHP/Next.js | Tests statiques ou mocks seulement |
| Déploiement Kubernetes | Socle statique; aucun cluster appliqué |
| Service IA | Préparation documentaire seulement |

La mémoire Windows limitée à 0,62 Gio lors du relevé historique était un
blocage technique réel à ce moment. Elle ne constitue pas une mesure actuelle
et ne remplace pas un nouveau préflight avant toute opération Docker.

### Portée des 28 tests ciblés

Le nombre a été vérifié par collecte pytest statique :

| Fichier | Nombre | Portée |
|---|---:|---|
| `test_compose_startup_order.py` | 1 | Génération statique Compose, sélections MySQL/MySQL+Backend, dépendances |
| `test_backend_mysql_contract.py` | 7 | Construction SQLAlchemy simulée, cinq noms MySQL manquants paramétrés et port invalide |
| `test_http_contract_sources.py` | 9 | Vérifications statiques PHP, Next.js, NextAuth, CAS, Groq et Backends |
| `test_dash_backend_http_contract.py` | 10 | Serveur HTTP local simulant méthodes, Bearer, 401/403/503, timeout et JSON |
| `test_windows_cli_import.py` | 1 | Compatibilité d'import du CLI Windows |

Total collecté : **28 cas pytest**.

Ces tests couvrent les sources et des comportements locaux/simulés. Ils ne
ouvrent pas de connexion MySQL réelle, ne démarrent pas Docker et ne prouvent
aucune intégration runtime PHP, Next.js, Dash, Backend ou IA complète.

## 10. Position dans la feuille de route

| Étape | Statut | Travail accompli | Preuve disponible | Travail restant |
|---|---|---|---|---|
| 4.2 — Préparation | **PARTIEL** | Compose sélectif, services, réseaux, volumes, healthchecks et image MySQL préparés | Sources Compose et tests statiques | `.env`, nom d'instance unique, collisions et Compose MySQL-only validés | Orchestration | Validation statique du Compose et absence de collision |
| 4.3 — Premier démarrage | **BLOQUÉ** | Runbooks MySQL seul et MySQL vers Backend préparés | Documents et matrice de preuve | RAM >= 1,5 Gio, secrets, volume neuf, autorisation et démarrage | Orchestration + propriétaire données | Conteneur running/healthy, journal propre, SQL authentifié, base et tables vérifiés |
| 4.4 — Communications | **PARTIEL** | URLs, ports, méthodes, JWT et formats comparés | Code source et tests Dash/HTTP statiques | Runtime PHP, Next.js, Dash, CAS et Backend | Propriétaires des fronts/Backend | Appels réels HTTP réussis ou erreurs attendues documentées |
| 4.5 — Fiabilisation | **PARTIEL** | Dépendances, healthchecks HTTP/TCP préparés | Compose, Kubernetes et code Backend | Panne/reprise, persistance et indisponibilité MySQL | Orchestration + Backend + données | Scénarios de reprise reproductibles avec preuves |
| 5 — Service IA | **PARTIEL** | Chatbot Dash/Groq identifié | Code chatbot Groq | Contrat et intégration autonome IA/Backend | Propriétaire IA | Service et contrat validés, avec tests runtime |
| 6 — Contrats interservices | **PARTIEL** | Contrats Backend/MySQL, PHP, Next.js, Dash et Groq consolidés | `docs/interservice-contracts.md` | Réponses propriétaires aux écarts | Responsables des modules | Chaque contrat est confirmé ou rejeté par une preuve |
| 7 — Tests globaux | **PARTIEL** | 28 cas pytest collectés, dont tests statiques, simulés et paramétrés | Résultat pytest réel hors Docker | Runtime Docker, auth, persistance, PHP/Next.js/IA | Orchestration + propriétaires | Suite runtime globale exécutée dans un environnement isolé |
| 8 — Documentation/livraison | **PARTIEL** | Guides, contrats, plan de tests, Kubernetes et checklist disponibles | Documents vérifiés et liens locaux | Sauvegarde/restauration, secrets, registry, Kubernetes et décisions | Orchestration + Kubernetes | Livraison approuvée avec preuves et rollback |

### Travaux prioritaires

**P0 — bloquants pour franchir l'étape 4.3**

- Orchestration : obtenir au moins 1,5 Gio de RAM Windows libre puis relancer uniquement le préflight.
- Orchestration : choisir un identifiant unique et vérifier conteneur, projet, réseau et volume.
- Orchestration : fournir localement les quatre variables MySQL réelles sans les placer dans le dépôt ou les logs.
- Orchestration : préparer puis valider un staging SQL neuf, sans données privées.
- Propriétaire données : autoriser l'utilisation des scripts sur un volume neuf et valider la liste des tables attendues.

**P1 — nécessaires à l'intégration**

- Orchestration/Backend : démarrer MySQL seul, puis Backend, avec preuve DNS/TCP, authentification, schéma et lecture.
- Backend : confirmer que `/health` reste limité ou fournir séparément une readiness dépendante de MySQL.
- PHP : confirmer CAS, session, timeout et exposition des erreurs.
- Next.js : confirmer cookie/JWT transmis, timeout, retry et codes d'erreur.
- Dash : confirmer le contrat TLS/certificat interne et les comptes de test.
- IA : fournir service, URL, méthode, payload, authentification, erreurs, retry et timeout.

**P2 — nécessaires aux tests et à la livraison**

- Orchestration : ajouter les tests statiques réellement manquants identifiés par les propriétaires.
- Orchestration : exécuter les scénarios de reprise sans toucher aux services DEV.
- Orchestration : valider sauvegarde/restauration hors des volumes DEV.
- Orchestration : remplacer les placeholders Kubernetes après smoke-tests autorisés.
- Orchestration : vérifier registry, Secrets externes, stockage, TLS, réseau et rollback.
- Responsable Kubernetes : approuver le cluster cible et sa fenêtre de déploiement.

## 11. Déploiement Kubernetes

Le Kubernetes fourni dans `kubernetes/base/` est préliminaire :

- aucune application n'a été déployée sur un cluster ;
- les tags d'image doivent être remplacés uniquement après build, registry et
  autorisation ;
- les Secrets externes, la StorageClass, les backups, le TLS, le DNS et le
  rollback restent à valider ;
- le Backend n'effectue pas de migration DDL au démarrage ;
- les scripts SQL Compose ne sont pas un mécanisme de migration Kubernetes ;
- les probes ne démontrent pas les parcours métier ni la connexion au schéma.

Suivre la [checklist Kubernetes](kubernetes-deployment-checklist.md) sans
appliquer les manifests avant que tous les gates soient autorisés.

## 12. Checklist de livraison

- [ ] mémoire suffisante pour l'environnement runtime isolé ;
- [ ] checkout livré et modifications locales acceptées ;
- [ ] `.env` complet sans secret versionné ;
- [ ] noms Compose, conteneurs, réseaux et volumes uniques ;
- [ ] image `mysql:8.4` disponible localement ou approvisionnée séparément ;
- [ ] scripts SQL vérifiés, nouveau volume uniquement ;
- [ ] MySQL authentifié, schéma confirmé ;
- [ ] Backend démarré seulement après MySQL ;
- [ ] `/health` interprété selon sa portée réelle ;
- [ ] tests Backend, PHP, Next.js, Dash et IA planifiés ;
- [ ] sauvegarde vérifiée avant toute évolution destructive ;
- [ ] Kustomize et validation statique exécutés ;
- [ ] registry, Secrets, stockage, réseau, TLS et rollback approuvés ;
- [ ] preuves de déploiement collectées sans exposer les secrets.

## 13. Point d’entrée de reprise

### Rôle de l’orchestrateur

Le rôle d’orchestration couvre Docker/Compose, configuration, réseaux,
contrats interservices, fiabilisation, tests globaux, Kubernetes et livraison.
Les modules Backend, PHP, Next.js, Dash et IA restent sous la responsabilité
de leurs développeurs. L’orchestrateur ne modifie leur logique métier que
coordonné avec eux et seulement lorsqu’une erreur d’orchestration le justifie.

### Bilan vérifié

- Les travaux jusqu’à la Mission 50 sont présents dans le checkout.
- 28 tests locaux ciblés ont été validés avec succès lors de la Mission 50 :
  ils couvrent les sources, la génération Compose, les paramètres SQLAlchemy
  et des réponses HTTP simulées.
- Les tests ne démontrent aucune communication Docker réelle.
- Les contrats PHP, Next.js, Dash, Backend/MySQL et Groq sont documentés.
- Une liste de questions propriétaires existe dans
  [Contrats interservices](interservice-contracts.md).
- Aucun démarrage MySQL/Backend, SQL, DDL, migration, build, pull ou
  déploiement n’a été effectué.
- Aucun commit, staging, push ou modification destructive n’a été effectué.

### Première mission à exécuter

La reprise commence par obtenir les réponses techniques des responsables des
modules. Cette action ne nécessite aucune ressource Docker.

Questions bloquantes :

- données : autorisation des scripts et liste des tables attendues ;
- Backend : endpoint GET de lecture approuvé et portée réelle de `/health` ;
- PHP/CAS : comportement runtime, données de test et jeton de service ;
- Next.js : timeout, retry, cookie/JWT et codes d’erreur attendus ;
- Dash : certificat interne, endpoint de lecture et compte de test ;
- IA : service autonome ou intégration Groq uniquement, plus contrat complet ;
- Kubernetes : cluster cible, registry, stockage, sauvegarde et rollback.

### Séquence ordonnée de reprise

1. Collecter les réponses propriétaires et les ajouter aux contrats existants.
2. Mesurer la mémoire avant toute tentative Docker.
3. Préparer un checkout ou une configuration isolée.
4. Fournir les secrets MySQL sans les inscrire dans Git ou les logs.
5. Vérifier les noms, ports, réseaux, volumes et scripts SQL.
6. Générer Compose avec uniquement `data_mysql`.
7. Valider le Compose statiquement.
8. Obtenir une autorisation explicite, puis démarrer uniquement MySQL.
9. Vérifier état, healthcheck, journaux, DNS/TCP, authentification, base et
   tables en lecture seule.
10. Démarrer ensuite uniquement le Backend et valider SQLAlchemy.
11. Valider PHP, Next.js et Dash contre les services isolés.
12. Ajouter l'intégration IA seulement après validation du contrat propriétaire.
13. Exécuter la fiabilisation, les tests globaux et les tests de reprise.
14. Préparer puis, après autorisation, valider Kubernetes.
15. Finaliser les preuves de sauvegarde, restauration et livraison.

### Vérifications avant reprise Docker

- mémoire Windows libre >= 1,5 Gio ;
- Docker Engine Linux disponible ;
- image `mysql:8.4` locale ;
- aucune collision de conteneur, projet, réseau ou volume ;
- aucun port MySQL publié ;
- les quatre variables MySQL disponibles localement ;
- scripts SQL exactement vérifiés ;
- volume neuf uniquement ;
- aucune donnée privée non autorisée ;
- autorisation explicite de démarrage.

Décisions GO/NO-GO :

| Décision | Conditions |
|---|---|
| **GO** | mémoire >= 1,5 Gio, Docker disponible, image locale, aucune collision, secrets complets, scripts vérifiés, autorisations obtenues |
| **NO-GO** | ressource insuffisante, Docker indisponible, image absente, collision, `.env` incomplet, SQL incertain, données privées ou autorisation absente |

## 14. Historique des travaux d'orchestration

### Phase 1 — Compréhension de l'existant

**Problème initial :** Learnagement était installé localement mais son
fonctionnement, ses dépendances, ses scripts de démarrage et ses frontières
Docker n'étaient pas consolidés.

**Travail réalisé :** analyse du dépôt réel, de `Learnagement.py`,
`bootstrap.py`, `env.py`, `docker_compose.py`, des services, des scripts SQL,
du Backend et des fronts.

**Résultat :** les responsabilités ont été séparées entre l'orchestration et
les modules fonctionnels, et les dépendances principales ont été cartographiées.

**Preuves :** commandes CLI, fichiers Docker, contrats et documents déjà
présents dans le checkout.

**Limite :** aucun démarrage runtime global n'a été réalisé pour conclure à
une intégration opérationnelle.

### Phase 2 — Préparation de l'infrastructure

**Problème initial :** les six services DEV, les réseaux, les ports, les
dépendances et les volumes n'étaient pas exploités comme un socle d'isolation.

**Travail réalisé :** cartographie des services Compose, préparation des réseaux
front/back, correction du montage phpMyAdmin, montage SQL en lecture seule,
healthchecks et sélection sélective des services.

**Résultat :** la génération de Compose peut distinguer MySQL seul,
MySQL+Backend ou l'ensemble DEV.

**Preuves :** `docker_compose.py` et le test statique
`test_compose_startup_order.py`.

**Limite :** aucun conteneur ni volume isolé n'a été créé dans cette mission.

### Phase 3 — Sécurisation du démarrage

**Problème initial :** l'environnement Windows natif était bloqué par
`termios`, les variables MySQL n'étaient pas consolidées et les scripts SQL
étaient potentiellement destructifs.

**Travail réalisé :** analyse de `.env`, `env.py`, `docker_compose.py`,
préparation de MySQL-only, protocole de secrets, vérification des dix scripts
et runbook MySQL/Backend.

**Résultat :** la procédure future peut isoler les noms, le réseau et le
volume avant tout démarrage.

**Preuves :** [mysql-first-start.md](mysql-first-start.md) et
[backend-mysql-validation-runbook.md](backend-mysql-validation-runbook.md).

**Limite :** aucun `.env` réel, volume, initialisation ou connexion MySQL
n'a été validé en runtime.

### Phase 4 — Intégration interservices

**Problème initial :** les échanges PHP, Next.js, Dash, Backend et IA étaient
partiellement connus mais pas consolidés dans une matrice vérifiable.

**Travail réalisé :** consolidation des URL, méthodes, JWT/cookies, ports,
formats, erreurs, timeout et niveaux de preuve dans les contrats interservices.

**Résultat :** les contrats et les questions propriétaires sont identifiés
sans créer d'endpoint fictif ni d'intégration IA autonome.

**Preuves :** [interservice-contracts.md](interservice-contracts.md) et tests
statistiques/simulés des clients.

**Limite :** les intégrations live restent à exécuter.

### Phase 5 — Tests et fiabilisation

**Problème initial :** il fallait distinguer les tests réellement utiles des
preuves runtime manquantes.

**Travail réalisé :** collecte de 28 cas pytest dans les cinq fichiers
ciblés, extension des contrats HTTP et préparation des scénarios de panne,
reprise et persistance.

**Résultat :** les tests statiques/simulés sont disponibles localement sans
Docker ni secret réel.

**Preuves :** collecte pytest, fichiers `tests/integration/*` et matrice
[integration-test-plan.md](integration-test-plan.md).

**Limite :** aucun test d'intégration runtime, aucune panne réelle, aucune
persistance ou restauration MySQL n'a été exécutée.

### Phase 6 — Préparation Kubernetes et CI/CD

**Problème initial :** les manifests, images, probes, registry et réseau
Kubernetes nécessitaient une préparation sans déploiement.

**Travail réalisé :** manifests/base Kustomize, Dockerfiles Kubernetes,
validateur statique, workflow CI, probes, NetworkPolicies et checklist.

Le workflow [.github/workflows/kubernetes-images.yml](../.github/workflows/kubernetes-images.yml)
est déclenché manuellement ou sur pull request selon les chemins concernés.
Il prépare :

- la validation Kustomize et `kubernetes/validate_base.py`;
- les tests de contrats Dash/Compose/CLI dans son job interservices;
- les tests unitaires Backend séparés;
- les builds/smoke-tests des images Backend, PHP, Next.js et Dash;
- l'interdiction de publication avec `push: false`.

Le job interservices ne liste pas les fichiers
`test_http_contract_sources.py` ni `test_backend_mysql_contract.py`; ces suites
doivent être ajoutées au workflow uniquement si elles sont jugées nécessaires
et si leur dépendance reste non destructive.

L'existence du workflow prouve sa préparation. Elle ne prouve pas qu'une
exécution GitHub Actions a déjà réussi; aucun identifiant de run ni historique
de plateforme n'est conservé dans le guide.

**Résultat :** les fichiers peuvent être validés statiquement et les quatre
images peuvent être construites/smoke-testées en CI.

**Preuves :** [kubernetes/base/](../kubernetes/base),
[kubernetes/validate_base.py](../kubernetes/validate_base.py),
[.github/workflows/kubernetes-images.yml](../.github/workflows/kubernetes-images.yml).

**Limite :** aucun workflow exécuté ou cluster validé n'a été prouvé par cette
documentation; registry, TLS, stockage et rollback restent ouverts.

### Phase 7 — Documentation et transmission

**Problème initial :** les travaux étaient dispersés entre sorties de missions
et plusieurs runbooks spécialisés.

**Travail réalisé :** centralisation dans ce guide, ajout des liens vers les
runbooks, contrats, tests, Kubernetes et procédure de reprise.

**Résultat :** une personne peut distinguer préparation, simulation et
validation réelle et connaître la prochaine opération autorisée.

**Limite :** les décisions propriétaires et les preuves runtime restent à
ajouter au fil de la reprise.

## 15. Inventaire des fichiers d'orchestration

| Chemin | Statut | Domaine | Objectif / travail | Résultat / vérification | Limite |
|---|---|---|---|---|---|
| `env.py` | Existant, consulté | Configuration | Chargement, génération et propagation des variables | Valeurs MySQL canoniques confirmées | Historique Git de modification non confirmé |
| `docker_compose.py` | Modifié | Docker/Compose | Génération des services, réseaux, volumes, dépendances et correction du montage SQL/phpMyAdmin | Tests statiques ciblés | Modifications antérieures non attribuables depuis Git seul |
| `.gitignore` | Modifié | Sécurité/configuration | Exclusion `.env`, Compose, SQL init, données et secrets | Règles vérifiées | Historique détaillé non confirmé |
| `Learnagement.py` | Existant, consulté | CLI | Start/stop, préparation SQL, Compose et attente health | Parcours statique vérifié | Démarrage runtime non exécuté |
| `tests/integration/test_compose_startup_order.py` | Créé/modifié — historique confirmé par les travaux précédents | Tests | Sélection MySQL, dépendances, volume/réseau/port | 1 cas collecté | Ne démarre pas Docker |
| `tests/integration/test_backend_mysql_contract.py` | Créé/modifié — historique confirmé par les travaux précédents | Tests | Construction SQLAlchemy simulée | 7 cas collectés | Aucun MySQL réel |
| `tests/integration/test_http_contract_sources.py` | Modifié lors de la Mission 50 | Tests | Contrats PHP, Next, CAS, NextAuth, Groq | 9 cas collectés | Aucun appel runtime |
| `tests/integration/test_dash_backend_http_contract.py` | Créé/modifié — historique confirmé par les travaux précédents | Tests | Serveur HTTP simulé Dash/Backend | 10 cas collectés | Aucun Backend réel |
| `tests/integration/test_windows_cli_import.py` | Créé/modifié — historique confirmé par les travaux précédents | Tests | Import CLI Windows | 1 cas collecté | Ne valide pas Docker |
| `kubernetes/validate_base.py` | Créé/modifié — historique confirmé par les travaux précédents | Kubernetes | Validation statique du rendu, ports, probes, egress, Secrets | Validation locale passée | Ne remplace pas un cluster |
| `.github/workflows/kubernetes-images.yml` | Créé/modifié — historique confirmé par les travaux précédents | CI/CD | Validation, tests, builds et smoke-tests images | Workflow préparé et configuré | Exécution GitHub non démontrée ici |
| `docs/mysql-first-start.md` | Créé/modifié — historique confirmé par les travaux précédents | Documentation | Procédure MySQL isolée | Liens et commandes vérifiés | Aucun démarrage exécuté |
| `docs/backend-mysql-validation-runbook.md` | Créé/modifié — historique confirmé par les travaux précédents | Documentation | Séquence MySQL puis Backend | Matrice et limites documentées | Tous statuts runtime ouverts |
| `docs/interservice-contracts.md` | Créé/modifié — historique confirmé par les travaux précédents | Documentation | Contrats et questions propriétaires | Liens et preuves qualifiés | Réponses propriétaires attendues |
| `docs/integration-test-plan.md` | Créé/modifié — historique confirmé par les travaux précédents | Documentation/tests | Matrice isolée/runtime | 28 cas collectés | Runtime bloqué |
| `docs/release-delivery-guide.md` | Modifié dans les missions de consolidation | Documentation | Point d'entrée de reprise et livraison | Liens/diff vérifiés | Aucun résultat runtime ajouté |

## 16. Synthèse pour la transmission aux collègues

**Ce que j'ai réalisé sur Learnagement**

- J'ai cartographié Docker, Compose, les services, les réseaux, les volumes,
  les scripts SQL et les dépendances.
- J'ai préparé un démarrage MySQL isolé, une validation Backend/MySQL, des
  contrats interservices et une base de tests locaux.
- J'ai préparé Kubernetes et sa validation statique sans déployer de cluster.
- J'ai documenté les limites réelles, les résultats statiques/simulés et les
  tâches encore dépendantes des responsables des modules.

**Ce qu'il reste à faire**

- Obtenir les réponses des propriétaires.
- Préparer une configuration et des secrets isolés.
- Récupérer suffisamment de mémoire Windows.
- Démarrer, vérifier puis fiabiliser MySQL et le Backend.
- Valider les interfaces, l'authentification, l'IA et Kubernetes.
- Prouver la livraison par des tests runtime et une procédure de rollback.

Le projet n'est pas terminé : les préparations sont avancées, mais aucune
intégration Docker réelle complète n'a été déclarée validée.
