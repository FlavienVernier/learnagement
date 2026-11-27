# Images Kubernetes Learnagement

Les anciens résultats et commandes de build ci-dessous documentent le
checkout de récupération. Dans le checkout de livraison courant, les images
n'ont pas été construites; la CI prépare des tags temporaires `ci-<SHA>` sans
publication. Les manifests gardent des placeholders jusqu'à validation et
autorisation d'une publication.

Ces Dockerfiles sont distincts des images DEV/Compose. Les commandes ci-dessous
utilisent la racine du dépôt comme build context et des fichiers
`Dockerfile.dockerignore` dédiés afin d'exclure les `.env`, certificats,
dépendances locales et données runtime.

Construire une image à la fois sur le contexte Docker autorisé :

```powershell
docker --context desktop-linux build -f docker/kubernetes/backend/Dockerfile -t learnagement/backend-k8s:ci-local .
docker --context desktop-linux build -f docker/kubernetes/front-php/Dockerfile -t learnagement/front-php-k8s:ci-local .
docker --context desktop-linux build -f docker/kubernetes/front-nextjs/Dockerfile -t learnagement/front-nextjs:ci-local .
docker --context desktop-linux build -f docker/kubernetes/front-dash/Dockerfile -t learnagement/front-dash:ci-local .
```

Les tags `ci-local` illustrent uniquement des builds locaux, qui ne sont pas
exécutés pendant cette mission. Les tags CI suivent les dépôts image des
manifests avec `ci-<SHA>`; aucun tag de release n'est décidé.

Incrémenter les tags après chaque modification et publier uniquement vers un
registry autorisé. Les tags locaux listés ne sont pas publiés. Les images de
base utilisent encore des tags, pas des digests; les versions transitives des
dépendances Python ne sont pas toutes verrouillées. Une promotion reproductible
entre environnements exige des digests de base et des lockfiles Python avec
versions/hashes validés.

## Conventions de runtime

| Image | Port | Utilisateur | Commande |
|---|---:|---|---|
| `learnagement/backend-k8s` | 4000 | UID/GID 10001 | `python app.py` |
| `learnagement/front-php-k8s` | 8080 | `www-data` (UID 33) | `apache2-foreground` |
| `learnagement/front-nextjs` | 3000 | `node` (UID 1000) | `npm run start -- --hostname 0.0.0.0` |
| `learnagement/front-dash` | 8050 | UID/GID 10001 | Gunicorn `main:server` |

PHP écoute sur 8080 pour permettre l'exécution non-root; Apache reçoit HTTP
interne et la terminaison TLS relève d'une configuration d'entrée encore à
décider. Dash utilise Gunicorn pour ne pas démarrer le serveur de développement
Flask de `main.py`.

Les processus reçoivent SIGTERM (Apache utilise SIGWINCH) et les applications
restent au premier plan. Les secrets ne sont pas copiés dans les images.

## Procédure de build et smoke-test isolés — Next.js et Dash

Construire séparément, depuis la racine du checkout et uniquement sur un
runner autorisé. Avant chaque image, vérifier la RAM hôte libre et l'utilisation
Docker; ne pas lancer le build si cela risque de dégrader des conteneurs actifs.
Buildx/WSL intégrés au même Docker Desktop ne fournissent pas une capacité
mémoire indépendante.

```powershell
# Préflight lecture seule
$os = Get-CimInstance Win32_OperatingSystem
"HostFreeGiB={0:N2}" -f ($os.FreePhysicalMemory / 1MB)
docker --context desktop-linux stats --no-stream

# Image Next.js — ne pas lancer Dash en parallèle
docker --context desktop-linux build -f docker/kubernetes/front-nextjs/Dockerfile `
  -t learnagement/front-nextjs:ci-local .
docker --context desktop-linux run --rm --entrypoint node `
  learnagement/front-nextjs:ci-local -e "console.log(process.getuid())"
docker --context desktop-linux run --rm --entrypoint sh `
  learnagement/front-nextjs:ci-local -c "test ! -e /app/.env"
