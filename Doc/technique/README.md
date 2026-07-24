# Roadmap & Évolutions Futures - Module Mobilité

Ce fichier recense les pistes d'amélioration techniques et fonctionnelles pour les futures versions du module de mobilité internationale. Ces suggestions visent à améliorer l'expérience utilisateur et à fournir de meilleurs outils d'analyse au service des Relations Internationales (RI).

---

## 1. Amélioration de la Gestion des Retardataires
Bien que la clôture de la Phase 1 soumette de force les paniers en attente, le système pourrait être durci. 
* **Évolution :** Implémenter un verrouillage total (backend et frontend) pour empêcher techniquement un étudiant de continuer à formuler ou modifier des vœux après le clic de clôture de la Phase 1 par l'administrateur. Actuellement, si l'interface n'est pas rafraîchie, un étudiant pourrait tenter des manipulations tardives.

## 2. Interface Dédiée pour les Étudiants Non Affectés
À l'heure actuelle, un étudiant qui n'est affecté à aucun de ses choix par l'algorithme (par manque de places ou quotas insuffisants) se retrouve face à son interface de Phase 3 sans bouton d'acceptation/refus, ce qui peut porter à confusion.
* **Évolution :** Créer un état d'interface spécifique (ex: bannière ou message explicite) informant clairement l'étudiant que l'algorithme n'a pas pu lui attribuer de place, et lui indiquant de contacter le service RI pour trouver une solution alternative.

## 3. Nouveaux KPI et Enrichissement des Statistiques
Le tableau de bord de l'administrateur (Centre de contrôle) pourrait inclure des métriques plus globales sur le catalogue des partenaires.
* **Nouvelles métriques sur les Universités :**
  * Nombre total d'universités enregistrées dans la base de données.
  * Nombre d'universités offrant activement des places pour le S8.
  * Nombre d'universités offrant activement des places pour le S9.
  * Nombre d'universités proposant des places pour les deux semestres (S8 et S9) ou pour un seul.
* **Nouveau Graphique de Performance (Taux de Succès) :**
  * Ajouter un graphique illustrant le **ratio d'affectation** : Le nombre total d'étudiants ayant obtenu une affectation par rapport au nombre total d'étudiants ayant participé (ayant fait des choix). Cela donnera au service RI une vision immédiate de la réussite de la campagne.
