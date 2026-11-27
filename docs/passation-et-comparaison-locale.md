# Passation et comparaison locale de Learnagement

> Objectif : transmettre l'état d'orchestration et fournir une méthode sûre de comparaison entre checkouts.

Ce document transmet l'état réel de l'orchestration Learnagement et décrit
comment comparer deux copies locales sans écraser les travaux respectifs.
Il ne remplace pas les documents spécialisés. Il ne constitue pas une preuve
qu'un démarrage Docker, une communication interservices ou un déploiement
fonctionne.

## 1. Référence vérifiée

- Branche courante : `dev`.
- HEAD vérifié : `315d5753fc05464b1ff912e5c36d3b54c33d2c00`.
- Aucun fichier n'est stagé.
- Les modifications suivies et les fichiers non suivis existants sont conservés.
- Aucun commit, staging, fusion, rebase, reset ou opération destructive n'a été
  effectué pour établir cette passation.

## 2. Bilan concret du travail d'orchestration

### Architecture Docker et configuration

Le travail d'orchestration a porté sur :

- la cartographie des services Compose ;
- les réseaux front/back ;
- les dépendances `service_healthy` ;
- les ports internes et hôtes ;
- les volumes persistants ;
- le montage read-only des scripts SQL ;
- la sélection MySQL seul ou MySQL+Backend ;
- la préparation de noms uniques pour les instances isolées ;
- la résolution canonique `MYSQL_SERVER=learnagement_data_mysql_<INSTANCE_NAME>`.

Preuves dans le dépôt :

- [docker_compose.py](../docker_compose.py) ;
- [env.py](../env.py) ;
- [Learnagement.py](../Learnagement.py) ;
- [mysql-first-start.md](mysql-first-start.md).

Ces fichiers montrent la configuration et les préconditions. Ils ne prouvent pas
qu'un démarrage, une résolution DNS ou une connexion MySQL ont réussi.

### Documentation de livraison

Les documents d'orchestration comprennent :

- [release-delivery-guide.md](release-delivery-guide.md) ;
- [interservice-contracts.md](interservice-contracts.md) ;
- [integration-test-plan.md](integration-test-plan.md) ;
- [mysql-first-start.md](mysql-first-start.md) ;
- [backend-mysql-validation-runbook.md](backend-mysql-validation-runbook.md) ;
- [kubernetes-readiness.md](kubernetes-readiness.md) ;
- [kubernetes-deployment-checklist.md](kubernetes-deployment-checklist.md).

Ces documents regroupent les commandes, les preuves attendues, les blocages,
les responsabilités et les critères d'arrêt. Ils ne remplacent pas les preuves
runtime.

### Contrats interservices

Les contrats disponibles ont été consolidés pour :

- PHP vers Backend ;
- Next.js vers Backend ;
- Dash vers Backend ;
- Backend vers MySQL ;
- chatbot Dash vers Groq ;
- futur service IA autonome, non implémenté.

Les contrats non confirmés restent ouverts. En particulier :

- timeout et retry Next.js ;
- politique CAS runtime ;
- transmission réelle du cookie/JWT Next.js ;
- certificats Dash ;
- liste et disponibilité des tables MySQL ;
- contrat propriétaire du futur service IA.

### Kubernetes et CI/CD

Le dépôt contient :

- le socle `kubernetes/base/` ;
- le validateur `kubernetes/validate_base.py` ;
- les Dockerfiles sous `docker/kubernetes/` ;
- le workflow `.github/workflows/kubernetes-images.yml`.

Le validateur a été décrit comme un contrôle statique réussissant localement.
Le workflow prépare la validation, les tests isolés, les builds et les
smoke-tests. Il utilise `push: false`; aucune publication d'image n'est
prévue par le workflow. Aucun run GitHub Actions ni cluster n'est démontré par
ce document.

### Tests

La collecte vérifiée contient 28 cas :

| Fichier | Cas collectés | Nature |
|---|---:|---|
| `test_compose_startup_order.py` | 1 | Génération/structure Compose |
| `test_backend_mysql_contract.py` | 7 | Construction SQLAlchemy simulée |
| `test_http_contract_sources.py` | 9 | Vérifications statiques des sources |
| `test_dash_backend_http_contract.py` | 10 | Serveur HTTP local simulé |
| `test_windows_cli_import.py` | 1 | Import CLI Windows |

Ces tests ne créent pas de MySQL réel et ne démarrent pas Docker. Une réussite
historique des tests isolés ne prouve pas une intégration runtime.

## 3. Validations réellement réalisées

Éléments vérifiés comme contrôles statiques ou locaux :

- état Git et HEAD ;
- liens Markdown locaux ;
- `git diff --check` ;
- génération SQLAlchemy remplacée par une capture fictive ;
- dépendances Compose statiques ;
- sélection MySQL-only statique ;
- rendu/validation des manifests Kubernetes ;
- 28 cas pytest collectés ;
- contrats source PHP, Next.js, CAS, Dash et Groq.

Lorsqu'un test a été exécuté historiquement, il reste limité à son périmètre :

- les tests MySQL remplacent `create_engine` et n'ouvrent pas de base ;
- les tests PHP/Next.js vérifient surtout les sources ;
- le test Dash utilise un serveur HTTP local ;
- les tests Compose vérifient le YAML généré et ne démarrent pas Docker.

## 4. Opérations runtime non réalisées

Les éléments suivants ne sont pas prouvés :

- démarrage MySQL isolé ;
- healthcheck MySQL réel ;
- initialisation des dix scripts sur un volume neuf ;
- authentification MySQL ;
- présence des tables attendues ;
- connexion SQLAlchemy réelle ;
- démarrage Backend après MySQL ;
- communication PHP/Next.js/Dash avec un Backend réel ;
- panne et reprise de MySQL ;
- persistance et restauration ;
- tests CAS avec un fournisseur réel ;
- intégration d'un service IA autonome ;
- déploiement Kubernetes ;
- publication d'image ;
- sauvegarde vérifiée et rollback runtime.

## 5. État des étapes

| Étape | État réel | Critère de fin |
|---|---|---|
| 4.2 — Préparation | Partiel | Compose/variables/ressources uniques validés statiquement |
| 4.3 — Premier démarrage | Bloqué | MySQL running/healthy avec preuve authentifiée et schéma |
| 4.4 — Communications | Partiel | Appels réels PHP, Next.js, Dash et Backend documentés |
| 4.5 — Fiabilisation | Partiel | Panne/reprise/persistance testées sur un environnement isolé |
| 5 — Service IA | Partiel | Contrat IA autonome confirmé et intégré |
| 6 — Contrats | Partiel | Contrats non ambigus confirmés par leurs propriétaires |
| 7 — Tests globaux | Partiel | Suite isolée plus suite runtime globale exécutée |
| 8 — Livraison | Partiel | Backup/restauration, registry, Kubernetes, rollback et preuves validés |

## 6. Répartition entre l'orchestration et les autres modules

### Périmètre d'orchestration

- Docker/Compose ;
- réseaux, volumes, ports ;
- `.env` et génération de configuration ;
- isolation des environnements ;
- contrats d'intégration ;
- tests statiques/simulés ;
- runbooks MySQL/Backend ;
- Kubernetes et CI/CD ;
- documentation et livraison.

### Périmètre fonctionnel

Les propriétaires restent responsables de :

- Backend : logique API, SQLAlchemy, authentification et schéma ;
- PHP : session, CAS, proxy et codes HTTP ;
- Next.js : NextAuth, cookie/JWT, timeout et retry ;
- Dash : requêtes, certificat, affichage et chatbot ;
- IA : contrat du futur service, fournisseur, outils et sécurité.

Les modifications de ces modules ne doivent pas être attribuées à
l'orchestration sans une preuve explicite de changement, telle qu'un diff ou
un historique Git vérifiable.

## 7. Procédure de comparaison des deux copies

Cette procédure ne demande aucun changement Git et ne compare le projet de la
collègue que lorsque son chemin local a été fourni.

### Informations à relever dans chaque copie

Pour chaque copie, relever séparément :

1. branche courante ;
2. HEAD ;
3. status suivi/non suivi ;
4. diff des fichiers suivis ;
5. fichiers non suivis ;
6. fichiers présents dans une copie et absents de l'autre ;
7. contenu des fichiers prioritaires ;
8. secrets jamais copiés ni affichés.

### Commandes de lecture seule

Ces commandes n'utilisent aucun dépôt distant et ne modifient rien :

```powershell
git branch --show-current
git rev-parse HEAD
git status --porcelain=v1 --untracked-files=all
git diff --stat
git diff --name-status
git diff --check
git ls-files --others --exclude-standard
git log -10 --oneline
git --no-pager diff -- <fichiers prioritaires>
```

Lorsqu'une collègue fournit son chemin local, une comparaison ponctuelle peut
être effectuée en lecture seule avec `git diff --no-index -- <copieA>/<fichier>
<copieB>/<fichier>`. Cette commande affiche uniquement les différences et ne
copie aucun fichier. Le chemin de la collègue ne doit pas être utilisé tant
qu'il n'a pas été fourni.

Ne pas utiliser `git add`, `git reset`, `git checkout`, `git merge`,
`git rebase`, `git clean` ou `git restore` pendant cette comparaison.

### Fichiers prioritaires

Comparer d'abord :

- `docker_compose.py`
- `env.py`
- `Learnagement.py`
- `backend_python/`
- `front_PHP/`
- `front_NextJS/`
- `front_DashPlotly/`
- `tests/integration/`
- `docs/`
- `kubernetes/`
- `docker/kubernetes/`
- `.github/workflows/`
- `.gitignore`

Comparer ensuite les fichiers SQL uniquement en lecture :

- `db/sql/*.sql`
- `db/docker-entrypoint-initdb.d/` uniquement pour vérifier sa présence.

Ne pas comparer ni fusionner les secrets locaux :

- `.env`
- `.env.*`
- certificats
- clés
- données privées
- volumes Docker.

## 8. Décider ensemble quelles modifications conserver

Adopter une méthode documentaire avant toute fusion :

1. produire un inventaire des fichiers modifiés ;
2. classer chaque différence :
   - identique ;
   - complémentaire ;
   - divergente ;
   - propriétaire d'un autre module ;
   - obsolète.
3. décider chaque divergence par propriétaire de domaine ;
4. conserver les modifications qui respectent les responsabilités ;
5. faire une copie de sauvegarde hors dépôt avant toute application ;
6. appliquer les changements petits et indépendants ;
7. tester uniquement après chaque lot ;
8. conserver les fichiers non résolus comme « à arbitrer », sans écraser.

Pour les mêmes lignes, ne pas choisir automatiquement une copie. Relire :

- l'objectif technique ;
- les dépendances ;
- les appels réels ;
- les tests existants ;
- les risques de données ;
- la personne responsable du module.

## 9. Proposition de répartition des tâches

### Orchestration

- finaliser les documents ;
- vérifier les variables et les noms Compose ;
- préparer les instances isolées ;
- produire les preuves MySQL/Backend ;
- valider Docker Compose ;
- préparer les manifests et les gates Kubernetes ;
- assurer la continuité du dépôt.

### Backend

- fournir l'endpoint GET de validation ;
- définir la portée de `/health` ;
- confirmer les tables attendues ;
- tester SQLAlchemy avec MySQL réel ;
- corriger uniquement les défauts Backend démontrés.

### PHP

- confirmer CAS, session et JWT ;
- fournir les codes HTTP attendus ;
- valider `/api.php` sur une instance isolée.

### Next.js

- confirmer le cookie/JWT transmis ;
- définir timeout et retry ;
- documenter les codes d'erreur ;
- valider `/token` et `/api/proxy`.

### Dash

- confirmer le certificat interne ;
- fournir un endpoint GET sûr ;
- fournir un compte de test ;
- valider les méthodes, erreurs et JSON.

### IA

- confirmer l'existence ou l'absence d'un service autonome ;
- fournir son contrat complet ;
- valider son intégration avec le Backend uniquement après confirmation.

### Données

- autoriser les scripts SQL sur un volume neuf ;
- confirmer les tables et migrations ;
- fournir les données privées seulement hors dépôt et hors journal.

### Kubernetes

- confirmer le registry ;
- confirmer les Secrets externes ;
- confirmer StorageClass/PVC ;
- confirmer TLS, réseau et rollback ;
- approuver toute application au cluster.

## 10. Plan de fusion progressif

1. Fusionner les documents de passation et les tests isolés.
2. Comparer puis stabiliser `.gitignore`, Docker Compose et environnement.
3. Comparer les modules fonctionnels sans les modifier tant que les contrats
   ne sont pas confirmés.
4. Réunir les tests et les contrats.
5. Préparer les scripts SQL sur un volume neuf.
6. Obtenir un GO explicite avant toute validation runtime.
7. Commencer MySQL seul, puis Backend, puis les fronts.
8. Ajouter l'IA uniquement après son contrat.
9. Tester Kubernetes seulement après les images, Secrets et autorisations.
10. Finaliser les preuves de livraison.

## 11. Première action

Une seule première action est nécessaire : comparer les statuts Git des deux
copies et produire un inventaire des fichiers modifiés ou non suivis.

Le chemin de la copie de la collègue n'a pas été fourni. Tant que ce chemin est
absent, aucune comparaison avec sa copie n'est effectuée.

## 12. Contrôles finaux

Cette passation doit être vérifiée sur :

- branche et HEAD ;
- fichier du guide central ;
- liens locaux ;
- absence de secret ;
- absence de fichier `.env` réel ;
- absence de modifications fonctionnelles attribuées ;
- cohérence des statuts runtime ;
- absence de contrevérité sur Docker, MySQL, IA ou Kubernetes.
