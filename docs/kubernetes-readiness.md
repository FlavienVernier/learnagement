# Matrice de préparation Kubernetes

## Périmètre et preuves

### État du checkout de livraison — 17 novembre 2026

Les contrôles Docker et les builds historiques décrits ci-dessous proviennent
du checkout de récupération et ne constituent pas une validation des images
dans le checkout de livraison. Les artefacts Kubernetes ont été transférés
depuis des fichiers locaux non suivis; aucune image n'a été construite, aucun
workflow n'a été exécuté et aucun déploiement n'a eu lieu dans ce checkout.
Le lockfile Composer a la même provenance locale; le build CI doit vérifier sa
cohérence avec `composer.json`. La CI ne publie pas d'images.

Cette matrice décrit l'environnement `dev-orchestration` et les configurations
présentes dans le checkout. Un premier Kustomize base préliminaire existe dans
`kubernetes/base/`; il ne constitue pas une validation de déploiement.

- Le contrôle en lecture seule du 16 novembre 2026 a confirmé Docker Engine
  29.8.2 réactif. Backend était `exited` (code 255); Next.js a d'abord été
  `running|unhealthy`, puis est revenu `running|healthy` sans action de cycle
  de vie après la fin de `npm ci` et la compilation de `/health`. PHP, Dash,
  MySQL et phpMyAdmin étaient `running|healthy`. Aucun conteneur n'a été
  démarré, arrêté ou redémarré.
- Le générateur suivi par Git est `docker_compose.py`. Le Compose actuellement
  utilisé est généré et non suivi par Git.
- Aucun manifeste Kubernetes préexistant n'a été trouvé avant la mission
  Kubernetes 01; le socle nouvellement créé reste statique et non déployé.
- Les configurations des conteneurs actifs utilisent des mounts du checkout
  (`/app`, `/var/www/html`, certificats et logs); MySQL utilise aussi un volume
  nommé pour `/var/lib/mysql`. Dash monte également `/data`.
- Aucun `requests`, `limits` CPU/mémoire ou utilisateur non-root n'est défini
  dans la configuration inspectée. Les conteneurs actifs s'exécutent avec
  l'utilisateur par défaut de leur image, qui est root pour les images
  contrôlées.

### Diagnostic correctif DEV — Mission 03

- **Backend** : exit 255, `OOMKilled=false`, `restart: no`, zéro redémarrage.
  Les derniers journaux accessibles montrent un démarrage et le service de
  requêtes avant la sortie, sans traceback fatal. Les événements Docker
  interrogés n'ont pas fourni la cause. La cause racine n'est donc pas
  confirmée et aucun patch applicatif Backend n'a été inventé. Un `docker
  start` est nécessaire pour rétablir les preuves live, mais reste en attente
  d'autorisation explicite.
- **Next.js** : Compose monte le code et `node_modules` depuis le disque
  Windows; l'entrypoint a installé 531 paquets en 28 minutes, puis Next dev a
  compilé `/health` plus longtemps que le timeout de probe de 5 s. La faible
  mémoire libre mesurée et l'erreur Watchpack historique `ENOMEM` renforcent
  le diagnostic de pression I/O/ressources, sans prouver un OOM actuel.
  L'application a fini par répondre HTTP 200 et le conteneur est healthy.
- **Correction Compose non intégrée à ce checkout** : le générateur livré
  monte encore `../front_NextJS/node_modules` depuis l'hôte et conserve
  `start_period: 30s` et `timeout: 5s` pour le probe Next. Le volume nommé et
  les délais de probe décrits dans des travaux antérieurs ne sont pas présents
  ici; ils ne doivent pas être considérés comme livrés.
- Le build Next.js Kubernetes n'a pas été repris : mémoire libre hôte de
  0,48 GiB au report du build, puis 0,24 GiB au dernier contrôle, avec charge
  observée du service Next DEV. Dash n'a pas été construit non plus. Les
  Dockerfiles Kubernetes sont isolés et aucun déploiement n'a eu lieu.

## Images Kubernetes construites pour la Mission 02

Les Dockerfiles isolés de `docker/kubernetes/` ne changent pas les images DEV
ni Compose. Aucun déploiement n'a été effectué.

| Service | État vérifié | État du socle Kustomize |
|---|---|---|
| Backend | Image locale `learnagement/backend-k8s:0.1.1` construite. Smoke ASGI isolé PASS : `/health` HTTP 200, UID 10001, aucun `.env`. Commande Uvicorn en override; aucun MySQL/DDL. | Image `0.1.1` référencée. Le `CMD python app.py` standard et le DDL restent non validés. |
| PHP | Build réussi; `/health` HTTP 200, UID 33, aucun `.env` embarqué. Aucun compte ou accès DB n'a été configuré pour le smoke. | Image locale `learnagement/front-php-k8s:0.1.0`, port conteneur 8080. |
| Next.js | `npm ci` réussi (cache); le build a atteint la compilation optimisée, puis a été interrompu quand le service DEV Next.js est devenu unhealthy. Docker restait réactif. Pas d'image ni de runtime validé. | Image reste un placeholder. |
| Dash | Build non tenté par prudence, car Next.js DEV était unhealthy et le build Python inclut des dépendances volumineuses. Le dossier data est vide et exclu du contexte; le code tolère l'absence de `data_reseau_polytech.json`, mais la fonctionnalité de données n'est pas prête. | Image reste un placeholder. |

Le contrôle des conteneurs par ancêtre de l'image PHP `0.1.0` n'a trouvé
aucun conteneur de smoke résiduel. Le conteneur Backend de smoke utilise
`--rm` et n'existait plus au contrôle suivant. Aucun `kubectl apply`, cycle de
vie Docker des six services, ou accès à `learnagement-dev-isolated` n'a été
effectué.

## Matrice de transposition

| Composant | État observé | Adaptation Kubernetes envisageable | Blocage / décision préalable |
|---|---|---|---|
| Backend Python | Actif; image construite localement depuis `python:3.14`; port 4000; `restart: no`; bind mount `/app`; `/health` ne vérifie pas MySQL. | Deployment + Service ClusterIP; readiness distincte de liveness; image immuable; configuration externalisée. | Ajouter/valider une readiness qui vérifie la connexion DB; définir la politique de reprise. Son entrypoint installe des dépendances et exécute pytest au démarrage : rendre le démarrage déterministe et sans installation/tests runtime avant déploiement. |
| PHP / Apache | Actif; image `php:8.5-apache`; ports 80/443 dans l'image, port 80 publié localement; bind mounts code, certificats et logs; `/health` local. | Deployment + Service ClusterIP; Ingress/TLS selon le point d'entrée retenu; logs vers stdout/stderr. | Retirer les mounts de code en production; fournir les certificats via Secret/gestionnaire TLS; vérifier les dépendances Composer verrouillées et éviter leur installation au démarrage. |
| Next.js | Actif; image `node:26-alpine`; port 3000; mounts `/app` et `node_modules`; healthcheck local; démarré par `npm run dev`. | Image de production immuable + Deployment/Service; Ingress si cette interface est exposée; readiness indépendante de l'authentification utilisateur. | Le conteneur observé est en mode développement et installe/reconstruit des dépendances au démarrage. Définir un build de production et séparer configuration publique/privée. |
| Dash | Actif; image construite depuis `python:3.14`; port 8050; mounts `/app`, `/data` et certificats; healthcheck local. | Deployment + Service ClusterIP; stockage persistant uniquement si le besoin de `/data` est confirmé. | Déterminer ce qui est conservé dans `/data`; remplacer les mounts du checkout; readiness ne vérifiant actuellement pas Backend/IA. Mesurer les ressources avant de fixer requests/limits. |
| MySQL | Actif; image `mysql:8.4`; port 3306 sans publication hôte; volume nommé `/var/lib/mysql`; scripts SQL montés dans `/docker-entrypoint-initdb.d`; redémarrage `always`. | StatefulSet + Service interne et PVC, ou service MySQL managé si décidé; probes adaptées; sauvegarde/restauration documentées. | Valider capacité, classe de stockage, sauvegardes, rétention et politique d'upgrade. Les scripts d'initialisation ne sont pas un mécanisme de migration sûre d'une base déjà initialisée : ne pas les rejouer sur le volume existant. |
| phpMyAdmin | Actif en développement; image sans version explicitement épinglée; accès hôte local sur le port 48080; pas de stockage applicatif. | Ne pas inclure dans le déploiement applicatif par défaut; éventuellement outil d'administration temporaire et strictement interne. | Confirmer s'il doit exister hors développement; ne pas l'exposer via une Ingress publique. |
| Service IA | Présent dans la configuration optionnelle, mais inactif lors du contrôle; port interne 8000; `/health` process et `/ready` vérifie la configuration, sans requête fournisseur. | Deployment + Service ClusterIP, uniquement après confirmation du contrat d'identité et du fournisseur. | `/chat` n'a pas de dépendance d'authentification observée; confirmer la frontière de confiance avec les propriétaires IA/architecture. Fournisseur, secrets, quotas et disponibilité réels ne sont pas validés. |
| Ollama | Optionnel, profil Compose `local-llm`, non actif; image `ollama/ollama:latest`; volume nommé pour les modèles; port 11434 interne. | Évaluer séparément un déploiement GPU/stockage dédié ou une solution fournisseur externe. | Besoins GPU, ressources, stockage des modèles, licences et stratégie d'exploitation à établir avant toute transposition. |

## Ports et exposition observés

| Service | Port conteneur | Publication locale actuelle | Orientation Kubernetes |
|---|---:|---|---|
| MySQL | 3306 | Aucune publication hôte | Service interne uniquement; NetworkPolicy limitée au Backend et aux opérations d'administration autorisées. |
| Backend | 4000 | `127.0.0.1:44000` | Service ClusterIP, non exposé directement par Ingress. |
| PHP | 80 (443 activable en production) | `40080:80` | Service ClusterIP derrière une Ingress selon le choix de l'interface et de TLS. |
| Next.js | 3000 | `127.0.0.1:43000` | Service ClusterIP derrière une Ingress si cette interface est retenue. |
| Dash | 8050 | `127.0.0.1:48050` | Service ClusterIP; exposition selon le parcours utilisateur approuvé. |
| phpMyAdmin | 80 | `127.0.0.1:48080` | Non exposé par défaut; accès administratif temporaire et restreint uniquement si nécessaire. |
| Service IA | 8000 | Aucune publication | Service ClusterIP après validation du contrat d'authentification. |
| Ollama | 11434 | Aucune publication | Réseau interne seulement si ce composant optionnel est retenu. |

## Contrats de probes et démarrage

| Service | Signal actuellement configuré/observé | Limite de ce signal | Cible de conception |
|---|---|---|---|
| MySQL | Healthcheck `mysqladmin ping` | Indique que le serveur répond, pas que les identifiants applicatifs et la base attendue fonctionnent. | Liveness légère; readiness vérifiant le service de base de données selon un mécanisme sécurisé. |
| Backend | `/health` | Répond indépendamment de MySQL; ne peut pas représenter la disponibilité du contrat Backend→DB. | Séparer liveness et readiness; readiness dépendant du test DB non destructif `SELECT 1`. |
| PHP, Next.js, Dash | Endpoints de santé locaux | Ne vérifient pas le Backend ni une transaction métier; un statut healthy ne prouve pas l'intégration. | Liveness locale; readiness de démarrage; dépendances réseau testées séparément et sans cascader toutes les pannes amont. |
| Service IA | `/health`; `/ready` vérifie la configuration | `/ready` ne prouve pas la disponibilité du fournisseur ou d'Ollama. | Décider si la readiness couvre la configuration seulement ou une dépendance amont, en évitant les probes coûteuses. |

`depends_on: service_healthy` ordonne le démarrage Compose mais ne définit pas la
reprise après une panne sur Kubernetes. Les applications doivent tolérer les
connexions refusées au démarrage et réessayer selon une stratégie bornée; les
probes Kubernetes ne remplacent pas cette logique.

## Risques et prérequis prioritaires

1. **Secrets dans la configuration générée — bloquant avant livraison.** Le
   générateur substitue des valeurs d'environnement dans des entrées
   d'environnement du Compose généré. Celui-ci n'est pas suivi par Git, mais
   ses valeurs restent lisibles dans le fichier généré sur le poste. Aucune
   valeur n'est reproduite ici. Avant Kubernetes, utiliser des Secrets
   Kubernetes alimentés par un gestionnaire adapté, contrôler les permissions
   et les journaux, et demander au propriétaire de décider si une rotation est
   nécessaire. Aucun secret n'a été modifié ou affiché pendant cette mission.
2. **Images et privilèges.** Les images de base observées utilisent des tags
   mutables ou non épinglés pour plusieurs services; les builds ne définissent
   pas d'utilisateur non-root. Définir une stratégie de versions/digests,
   d'analyse d'images, de mises à jour et de `securityContext` avant livraison.
3. **Images de développement.** Les mounts du code local et le lancement
   `next dev` ne sont pas adaptés à un déploiement reproductible. Retirer les
   bind mounts applicatifs des workloads de production et construire des
   artefacts immuables.
4. **Données et migrations.** Le volume MySQL est persistant; les scripts
   versionnés présents dans `db/docker-entrypoint-initdb.d` sont montés comme
   scripts d'initialisation. Établir une procédure de migration versionnée,
   sauvegarde et retour arrière avant d'automatiser une mise à jour. Aucun
   test de panne ou de restauration n'a été réalisé. Compose définit également
   un argument de démarrage MySQL spécifique qui n'est pas repris dans le
   premier StatefulSet; confirmer sa nécessité/parité avec le propriétaire DB.
5. **Réseau.** Traduire les deux réseaux Compose par des Services et des
   NetworkPolicies explicites. Le Backend est actuellement le seul pont entre
   le réseau Front et le réseau Back; MySQL ne publie pas de port hôte.
   Préserver cette frontière, ne pas exposer phpMyAdmin ni MySQL publiquement.
6. **Capacité et observabilité.** Mesurer CPU/RAM, définir `requests`/`limits`,
   centraliser logs/metrics, et préciser les alertes et identifiants de
   corrélation. Les contraintes de ressources ne sont pas configurées dans
   Compose et aucune mesure de charge n'est une preuve disponible.
7. **Exposition et TLS.** Choisir explicitement les interfaces accessibles,
   l'Ingress, les certificats, les en-têtes proxy et la terminaison TLS.
   Les certificats actuels sont montés depuis l'hôte; aucune stratégie TLS
   Kubernetes n'est fournie.

## État de préparation

| Sujet | État |
|---|---|
| Cartographie des workloads actifs/optionnels et ports internes | Documentée à partir de la configuration et de l'état runtime existants |
| Contrats réseau Compose et persistance MySQL | Documentés; aucune ressource modifiée |
| Readiness métier des dépendances | Partielle; des probes DB et propriétaires doivent confirmer les contrats |
| Disponibilité DEV au dernier contrôle | Backend arrêté (255, cause inconnue); Next.js revenu healthy; autres quatre services healthy. |
| Images reproductibles / non-root | PHP `0.1.0` et Backend `0.1.2` construites localement; smoke Backend isolé `/health` 200, UID 10001, aucun `.env`, aucun réseau/DB. Next.js et Dash non construits : 0,78 Gio libres et ressources DEV actives. Tags locaux non publiés; dépendances Python transitives et digests de base non verrouillés. |
| Secrets et mesure des ressources | Prérequis ouverts; valeurs de production et mesures CPU/RAM non disponibles. |
| Kustomize base | Créé dans `kubernetes/base/`; 15 ressources rendues et vérifiées statiquement, sans cluster |
| Déploiement et tests Kubernetes | Non exécutés; aucun contexte/cluster configuré |

Prochaine étape recommandée : le propriétaire Backend/DB doit déterminer la
cause de l'exit 255 et valider le plan d'initialisation des vues. L'image
Backend `0.1.2` est maintenant reconstruite et smoke-testée en réseau isolé;
aucun DDL n'a été exécuté. Le build Next.js de production a été reporté en
Mission 06 : 0,78 Gio de mémoire hôte libre, tandis que le conteneur Next.js
DEV utilisait 505 Mio et 81 % CPU. Ne pas solliciter davantage cette machine
tant que la marge reste faible; utiliser un builder séparé autorisé ou
reprendre lorsque davantage de mémoire est libre. Décider des Secrets,
StorageClass, sauvegardes et provenance de `/data` avant tout déploiement.

### Mise à jour Mission 04 — frontière de démarrage Backend

- Le serveur source ne lance plus l'initialisation DB au démarrage; les
  opérations `CREATE OR REPLACE VIEW ExplicitSecondaryKs_*` ne sont accessibles
  que via l'opt-in explicite `python init.py --apply`.
- Deux tests isolés passent sous Python 3.13.2. Ils ne se connectent pas à la
  base et ne démontrent ni la disponibilité des vues existantes ni la
  readiness DB. Le démarrage DEV n'a pas été tenté.
- Le tag Backend `0.1.2` a été construit et smoke-testé; le manifest référence
  ce tag. Le test utilisait des valeurs auth factices, réseau `none`, et aucun
  accès MySQL; cela ne valide ni schéma DB, ni routes métier, ni déploiement.
- Next.js et Dash restent non construits; leurs placeholders d'image n'ont pas
  été remplacés. Aucune ressource Kubernetes n'a été appliquée.
- Mémoire libre mesurée pendant la mission : environ 0,70 Gio au départ et
  0,85 Gio après le build Backend. Cette marge ne justifie pas les builds
  Next.js/Dash lourds sans risque de pression supplémentaire sur les services.

### Mise à jour Mission 06 — image Next.js

- Checkout `dev`, HEAD `0b17a19bbe1b78fd322b56ac4b9352c091481b27`; Docker
  Engine 29.8.2 disponible. Cinq conteneurs applicatifs DEV étaient healthy;
  Backend restait arrêté (255) et AI/Ollama optionnels étaient arrêtés (0).
- Mémoire libre hôte : **0,78 Gio**; Next.js DEV : **505 Mio, 81 % CPU**;
  Dash DEV : **213 Mio, 43 % CPU**. Le build Next.js n'a pas été lancé afin de
  protéger les workloads actifs. Aucun test runtime de l'image n'a donc été
  effectué.
- Le tag `learnagement/front-nextjs-k8s:0.1.1` n'est pas présent. Le
  placeholder Next.js et les 14 ressources restent inchangés; aucun déploiement
  n'a été effectué.
- Après obtention d'une marge mémoire suffisante ou d'un builder isolé :
  construire uniquement Next.js, puis tester le démarrage production,
  `/health`, UID non-root et absence de `.env` avant toute mise à jour Kustomize.

### Mise à jour Mission 07 — capacité de build et reprise

- Préflight : **1,02 Gio** libres sur Windows; Docker Desktop Linux
  (`desktop-linux`) a **3,72 Gio** et 8 CPU. Next.js DEV utilisait environ
  506 Mio / 73 % CPU; Dash DEV 213 Mio / 70 % CPU. Les cinq conteneurs
  applicatifs actifs étaient healthy; Backend est resté arrêté (255).
- Ubuntu WSL2 n'est pas une capacité séparée : elle partage le moteur
  `docker-desktop`; il ne lui restait qu'environ 1,1 Gio disponibles et son
  swap de 1 Gio était presque rempli. Les deux builders Buildx existants
  (`default`, `desktop-linux`) utilisent le même daemon. Aucun binaire
  standalone podman/buildah/buildctl/nerdctl ni endpoint de build distant
  autorisé n'a été trouvé.
- Décision : aucun build Next.js/Dash n'a été lancé. Le buildx
  `docker-container` consommerait la même mémoire. Aucun contenu source n'a
  été transféré à un service de build public/tiers; aucun builder n'a été
  créé/configuré. Les placeholders Kustomize sont conservés.
- Reprise : l'opérateur doit fournir un builder self-hosted/organisationnel
  autorisé ayant déjà le checkout, ou davantage de marge mémoire locale sans
  arrêter les services DEV. Construire Next.js puis Dash séquentiellement,
  smoke-tester chaque image, et ne remplacer chaque placeholder qu'après
  réussite.
- La checklist de gates et d'autorisation avant déploiement est dans
  [`kubernetes-deployment-checklist.md`](kubernetes-deployment-checklist.md).

### Mise à jour Mission 10 — readiness, sécurité et cohérence des manifests

- Backend startup/liveness continuent d'utiliser `/health`, endpoint public qui
  confirme seulement que l'API répond. La readiness exécute une connexion TCP
  vers le DNS et le port MySQL de la ConfigMap; une DB indisponible retire le
  Backend des endpoints Ready sans redémarrage déclenché par la liveness.
- Cette readiness ne teste ni authentification MySQL, permissions, schéma ou
  vues. Une readiness applicative DB reste à faire valider par le propriétaire
  Backend/DB; aucun code métier n'a été modifié.
- Les workloads Backend, PHP, Next.js et Dash imposent maintenant les UID
  correspondant aux Dockerfiles, `runAsNonRoot`, aucune élévation de privilèges,
  suppression de toutes les capabilities et seccomp `RuntimeDefault`.
  L'exécution réelle de Next.js/Dash sous ces contraintes reste à prouver après
  build et smoke-test de leurs images; MySQL n'est pas forcé sous un UID non-root.
- Les Services sélectionnent les labels des workloads, les `targetPort` nommés
  correspondent aux ports conteneurs et les probes HTTP utilisent les ports
  déclarés. `python kubernetes/validate_base.py` contrôle ces contrats sur le
  rendu et Kustomize rendait alors 14 ressources; aucun Secret n'a été ajouté.
- À la Mission 10, les NetworkPolicies limitaient l'ingress MySQL/Backend.
  Mission 11 ajoute une politique egress Backend limitée au MySQL TCP/3306 et
  DNS TCP/UDP 53. PHP, Next.js et Dash conservent une sortie ouverte : les
  destinations CAS et IA doivent être confirmées avant de la restreindre.
  L'application des politiques dépend du CNI. L'absence d'Ingress expose les
  frontends uniquement en ClusterIP, donc aucun accès navigateur externe n'est
  fourni par cette base.
- Les Deployments conservent `Recreate`: un rollout peut interrompre chaque
  interface et le Backend. Le passage à `RollingUpdate` est différé jusqu'à la
  mesure de capacité et la validation de compatibilité Backend/DB.
- Au contrôle Docker en lecture seule de cette mission, Backend était
  `running|healthy` (`RestartCount=0`, `OOMKilled=false`) et MySQL healthy;
  la cause du précédent exit 255 demeure inconnue. Ce statut est une observation
  Docker, pas une preuve de requête SQL ni de route métier. Aucun conteneur n'a
  été redémarré ou manipulé.
- Aucun `kubectl apply`, accès DB, build, cycle de vie de conteneur ou accès
  navigateur/live n'a été effectué pendant cette validation.

### Mise à jour Mission 11 — rollout, egress et images

- Décision : conserver `Recreate` pour Backend/PHP/Next.js/Dash. Les replicas
  sont à 1, les probes ne couvrent que l'API/processus et l'accès TCP Backend à
  MySQL, et la marge de ressources, les sessions, les migrations DB et la
  compatibilité de versions simultanées ne sont pas prouvées. Le passage à
  `RollingUpdate` (`maxUnavailable: 0`, `maxSurge: 1`) reste conditionné à ces
  preuves; MySQL reste single-replica `OnDelete` et ne peut fournir du zéro
  downtime.
- Flux confirmés : Backend→MySQL TCP/3306; Backend/frontends→DNS TCP/UDP 53;
  PHP/Next.js/Dash→Backend TCP/4000. Les NetworkPolicies ingress existantes
  autorisent ces appels. Backend ne montre pas de client réseau externe dans
  les sources inspectées.
- Egress Backend est maintenant isolée à MySQL/TCP 3306 et DNS/TCP+UDP 53.
  La destination DNS est volontairement non restreinte pour tolérer les
  implémentations CoreDNS/NodeLocal différentes; un cluster cible doit valider
  son CNI et le chemin DNS avant déploiement.
- Egress des frontends reste ouverte : PHP vérifie des tickets auprès de
  `CAS_HOST`, Dash peut contacter `AI_SERVICE_URL`/`ai_service_<instance>`, et
  l'IA/Ollama/RAG ne sont pas représentés par les ressources de ce base. Les
  endpoints, ports, TLS et décisions d'exposition doivent être fournis par
  les responsables avant toute restriction.
- Rollout StatefulSet MySQL : une seule réplique, PVC persistant, `OnDelete`;
  aucun mécanisme de haute disponibilité/upgrade DB sans interruption n'est
  fourni.
- Dockerfile Kubernetes : ports/commandes correspondent aux manifests; PHP
  UID 33, Backend/Dash UID 10001, Next.js UID 1000 correspondent aux contextes
  déclarés. Les images Next.js/Dash restent absentes et leurs contraintes
  runtime `/tmp`, données Dash, non-root et probes `/health` ne sont pas
  vérifiées par exécution. Le validateur compare maintenant statiquement
  les ports exposés, users et commandes de démarrage aux Deployments.
- Préflight build Mission 11 : environ 0,50 GiB de RAM hôte libre; Docker
  Desktop expose 3,72 GiB total, avec neuf conteneurs actifs dont deux stacks
  isolés et les services `dev-orchestration`. Aucun build n'a été démarré pour
  ne pas accroître la pression sur ces workloads. Les tags Next.js/Dash
  Kubernetes ne sont pas présents localement.
- Aucune image, conteneur, volume, base ou cluster n'a été modifié; aucune
  commande `kubectl apply` n'a été exécutée.

### Mission 12 — voie CI de construction des images

- `.github/workflows/kubernetes-images.yml` définit une construction
  séquentielle Next.js puis Dash sur runner GitHub hébergé, avec cache BuildKit
  séparé, smoke-tests d'UID, d'absence de `.env` et de `/health`.
- Le workflow ne publie aucune image, n'utilise aucun secret et ne possède
  que `contents: read`. Ses tags `ci-<SHA>` sont temporaires; les placeholders
  Kustomize restent intentionnels jusqu'au choix de références de déploiement.
- Aucun build ni smoke-test distant n'a été exécuté. Le remote `origin` est un
  chemin local; le workflow doit être transféré au dépôt GitHub autorisé avant
  de pouvoir l'exécuter. Les images Next.js et Dash restent non construites et
  les digests de déploiement manquants.
- Le smoke-test Dash passe `SESSION_TIMEOUT=900`, valeur non secrète; aucune
  clé JWT n'est fournie. Cela valide uniquement démarrage et santé, pas les
  parcours Backend/IA, la présence de données ou les fonctions métier.

### Mission 13 — dépôt CI identifié, livraison non autorisée

- GitHub CLI est authentifié comme `ZANA-JB`. La recherche de dépôts et la
  comparaison exacte du commit ont identifié
  [`FlavienVernier/learnagement`](https://github.com/FlavienVernier/learnagement)
  : dépôt public, branche par défaut `dev`, permission observée `WRITE`.
- Le HEAD distant de `dev` est exactement
  `0b17a19bbe1b78fd322b56ac4b9352c091481b27`, identique au checkout autorisé.
  Les noms similaires des autres dépôts de la recherche n'ont pas servi à
  choisir ce candidat; le SHA, le nom de projet, la branche et le propriétaire
  de commit concordent.
- Aucun workflow n'est présent dans `.github/workflows/` de la branche distante.
  Le checkout de travail a lui-même de nombreux changements et fichiers
  non suivis; aucune branche/remote n'a été modifié, aucun fichier n'a été
  stage, commit ou poussé, et aucun workflow distant n'a été déclenché.
- Le premier build ne peut pas être livré comme workflow isolé : le HEAD
  distant ne contient pas encore les deux Dockerfiles Kubernetes ni leurs
  `.dockerignore` dédiés. Il contient `front_DashPlotly/main.py` avec sa route
  `/health`. Pour Next.js 16.4.5, l'implémentation locale recherche `route`
  avec les extensions de page configurées, ce qui inclut `.tsx`; le fichier
  suivi `front_NextJS/app/health/route.tsx` est donc reconnu comme Route
  Handler. La documentation Next.js illustre officiellement `route.ts` et
  `route.js`, mais le matcher livré dans 16.4.5 accepte aussi `tsx`. Comme le
  workspace contient en plus un `route.ts` local non suivi avec le même
  handler, le Dockerfile-specific ignorefile exclut désormais uniquement ce
  doublon du contexte Kubernetes. Le fichier suivi `route.tsx` reste le
  handler utilisé par le smoke-test. Aucun build n'a été exécuté.
- À la Mission 13, `actionlint` n'était pas installé. La Mission 14 a téléchargé
  temporairement l'asset Windows officiel v1.7.12, vérifié son SHA-256 avec le
  fichier de checksums GitHub, validé le workflow avec exit code 0, puis
  supprimé le dossier temporaire. Aucun outil n'a été ajouté au PATH global.
- Les trois actions tierces sont épinglées à des commits récupérés depuis les
  tags officiels `actions/checkout` v4, `docker/setup-buildx-action` v3 et
  `docker/build-push-action` v6. `persist-credentials: false` limite la
  conservation du credential de checkout; les smoke-tests nettoient aussi
  leurs conteneurs sur sortie, interruption et terminaison.

### Mission 14 — route et lot CI vérifiés

- Next.js locké à `16.4.5`; `next/dist/server/config-shared.js` définit les
  extensions par défaut `tsx`, `ts`, `jsx`, `js`, et son matcher reconnaît
  `route.<extension>`. Le handler suivi `route.tsx` expose GET et retourne
  `{"status":"ok"}` sans auth, DB ni dépendance réseau. Le workflow attend
  précisément ce corps.
- Un second `route.ts` local non suivi était présent au même segment.
  `docker/kubernetes/front-nextjs/Dockerfile.dockerignore` exclut uniquement
  ce doublon du contexte d'image, en préservant les deux fichiers source du
  workspace. Aucun build n'a été lancé.
- Le smoke-test Dash lance Gunicorn avec `SESSION_TIMEOUT=900`, seule valeur
  de configuration requise lors de l'import. La route `/health` ne déclenche
  pas les callbacks Dash; Backend/IA sont appelés uniquement par leurs
  fonctions applicatives, pas par ce healthcheck.
- `actionlint` v1.7.12 (asset temporaire avec checksum vérifié): PASS, exit 0.
  Le YAML/contrat, `bash -n`, rendu Kustomize (15 ressources),
  `python -B kubernetes/validate_base.py` et `git diff --check` passent.
- Aucun build ou smoke-test d'image n'a été exécuté. Les fichiers CI
  indispensables et les exclusions figurent dans
  `docs/kubernetes-deployment-checklist.md`; aucun workflow distant n'a été
  déclenché.

### Mise à jour Mission 09 — résilience du proxy Next.js

- Le proxy conserve le statut Backend `5xx`, mais renvoie désormais un corps
  générique `{ "error": "Backend service error." }` au lieu de relayer les
  détails internes éventuels. Les statuts d'erreur client 4xx continuent de
  relayer le corps applicatif attendu.
- Le timeout Backend du proxy reste 30 s; les erreurs réseau et délais sans
  réponse restent des réponses HTTP 502 génériques. Le proxy n'effectue pas de
  retry automatique, afin d'éviter de rejouer silencieusement les POST; la
  récupération est démontrée par un nouvel appel explicite dans un test
  simulé.
- `npm run test:proxy-resilience` : **8 passed, 0 failed**. L'adaptateur Axios
  est simulé; aucun Backend, MySQL ou service DEV n'est appelé. Le test démontre
  un comportement applicatif simulé, pas une récupération E2E live.
- Le runner global `test:orchestration` n'a pas été lancé : il exécute un
  `SELECT 1` via Backend/MySQL et le Backend DEV est arrêté. Aucun accès DB
  n'était autorisé dans cette mission.
- Étapes 4.4/4.5/6/7 avancent côté contrat et tests isolés; les parcours live
  authentifiés, failover réel et persistance après redémarrage restent ouverts.

### Diagnostic isolé Backend — tests A, B et C

- Une image temporaire `learnagement-backend-255-lab:latest` a été construite
  depuis un contexte allowlisté copié du checkout de récupération. Elle n'est
  pas une image Kubernetes du checkout de livraison et n'a pas été publiée.
- Les tests A (maintien sur 5 minutes) et C (observation passive sur 15
  minutes, 31 relevés) ont démarré Uvicorn et obtenu `/health` HTTP 200. Aucun
  arrêt spontané, redémarrage ou OOM n'a été observé. Les conteneurs utilisaient
  `--network none`, sans montage ni port publié; aucune connexion MySQL n'a été
  effectuée.
- Le test B et les arrêts demandés en fin de A et C se sont terminés
  gracieusement avec le code 0. Le scénario contrôlé ne reproduit pas le code
  255.
- Ces observations démontrent seulement la stabilité de cette reproduction
  isolée. Elles ne déterminent pas la cause du code 255 historique du Backend
  DEV, ne valident pas le checkout de livraison, et ne remplacent ni les
  smoke-tests CI des quatre images ni un test d'intégration avec une base
  dédiée. Le conteneur DEV n'a pas été redémarré.

### Validation locale — ordonnancement Compose et CLI Windows

- `docker_compose.py` génère déjà les dépendances de santé en chaîne :
  Backend attend MySQL `service_healthy`, puis PHP, Next.js et Dash attendent
  le Backend `service_healthy`. Un test de régression analyse le Compose
  généré dans un répertoire temporaire, sans démarrer de conteneur.
- L'import POSIX `termios` est désormais limité au chemin de restauration TTY
  non-Windows. Sous Windows, `tools` s'importe et `Learnagement.py --help`
  fonctionne; cela ne prouve pas le démarrage complet de la stack native.
- Les trois tests d'intégration mockés/locaux passent sous Python 3.11
  (**9 passed**) et Python 3.13 (**9 passed**, un avertissement non bloquant
  du plugin pytest Dash). Ils couvrent le contrat Dash→Backend simulé, l'ordre
  de démarrage Compose statique et l'import sans `termios`.
- Kustomize rend 15 ressources et `kubernetes/validate_base.py` passe. Le
  workflow a été parsé et ses contrats locaux vérifiés, mais GitHub Actions
  n'a pas été déclenché.
- Aucun build local n'a été lancé : le préflight relevait 0,71 Gio de RAM
  hôte libre et neuf conteneurs DEV actifs. Aucune image, aucun service et
  aucune donnée métier n'ont été modifiés.
- La source officielle des consignes du professeur et des critères
  d'acceptation n'est pas présente parmi les documents identifiés du checkout;
  la TODO générale du dépôt se déclare elle-même obsolète. La readiness
  technique ne remplace pas cette source de vérité.
