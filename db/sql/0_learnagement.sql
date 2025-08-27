
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
DROP TABLE IF EXISTS `APC_apprentissage_critique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_apprentissage_critique` (
  `id_apprentissage_critique` int NOT NULL AUTO_INCREMENT,
  `id_niveau` int NOT NULL,
  `libelle_apprentissage` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id_apprentissage_critique`),
  UNIQUE KEY `SECONDARY` (`libelle_apprentissage`),
  KEY `FK_apprentissage_critique_as_niveau` (`id_niveau`),
  CONSTRAINT `FK_apprentissage_critique_as_niveau` FOREIGN KEY (`id_niveau`) REFERENCES `APC_niveau` (`id_niveau`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_apprentissage_critique_as_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_apprentissage_critique_as_module` (
  `id_apprentissage_critique` int NOT NULL,
  `id_module` int NOT NULL,
  `type_lien` enum('Requis','Recommandé','Complémentaire') CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'Requis',
  PRIMARY KEY (`id_apprentissage_critique`,`id_module`),
  UNIQUE KEY `SECONDARY` (`id_apprentissage_critique`,`id_module`) USING BTREE,
  KEY `FK_apprentissage_critique_as_module_as_module` (`id_module`),
  CONSTRAINT `FK_apprentissage_critique_as_module_as_apprentissage_critique` FOREIGN KEY (`id_apprentissage_critique`) REFERENCES `APC_apprentissage_critique` (`id_apprentissage_critique`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_apprentissage_critique_as_module_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_competence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_competence` (
  `id_competence` int NOT NULL AUTO_INCREMENT,
  `libelle_competence` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `code_competence` varchar(25) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_competence`),
  UNIQUE KEY `SECONDARY` (`code_competence`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_competence_as_filiere_as_statut`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_competence_as_filiere_as_statut` (
  `id_competence` int NOT NULL,
  `id_filiere` int NOT NULL,
  `id_statut` int NOT NULL,
  PRIMARY KEY (`id_competence`,`id_filiere`,`id_statut`),
  UNIQUE KEY `SECONDARY` (`id_competence`,`id_filiere`,`id_statut`) USING BTREE,
  KEY `competence_as_filiere_as_statut_2_filiere` (`id_filiere`),
  KEY `competence_as_filiere_as_statut_2_statut` (`id_statut`) USING BTREE,
  CONSTRAINT `competence_as_filiere_as_statut_2_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `competence_as_filiere_as_statut_2_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `competence_as_filiere_as_statut_2_statut` FOREIGN KEY (`id_statut`) REFERENCES `LNM_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_composante_essentielle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_composante_essentielle` (
  `id_composante_essentielle` int NOT NULL AUTO_INCREMENT,
  `id_competence` int NOT NULL,
  `libelle_composante_essentielle` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id_composante_essentielle`),
  UNIQUE KEY `SECONDARY` (`libelle_composante_essentielle`),
  KEY `FK_composante_essentielle_as_competence` (`id_competence`),
  CONSTRAINT `FK_composante_essentielle_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_niveau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_niveau` (
  `id_niveau` int NOT NULL AUTO_INCREMENT,
  `id_competence` int NOT NULL,
  `niveau` int NOT NULL,
  `libelle_niveau` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id_niveau`),
  UNIQUE KEY `SECONDARY` (`id_competence`,`niveau`) USING BTREE,
  CONSTRAINT `FK_niveau_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `APC_situation_professionnelle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APC_situation_professionnelle` (
  `id_situation_professionnelle` int NOT NULL AUTO_INCREMENT,
  `id_competence` int NOT NULL,
  `libelle_situation` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id_situation_professionnelle`),
  UNIQUE KEY `SECONDARY` (`id_competence`,`libelle_situation`) USING BTREE,
  KEY `FK_situation_professionnelle_as_competence` (`id_competence`),
  CONSTRAINT `FK_situation_professionnelle_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `CLASS_absence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLASS_absence` (
  `id_session` int NOT NULL,
  `id_etudiant` int NOT NULL,
  PRIMARY KEY (`id_session`,`id_etudiant`),
  UNIQUE KEY `SECONDARY` (`id_session`,`id_etudiant`) USING BTREE,
  KEY `FK_absence_as_etudiant` (`id_etudiant`),
  CONSTRAINT `FK_absence_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_absence_as_session` FOREIGN KEY (`id_session`) REFERENCES `CLASS_session` (`id_session`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `CLASS_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLASS_session` (
  `id_session` int NOT NULL AUTO_INCREMENT,
  `id_module_sequence` int NOT NULL,
  `id_groupe` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `schedule` datetime DEFAULT NULL,
  PRIMARY KEY (`id_session`),
  UNIQUE KEY `SECONDARY` (`id_module_sequence`,`id_groupe`) USING BTREE,
  KEY `FK_seance_to_be_affected_as_groupe` (`id_groupe`),
  KEY `FK_session_to_enseignant` (`id_enseignant`),
  CONSTRAINT `FK_seance_to_be_affected_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `LNM_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_seance_to_be_affected_as_module_sequence` FOREIGN KEY (`id_module_sequence`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_session_to_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=1394 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ETU_classical_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ETU_classical_evaluation` (
  `id_classical_evaluation` int NOT NULL AUTO_INCREMENT,
  `id_etudiant` int NOT NULL,
  `id_evaluation_type` int NOT NULL,
  `evaluation` int NOT NULL,
  `date` datetime NOT NULL,
  `id_module` int NOT NULL,
  PRIMARY KEY (`id_classical_evaluation`),
  KEY `FK_id_etudiant` (`id_etudiant`),
  KEY `FK_evaluation_type` (`id_evaluation_type`),
  KEY `FK_classical_evaluation_as_module` (`id_module`),
  CONSTRAINT `FK_classical_evaluation_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_classical_evaluation_as_evaluation_type` FOREIGN KEY (`id_evaluation_type`) REFERENCES `LNM_evaluation_type` (`id_evaluation_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_classical_evaluation_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ETU_competence_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ETU_competence_evaluation` (
  `id_competence_evaluation` int NOT NULL AUTO_INCREMENT,
  `id_etudiant` int NOT NULL,
  `id_apprentissage_critique` int NOT NULL,
  `id_evaluation_type` int NOT NULL,
  `evaluation` varchar(15) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id_competence_evaluation`),
  UNIQUE KEY `SECONDARY` (`id_etudiant`,`id_apprentissage_critique`,`date`),
  KEY `FK_competence_evaluation_as_apprentissage_critique` (`id_apprentissage_critique`),
  KEY `FK_competence_evaluation_as_evaluation_type` (`id_evaluation_type`),
  CONSTRAINT `FK_competence_evaluation_as_apprentissage_critique` FOREIGN KEY (`id_apprentissage_critique`) REFERENCES `APC_apprentissage_critique` (`id_apprentissage_critique`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_competence_evaluation_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_competence_evaluation_as_evaluation_type` FOREIGN KEY (`id_evaluation_type`) REFERENCES `LNM_evaluation_type` (`id_evaluation_type`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=11838 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ETU_polypoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ETU_polypoint` (
  `id_polypoint` int NOT NULL AUTO_INCREMENT,
  `intitule` varchar(100) NOT NULL,
  `tache` varchar(50) NOT NULL,
  `nb_point` int NOT NULL,
  `annee_universitaire` varchar(9) NOT NULL,
  `id_etudiant` int NOT NULL,
  PRIMARY KEY (`id_polypoint`),
  KEY `FK_polypoint_as_etudiant` (`id_etudiant`),
  CONSTRAINT `FK_polypoint_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `EXT_seance_planned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EXT_seance_planned` (
  `id_seance_planned` int NOT NULL AUTO_INCREMENT,
  `id_seance_type` int NOT NULL,
  `date` datetime NOT NULL,
  `duree_h` time NOT NULL,
  `id_module` int NOT NULL,
  `id_enseignant` int NOT NULL,
  PRIMARY KEY (`id_seance_planned`),
  UNIQUE KEY `SECONDARY` (`date`,`id_enseignant`,`id_module`,`id_seance_type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Data extracted from calendar system';
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_administratif`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_administratif` (
  `id_administratif` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(25) NOT NULL,
  `prenom` varchar(25) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `password_updated` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_administratif`),
  UNIQUE KEY `mail` (`mail`),
  UNIQUE KEY `SECONDARY` (`nom`,`prenom`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_enseignant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_enseignant` (
  `id_enseignant` int NOT NULL AUTO_INCREMENT,
  `prenom` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nom` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mail` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password_updated` int NOT NULL DEFAULT '0',
  `statut` enum('permanent','vacataire') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'permanent',
  `id_discipline` int DEFAULT NULL,
  `composante` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `service statutaire` int NOT NULL,
  `décharge` int NOT NULL,
  `service effectif` float NOT NULL DEFAULT '192',
  `HCAutorisees` tinyint(1) NOT NULL DEFAULT '1',
  `commentaire` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_enseignant`),
  UNIQUE KEY `SECONDARY` (`prenom`,`nom`) USING BTREE,
  UNIQUE KEY `mail` (`mail`),
  KEY `FK_enseignant_as_discipline` (`id_discipline`),
  CONSTRAINT `FK_enseignant_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_etudiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_etudiant` (
  `id_etudiant` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(25) NOT NULL,
  `prenom` varchar(25) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `password_updated` int NOT NULL DEFAULT '0',
  `id_promo` int NOT NULL,
  PRIMARY KEY (`id_etudiant`),
  UNIQUE KEY `SECONDARY` (`nom`,`prenom`) USING BTREE,
  UNIQUE KEY `mail` (`mail`),
  KEY `FK_etudiant_as_promo` (`id_promo`),
  CONSTRAINT `FK_etudiant_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=540 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_etudiant_as_groupe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_etudiant_as_groupe` (
  `id_etudiant` int NOT NULL,
  `id_groupe` int NOT NULL,
  PRIMARY KEY (`id_etudiant`,`id_groupe`),
  UNIQUE KEY `SECONDARY` (`id_etudiant`,`id_groupe`),
  KEY `FK_etudiant_as_groupe_as_groupe` (`id_groupe`),
  CONSTRAINT `FK_etudiant_as_groupe_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_etudiant_as_groupe_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `LNM_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_evaluation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_evaluation_type` (
  `id_evaluation_type` int NOT NULL AUTO_INCREMENT,
  `evaluation_name` varchar(50) NOT NULL,
  `heighest_value` varchar(15) NOT NULL,
  `lowest_value` varchar(15) NOT NULL,
  `valudation_value` varchar(15) NOT NULL,
  `ordered_allowed_values` text,
  `ordered_value_descriptions` text,
  PRIMARY KEY (`id_evaluation_type`),
  UNIQUE KEY `SECONDARY` (`evaluation_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_filiere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_filiere` (
  `id_filiere` int NOT NULL,
  `nom_filiere` varchar(11) NOT NULL,
  `nom_long` varchar(50) DEFAULT NULL,
  `id_responsable` int DEFAULT NULL,
  PRIMARY KEY (`id_filiere`),
  UNIQUE KEY `SECONDARY` (`nom_filiere`) USING BTREE,
  KEY `FK_filiere_as_responsable` (`id_responsable`),
  CONSTRAINT `FK_filiere_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_groupe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_groupe` (
  `id_groupe` int NOT NULL AUTO_INCREMENT,
  `nom_groupe` varchar(20) NOT NULL,
  `id_promo` int NOT NULL,
  `id_groupe_type` int NOT NULL,
  PRIMARY KEY (`id_groupe`),
  UNIQUE KEY `SECONDARY` (`nom_groupe`),
  KEY `FK_groupe_as_promo` (`id_promo`),
  KEY `FK_groupe_as_groupe_type` (`id_groupe_type`),
  CONSTRAINT `FK_groupe_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `LNM_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_groupe_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_groupe_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_groupe_type` (
  `id_groupe_type` int NOT NULL,
  `groupe_type` varchar(10) NOT NULL,
  `commentaire` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_groupe_type`),
  UNIQUE KEY `SECONDARY` (`groupe_type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_promo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_promo` (
  `id_promo` int NOT NULL AUTO_INCREMENT,
  `id_filiere` int DEFAULT NULL,
  `id_statut` int DEFAULT NULL,
  `annee` int NOT NULL,
  `parcour` varchar(25) DEFAULT NULL,
  `site` varchar(25) NOT NULL,
  `nbGroupeCM` int NOT NULL DEFAULT '1',
  `nbGroupeTD` int NOT NULL,
  `nbGroupeTP` int NOT NULL,
  `id_responsable` int DEFAULT NULL,
  PRIMARY KEY (`id_promo`),
  UNIQUE KEY `SECONDARY` (`id_filiere`,`id_statut`,`annee`,`site`,`parcour`) USING BTREE,
  KEY `FK_promo_as_statut` (`id_statut`),
  KEY `FK_promo_as_responsable` (`id_responsable`),
  CONSTRAINT `FK_promo_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_promo_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_promo_as_statut` FOREIGN KEY (`id_statut`) REFERENCES `LNM_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_rendu_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_rendu_module` (
  `id_rendu_module` int NOT NULL AUTO_INCREMENT,
  `description` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `id_module` int NOT NULL,
  PRIMARY KEY (`id_rendu_module`),
  UNIQUE KEY `SECONDARY` (`description`,`date`,`id_module`) USING BTREE,
  KEY `FK_rendu_module_as_module` (`id_module`),
  CONSTRAINT `FK_rendu_module_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_rendu_module_as_enseignant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_rendu_module_as_enseignant` (
  `id_rendu_module` int NOT NULL,
  `id_enseignant` int NOT NULL,
  PRIMARY KEY (`id_rendu_module`,`id_enseignant`),
  KEY `FK_rendu_module_as_enseignant_as_enseignant` (`id_enseignant`),
  CONSTRAINT `FK_rendu_module_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_rendu_module_as_enseignant_as_rendu_module` FOREIGN KEY (`id_rendu_module`) REFERENCES `LNM_rendu_module` (`id_rendu_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_rendu_module_as_etudiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_rendu_module_as_etudiant` (
  `id_rendu_module` int NOT NULL,
  `id_etudiant` int NOT NULL,
  `date_depot` date NOT NULL,
  `avancement` decimal(3,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`id_rendu_module`,`id_etudiant`),
  KEY `FK_rendu_module_as_etudiant_as_etudiant` (`id_etudiant`),
  CONSTRAINT `FK_rendu_module_as_etudiant_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_rendu_module_as_etudiant_as_rendu_module` FOREIGN KEY (`id_rendu_module`) REFERENCES `LNM_rendu_module` (`id_rendu_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_seanceType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_seanceType` (
  `id_seance_type` int NOT NULL,
  `type` varchar(10) NOT NULL,
  `commentaire` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id_seance_type`),
  UNIQUE KEY `SECONDARY` (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_semestre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_semestre` (
  `id_semestre` tinyint NOT NULL,
  `semestre` varchar(3) NOT NULL,
  PRIMARY KEY (`id_semestre`),
  UNIQUE KEY `SECONDARY` (`semestre`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_stage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_stage` (
  `id_stage` int NOT NULL AUTO_INCREMENT,
  `entreprise` varchar(100) NOT NULL,
  `intitulé` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `ville` varchar(50) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `nature` varchar(50) NOT NULL,
  `id_etudiant` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  PRIMARY KEY (`id_stage`),
  UNIQUE KEY `SECONDARY` (`entreprise`,`intitulé`),
  KEY `FK_stage_as_etudiant` (`id_etudiant`),
  KEY `FK_stage_as_enseignant` (`id_enseignant`),
  CONSTRAINT `FK_stage_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_stage_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_statut`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_statut` (
  `id_statut` int NOT NULL AUTO_INCREMENT,
  `nom_statut` varchar(10) NOT NULL,
  `Description` varchar(100) NOT NULL,
  PRIMARY KEY (`id_statut`),
  UNIQUE KEY `SECONDARY` (`nom_statut`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `LNM_universite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LNM_universite` (
  `id_universite` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(250) NOT NULL,
  `nom_court` varchar(50) NOT NULL,
  `ville` varchar(50) NOT NULL,
  `pays` varchar(50) NOT NULL,
  PRIMARY KEY (`id_universite`),
  UNIQUE KEY `SECONDARY` (`nom_court`) USING BTREE,
  UNIQUE KEY `nom` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_dependance_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_dependance_sequence` (
  `id_sequence_prev` int NOT NULL,
  `id_sequence_next` int NOT NULL,
  PRIMARY KEY (`id_sequence_prev`,`id_sequence_next`),
  KEY `FK_dependance_sequence_as_module_sequencage_next` (`id_sequence_next`),
  CONSTRAINT `FK_dependance_sequence_as_module_sequencage_next` FOREIGN KEY (`id_sequence_next`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_dependance_sequence_as_module_sequencage_prev` FOREIGN KEY (`id_sequence_prev`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_discipline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_discipline` (
  `id_discipline` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) NOT NULL,
  PRIMARY KEY (`id_discipline`),
  UNIQUE KEY `SECONDARY` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_learning_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_learning_unit` (
  `id_learning_unit` int NOT NULL AUTO_INCREMENT,
  `learning_unit_code` varchar(10) NOT NULL,
  `learning_unit_name` varchar(50) NOT NULL,
  `id_promo` int NOT NULL,
  PRIMARY KEY (`id_learning_unit`),
  UNIQUE KEY `SECONDARY` (`learning_unit_code`,`id_promo`) USING BTREE,
  KEY `FK_learning_unit_as_promo` (`id_promo`),
  CONSTRAINT `FK_learning_unit_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_module` (
  `id_module` int NOT NULL AUTO_INCREMENT,
  `code_module` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nom` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ECTS` decimal(10,1) DEFAULT NULL,
  `id_discipline` int NOT NULL,
  `id_semestre` tinyint NOT NULL,
  `hCM` float DEFAULT NULL,
  `hTD` float DEFAULT NULL,
  `hTP` float DEFAULT NULL,
  `hTPTD` float DEFAULT NULL,
  `hPROJ` float DEFAULT NULL,
  `hPersonnelle` float DEFAULT NULL,
  `id_responsable` int DEFAULT NULL,
  `commentaire` text,
  PRIMARY KEY (`id_module`),
  UNIQUE KEY `SECONDARY` (`code_module`) USING BTREE,
  KEY `FK_module_as_enseignant` (`id_responsable`),
  KEY `FK_module_as_semestre` (`id_semestre`),
  KEY `FK_module_as_discipline` (`id_discipline`),
  CONSTRAINT `FK_module_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`),
  CONSTRAINT `FK_module_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre` (`id_semestre`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_module_as_learning_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_module_as_learning_unit` (
  `id_module` int NOT NULL,
  `id_learning_unit` int NOT NULL,
  PRIMARY KEY (`id_module`,`id_learning_unit`),
  UNIQUE KEY `SECONDARY` (`id_module`,`id_learning_unit`),
  KEY `FK_module_as_learning_unit_as_learning_unit` (`id_learning_unit`),
  CONSTRAINT `FK_module_as_learning_unit_as_learning_unit` FOREIGN KEY (`id_learning_unit`) REFERENCES `MAQUETTE_learning_unit` (`id_learning_unit`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_as_learning_unit_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_module_sequencage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_module_sequencage` (
  `id_module_sequencage` int NOT NULL AUTO_INCREMENT,
  `id_module` int NOT NULL,
  `nombre` int NOT NULL,
  `id_seance_type` int DEFAULT NULL,
  `id_groupe_type` int NOT NULL,
  `duree_h` decimal(10,1) NOT NULL,
  `id_intervenant_principal` int DEFAULT NULL,
  PRIMARY KEY (`id_module_sequencage`),
  UNIQUE KEY `SECONDARY` (`id_module`,`id_seance_type`,`id_groupe_type`,`duree_h`) USING BTREE,
  KEY `FK_module_sequencage_as_intervenant_principal` (`id_intervenant_principal`),
  KEY `FK_module_sequencage_as_groupe_type` (`id_groupe_type`),
  KEY `FK_module_sequencage_as_seanceType` (`id_seance_type`),
  CONSTRAINT `FK_module_sequencage_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `LNM_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_sequencage_as_intervenant_principal` FOREIGN KEY (`id_intervenant_principal`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_sequencage_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_sequencage_as_seanceType` FOREIGN KEY (`id_seance_type`) REFERENCES `LNM_seanceType` (`id_seance_type`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MAQUETTE_module_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MAQUETTE_module_sequence` (
  `id_module_sequence` int NOT NULL AUTO_INCREMENT,
  `id_module_sequencage` int DEFAULT NULL,
  `numero_ordre` int DEFAULT NULL,
  `id_intervenant_principal` int DEFAULT NULL,
  `commentaire` text,
  PRIMARY KEY (`id_module_sequence`),
  UNIQUE KEY `SECONDARY` (`id_module_sequencage`,`numero_ordre`) USING BTREE,
  KEY `FK_module_sequence_as_enseignant` (`id_intervenant_principal`),
  CONSTRAINT `FK_module_sequence_as_enseignant` FOREIGN KEY (`id_intervenant_principal`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_module_sequence_as_module_sequencage` FOREIGN KEY (`id_module_sequencage`) REFERENCES `MAQUETTE_module_sequencage` (`id_module_sequencage`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=812 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MRDBF_system_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MRDBF_system_request` (
  `id_system_request` int NOT NULL AUTO_INCREMENT,
  `groupe_of_system_request` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nom` varchar(50) NOT NULL,
  `request` text NOT NULL,
  PRIMARY KEY (`id_system_request`),
  UNIQUE KEY `SECONDARY` (`nom`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `VIEW_check`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VIEW_check` (
  `id_view` int NOT NULL AUTO_INCREMENT,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `request` text NOT NULL,
  PRIMARY KEY (`id_view`),
  UNIQUE KEY `SECONDARY` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `VIEW_display`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VIEW_display` (
  `id_view` int NOT NULL AUTO_INCREMENT,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Unclassified',
  `request` text NOT NULL,
  PRIMARY KEY (`id_view`),
  UNIQUE KEY `SECONDARY` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `VIEW_parameters_of_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VIEW_parameters_of_views` (
  `id_parameters_of_views` int NOT NULL AUTO_INCREMENT,
  `userId` int DEFAULT NULL,
  `sessionId` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_semestre` tinyint DEFAULT NULL,
  `id_module` int DEFAULT NULL,
  `id_discipline` int DEFAULT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_filiere` int DEFAULT NULL,
  `id_statut` int DEFAULT NULL,
  PRIMARY KEY (`id_parameters_of_views`),
  UNIQUE KEY `sessionId` (`sessionId`),
  KEY `FK_parameters_of_views_as_semestre` (`id_semestre`),
  KEY `FK_parameters_of_views_as_module` (`id_module`),
  KEY `FK_parameters_of_views_as_enseignant` (`id_enseignant`),
  KEY `FK_parameters_of_views_as_discipline` (`id_discipline`),
  KEY `FK_parameters_of_views_as_status` (`id_statut`),
  KEY `FK_parameters_of_views_as_filiere` (`id_filiere`),
  CONSTRAINT `FK_parameters_of_views_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_parameters_of_views_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_parameters_of_views_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_parameters_of_views_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_parameters_of_views_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre` (`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_parameters_of_views_as_status` FOREIGN KEY (`id_statut`) REFERENCES `LNM_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `VIEW_updatable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VIEW_updatable` (
  `id_updatable` int NOT NULL AUTO_INCREMENT,
  `sortIndex` int NOT NULL,
  `table_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `table_name_displayed` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `allow_insert` tinyint NOT NULL,
  `allow_update` tinyint NOT NULL,
  `request` text NOT NULL,
  PRIMARY KEY (`id_updatable`),
  UNIQUE KEY `SECONDARY` (`table_name`) USING BTREE,
  UNIQUE KEY `table_name_displayed` (`table_name_displayed`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

