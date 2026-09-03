# Documentation Technique : Module de Mobilité Internationale (Learnagement)

Ce document s'adresse aux futurs développeurs et mainteneurs du projet. Il détaille l'architecture logicielle, les mécanismes de sécurité, la structure des données et la logique métier du module de gestion de la mobilité étudiante. Il centralise toutes les informations historiques et récentes du projet.

---

## 1. Architecture des Données et Modèle Relationnel (SGBD)

Le système de mobilité s'appuie sur une structure relationnelle conçue pour gérer la double contrainte des places : **places globales par université** et **places spécifiques par filière**. Le code métier backend se trouve principalement dans `backend_python/user/LNM_university.py` et `LNM_mobility_assignment.py`.

### Tables Principales

*   **`MOB_partner_university`** : Catalogue des universités (Nom, Pays, Code, Note minimale, Latitude/Longitude). Stocke les quotas globaux fixes (`S8_places`, `S9_places`) et les places restantes dynamiques calculées par le système.
*   **`MOB_partner_university_places`** : Table de liaison pour les quotas par filière et par année. **(Totalement Statut-Agnostique)**
    *   Clés étrangères : `id_partner_university` et `id_filiere`. Colonne : `annee`.
    *   *Logique de visibilité :* L'algorithme et la visibilité des places se basent uniquement sur la filière de l'étudiant, indépendamment de son statut (ex: FISE vs FISA sont regroupés sous les mêmes places universitaires).
*   **`MOB_wishes`** : Vœux des étudiants. Attributs clés : `priority` (de 1 à 6), `id_partner_university`, `id_semestre` (8 ou 9).
    *   **Marqueur de validation :** La colonne `date_soumission`. Si elle est `NULL`, le panier est "En cours". Si elle a une valeur, le panier est "Soumis" (verrouillé).
*   **`MOB_assignment`** : Résultats d'affectation finaux. Ne contient que les étudiants qui ont obtenu une place. `status` : `'pending'`, `'accepted'`, `'declined'`.

### Note d'Architecture Cruciale : `id_promo` vs `id_filiere`
Historiquement, les places dans la table `MOB_partner_university_places` étaient liées à un `id_promo`. **Cette approche a été abandonnée et migrée vers l'utilisation de `id_filiere`.**
* **Pourquoi ce changement ?** Une promotion correspond à une filière ET à un statut (ex: FISE ou FISA). Les universités partenaires négocient des places pour une spécialité (filière), peu importe si l'étudiant est en alternance ou en formation initiale. Si on gardait `id_promo`, le système séparerait artificiellement les places des alternants et des initiaux, ce qui fausserait l'algorithme.
* **Intégration et Migration des données :** Ce changement structurel n'est pas présent dans les vieux scripts de création (`V0.0.0__schema_init.sql`). Il est apporté en base par le script de migration `V0.2.8_clean_mobility.sql` qui altère la table. **Pourquoi avoir utilisé une requête de migration (`UPDATE`) plutôt que de vider la table ?** C'était une obligation technique pour **sauvegarder les données des places universitaires** qui étaient déjà insérées dans la base par les scripts précédents (comme `data_small`). Cela permet de ne perdre aucune donnée historique sur les quotas des universités, afin de pouvoir les exploiter directement avec le jeu de données de test. C'est une modification fondamentale pour le fonctionnement réaliste de l'algorithme. **À noter pour le déploiement final :** Ce script de migration est universel. Si l'application est déployée sur une base de données totalement vierge (sans données préalables), la requête UPDATE s'exécutera à vide sans générer d'erreur, et le schéma de la table sera correctement finalisé avec les bonnes contraintes. Le script est donc "production-ready" et gère tous les cas de figure.

### Jeu de Données de Test (`V0.2.9__data_small__mobilite_test.sql`)
Pour tester l'algorithme de manière isolée et exhaustive (toutes les filières, différents cas d'égalité, quotas d'universités), un fichier de test dédié a été créé dans le dossier `db/sql/`.
* **Rôle :** Ce script n'est pas conçu pour être lancé automatiquement lors de l'initialisation de production. Il sert d'environnement "bac à sable" manuel pour les développeurs.
* **Fonctionnement :** Lorsqu'il est exécuté manuellement (ou par l'outil de migration de dev), il nettoie les tables de mobilité (`DELETE FROM MOB_assignment`, `MOB_wishes`) et supprime tous les étudiants des promotions de test (années 3 et 4) pour éviter les doublons. Il insère ensuite 39 faux étudiants, dont certains ont déjà des notes et des vœux soumis, prêts à être "avalés" par l'algorithme de Phase 3.

### Étanchéité Multi-Années
Toutes les requêtes SQL du module intègrent un filtre strict (ex: `JOIN LNM_promo p ON e.id_promo = p.id_promo WHERE p.annee = 4`) pour s'assurer que seuls les étudiants actuellement en 4ème année sont traités et que les vœux, scores et affectations d'une année scolaire ne polluent jamais la campagne suivante.

---

## 2. Le Workflow de la Mobilité (Les 4 Phases)

Le système est conçu comme une machine à états stricte, divisée en 4 phases :

### Phase 1 : Lancement de la Campagne
L'administration déclenche l'ouverture (`POST /university/admin/campaign/launch`). Le système calcule automatiquement le `mobility_z_score` (Moyenne Centrée Réduite) de chaque étudiant éligible. Ce score servira au tri pour l'algorithme, assurant une équité inter-filières.

### Phase 2 : Soumission des Vœux (Espace Étudiant)
Les étudiants parcourent le catalogue, ajoutent des universités à leur panier (jusqu'à 6 vœux), et valident définitivement leur liste. 

### Phase 3 : Diagnostic et Suivi (Administration)
L'administration dispose d'un tableau de bord en temps réel pour suivre les soumissions et générer des exports. À la fin de cette phase, l'administration clique sur "Clôturer l'étape 1", ce qui force automatiquement la soumission des paniers des retardataires.

### Phase 4 : Algorithme d'Affectation (Round-Robin)
L'administration lance l'algorithme en tâche de fond (`POST /university/admin/assignment/run`).
1.  Les étudiants sont triés par `mobility_z_score` décroissant.
2.  Pour chaque étudiant, l'algorithme valide le vœu si et seulement si 3 conditions sont remplies : **Places globales > 0**, **Places filière > 0**, et **Quota de départ administration > 0**.
3.  Le traitement est asynchrone (`BackgroundTasks`).

---

## 3. Sécurité, API et Gestion des Rôles (RBAC)

Le backend (FastAPI en Python) applique une sécurité stricte combinant injection de dépendances et filtrage SQL.

### RBAC et `SQLRequest`
Toutes les requêtes vers la base de données passent par un wrapper `db_request(current_user, sql_request)`. L'objet `SQLRequest` impose l'attribut `allowedRolesRequester` (ex: `["relations_internationales"]` ou `["etudiant"]`). La fonction `db_request` vérifie l'intersection avec les rôles issus du token JWT de l'utilisateur.

### Protection contre les failles IDOR (Insecure Direct Object Reference)
Dans les routes sensibles (ajout/suppression de vœux), l'application vérifie formellement que l'ID ciblé dans l'URL correspond à la personne connectée (`if current_user.id != id_etudiant: raise 403`).
*   **Blocage volontaire des Administrateurs :** Cette règle bloque même l'administration. Un admin n'a *pas le droit* de modifier les vœux à la place d'un étudiant. Il doit utiliser la route de *réinitialisation* (`/reset-wishes`) pour rendre la main à l'étudiant.
*   **Données publiques :** Les routes de consultation (catalogue) ne nécessitent pas cette protection car les données sont communes à la filière.

### Sécurité de la tâche asynchrone
La route `assignment/run` est asynchrone. L'objet `current_user` est passé en paramètre à la tâche de fond, garantissant que les vérifications `db_request` internes s'exécuteront avec les bons droits d'administration.

### Timeout de Session (Avertissement)
Le frontend conserve l'état de créations complexes (ex: redoublants, places par filières) en RAM. Si l'administrateur prend trop de temps, son token JWT expire et l'enregistrement échouera.

---

## 4. Gestion des Cas Particuliers Métier

*   **Étudiants Redoublants :** Injectés manuellement avec leur Z-score pré-calculé avant le lancement, puis exclus mathématiquement de la moyenne de la cohorte.
*   **Le faux choix "Stage" :** L'université fictive "École Polytech Annecy-Chambéry" permet de formuler un vœu de stage sans décrémenter les quotas physiques partenaires.
*   **Étudiants Non Affectés :** Ignorés par l'algorithme. Exportables via `/unassigned-students/export` (requête `LEFT JOIN`).
*   **Désynchronisation des places (Le Reliquat) :** Les places restantes ne sont pas mises à jour à chaque clic. La fonction `sync_db_remaining_places` recalcule tout depuis zéro sur la base des statuts `'accepted'` pour éviter les *race conditions*.
*   **Transition Annuelle des Promotions :** Pour que la logique d'étanchéité multi-années fonctionne (filtre sur les années 4 et 5), les étudiants doivent changer de promotion à chaque rentrée. Voici la requête SQL illustrant le passage :
```sql
-- 1. Passage des 4ème année en 5ème année (sortent du scope d'affectation principal)
UPDATE LNM_etudiant SET id_promo = 16 WHERE id_promo = 15; -- IDU4 -> IDU5
UPDATE LNM_etudiant SET id_promo = 19 WHERE id_promo = 18; -- MM4  -> MM5
UPDATE LNM_etudiant SET id_promo = 22 WHERE id_promo = 21; -- SNI4 -> SNI5
UPDATE LNM_etudiant SET id_promo = 25 WHERE id_promo = 24; -- BAT4 -> BAT5
UPDATE LNM_etudiant SET id_promo = 28 WHERE id_promo = 27; -- EIT4 -> EIT5
UPDATE LNM_etudiant SET id_promo = 31 WHERE id_promo = 30; -- MC4  -> MC5

-- 2. Passage des 3ème année en 4ème année (les "montants", deviennent éligibles à l'algo)
UPDATE LNM_etudiant SET id_promo = 15 WHERE id_promo = 5;  -- IDU3 -> IDU4
UPDATE LNM_etudiant SET id_promo = 18 WHERE id_promo = 17; -- MM3  -> MM4
UPDATE LNM_etudiant SET id_promo = 21 WHERE id_promo = 20; -- SNI3 -> SNI4
UPDATE LNM_etudiant SET id_promo = 24 WHERE id_promo = 23; -- BAT3 -> BAT4
UPDATE LNM_etudiant SET id_promo = 27 WHERE id_promo = 26; -- EIT3 -> EIT4
UPDATE LNM_etudiant SET id_promo = 30 WHERE id_promo = 29; -- MC3  -> MC4

-- 3. (Optionnel selon le workflow) Vider les affectations et réinitialiser les vœux des doublants
-- L'API reset-wishes et le lancement de campagne s'occupent déjà de nettoyer ces données si besoin.
```

---

## 5. Pour continuer le développement...

Si vous reprenez ce code, voici les points d'évolution potentiels :
1.  **Dynamisation des Semestres :** L'abstraction du filtrage par semestre (`S8`, `S9`) devra être revue si de nouveaux semestres (ex: `S7`) sont ouverts à la mobilité.
2.  **Nouvelles règles RBAC :** L'évolution de l'architecture core pourrait nécessiter de passer les `allowedRolesRequester` sous format dictionnaire (ex: `{"roles": ["relations_internationales"]}`).
3.  **Moteur d'algorithme :** Le Round-Robin actuel favorise le classement absolu. Si une équité stricte inter-filières est requise, le tri dans `execute_assignment_task` devra être pondéré.

---

## Annexe : Routes API (Exhaustives)

### Espace Étudiant & Accès Public
| Méthode | Route API | Rôle Requis | Description |
|---|---|---|---|
| **GET** | `/university/` | `connected_user` | Récupère le catalogue public des universités |
| **GET** | `/university/etudiant/{id}` | `etudiant` | Récupère les infos générales de l'étudiant |
| **GET** | `/university/etudiant/{id}/campaign-status` | `etudiant` | Vérifie si la campagne est ouverte |
| **GET** | `/university/etudiant/{id}/wishes` | `etudiant` | Liste le panier actuel de l'étudiant |
| **POST** | `/university/etudiant/{id}/wish/{id_univ}` | `etudiant` | Ajoute une université au panier |
| **DELETE** | `/university/etudiant/{id}/wish/{id_univ}/semestre/{id_sem}`| `etudiant` | Retire un vœu du panier |
| **POST** | `/university/etudiant/{id}/wish/.../move/{dir}` | `etudiant` | Modifie la priorité d'un vœu (monter/descendre) |
| **POST** | `/university/etudiant/{id}/wishes/submit` | `etudiant` | Verrouille et soumet le panier |
| **GET** | `/university/etudiant/{id}/assignment` | `etudiant` | Affiche l'affectation finale (Phase 3) |
| **POST** | `/university/etudiant/{id}/assignment/decision` | `etudiant` | L'étudiant accepte ou refuse l'affectation |
| **GET** | `/university/etudiant/{id}/quota` | `connected_user` | Consulte le nombre de vœux maximum |

### Administration (Relations Internationales)
*Toutes les routes ci-dessous exigent le rôle `relations_internationales`.*

| Méthode | Route API | Description |
|---|---|---|
| **GET** | `/university/admin/catalog` | Liste brute pour la gestion des universités |
| **POST** | `/university/admin` | Création d'une nouvelle université partenaire |
| **PUT** | `/university/admin/{id_univ}` | Édition des quotas d'une université existante |
| **GET** | `/university/admin/mobility-quotas` | Consultation des quotas globaux de départ par filière |
| **POST** | `/university/admin/mobility-quotas` | Sauvegarde des quotas de départ |
| **POST** | `/university/admin/campaign/launch` | Ouvre la campagne et injecte les Z-scores / doublants |
| **GET** | `/university/admin/campaign/doublant/{id}` | Cherche les notes d'un étudiant pour l'ajouter en doublant |
| **GET** | `/university/admin/wishes` | Liste tabulaire de tous les paniers étudiants |
| **POST** | `/university/admin/wishes/force-submit` | Clôture Phase 1 (soumission forcée des retardataires) |
| **GET** | `/university/admin/wishes/export` | Exporte les vœux au format Excel |
| **POST** | `/university/admin/mobility/reset-wishes/{id}` | Annule la soumission d'un étudiant (retour au statut En Cours) |
| **GET** | `/university/admin/mobility/diagnostics` | Données pour les camemberts de diagnostic |
| **GET** | `/university/admin/mobility/diagnostics/export/{cat}` | Export ciblé (Soumis, Retardataires...) |
| **GET** | `/university/admin/mobility/submitted-students` | Liste des étudiants soumis pour suivi administratif |
| **POST** | `/university/admin/assignment/run` | Lance l'algorithme d'affectation (Tâche Asynchrone) |
| **GET** | `/university/admin/assignment/status` | Vérifie la progression de l'algorithme |
