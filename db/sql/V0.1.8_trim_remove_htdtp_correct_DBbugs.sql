UPDATE MAQUETTE_module
SET `hTD`= IFNULL(`hTD`, 0) + `hTPTD`, `hTPTD`=NULL
WHERE `hTPTD` IS NOT NULL;

ALTER TABLE MAQUETTE_module
DROP COLUMN `hTPTD`;

ALTER TABLE `ETU_polypoint` ADD UNIQUE `SECONDARY` (`intitule`, `tache`, `nb_point`, `annee_universitaire`) USING BTREE;

ALTER TABLE `MOB_partner_university` CHANGE `code` `code` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL;
ALTER TABLE `MOB_partner_university` ADD UNIQUE `SECONDARY` (`code`) USING BTREE;

ALTER TABLE `LNM_rendu_module_as_enseignant` ADD UNIQUE `SECONDARY` (`id_rendu_module`, `id_enseignant`) USING BTREE;

ALTER TABLE `LNM_rendu_module_as_etudiant` ADD UNIQUE `SECONDARY`(`id_rendu_module`, `id_etudiant`) USING BTREE;

ALTER TABLE learnagement.APC_competence_as_filiere_as_statut DROP FOREIGN KEY competence_as_filiere_as_statut_2_statut;
ALTER TABLE `APC_competence_as_filiere_as_statut` DROP INDEX `competence_as_filiere_as_statut_2_statut`;
ALTER TABLE `APC_competence_as_filiere_as_statut` DROP INDEX `SECONDARY`;
ALTER TABLE `APC_competence_as_filiere_as_statut`
  DROP PRIMARY KEY,
   ADD PRIMARY KEY(
     `id_competence`,
     `id_filiere`
   );
ALTER TABLE `APC_competence_as_filiere_as_statut` DROP `id_statut`;
ALTER TABLE `APC_competence_as_filiere_as_statut` ADD UNIQUE `SECONDARY` (`id_competence`, `id_filiere`) USING BTREE;
ALTER TABLE `APC_competence_as_filiere_as_statut` DROP FOREIGN KEY `competence_as_filiere_as_statut_2_competence`;
ALTER TABLE `APC_competence_as_filiere_as_statut` ADD CONSTRAINT `FK_competence_as_filiere_2_competence`
    FOREIGN KEY (`id_competence`) REFERENCES `APC_competence`(`id_competence`)
        ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE `APC_competence_as_filiere_as_statut` DROP FOREIGN KEY `competence_as_filiere_as_statut_2_filiere`;
ALTER TABLE `APC_competence_as_filiere_as_statut` ADD CONSTRAINT `FK_competence_as_filiere_2_filiere`
    FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere`(`id_filiere`)
        ON DELETE RESTRICT ON UPDATE RESTRICT;

 RENAME TABLE `learnagement`.`LNM_seanceType` TO `learnagement`.`LNM_seance_type`;