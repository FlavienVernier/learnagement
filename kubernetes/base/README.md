# Learnagement Kubernetes base (préliminaire)

> Objectif : expliquer les ressources Kustomize, la configuration externe attendue et les limites du socle non déployé.

Ce Kustomize base matérialise les ressources et frontières réseau ciblées. Il
n'est pas prêt à être déployé. Dans le checkout de livraison courant, aucune
image n'a été construite ou publiée; les quatre images applicatives restent
explicitement des placeholders. Les images de production et les
configurations/Secrets externes restent à fournir.
Il n'existe pas encore d'Ingress ni de classe de stockage confirmée.

## Rendu statique

Depuis la racine du dépôt :

```powershell
kubectl kustomize kubernetes/base
python kubernetes/validate_base.py
```

Cette commande ne contacte pas un cluster et ne crée aucune ressource. Ne pas
utiliser `kubectl apply` avec ce dossier. Le validateur structurel requiert
PyYAML; si le module manque dans l'environnement Python sélectionné, installez
la dépendance isolée avec
`python -m pip install -r kubernetes/requirements-validation.txt`.
Il vérifie également la cohérence statique entre le port, l'utilisateur et la
commande de chaque Dockerfile Kubernetes et son Deployment; cela ne remplace
pas un build ni un smoke-test d'image.

Dans le checkout de livraison, le 17 novembre 2026, `kubectl kustomize
kubernetes/base` et `python -B kubernetes/validate_base.py` ont réussi :
15 ressources rendues et contrats statiques vérifiés. Aucun cluster ni
`kubectl apply` n'a été utilisé.

## Ressources

- `Namespace/learnagement` isole les noms et ressources Kubernetes de ce socle.
- `learnagement-network-config` contient uniquement les adresses de services
  et valeurs de transport interne confirmées par le code.
- `backend.yaml` fournit un Service ClusterIP et un Deployment Backend. Son
  image est un placeholder à remplacer après validation et publication
  approuvée.
- `interfaces.yaml` fournit les Services/Deployments PHP, Next.js et Dash.
  Les trois images restent des placeholders jusqu'à la validation et la
  publication approuvée de leurs images.
- `mysql.yaml` fournit un Service interne et un StatefulSet MySQL avec un PVC
  de 10 Gi provisoire, rétention PVC sur scale/delete, et mise à jour manuelle
  `OnDelete`.
- `networkpolicy.yaml` restreint l'ingress MySQL au Backend et l'ingress
  Backend aux trois interfaces. L'egress Backend est limitée au Service MySQL
  en TCP/3306 et aux requêtes DNS TCP/UDP 53. L'egress des trois frontends
  reste ouverte : PHP valide des tickets CAS externes et Dash contacte le
  service IA non inclus dans ce socle; leurs destinations exactes ne sont pas
  encore déclarées. L'application des politiques dépend d'un CNI compatible.
- phpMyAdmin, le service IA et Ollama ne sont pas inclus : ils restent
  optionnels et nécessitent une décision d'exposition/authentification.

Le Backend utilise `/health` pour startup/liveness et une readiness distincte
qui vérifie la résolution DNS et l'ouverture TCP vers `MYSQL_SERVER:MYSQL_PORT`.
Une panne de MySQL retire donc le Backend des endpoints Ready sans provoquer
son redémarrage par la liveness. Ce contrôle TCP ne valide ni les identifiants
applicatifs, ni les permissions, ni le schéma ou les vues. Les probes MySQL
reprennent `mysqladmin ping`; elles ne valident pas les identifiants
applicatifs.

Les quatre images applicatives sont déclarées non-root, sans privilèges
d'élévation et sans capabilities Linux, avec le profil seccomp
`RuntimeDefault`. MySQL conserve le comportement de l'image officielle et
n'est pas forcé sous un UID non-root.

Dash ne reçoit pas de volume `/data`: le code inspecté ne fait qu'essayer de
lire `/data/data_reseau_polytech.json`, tolère son absence et ne contient pas
d'écriture vers ce chemin. Ce fichier est absent du checkout de livraison et
du contexte d'image; la fonctionnalité de données associée n'est donc pas
alimentée. Ne pas créer de PVC avant qu'un propriétaire fournisse la donnée et
confirme un besoin de persistance.

Les Deployments conservent actuellement la stratégie `Recreate`: un
remplacement provoque une indisponibilité pendant le rollout. Une stratégie
`RollingUpdate` n'est pas activée sans mesures de capacité et validation de
compatibilité des versions Backend/DB. MySQL reste en StatefulSet à une
réplique avec stratégie `OnDelete`; un rolling update de DB ne fournit pas de
haute disponibilité et n'est pas automatique.

Ordre opérationnel recommandé (sans équivaloir à un `kubectl apply`) :
fournir d'abord les Secrets/ConfigMaps et confirmer StorageClass/PVC, attendre
MySQL Ready, puis Backend Ready, et enfin déployer/valider les interfaces.
Un changement MySQL ou de schéma doit être planifié et approuvé séparément;
aucun ordre de création YAML ne garantit une migration rétrocompatible.

