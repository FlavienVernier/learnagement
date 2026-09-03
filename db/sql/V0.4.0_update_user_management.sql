ALTER TABLE `LNM_administratif` ADD `id_utilisateur` INT NOT NULL DEFAULT 0 FIRST, ADD UNIQUE `user_id_administratif` (`id_utilisateur`);
ALTER TABLE `LNM_enseignant` ADD `id_utilisateur` INT NOT NULL DEFAULT 0 FIRST, ADD UNIQUE `user_id_enseignant` (`id_utilisateur`);
ALTER TABLE `LNM_etudiant` ADD `id_utilisateur` INT NOT NULL DEFAULT 0 FIRST, ADD UNIQUE `user_id_etudiant` (`id_utilisateur`);

CREATE TABLE LNM_user_id_generator (
    id_user_id_generator INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW LNM_utilisateur AS
SELECT id_utilisateur, nom, prenom, mail, 'enseignant' AS type FROM LNM_enseignant
UNION ALL
SELECT id_utilisateur, nom, prenom, mail, 'etudiant' AS type FROM LNM_etudiant
UNION ALL
SELECT id_utilisateur, nom, prenom, mail, 'administratif' AS type FROM LNM_administratif;