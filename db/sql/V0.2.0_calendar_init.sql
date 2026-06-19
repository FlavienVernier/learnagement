CREATE TABLE IF NOT EXISTS `LNM_calendar` (
    `id_calendar` INT AUTO_INCREMENT PRIMARY KEY,
    `url_name` VARCHAR(255) NOT NULL,

    -- Correction de la syntaxe pour la clé unique composée
    UNIQUE KEY `SECONDARY` (`url_name`, `id_etudiant`, `id_enseignant`, `id_administratif`),
    
    -- Identifiants uniques individuels
    `id_etudiant` INT DEFAULT NULL UNIQUE,
    `id_enseignant` INT DEFAULT NULL UNIQUE,
    `id_administratif` INT DEFAULT NULL UNIQUE,
    
    `url` TEXT NOT NULL,

    -- Contraintes de clés étrangères
    CONSTRAINT `fk_cal_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant`(`id_etudiant`) ON DELETE CASCADE,
    CONSTRAINT `fk_cal_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant`(`id_enseignant`) ON DELETE CASCADE,
    CONSTRAINT `fk_cal_administratif` FOREIGN KEY (`id_administratif`) REFERENCES `LNM_administratif`(`id_administratif`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;