docker --context desktop-linux run --detach --rm `
  --name learnagement-nextjs-k8s-smoke-011 `
  --publish 127.0.0.1:43001:3000 learnagement/front-nextjs:ci-local
$health = $null
$deadline = [DateTime]::UtcNow.AddSeconds(60)
do {
  try { $health = Invoke-RestMethod http://127.0.0.1:43001/health -TimeoutSec 2 }
  catch { Start-Sleep -Seconds 2 }
} while (-not $health -and [DateTime]::UtcNow -lt $deadline)
if ($health.status -ne "ok") {
  docker --context desktop-linux logs learnagement-nextjs-k8s-smoke-011
  docker --context desktop-linux stop learnagement-nextjs-k8s-smoke-011
  throw "Next.js /health failed"
}
docker --context desktop-linux stop learnagement-nextjs-k8s-smoke-011

# Vérifier de nouveau la capacité avant Dash; ne pas poursuivre si la marge
# disponible est insuffisante.
$os = Get-CimInstance Win32_OperatingSystem
"HostFreeGiB={0:N2}" -f ($os.FreePhysicalMemory / 1MB)
docker --context desktop-linux stats --no-stream

# Image Dash
docker --context desktop-linux build -f docker/kubernetes/front-dash/Dockerfile `
  -t learnagement/front-dash:ci-local .
docker --context desktop-linux run --rm --entrypoint python `
  learnagement/front-dash:ci-local -c "import os; print(os.getuid())"
docker --context desktop-linux run --rm --entrypoint sh `
  learnagement/front-dash:ci-local -c "test ! -e /app/.env"
docker --context desktop-linux run --detach --rm `
  --name learnagement-dash-k8s-smoke-010 `
  --publish 127.0.0.1:48051:8050 -e SESSION_TIMEOUT=900 `
  learnagement/front-dash:ci-local
$health = $null
$deadline = [DateTime]::UtcNow.AddSeconds(60)
do {
  try { $health = Invoke-RestMethod http://127.0.0.1:48051/health -TimeoutSec 2 }
  catch { Start-Sleep -Seconds 2 }
} while (-not $health -and [DateTime]::UtcNow -lt $deadline)
if ($health.status -ne "ok") {
  docker --context desktop-linux logs learnagement-dash-k8s-smoke-010
  docker --context desktop-linux stop learnagement-dash-k8s-smoke-010
  throw "Dash /health failed"
}
docker --context desktop-linux stop learnagement-dash-k8s-smoke-010
```

Le résultat `/health`, l'UID et l'absence de `.env` doivent être contrôlés
avant de considérer chaque image smoke-testée. `SESSION_TIMEOUT=900` est une
valeur non secrète utilisée uniquement pour ce test local; ne pas y ajouter de
jeton ni de clé de production. Si une commande ou le healthcheck échoue,
collecter les logs du conteneur temporaire et le retirer par son nom exact;
ne pas remplacer le placeholder Kustomize. Le smoke HTTP prouve uniquement le
démarrage et la route santé, pas les contrats Backend/DB/IA. `--rm` supprime
le conteneur temporaire après son arrêt; aucune commande ne cible les services
DEV ni leurs volumes.

## Progression / limites

- PHP `0.1.0`: image construite; smoke local `/health` HTTP 200 sous UID 33;
  `.env` absent de l'image.
- Backend `0.1.1`: build PASS après conservation du pin `typing` existant et
  ajout de `Pygments==2.20.0`. Smoke ASGI isolé PASS : `/health` HTTP 200,
  UID 10001, aucun `/app/.env`. Le smoke a remplacé la commande par défaut par
  Uvicorn; aucune connexion MySQL ou initialisation DDL n'a été effectuée.
  Cette image est antérieure à la séparation du démarrage et du DDL; la version
  actuelle `0.1.2` construite et smoke-testée est décrite plus bas.
- Next.js: le build de production précédemment lancé a atteint `Creating an
  optimized production build ...`, puis a été interrompu quand le conteneur
  DEV Next.js est devenu unhealthy. Il n'a pas été relancé : la mémoire libre
  hôte était de 0,48 GiB au report du build, puis 0,24 GiB au dernier contrôle;
  le service DEV utilisait environ 470–485 MiB et jusqu'à 156 % CPU. Aucune
  image ni référence de manifest n'est validée.
- Dash: build non tenté pour la même pression de ressources; ses dépendances
  incluent PyTorch CPU et sentence-transformers. Aucune image ni référence de
  manifest n'est validée.

Au contrôle en lecture seule du 16 novembre 2026, Docker Engine 29.8.2
répondait. Backend était exited (255; sans OOM ni trace fatale conservée);
Next.js est revenu healthy naturellement après `npm ci` (531 paquets en
28 min), le démarrage Next dev et la compilation de `/health`. PHP, Dash,
MySQL et phpMyAdmin étaient healthy. Aucun conteneur DEV n'a été démarré,
arrêté ou reconstruit. Le volume Next `node_modules` et les seuils de santé
ajustés dans le générateur Compose ne prendront effet qu'après génération et
recréation autorisée.

Le test `python -m pytest -q tests/test_isolation_guards.py` a réussi :
60 passed. Il vérifie le nouveau volume nommé par instance en générant un
Compose temporaire puis en le normalisant avec `docker compose config`; il ne
crée aucun conteneur ni volume.

Le contexte Dash exclut `front_DashPlotly/data/`; le code référence
`../data/data_reseau_polytech.json` et tolère son absence avec un dataset vide.
Le dossier local était vide lors de l'inspection; le mode de fourniture des
données reste à décider avant d'activer le parcours correspondant.

### Mission 11 — build reporté, stratégie de rollout et réseau

- Préflight en lecture seule : RAM hôte libre environ **0,50 GiB**; Docker
  Desktop expose **3,72 GiB** au moteur et 8 CPU. Neuf conteneurs étaient
  actifs, dont les stacks `dev-orchestration` et `dev-isolated`; Next.js
  `dev-orchestration` consommait environ 467 MiB et 66% CPU. Aucun conteneur
  Dash n'apparaissait dans la liste des neuf actifs; plusieurs images Dash
  DEV/candidates volumineuses sont présentes en cache. Aucun build Next.js/Dash
  n'a été tenté afin de préserver les workloads actifs.
- Les tags Kubernetes Next.js/Dash ne sont pas présents localement. Les
  Dockerfiles correspondent statiquement aux ports (3000/8050), commandes et
  UID du manifeste. L'exécution réelle sous securityContext, le startup,
  `/health`, `/app/.env` et les besoins runtime restent à vérifier avec la
  procédure ci-dessus; le dossier de données Dash est vide.
- Les quatre Deployments gardent `Recreate`: un seul replica, readiness non
  métier, capacité de surge non démontrée et migrations Backend/DB non
  qualifiées. Le StatefulSet MySQL reste single-replica `OnDelete`; aucune
  promesse de mise à jour sans interruption.
- La NetworkPolicy `backend-egress` autorise uniquement MySQL TCP/3306 et DNS
  TCP/UDP 53. PHP, Next.js et Dash gardent l'egress ouverte. CAS externe côté
  PHP, AI_SERVICE/LLM côté Dash, et dépendances RAG doivent être confirmés
  avant d'ajouter des restrictions. Le CNI et le résolveur DNS cible restent
  à valider.
- Aucun cluster, conteneur/volume DEV, image existante, MySQL ou builder n'a
  été manipulé; aucun `kubectl apply` n'a été lancé.

## Backend — frontière démarrage / DDL (Mission 04)

Le code source sépare désormais le démarrage Uvicorn de l'initialisation DB :
`python app.py` ne lance pas `init.init()`. Les opérations existantes
`CREATE OR REPLACE VIEW ExplicitSecondaryKs_*` restent déclenchées uniquement
par `python init.py --apply`. Les routes métier peuvent dépendre de ces vues;
leur existence doit être vérifiée et leur création versionnée avec validation
du propriétaire Backend/DB avant déploiement. Aucun DDL n'a été appliqué à DEV.

Les tests isolés de la frontière passent **2/2** sous Python 3.13.2; Uvicorn et
la fonction DDL sont interceptés par les tests. Ils ne prouvent pas le
comportement de l'image `0.1.1` déjà construite, l'accès réel à MySQL, ni
l'existence des vues. Rebuilder l'image Backend sous un nouveau tag avant de
mettre à jour/référencer une version Kubernetes.

Backend `0.1.2` a été construit depuis le Dockerfile Kubernetes et testé dans
un conteneur temporaire `--network none`: démarrage standard Uvicorn, `/health`
HTTP 200, UID 10001, aucun `.env` dans `/app`. Le test a utilisé une clé JWT
factice uniquement pour satisfaire la configuration d'import; aucun accès
MySQL/DDL n'était possible. `kubernetes/base/backend.yaml` référence maintenant
`0.1.2`.

Next.js et Dash restent non construits. La mémoire libre hôte mesurée était de
0,70 GiB avant le build Backend et 0,85 GiB ensuite; cela reste insuffisant
pour un build Next.js d'optimisation ou l'image Dash, dont le Dockerfile
installe PyTorch CPU et sentence-transformers. Leurs placeholders Kustomize
restent intentionnels jusqu'à obtention de builds et smoke tests réels.

### Mission 06 — Next.js différé pour manque de mémoire

Au contrôle pré-build, l'hôte avait **0,78 GiB libres** et Docker environ
**3,72 GiB** de mémoire disponible. Le Next.js DEV healthy utilisait environ
**505 MiB et 81 % CPU**; Dash DEV utilisait environ **213 MiB et 43 % CPU**.
Le build de production Next.js n'a pas été tenté pour éviter de perturber les
services. Le tag `learnagement/front-nextjs-k8s:0.1.1` n'existe pas encore;
aucun smoke-test n'a été effectué et le placeholder Kustomize est volontaire.

Le Dockerfile dédié réalise `npm ci`, `npm run build --webpack` et démarre
Next.js en mode production sur le port 3000 sous l'utilisateur `node`. Le
fichier `Dockerfile.dockerignore` exclut `.env`, clés/certificats, `node_modules`
et `.next` locaux. La configuration runtime Kustomize fournit
`JWT_SIGNING_KEY` par Secret et `INSTANCE_PROTOCOL`,
`BACKEND_PYTHON_DOCKER_URL` et `BACKEND_PYTHON_DOCKER_PORT` par ConfigMap;
aucune valeur réelle n'est intégrée à l'image. Le endpoint configuré pour les
probes est `/health`, mais il reste à tester sur l'image de production.

Reprendre sur un builder autorisé avec une marge mémoire nettement supérieure,
en construisant Next.js seul. Ne remplacer le placeholder qu'après le
smoke-test complet de l'image.

### Mission 07 — vérification des options de build

- Docker Buildx expose `default` et `desktop-linux`, mais les deux ciblent le
  même Docker Desktop Linux (29.8.2, 3.72 GiB, 8 CPU). Créer un builder
  `docker-container` ne créerait pas une capacité mémoire indépendante.
- Ubuntu WSL2 est installé/intégré, mais utilise le même daemon Docker et la
  même mémoire hôte; lecture `free -h`: 1.1 GiB disponibles et swap de 1 GiB
  presque pleine. Aucun `podman`, `buildah`, `buildctl` ou `nerdctl` autonome
  n'est installé. Pas de `.wslconfig` utilisateur de ressources détecté.
- Aucune machine/self-hosted runner distant préconfiguré n'est disponible dans
  cet environnement. Le checkout n'a pas été envoyé à un service tiers.
- Décision opérationnelle : conserver les services DEV et différer les deux
  builds. Reprise recommandée sur runner organisationnel autorisé ayant déjà
  accès au checkout, ou après accroissement de la mémoire disponible sans
  arrêt/recréation des services DEV. Construire une image à la fois avec les
  commandes versionnées plus haut, puis exécuter les smoke-tests avant
  d'éditer les manifests.

Le Dockerfile Dash utilise CPU PyTorch et sentence-transformers; aucun build
ni téléchargement associé n'a été lancé dans cette mission. Les tags
Next.js `0.1.1` et Dash `0.1.0` ne sont pas déclarés comme construits tant
qu'un build réel n'a pas abouti.

## Mission 12 — workflow CI de build et smoke-test

Le workflow [Kubernetes image builds](../../.github/workflows/kubernetes-images.yml)
construit Next.js puis Dash séquentiellement sur un runner GitHub hébergé.
Il utilise les contextes Docker racine requis par les instructions `COPY`,
les Dockerfiles et fichiers `.dockerignore` dédiés, ainsi qu'un cache BuildKit
GitHub Actions séparé pour chaque image.

- Déclenchement : `workflow_dispatch`, ou pull request touchant un Dockerfile,
  son `.dockerignore`, l'application correspondante, les manifests Kubernetes
  de base ou ce workflow.
- Permissions : `contents: read` seulement. Le workflow ne référence aucun
  secret, n'exécute pas de login registry et ne pousse aucune image.
- Les actions `actions/checkout` v4, `docker/setup-buildx-action` v3 et
  `docker/build-push-action` v6 sont référencées par leurs SHA de commit
  officiels; `persist-credentials: false` empêche le credential checkout de
  rester dans la configuration Git du runner après récupération du code.
- Les noms de repository des tags reprennent les manifests (`learnagement/front-nextjs`
  et `learnagement/front-dash`); le tag temporaire `ci-<SHA complet>` identifie
  le commit testé. Les manifests gardent leurs placeholders et aucun tag
  de release n'est décidé par ce workflow.
- Après chaque build, le smoke-test vérifie l'UID runtime (Next.js 1000,
  Dash 10001), l'absence de `/app/.env` et `/health` avec une attente bornée.
  Dash reçoit seulement `SESSION_TIMEOUT=900`, valeur de test non secrète déjà
  documentée pour le smoke local. Aucun jeton ou clé n'est injecté.
- `load: true` rend l'image disponible au Docker du runner pendant son
  smoke-test. Le workflow retire ensuite l'image; conteneurs et images ne sont
  pas conservés comme artefacts, et le runner éphémère est détruit après le
  job.
- Les conteneurs de smoke-test sont nommés avec l'ID/essai du workflow et sont
  arrêtés via `trap` à la sortie normale, sur `INT` ou sur `TERM`; l'option
  `--rm` retire ensuite le conteneur temporaire.

Une fois le workflow présent sur la branche par défaut du dépôt GitHub
autorisé, ouvrir **Actions → Kubernetes image builds → Run workflow** pour un
lancement manuel. Les PR déclenchées par les chemins ci-dessus exécutent les
mêmes deux jobs en séquence. Les logs se consultent dans l'exécution, puis dans
le job et l'étape en échec; conserver le SHA et les logs de build pour le
diagnostic. Un échec `npm ci`/`next build` concerne
le build Node ou l'application; un échec pip peut signaler une version de
paquet/plateforme ou l'accès à l'index PyTorch; un timeout peut signaler la
durée de compilation ou les ressources du runner. Le workflow n'a pas encore
été exécuté dans GitHub.

Le remote du checkout local pointe actuellement vers un chemin disque local,
pas vers GitHub. Le workflow ne pourra être exécuté qu'après sa mise à
disposition sur le dépôt GitHub de l'équipe; aucun push n'a été fait ici.

### Publication ultérieure

La publication est hors périmètre et nécessite une décision explicite sur le
registry, le nom de package, la visibilité, les tags immuables et la promotion
vers le cluster. Pour GHCR, prévoir les permissions minimales `packages: write`
et vérifier les droits du dépôt sur le package avec `GITHUB_TOKEN`; un autre
registry demandera ses identifiants dans GitHub Actions Secrets ou un mécanisme
OIDC approuvé par son propriétaire. Aucun secret ni permission de publication
n'est configuré dans le workflow actuel. Après autorisation, publier une image
seulement après smoke-test et conserver son digest; remplacer les placeholders
uniquement par les références réellement publiées et vérifiées.
