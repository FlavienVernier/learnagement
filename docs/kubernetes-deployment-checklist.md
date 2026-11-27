# Checklist de préparation au déploiement Kubernetes

> Objectif : suivre les prérequis, autorisations et preuves à réunir avant tout déploiement Kubernetes.

Cette checklist est un gate opératoire, pas une autorisation de déploiement.
Le socle `kubernetes/base/` n'a pas été appliqué à un cluster. Toute action
sur un cluster, une base réelle ou un service DEV exige une autorisation
explicite préalable.

## État du checkout de livraison — 17 novembre 2026

Les validations d'images cochées dans les notes historiques ci-dessous ont été
réalisées dans le checkout de récupération; elles ne prouvent pas la
reproductibilité des images dans ce checkout. Les quatre images ne sont pas
construites ici, le workflow n'a pas été exécuté et aucune image n'a été
publiée. Le `composer.lock` provient d'un fichier local non suivi du checkout
de récupération; sa cohérence sera contrôlée par le build Composer de la CI.

## 1. Capacité de build et provenance des images

- [ ] Construire et smoke-tester Backend, PHP, Next.js et Dash dans le
  workflow `Kubernetes image validation`; le workflow ne publie pas d'image.
- [x] Le handler Next.js `/health` est présent dans le checkout de livraison
  et inclus dans le contexte Docker.
- [ ] Après un build CI réussi, construire les images destinées au déploiement
  avec des tags approuvés et enregistrer leurs digests, Dockerfiles et versions
  de dépendances; les tags CI dérivés du SHA ne sont pas publiés.
- [ ] Enregistrer les digests, tags, Dockerfiles et versions de dépendances
  utilisés pour chaque build; aucun tag local ne constitue une publication.
- [ ] Effectuer une analyse d'image et corriger les vulnérabilités bloquantes
  selon le processus de l'équipe.

**Gate actuel : validation locale requise, puis exécution CI après livraison.**
Le workflow et les manifests restent locaux à ce checkout et ne sont ni
stagés ni publiés. Les images des manifests restent des placeholders; le
workflow ne publie rien et ne les remplace pas. Aucun build Docker local n'est
autorisé par cette mission.

Le Dockerfile PHP installe `curl`, `dom`, `mysqli` et `simplexml`; le smoke-test
CI vérifie leur chargement. Le validateur statique exige aussi la présence de
ces extensions dans le Dockerfile. Ces contrôles ne sont pas encore confirmés
par un build exécuté dans GitHub Actions.

### Lot minimal à examiner avant livraison

| Fichier | État local | Utilité / dépendance | Indispensable |
|---|---|---|---|
| `.github/workflows/kubernetes-images.yml` | Non suivi | Build et smoke-test CI; déclencheur du premier run manuel | Oui |
| `docker/kubernetes/front-nextjs/Dockerfile` | Non suivi | Build Next.js depuis le contexte racine, package-lock et configuration de l'application | Oui |
| `docker/kubernetes/front-nextjs/Dockerfile.dockerignore` | Transféré et ajusté dans le checkout de livraison | Limite le contexte sans exclure le handler `/health` | Oui |
| `docker/kubernetes/front-dash/Dockerfile` | Non suivi | Build Dash et dépendances Python/PyTorch depuis le contexte racine | Oui |
| `docker/kubernetes/front-dash/Dockerfile.dockerignore` | Non suivi | Exclut secrets, tests et données runtime du contexte | Oui |
| `.gitignore` | Modifié dans le checkout de livraison | Réinclut seulement le workflow Kubernetes et `front_PHP/composer.lock` | Nécessaire pour versionner la CI et le lockfile |
| `front_NextJS/app/health/route.tsx` | Suivi dans le checkout de livraison | Handler GET sans auth/DB/service, réponse JSON `{"status":"ok"}` | Oui, nécessaire aux probes et smoke-tests |
| `docker/kubernetes/front-nextjs/Dockerfile.dockerignore` | Modifié dans le checkout de livraison | Exclut le doublon local non suivi `front_NextJS/app/health/route.ts` du contexte d'image | Oui, évite deux handlers au même segment |
| `front_PHP/composer.lock` | Transféré depuis un fichier local non suivi | Verrouille les dépendances Composer utilisées par l'image PHP | Oui; validation par build CI encore requise |