Les requests/limits totalisent environ 800m CPU et 1664 Mi mémoire demandés,
pour des limites cumulées de 4 CPU et 5 Gi; ces valeurs ne sont pas issues de
mesures et ne décrivent pas la capacité libre du cluster cible. Un `maxSurge: 1`
ajouterait encore la demande du Pod remplacé. Les commandes de build et leur
état sont décrits dans
[`docker/kubernetes/README.md`](../../docker/kubernetes/README.md).
Les gates opérationnels avant un premier déploiement sont suivis dans la
[`checklist Kubernetes`](../../docs/kubernetes-deployment-checklist.md).

## Configurations et Secrets externes obligatoires

Aucune donnée secrète n'est versionnée ici. Avant tout essai de déploiement,
fournir dans le namespace `learnagement` :

1. Secret `learnagement-database-credentials` avec les clés
   `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` et `MYSQL_ROOT_PASSWORD`.
   Le Backend reçoit les deux clés de compte et de base sous les noms de
   variables réellement attendus (`MYSQL_USER_LOGIN`, `MYSQL_USER_PASSWORD`,
   `MYSQL_DB`).
2. Secret `learnagement-auth-secrets` avec `JWT_SIGNING_KEY`; cette clé est
   partagée par Backend, Next.js et Dash selon les usages présents dans le
   code.
3. ConfigMap `learnagement-app-config` avec `SESSION_TIMEOUT` et les valeurs
   de navigation Dash `INSTANCE_URL`, `FRONT_PHP_PORT` et
   `FRONT_NEXTAUTH_PORT`. Les valeurs autorisées/hôtes publics ne sont pas
   fournis dans le dépôt et ne sont donc pas inventés.
4. Secret `learnagement-php-runtime` contenant la clé fichier `.env`. Produire
   ce fichier à partir de la configuration PHP approuvée, sans secrets DB :
   PHP doit joindre le Backend, et ne doit pas recevoir les identifiants
   MySQL.

Ces objets sont volontairement absents du Kustomize base et doivent être
générés par le gestionnaire de secrets/configuration de l'environnement cible.

## Blocages avant déploiement

- Les configurations DEV/Compose montent le code depuis l'hôte et utilisent
  des commandes de développement. Des Dockerfiles dédiés existent dans
  `docker/kubernetes/`; les quatre images doivent encore être construites et
  validées depuis le checkout de livraison. Les tags des manifests restent
  donc des placeholders.
- Compose définit un argument de démarrage MySQL en plus de l'image officielle;
  ce base ne le reprend pas. Vérifier la parité de cet argument et son besoin
  avec le propriétaire DB avant tout déploiement.
- Le code source `backend_python/app.py` n'exécute plus `init.init()` au
  démarrage. `backend_python/init.py --apply` peut exécuter des
  `CREATE OR REPLACE VIEW` pour les vues `ExplicitSecondaryKs_*`; aucune
  exécution n'a eu lieu sur DEV. Le propriétaire DB doit valider un plan de
  migration, sauvegarde et retour arrière avant d'exécuter ce DDL.
- Les scripts `db/docker-entrypoint-initdb.d` ne sont pas montés dans le
  StatefulSet : les scripts d'initialisation MySQL ne sont pas un mécanisme de
  migration pour un volume déjà initialisé.
- Le PVC de 10 Gi suppose une StorageClass par défaut et n'est pas dimensionné
  sur mesure. Vérifier la rétention PV effective, les sauvegardes testées et la
  capacité avant d'appliquer.
- Le code Dash essaie de lire `/data/data_reseau_polytech.json`, tolère le
  fichier absent et ne contient pas d'écriture vers `/data`. Ce fichier est
  absent du checkout et du contexte d'image; aucun volume persistant n'est
  défini. Le propriétaire Dash doit fournir la donnée et préciser son mode de
  distribution avant d'activer la fonctionnalité correspondante.
- `ENV=dev` et HTTP interne correspondent au chemin d'exécution non-TLS
  observé; ce socle ne constitue pas une configuration de production. Aucun
  Ingress, nom DNS, TLS ou exposition publique n'est choisi.
- Les probes ne démontrent ni les flux métier ni l'acceptation d'un compte
  Backend. L'authentification IA et Ollama ne sont pas incluses.
- Au contrôle du 16 novembre 2026, les conteneurs DEV Backend et Next.js
  ont présenté une dégradation : Backend exited (255, cause non déterminée);
  Next.js a fini par redevenir healthy après 28 min d'installation de paquets
  et compilation à froid de `/health`. Le build Kubernetes Next.js a été
  reporté; la mémoire libre hôte est descendue à 0,24 GiB au dernier contrôle.
  Aucun déploiement ne doit être tenté avant la résolution Backend et la
  validation de toutes les images.
- Mission 06 : le build Next.js est reporté, sans tentative, avec 0,78 Gio de
  mémoire hôte libre; le Next.js DEV actif utilisait environ 505 Mio et 81 %
  CPU. Aucun changement de conteneur DEV n'a été fait.
- Mission 07 : le build reste reporté. Windows avait 1,02 Gio libres;
  Ubuntu WSL partage le même Docker Desktop avec 1,1 Gio disponibles et un
  swap presque saturé. Les builders Buildx existants ciblent le même daemon;
  aucun endpoint distant ou moteur standalone autorisé n'est disponible.
  Les placeholders Next.js et Dash restent intentionnels.

Le socle est validé statiquement uniquement. Aucun `kubectl apply`, cluster,
volume MySQL ou conteneur DEV n'a été utilisé. Des conteneurs temporaires
isolés ont servi aux smoke tests des images.
