-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : mysql
-- Généré le : mar. 09 juil. 2024 à 13:15
-- Version du serveur : 8.0.35
-- Version de PHP : 8.2.13

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `learnagement`
--

-- --------------------------------------------------------

--
-- Structure de la table `INFO_check`
--

CREATE TABLE `INFO_check` (
  `id_view` int NOT NULL,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_dependance_sequence`
--

CREATE TABLE `INFO_dependance_sequence` (
  `id_sequence_prev` int NOT NULL,
  `id_sequence_next` int NOT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_discipline`
--

CREATE TABLE `INFO_discipline` (
  `id_discipline` int NOT NULL,
  `nom` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_display_limit`
--

CREATE TABLE `INFO_display_limit` (
  `id_display_limit` int NOT NULL,
  `display_limit` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_enseignant`
--

CREATE TABLE `INFO_enseignant` (
  `id_enseignant` int NOT NULL,
  `prenom` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nom` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mail` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `statut` enum('permanent','vacataire') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'permanent',
  `id_discipline` int DEFAULT NULL,
  `composante` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `service statutaire` int NOT NULL,
  `décharge` int NOT NULL,
  `service effectif` float NOT NULL DEFAULT '192',
  `HCAutorisees` tinyint(1) NOT NULL DEFAULT '1',
  `fullName` varchar(50) DEFAULT NULL,
  `commentaire` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_etat_module`
--

CREATE TABLE `INFO_etat_module` (
  `id_etat_module` int NOT NULL,
  `etat` varchar(11) NOT NULL,
  `commentaire` text,
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_filiere`
--

CREATE TABLE `INFO_filiere` (
  `id_filiere` int NOT NULL,
  `nom_filiere` varchar(11) NOT NULL,
  `nom_long` varchar(50) DEFAULT NULL,
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_groupe`
--

CREATE TABLE `INFO_groupe` (
  `id_groupe` int NOT NULL,
  `nom_groupe` varchar(20) NOT NULL,
  `id_promo` int NOT NULL,
  `id_groupe_type` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_groupe_type`
--

CREATE TABLE `INFO_groupe_type` (
  `id_groupe_type` int NOT NULL,
  `groupe_type` varchar(10) NOT NULL,
  `commentaire` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_learning_unit`
--

CREATE TABLE `INFO_learning_unit` (
  `id_learning_unit` int NOT NULL,
  `learning_unit_code` varchar(10) NOT NULL,
  `learning_unit_name` varchar(50) NOT NULL,
  `id_promo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module`
--

CREATE TABLE `INFO_module` (
  `id_module` int NOT NULL,
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
  `id_etat_module` int DEFAULT NULL,
  `commentaire` text,
  `modifiable` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module_as_learning_unit`
--

CREATE TABLE `INFO_module_as_learning_unit` (
  `id_module` int NOT NULL,
  `id_learning_unit` int NOT NULL,
  `modifiable` tinyint(1) NOT NULL DEFAULT '0',
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module_sequencage`
--

CREATE TABLE `INFO_module_sequencage` (
  `id_module_sequencage` int NOT NULL,
  `id_module` int NOT NULL,
  `nombre` int NOT NULL,
  `id_seance_type` int DEFAULT NULL,
  `id_groupe_type` int NOT NULL,
  `duree_h` decimal(10,1) NOT NULL,
  `intervenant_principal` int DEFAULT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- --------------------------------------------------------

--
-- Structure de la table `INFO_module_sequence`
--

CREATE TABLE `INFO_module_sequence` (
  `id_module_sequence` int NOT NULL,
  `id_module_sequencage` int DEFAULT NULL,
  `numero_ordre` int DEFAULT NULL,
  `commentaire` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- --------------------------------------------------------

--
-- Structure de la table `INFO_parameters_of_views`
--

CREATE TABLE `INFO_parameters_of_views` (
  `id_parameters_of_views` int NOT NULL,
  `userId` int DEFAULT NULL,
  `sessionId` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_semestre` tinyint DEFAULT NULL,
  `id_module` int DEFAULT NULL,
  `id_discipline` int DEFAULT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_filiere` int DEFAULT NULL,
  `id_statut` int DEFAULT NULL,
  `id_display_limit` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_promo`
--

CREATE TABLE `INFO_promo` (
  `id_promo` int NOT NULL,
  `id_filiere` int DEFAULT NULL,
  `id_statut` int DEFAULT NULL,
  `annee` int NOT NULL,
  `parcour` varchar(25) DEFAULT NULL,
  `site` varchar(25) NOT NULL,
  `nbGroupeCM` int NOT NULL DEFAULT '1',
  `nbGroupeTD` int NOT NULL,
  `nbGroupeTP` int NOT NULL,
  `modifiable` int NOT NULL DEFAULT '1',
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seanceType`
--

CREATE TABLE `INFO_seanceType` (
  `id_seance_type` int NOT NULL,
  `type` varchar(10) NOT NULL,
  `commentaire` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seance_planned`
--

CREATE TABLE `INFO_seance_planned` (
  `id_seance_planned` int NOT NULL,
  `type` varchar(10) NOT NULL,
  `date` datetime NOT NULL,
  `duree_h` time NOT NULL,
  `id_module` int NOT NULL,
  `id_enseignant` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seance_to_be_affected`
--

CREATE TABLE `INFO_seance_to_be_affected` (
  `id_seance_to_be_affected` int NOT NULL,
  `id_module_sequence` int DEFAULT NULL,
  `id_groupe` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seance_to_be_affected_as_enseignant`
--

CREATE TABLE `INFO_seance_to_be_affected_as_enseignant` (
  `id_seance_to_be_affected_as_enseignant` int NOT NULL,
  `id_seance_to_be_affected` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_semestre`
--

CREATE TABLE `INFO_semestre` (
  `id_semestre` tinyint NOT NULL,
  `semestre` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_statut`
--

CREATE TABLE `INFO_statut` (
  `id_statut` int NOT NULL,
  `nom_statut` varchar(10) NOT NULL,
  `Description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_type_seance_to_be_affected`
--

CREATE TABLE `INFO_type_seance_to_be_affected` (
  `id_type_seance_to_be_affected` int NOT NULL,
  `id_module_sequencage` int NOT NULL,
  `id_groupe` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_type_seance_to_be_affected_as_enseignant`
--

CREATE TABLE `INFO_type_seance_to_be_affected_as_enseignant` (
  `id_type_seance_to_be_affected_as_enseignant` int NOT NULL,
  `id_type_seance_to_be_affected` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_updatable`
--

CREATE TABLE `INFO_updatable` (
  `id_updatable` int NOT NULL,
  `sortIndex` int NOT NULL,
  `table_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `table_name_displayed` varchar(30) NOT NULL,
  `group_of-views` varchar(30) DEFAULT NULL,
  `allow_insert` tinyint NOT NULL,
  `allow_update` tinyint NOT NULL,
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_view`
--

CREATE TABLE `INFO_view` (
  `id_view` int NOT NULL,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Unclassified',
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `INFO_check`
--
ALTER TABLE `INFO_check`
  ADD PRIMARY KEY (`id_view`),
  ADD UNIQUE KEY `SECONDARY` (`name`);

--
-- Index pour la table `INFO_dependance_sequence`
--
ALTER TABLE `INFO_dependance_sequence`
  ADD PRIMARY KEY (`id_sequence_prev`,`id_sequence_next`),
  ADD KEY `FK_dependance_sequence_as_module_sequencage_next` (`id_sequence_next`),
  ADD KEY `FK_dependance_sequence_as_enseignant` (`id_responsable`);

--
-- Index pour la table `INFO_discipline`
--
ALTER TABLE `INFO_discipline`
  ADD PRIMARY KEY (`id_discipline`),
  ADD UNIQUE KEY `SECONDARY` (`nom`);

--
-- Index pour la table `INFO_display_limit`
--
ALTER TABLE `INFO_display_limit`
  ADD PRIMARY KEY (`id_display_limit`),
  ADD UNIQUE KEY `SECONDARY` (`display_limit`);

--
-- Index pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  ADD PRIMARY KEY (`id_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`prenom`,`nom`) USING BTREE,
  ADD UNIQUE KEY `mail` (`mail`),
  ADD KEY `FK_enseignant_as_discipline` (`id_discipline`);

--
-- Index pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  ADD PRIMARY KEY (`id_etat_module`),
  ADD UNIQUE KEY `SECONDARY` (`etat`),
  ADD KEY `FK_etat_module_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_filiere`
--
ALTER TABLE `INFO_filiere`
  ADD PRIMARY KEY (`id_filiere`),
  ADD UNIQUE KEY `SECONDARY` (`nom_filiere`) USING BTREE,
  ADD KEY `FK_filiere_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_groupe`
--
ALTER TABLE `INFO_groupe`
  ADD PRIMARY KEY (`id_groupe`),
  ADD UNIQUE KEY `SECONDARY` (`nom_groupe`),
  ADD KEY `FK_groupe_as_promo` (`id_promo`),
  ADD KEY `FK_groupe_as_groupe_type` (`id_groupe_type`);

--
-- Index pour la table `INFO_groupe_type`
--
ALTER TABLE `INFO_groupe_type`
  ADD PRIMARY KEY (`id_groupe_type`),
  ADD UNIQUE KEY `SECONDARY` (`groupe_type`) USING BTREE;

--
-- Index pour la table `INFO_learning_unit`
--
ALTER TABLE `INFO_learning_unit`
  ADD PRIMARY KEY (`id_learning_unit`),
  ADD UNIQUE KEY `SECONDARY` (`learning_unit_code`,`id_promo`) USING BTREE,
  ADD KEY `FK_learning_unit_as_promo` (`id_promo`);

--
-- Index pour la table `INFO_module`
--
ALTER TABLE `INFO_module`
  ADD PRIMARY KEY (`id_module`),
  ADD UNIQUE KEY `SECONDARY` (`code_module`) USING BTREE,
  ADD KEY `FK_module_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_as_semestre` (`id_semestre`),
  ADD KEY `FK_module_as_discipline` (`id_discipline`),
  ADD KEY `FK_module_as_etat_module` (`id_etat_module`);

--
-- Index pour la table `INFO_module_as_learning_unit`
--
ALTER TABLE `INFO_module_as_learning_unit`
  ADD PRIMARY KEY (`id_module`,`id_learning_unit`),
  ADD KEY `FK_module_as_learning_unit_as_learning_unit` (`id_learning_unit`),
  ADD KEY `FK_module_sequencage_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_module_sequencage`
--
ALTER TABLE `INFO_module_sequencage`
  ADD PRIMARY KEY (`id_module_sequencage`),
  ADD UNIQUE KEY `SECONDARY` (`id_module`,`id_seance_type`,`id_groupe_type`,`duree_h`) USING BTREE,
  ADD KEY `FK_module_sequencage_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_sequencage_as_intervenant_principal` (`intervenant_principal`),
  ADD KEY `FK_module_sequencage_as_groupe_type` (`id_groupe_type`),
  ADD KEY `FK_module_sequencage_as_seanceType` (`id_seance_type`);

--
-- Index pour la table `INFO_module_sequence`
--
ALTER TABLE `INFO_module_sequence`
  ADD PRIMARY KEY (`id_module_sequence`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequencage`,`numero_ordre`) USING BTREE;

--
-- Index pour la table `INFO_parameters_of_views`
--
ALTER TABLE `INFO_parameters_of_views`
  ADD PRIMARY KEY (`id_parameters_of_views`),
  ADD UNIQUE KEY `sessionId` (`sessionId`),
  ADD KEY `FK_parameters_of_views_as_semestre` (`id_semestre`),
  ADD KEY `FK_parameters_of_views_as_module` (`id_module`),
  ADD KEY `FK_parameters_of_views_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_parameters_of_views_as_discipline` (`id_discipline`),
  ADD KEY `FK_parameters_of_views_as_status` (`id_statut`),
  ADD KEY `FK_parameters_of_views_as_display_limit` (`id_display_limit`),
  ADD KEY `FK_parameters_of_views_as_filiere` (`id_filiere`);

--
-- Index pour la table `INFO_promo`
--
ALTER TABLE `INFO_promo`
  ADD PRIMARY KEY (`id_promo`),
  ADD UNIQUE KEY `SECONDARY` (`id_filiere`,`id_statut`,`annee`,`site`,`parcour`) USING BTREE,
  ADD KEY `FK_promo_as_statut` (`id_statut`),
  ADD KEY `FK_promo_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_seanceType`
--
ALTER TABLE `INFO_seanceType`
  ADD PRIMARY KEY (`id_seance_type`),
  ADD UNIQUE KEY `SECONDARY` (`type`);

--
-- Index pour la table `INFO_seance_planned`
--
ALTER TABLE `INFO_seance_planned`
  ADD PRIMARY KEY (`id_seance_planned`),
  ADD UNIQUE KEY `date` (`date`,`id_enseignant`),
  ADD KEY `FK_seance_seanceType` (`type`);

--
-- Index pour la table `INFO_seance_to_be_affected`
--
ALTER TABLE `INFO_seance_to_be_affected`
  ADD PRIMARY KEY (`id_seance_to_be_affected`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequence`,`id_groupe`) USING BTREE,
  ADD KEY `FK_seance_to_be_affected_as_groupe` (`id_groupe`);

--
-- Index pour la table `INFO_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_seance_to_be_affected_as_enseignant`
  ADD PRIMARY KEY (`id_seance_to_be_affected_as_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`id_seance_to_be_affected`) USING BTREE,
  ADD KEY `FK_seance_to_be_affected_as_enseignant_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_seance_to_be_affected_as_enseignant_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_semestre`
--
ALTER TABLE `INFO_semestre`
  ADD PRIMARY KEY (`id_semestre`),
  ADD UNIQUE KEY `SECONDARY` (`semestre`) USING BTREE;

--
-- Index pour la table `INFO_statut`
--
ALTER TABLE `INFO_statut`
  ADD PRIMARY KEY (`id_statut`),
  ADD UNIQUE KEY `SECONDARY` (`nom_statut`);

--
-- Index pour la table `INFO_type_seance_to_be_affected`
--
ALTER TABLE `INFO_type_seance_to_be_affected`
  ADD PRIMARY KEY (`id_type_seance_to_be_affected`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequencage`,`id_groupe`) USING BTREE,
  ADD KEY `FK_type_seance_to_be_affected_as_groupe` (`id_groupe`);

--
-- Index pour la table `INFO_type_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_type_seance_to_be_affected_as_enseignant`
  ADD PRIMARY KEY (`id_type_seance_to_be_affected_as_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`id_type_seance_to_be_affected`) USING BTREE,
  ADD KEY `FK_type_seance_to_be_affected_as_enseignant_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_type_seance_to_be_affected_as_enseignant_as_responsable` (`id_responsable`);

--
-- Index pour la table `INFO_updatable`
--
ALTER TABLE `INFO_updatable`
  ADD PRIMARY KEY (`id_updatable`),
  ADD UNIQUE KEY `SECONDARY` (`table_name`) USING BTREE,
  ADD UNIQUE KEY `table_name_displayed` (`table_name_displayed`);

--
-- Index pour la table `INFO_view`
--
ALTER TABLE `INFO_view`
  ADD PRIMARY KEY (`id_view`),
  ADD UNIQUE KEY `SECONDARY` (`name`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `INFO_check`
--
ALTER TABLE `INFO_check`
  MODIFY `id_view` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_discipline`
--
ALTER TABLE `INFO_discipline`
  MODIFY `id_discipline` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_display_limit`
--
ALTER TABLE `INFO_display_limit`
  MODIFY `id_display_limit` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  MODIFY `id_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  MODIFY `id_etat_module` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_groupe`
--
ALTER TABLE `INFO_groupe`
  MODIFY `id_groupe` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_learning_unit`
--
ALTER TABLE `INFO_learning_unit`
  MODIFY `id_learning_unit` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_module`
--
ALTER TABLE `INFO_module`
  MODIFY `id_module` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_module_sequencage`
--
ALTER TABLE `INFO_module_sequencage`
  MODIFY `id_module_sequencage` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_module_sequence`
--
ALTER TABLE `INFO_module_sequence`
  MODIFY `id_module_sequence` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_parameters_of_views`
--
ALTER TABLE `INFO_parameters_of_views`
  MODIFY `id_parameters_of_views` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_promo`
--
ALTER TABLE `INFO_promo`
  MODIFY `id_promo` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_seance_planned`
--
ALTER TABLE `INFO_seance_planned`
  MODIFY `id_seance_planned` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_seance_to_be_affected`
--
ALTER TABLE `INFO_seance_to_be_affected`
  MODIFY `id_seance_to_be_affected` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_seance_to_be_affected_as_enseignant`
  MODIFY `id_seance_to_be_affected_as_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_statut`
--
ALTER TABLE `INFO_statut`
  MODIFY `id_statut` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_type_seance_to_be_affected`
--
ALTER TABLE `INFO_type_seance_to_be_affected`
  MODIFY `id_type_seance_to_be_affected` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_type_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_type_seance_to_be_affected_as_enseignant`
  MODIFY `id_type_seance_to_be_affected_as_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_updatable`
--
ALTER TABLE `INFO_updatable`
  MODIFY `id_updatable` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_view`
--
ALTER TABLE `INFO_view`
  MODIFY `id_view` int NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `INFO_dependance_sequence`
--
ALTER TABLE `INFO_dependance_sequence`
  ADD CONSTRAINT `FK_dependance_sequence_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_next` FOREIGN KEY (`id_sequence_next`) REFERENCES `INFO_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_prev` FOREIGN KEY (`id_sequence_prev`) REFERENCES `INFO_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  ADD CONSTRAINT `FK_enseignant_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  ADD CONSTRAINT `FK_etat_module_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_filiere`
--
ALTER TABLE `INFO_filiere`
  ADD CONSTRAINT `FK_filiere_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_groupe`
--
ALTER TABLE `INFO_groupe`
  ADD CONSTRAINT `FK_groupe_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `INFO_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_groupe_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `INFO_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_learning_unit`
--
ALTER TABLE `INFO_learning_unit`
  ADD CONSTRAINT `FK_learning_unit_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `INFO_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_module`
--
ALTER TABLE `INFO_module`
  ADD CONSTRAINT `FK_module_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`),
  ADD CONSTRAINT `FK_module_as_etat_module` FOREIGN KEY (`id_etat_module`) REFERENCES `INFO_etat_module` (`id_etat_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `INFO_semestre` (`id_semestre`);

--
-- Contraintes pour la table `INFO_module_as_learning_unit`
--
ALTER TABLE `INFO_module_as_learning_unit`
  ADD CONSTRAINT `FK_module_as_learning_unit_as_learning_unit` FOREIGN KEY (`id_learning_unit`) REFERENCES `INFO_learning_unit` (`id_learning_unit`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_learning_unit_as_module` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_module_sequencage`
--
ALTER TABLE `INFO_module_sequencage`
  ADD CONSTRAINT `FK_module_sequencage_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `INFO_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_intervenant_principal` FOREIGN KEY (`intervenant_principal`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_module` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_seanceType` FOREIGN KEY (`id_seance_type`) REFERENCES `INFO_seanceType` (`id_seance_type`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_module_sequence`
--
ALTER TABLE `INFO_module_sequence`
  ADD CONSTRAINT `FK_module_sequence_as_module_sequencage` FOREIGN KEY (`id_module_sequencage`) REFERENCES `INFO_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `INFO_parameters_of_views`
--
ALTER TABLE `INFO_parameters_of_views`
  ADD CONSTRAINT `FK_parameters_of_views_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_display_limit` FOREIGN KEY (`id_display_limit`) REFERENCES `INFO_display_limit` (`id_display_limit`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `INFO_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_module` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `INFO_semestre` (`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_status` FOREIGN KEY (`id_statut`) REFERENCES `INFO_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_promo`
--
ALTER TABLE `INFO_promo`
  ADD CONSTRAINT `FK_promo_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `INFO_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_promo_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_promo_as_statut` FOREIGN KEY (`id_statut`) REFERENCES `INFO_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_seance_planned`
--
ALTER TABLE `INFO_seance_planned`
  ADD CONSTRAINT `FK_seance_seanceType` FOREIGN KEY (`type`) REFERENCES `INFO_seanceType` (`type`);

--
-- Contraintes pour la table `INFO_seance_to_be_affected`
--
ALTER TABLE `INFO_seance_to_be_affected`
  ADD CONSTRAINT `FK_seance_to_be_affected_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `INFO_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_module_sequence` FOREIGN KEY (`id_module_sequence`) REFERENCES `INFO_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `INFO_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_seance_to_be_affected_as_enseignant`
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_seance_to_be_affected` FOREIGN KEY (`id_seance_to_be_affected`) REFERENCES `INFO_seance_to_be_affected` (`id_seance_to_be_affected`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `INFO_type_seance_to_be_affected`
--
ALTER TABLE `INFO_type_seance_to_be_affected`
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `INFO_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_module_sequence` FOREIGN KEY (`id_module_sequencage`) REFERENCES `INFO_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `INFO_type_seance_to_be_affected_as_enseignant`
--
ALTER TABLE `INFO_type_seance_to_be_affected_as_enseignant`
  ADD CONSTRAINT `FK_tseance_to_be_affected_as_enseignant_as_seance_to_be_affected` FOREIGN KEY (`id_type_seance_to_be_affected`) REFERENCES `INFO_type_seance_to_be_affected` (`id_type_seance_to_be_affected`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_enseignant_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
