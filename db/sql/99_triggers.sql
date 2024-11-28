CREATE TRIGGER `generate_seance_from_sequence` AFTER INSERT ON `MAQUETTE_module_sequence`
 FOR EACH ROW INSERT IGNORE INTO CLASS_session_to_be_affected (`id_module_sequence`, `id_groupe`)
SELECT
  `learnagement`.`MAQUETTE_module_sequence`.`id_module_sequence` AS `id_module_sequence`,
  `learnagement`.`LNM_groupe`.`id_groupe` AS `id_groupe`
  
  FROM `MAQUETTE_module`

  JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
  JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
  JOIN LNM_promo ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
  
  JOIN `LNM_groupe` ON `LNM_promo`.`id_promo` = `LNM_groupe`.`id_promo`
  
  JOIN `MAQUETTE_module_sequencage` ON (`MAQUETTE_module`.`id_module` = `MAQUETTE_module_sequencage`.`id_module`) AND (`LNM_groupe`.`id_groupe_type` = `MAQUETTE_module_sequencage`.`id_groupe_type`)
  JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage;

CREATE TRIGGER `generate_sequence_from_sequencage` AFTER INSERT ON `MAQUETTE_module_sequencage`
 FOR EACH ROW INSERT IGNORE INTO `MAQUETTE_module_sequence`  (`id_module_sequencage`,`numero_ordre`,`commentaire`)
SELECT `id_module_sequencage`, orders, null
FROM `MAQUETTE_module_sequencage`, 
(VALUES ROW (1), ROW(2), ROW(3), ROW (4), ROW(5), ROW(6), ROW (7), ROW(8), ROW(9), 
 ROW (10), ROW (11), ROW(12), ROW(13), ROW (14), ROW(15), ROW(16), ROW (17), ROW(18), ROW(19),
 ROW (20), ROW (21), ROW(22), ROW(23), ROW (24), ROW(25), ROW(26), ROW (27), ROW(28), ROW(29),
 ROW (30), ROW (31), ROW(32), ROW(33), ROW (34), ROW(35), ROW(36), ROW (37), ROW(38), ROW(39)  ) sub(orders)
WHERE orders <= nombre;

CREATE TRIGGER `generate_type_seance_from_sequencage` AFTER INSERT ON `MAQUETTE_module_sequencage`
 FOR EACH ROW INSERT IGNORE INTO CLASS_session_type_to_be_affected (`id_module_sequencage`, `id_groupe`)
(
SELECT
  `learnagement`.`MAQUETTE_module_sequencage`.`id_module_sequencage` AS `id_module_sequencage`,
  `learnagement`.`LNM_groupe`.`id_groupe` AS `id_groupe`
  
  FROM `learnagement`.`MAQUETTE_module`

  JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
  JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
  JOIN LNM_promo ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
  
  JOIN `learnagement`.`LNM_groupe` ON `learnagement`.`LNM_promo`.`id_promo` = `learnagement`.`LNM_groupe`.`id_promo`
  JOIN `learnagement`.`MAQUETTE_module_sequencage` ON (`learnagement`.`MAQUETTE_module`.`id_module` = `learnagement`.`MAQUETTE_module_sequencage`.`id_module`) AND (`learnagement`.`LNM_groupe`.`id_groupe_type` = `learnagement`.`MAQUETTE_module_sequencage`.`id_groupe_type`)
)
