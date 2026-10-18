# Mesures de sécurité

## Authentification

- Connexion via le **CAS de l'établissement** (comptes locaux possibles, mots de passe hachés en **bcrypt**).
- Jeton **JWT signé (HS256)** à durée de vie limitée.
- Un compte local **inactif et sans mot de passe** est refusé.
- Les comptes CAS ne sont créés que si l'utilisateur appartient à un **groupe autorisé**.

## Contrôle d'accès

- Chaque requête SQL déclare les **rôles autorisés**. Un contrôle centralisé, **refusant par défaut** (HTTP 403), s'applique avant toute exécution.
- Les fonctions d'administration (lancement de l'algorithme, quotas, exports, remise à zéro, statuts) sont réservées au rôle **`relations_internationales`**.
- Un étudiant ne peut consulter ni modifier que **ses propres vœux** (vérification de son identifiant) et **son propre statut d'affectation**.
- Les vœux ne sont plus modifiables **après soumission**. L'ajout de vœux est bloqué tant que la **campagne n'est pas ouverte**.

## Protection des données et du code

- **Requêtes SQL paramétrées** (pas de concaténation de saisies utilisateur).
- **Chiffrement des échanges en production** (TLS) et secrets en **variables d'environnement**.
- **Minimisation** : seules les données listées dans les mentions sont traitées. Aucune donnée sensible au sens de l'**article 9**.
- **Tests automatisés** du moteur de contrôle d'accès et de l'authentification CAS.

## À confirmer côté infrastructure

- [ ] Localisation et hébergeur
- [ ] Sauvegardes et leur durée
- [ ] Chiffrement au repos
- [ ] Politique de journalisation
- [ ] Procédure d'effacement en fin de conservation