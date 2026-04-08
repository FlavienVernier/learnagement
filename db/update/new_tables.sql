CREATE TABLE IF NOT EXISTS `learnagement`.`LNM_role`
    (`id_role` INT NOT NULL AUTO_INCREMENT ,
     `role` VARCHAR(50) NOT NULL ,
     PRIMARY KEY (`id_role`),
     UNIQUE `SECONDARY` (`role`))
ENGINE = InnoDB;

CREATE TABLE `learnagement`.`LNM_enseignant_as_role`
    (`id_enseignant` INT NOT NULL ,
     `id_role` INT NOT NULL ,
     PRIMARY KEY (`id_enseignant`, `id_role`),
     UNIQUE `SECONDARY` (`id_enseignant`, `id_role`),
     CONSTRAINT `FK_enseignant_as_role_as_enseignant`
        FOREIGN KEY (`id_enseignant`)
            REFERENCES `LNM_enseignant`(`id_enseignant`)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT,
     CONSTRAINT `FK_enseignant_as_role_as_role`
        FOREIGN KEY (`id_role`)
            REFERENCES `LNM_role`(`id_role`)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT
    )
ENGINE = InnoDB;

CREATE TABLE `learnagement`.`LNM_administratif_as_role`
    (`id_administratif` INT NOT NULL ,
     `id_role` INT NOT NULL ,
     PRIMARY KEY (`id_administratif`, `id_role`),
     UNIQUE `SECONDARY` (`id_administratif`, `id_role`),
     CONSTRAINT `FK_administratif_as_role_as_administratif`
        FOREIGN KEY (`id_administratif`)
            REFERENCES `LNM_administratif`(`id_administratif`)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT,
     CONSTRAINT `FK_administratif_as_role_as_role`
        FOREIGN KEY (`id_role`)
            REFERENCES `LNM_role`(`id_role`)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT
    )
ENGINE = InnoDB;
