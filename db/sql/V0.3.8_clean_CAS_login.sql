ALTER TABLE `LNM_enseignant` DROP `service effectif`;

ALTER TABLE `LNM_administratif` CHANGE `loggin` `login` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_enseignant` CHANGE `loggin` `login` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;
ALTER TABLE `LNM_etudiant` CHANGE `loggin` `login` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL;