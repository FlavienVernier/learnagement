ALTER TABLE `LNM_enseignant` DROP `service effectif`;

ALTER TABLE `LNM_administratif` CHANGE `loggin` `login` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_enseignant` CHANGE `loggin` `login` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_etudiant` CHANGE `loggin` `login` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;

ALTER TABLE `LNM_administratif` ADD `intern_account` TINYINT NOT NULL DEFAULT '1' AFTER `login`;
ALTER TABLE `LNM_enseignant` ADD `intern_account` TINYINT NOT NULL DEFAULT '1' AFTER `login`;
ALTER TABLE `LNM_etudiant` ADD `intern_account` TINYINT NOT NULL DEFAULT '1' AFTER `login`;

ALTER TABLE `LNM_administratif` CHANGE `password` `password` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_enseignant` CHANGE `password` `password` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_etudiant` CHANGE `password` `password` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;

ALTER TABLE `LNM_enseignant` CHANGE `service statutaire` `service statutaire` INT NOT NULL DEFAULT '192';
ALTER TABLE `LNM_enseignant` CHANGE `decharge` `decharge` INT NOT NULL DEFAULT '0';

DROP TABLE `VIEW_updatable`;
DROP TABLE `VIEW_parameters_of_views`;
DROP TABLE `VIEW_display`;
DROP TABLE `VIEW_check`;
DROP TABLE `MRDBF_system_request`;