`front_NextJS/package.json`, `package-lock.json`,
`front_DashPlotly/requirements.txt` et `front_DashPlotly/main.py` proviennent
du HEAD de livraison. Les manifests, Dockerfiles Backend/PHP, documents et
handler Next `/health` ont été transférés depuis des fichiers locaux non
suivis du checkout de récupération. Les autres modifications locales
applicatives ou données ne font pas partie du transfert.

## 2. Contrats, configuration et secrets

- [ ] Fournir les Secrets dans le namespace `learnagement` via le mécanisme
  approuvé; ne jamais placer de valeur secrète dans Git, une commande tracée,
  un log ou une image.
- [ ] Confirmer que les ConfigMaps fournissent aux interfaces les DNS/ports
  Backend et que leurs clés correspondent aux variables réellement lues par
  les applications.
- [ ] Confirmer l'hôte public, le protocole, l'Ingress et la terminaison TLS;
  aucune adresse ou classe d'Ingress n'est définie par le socle actuel.
- [ ] Valider avec les responsables applicatifs les contrats d'authentification
  des parcours Backend ↔ PHP, Next.js et Dash.
- [ ] Obtenir un compte de test non-production et un endpoint métier GET
  approuvé pour le test authentifié de bout en bout.

## 3. Backend et schéma MySQL

- [x] Le code source démarre le serveur sans appeler le DDL; l'opt-in
  `python init.py --apply` est séparé.
- [x] Suite Backend complète : 152 tests réussis sous Python 3.13; aucun accès
  à une vraie base. Une mise en garde de dépréciation Starlette subsiste.
- [ ] Le propriétaire Backend/DB confirme l'existence et la version des vues
  `ExplicitSecondaryKs_*` attendues par les routes.
- [ ] Le propriétaire DB approuve une migration versionnée, son ordre
  d'exécution, une sauvegarde vérifiée et une procédure de retour arrière.
- [ ] Valider sur une base d'intégration dédiée, jamais sur DEV, que le
  Backend démarre et que ses routes métier requises fonctionnent.
- [x] Le manifest Backend distingue désormais startup/liveness HTTP `/health`
  de la readiness, qui vérifie la résolution et l'ouverture TCP vers le
  Service MySQL.
- [ ] Ajouter/valider une readiness applicative qui confirme authentification,
  permissions et schéma DB; le contrôle TCP manifest ne les vérifie pas.
- [ ] Valider sur les images et le cluster cibles que les contextes non-root,
  capabilities supprimées et seccomp `RuntimeDefault` sont compatibles avec
  les chemins d'écriture runtime.
- [ ] Déterminer la cause de l'exit 255 du Backend DEV avant toute demande de
  démarrage de ce conteneur. Le dernier état Docker connu indique
  `OOMKilled=false`, `RestartCount=0`; les logs conservés ne montrent pas de
  traceback fatal. Les tests isolés A (5 min) et C (15 min) sur l'image
  temporaire issue du checkout de récupération sont restés sains; ils ne
  reproduisent ni n'expliquent cet exit 255.

## 4. Stockage, réseau et ressources

- [ ] Confirmer la StorageClass, capacité PVC, rétention, sauvegardes et
  restauration MySQL sur l'environnement cible.
- [ ] Valider que les scripts `docker-entrypoint-initdb.d` ne sont pas
  considérés comme un mécanisme de migration d'un volume déjà initialisé.
- [ ] Confirmer le besoin et la provenance des données Dash : `data/` est vide
  dans le checkout observé et exclu du contexte de build.
- [x] L'egress Backend est limitée à MySQL/TCP 3306 et DNS/TCP+UDP 53.
- [ ] Vérifier que le CNI cible applique les NetworkPolicies et que son
  résolveur DNS est compatible avec la règle 53 (destination non restreinte
  pour tolérer CoreDNS ou NodeLocal DNS).
