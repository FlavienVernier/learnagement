
ALTER TABLE `MOB_partner_university`
    DROP COLUMN `S8_total_places`,
    DROP COLUMN `S8_MM`,
    DROP COLUMN `S8_MC`,
    DROP COLUMN `S8_MMT`,
    DROP COLUMN `S8_SNI`,
    DROP COLUMN `S8_BAT`,
    DROP COLUMN `S8_EIT`,
    DROP COLUMN `S8_IDU`,
    DROP COLUMN `S8_ESB`,
    DROP COLUMN `S8_AM`,
    DROP COLUMN `S9_total_places`,
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
    add `mobility_note` INT NULL AFTER `mobility_completed`;

ALTER TABLE `MOB_wishes`
    ADD `id_semestre` TINYINT NOT NULL AFTER `id_partner_university`,
    ADD CONSTRAINT `FK_wishes_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre`(`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT;