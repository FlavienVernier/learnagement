
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `generate_sequence_from_sequencage` AFTER INSERT ON `MAQUETTE_module_sequencage` FOR EACH ROW INSERT IGNORE INTO `MAQUETTE_module_sequence`  (`id_module_sequencage`,`numero_ordre`,`commentaire`)
SELECT `id_module_sequencage`, orders, null
FROM `MAQUETTE_module_sequencage`, 
(VALUES ROW (1), ROW(2), ROW(3), ROW (4), ROW(5), ROW(6), ROW (7), ROW(8), ROW(9), 
 ROW (10), ROW (11), ROW(12), ROW(13), ROW (14), ROW(15), ROW(16), ROW (17), ROW(18), ROW(19),
 ROW (20), ROW (21), ROW(22), ROW(23), ROW (24), ROW(25), ROW(26), ROW (27), ROW(28), ROW(29),
 ROW (30), ROW (31), ROW(32), ROW(33), ROW (34), ROW(35), ROW(36), ROW (37), ROW(38), ROW(39)  ) sub(orders)
WHERE orders <= nombre */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `generate_type_seance_from_sequencage` AFTER INSERT ON `MAQUETTE_module_sequencage` FOR EACH ROW INSERT IGNORE INTO CLASS_session_type_to_be_affected (`id_module_sequencage`, `id_groupe`)
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

/*
CREATE TRIGGER `check_student_group_inserted_into_absence` BEFORE INSERT ON CLASS_absence 
FOR EACH ROW
BEGIN 
    SET @id_etudiant = (SELECT LNM_etudiant.id_etudiant
	FROM CLASS_absence
	JOIN CLASS_session_to_be_affected_as_enseignant ON  CLASS_session_to_be_affected_as_enseignant.id_seance_to_be_affected_as_enseignant = CLASS_absence.id_seance_to_be_affected_as_enseignant
	JOIN CLASS_session_to_be_affected ON CLASS_session_to_be_affected.id_seance_to_be_affected = CLASS_session_to_be_affected_as_enseignant.id_seance_to_be_affected
	JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session_to_be_affected.id_groupe
	JOIN LNM_etudiant ON LNM_etudiant.id_groupe = LNM_groupe.id_groupe
	WHERE CLASS_absence.id_seance_to_be_affected_as_enseignant = NEW.id_seance_to_be_affected_as_enseignant AND LNM_etudiant.id_etudiant=NEW.id_etudiant);
    IF (NEW.id_etudiant != @id_etudiant)
    THEN
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Etudiant : `LNM_etudiant.nom` `LNM_etudiant.prenom` n appartient au groupe `LNM_groupe.nom_groupe`';
    END IF;
END;
*/ */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `generate_seance_from_sequence` AFTER INSERT ON `MAQUETTE_module_sequence` FOR EACH ROW INSERT IGNORE INTO CLASS_session_to_be_affected (`id_module_sequence`, `id_groupe`)
SELECT
  `learnagement`.`MAQUETTE_module_sequence`.`id_module_sequence` AS `id_module_sequence`,
  `learnagement`.`LNM_groupe`.`id_groupe` AS `id_groupe`
  
  FROM `MAQUETTE_module`

  JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
  JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit
  JOIN LNM_promo ON MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
  
  JOIN `LNM_groupe` ON `LNM_promo`.`id_promo` = `LNM_groupe`.`id_promo`
  
  JOIN `MAQUETTE_module_sequencage` ON (`MAQUETTE_module`.`id_module` = `MAQUETTE_module_sequencage`.`id_module`) AND (`LNM_groupe`.`id_groupe_type` = `MAQUETTE_module_sequencage`.`id_groupe_type`)
  JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequencage = MAQUETTE_module_sequencage.id_module_sequencage */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