- [ ] Cartographier/valider les sorties PHP→CAS et Dash→service IA/fournisseurs;
  l'egress de PHP, Next.js et Dash reste ouverte à ce stade. Ne la restreindre
  qu'après confirmation des destinations et ports par les responsables.
- [ ] Mesurer les besoins CPU/RAM des images en charge représentative; les
  valeurs actuelles des manifests sont provisoires et non issues de mesures.
- [x] Décision Mission 11 : conserver `Recreate` pour les quatre Deployments;
  la capacité, les probes métier et la compatibilité des versions Backend/DB
  ne prouvent pas encore qu'un `RollingUpdate` serait sans coupure.
- [ ] Pour PHP/Next.js/Dash, mesurer la capacité de surge et valider readiness,
  sessions et parcours sous charge avant d'envisager `maxUnavailable: 0`,
  `maxSurge: 1`.
- [ ] Pour Backend, valider migrations rétrocompatibles, fonctionnement de deux
  versions simultanées et pool DB avant d'envisager un `RollingUpdate`.
- [ ] Pour MySQL, prévoir une migration maîtrisée/sauvegarde; une seule réplique
  `OnDelete` implique une indisponibilité lors de son remplacement.

## 5. Contrôles statiques avant toute demande de déploiement

Depuis la racine du checkout :

```powershell
kubectl kustomize kubernetes/base
python kubernetes/validate_base.py
git diff --check
```

- [x] Le rendu Kustomize produit 15 ressources après ajout de la politique
  egress Backend.
- [x] `kubernetes/validate_base.py` parse le rendu et contrôle selectors,
  ports de Services, probes, readiness Backend/MySQL, règles d'egress,
  NetworkPolicies, contextes de sécurité, Secrets externes, placeholders
  d'images, stratégies de rollout et contrats statiques Dockerfile
  port/utilisateur/commande.
- [x] Mission 10 : readiness Backend/MySQL, utilisateurs non-root, capabilities
  supprimées et seccomp `RuntimeDefault` sont vérifiés dans les manifests.
- [ ] Après les smoke-tests Next.js et Dash, remplacer uniquement les
  placeholders par les tags construits et revalider le rendu.
- [ ] Confirmer qu'aucune donnée secrète n'est embarquée dans les manifests.
- [ ] Examiner le diff complet et faire approuver les modifications par les
  propriétaires des composants concernés.

## 6. Gate d'autorisation et vérification post-déploiement

- [ ] Obtenir l'approbation explicite du propriétaire de l'environnement
  Kubernetes et convenir d'une fenêtre de déploiement/rollback.
- [ ] Appliquer les manifests uniquement après validation de tous les gates
  précédents; ce document n'autorise pas `kubectl apply`.
- [ ] Vérifier l'état des Pods, Events, probes, endpoints internes et logs
  sans publier de secrets.
- [ ] Exécuter les smoke-tests HTTP puis les parcours authentifiés de lecture
  avec les comptes et endpoints de test approuvés.
- [ ] Documenter les résultats, incidents et décision de progression.

## Prochaine séquence

1. Revoir la liste minimale ci-dessus et isoler les lignes `.gitignore`
   nécessaires des changements préexistants avant toute livraison.
2. Après autorisation, rendre le workflow et ses Dockerfiles disponibles sur
   `dev`; le lancement
   manuel requiert sa présence sur la branche par défaut. Une PR déclenchera
   ce workflow uniquement une fois celui-ci présent dans sa branche de base.
3. Déclencher manuellement `Kubernetes image builds` et vérifier les logs de
   build et smoke-test pour Next.js puis Dash; le runner
   ne conserve pas les images après le job.
4. Choisir et autoriser un registry ainsi que les tags de déploiement; publier
   les images et remplacer les placeholders seulement après smoke-test.
5. Fermer les gates DB, Secrets, stockage, TLS, réseau et tests authentifiés
   avant toute demande de déploiement.
