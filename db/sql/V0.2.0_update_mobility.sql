DROP TABLE IF EXISTS `MOB_partner_university_places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MOB_partner_university_places` (
  `id_partner_university` int NOT NULL,
  `id_promo` int NOT NULL,
  `number_of_places` int NOT NULL,
  PRIMARY KEY (`id_partner_university`,`id_promo`),
  UNIQUE KEY `SECONDARY` (`id_partner_university`,`id_promo`) USING BTREE,
  KEY `FK_partner_university_places_as_promo` (`id_promo`),
  CONSTRAINT `FK_partner_university_places_as_partner_university` FOREIGN KEY (`id_partner_university`) REFERENCES `MOB_partner_university` (`id_partner_university`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_partner_university_places_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `MOB_wishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MOB_wishes` (
  `id_wish` int NOT NULL AUTO_INCREMENT,
  `id_etudiant` int NOT NULL,
  `id_partner_university` int NOT NULL,
  `priority` int NOT NULL,
  `submission_date` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id_wish`),
  UNIQUE KEY `SECONDARY` (`id_etudiant`,`priority`) USING BTREE,
  KEY `FK_wishes_as_etudiant` (`id_etudiant`),
  KEY `FK_wishes_as_partner_university` (`id_partner_university`),
  CONSTRAINT `FK_wishes_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_wishes_as_partner_university` FOREIGN KEY (`id_partner_university`) REFERENCES `MOB_partner_university` (`id_partner_university`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;