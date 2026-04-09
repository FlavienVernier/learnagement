ALTER TABLE `LNM_administratif` ADD `loggin` VARCHAR(20) NULL DEFAULT NULL AFTER `mail`;
ALTER TABLE `LNM_administratif` ADD UNIQUE(`loggin`);

ALTER TABLE `LNM_enseignant` ADD `loggin` VARCHAR(20) NULL DEFAULT NULL AFTER `mail`;
ALTER TABLE `LNM_enseignant` ADD UNIQUE(`loggin`);

ALTER TABLE `LNM_etudiant` ADD `loggin` VARCHAR(20) NULL DEFAULT NULL AFTER `mail`;
ALTER TABLE `LNM_etudiant` ADD UNIQUE(`loggin`);