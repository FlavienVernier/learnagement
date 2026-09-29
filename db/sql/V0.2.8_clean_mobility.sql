
ALTER TABLE `MOB_partner_university`
--  DROP COLUMN `S8_total_places`,
    DROP COLUMN `S8_MM`,
    DROP COLUMN `S8_MC`,
    DROP COLUMN `S8_MMT`,
    DROP COLUMN `S8_SNI`,
    DROP COLUMN `S8_BAT`,
    DROP COLUMN `S8_EIT`,
    DROP COLUMN `S8_IDU`,
    DROP COLUMN `S8_ESB`,
    DROP COLUMN `S8_AM`,
--    DROP COLUMN `S9_total_places`,
    DROP COLUMN `S9_MM`,
    DROP COLUMN `S9_MC`,
    DROP COLUMN `S9_MMT`,
    DROP COLUMN `S9_SNI`,
    DROP COLUMN `S9_BAT`,
    DROP COLUMN `S9_EIT`,
    DROP COLUMN `S9_IDU`,
    DROP COLUMN `S9_ESB`,
    DROP COLUMN `S9_AM`,
    ADD `max_places` INT NULL AFTER `country`,
    ADD `link_to_info` VARCHAR(250) NULL AFTER `type`;

ALTER TABLE `LNM_etudiant`
    ADD `mobility_completed` BOOLEAN NOT NULL DEFAULT FALSE AFTER `id_origine`,
    ADD `mobility_note` INT NULL AFTER `mobility_completed`,
    ADD `mobility_z_score` FLOAT NULL DEFAULT NULL AFTER `mobility_note`;

ALTER TABLE `MOB_wishes`
    ADD `id_semestre` TINYINT NOT NULL AFTER `id_partner_university`,
    ADD CONSTRAINT `FK_wishes_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre`(`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT;

CREATE TABLE `MOB_assignment` (
    `id_assignment` INT NOT NULL AUTO_INCREMENT,
    `id_etudiant` INT NOT NULL,
    `id_partner_university` INT NOT NULL,
    `id_semestre` TINYINT NOT NULL,
    `status` ENUM('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending',
    PRIMARY KEY (`id_assignment`),
    UNIQUE KEY `UX_assignment_etudiant` (`id_etudiant`),
    UNIQUE KEY `SECONDARY` (`id_etudiant`, `id_partner_university`,`id_semestre`) USING BTREE,
    CONSTRAINT `FK_assignment_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT `FK_assignment_partner_university` FOREIGN KEY (`id_partner_university`) REFERENCES `MOB_partner_university` (`id_partner_university`) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT `FK_assignment_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre` (`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



-- Ajout du faux choix pour les stages !!! NE DOIT PAS ETRE DANS LA STRUCTURE !!!
-- INSERT INTO `MOB_partner_university`
--    (`name`, `code`, `latitude`, `longitude`, `address`, `country`, `languages`,`type`)
-- VALUES
--    ('Polytech Annecy-Chambery', 'MOB_STAGE', 45.919731, 6.157739, '5 chemin de Bellevue, 74940 Annecy-le-Vieux', 'France', 'francais','stage');

ALTER TABLE `MOB_partner_university`
    ADD `S8_remaining_places` INT NULL AFTER `S9_total_places`,
    ADD `S9_remaining_places` INT NULL AFTER `S8_remaining_places`;


ALTER TABLE `MOB_partner_university_places`
    ADD `remaining_places` INT NULL AFTER `number_of_places`;

CREATE TABLE `MOB_filiere_quotas` (
    `id_quota` INT NOT NULL AUTO_INCREMENT,
    `id_filiere` INT NOT NULL,
    `annee_scolaire` VARCHAR(20) NOT NULL,
    `id_semestre` INT NOT NULL,
    `places` INT NOT NULL,
    PRIMARY KEY (`id_quota`),
    UNIQUE KEY `SECONDARY` (`id_filiere`, `annee_scolaire`,`id_semestre`) USING BTREE,
    CONSTRAINT `fk_mob_filiere_quotas_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `MOB_partner_university_places`
    ADD `id_filiere` INT NULL AFTER `id_partner_university`,
    ADD `annee` INT NULL AFTER `id_filiere`;

-- Alternative : Si la base ne contient pas encore de places, ou pour réinitialiser complètement
-- la table avant de changer la structure, on peut utiliser :
-- TRUNCATE TABLE `MOB_partner_university_places`;

-- Migration des données : On récupère id_filiere et annee via id_promo
UPDATE `MOB_partner_university_places` m
JOIN `LNM_promo` p ON m.id_promo = p.id_promo
SET m.id_filiere = p.id_filiere,
    m.annee = p.annee;

-- On supprime les lignes qui n'ont pas pu être matchées (au cas où, bien que ça ne devrait pas arriver)
DELETE FROM `MOB_partner_university_places` WHERE id_filiere IS NULL OR annee IS NULL;

ALTER TABLE `MOB_partner_university_places`
    DROP FOREIGN KEY `FK_partner_university_places_as_promo`,
    DROP KEY `FK_partner_university_places_as_promo`,
    DROP INDEX `SECONDARY`,
    DROP PRIMARY KEY,
    DROP COLUMN `id_promo`,
    MODIFY `id_filiere` INT NOT NULL,
    MODIFY `annee` INT NOT NULL,
    ADD PRIMARY KEY (`id_partner_university`, `id_filiere`, `annee`),
    ADD UNIQUE KEY `SECONDARY` (`id_partner_university`, `id_filiere`, `annee`) USING BTREE,
    ADD CONSTRAINT `FK_partner_university_places_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT;