-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : mysql
-- Généré le : ven. 08 déc. 2023 à 21:27
-- Version du serveur : 8.0.33
-- Version de PHP : 8.2.8

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
-- Structure de la table `INFO_dependances`
--

CREATE TABLE `INFO_dependances` (
  `id_dependances` int NOT NULL,
  `id_module precedant` int NOT NULL,
  `type precedant` varchar(10) NOT NULL,
  `numero seance precedant` int NOT NULL,
  `id_module suivant` int NOT NULL,
  `type suivant` varchar(10) NOT NULL,
  `numero seance suivant` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_dependances_seance_to_be_planned`
--

CREATE TABLE `INFO_dependances_seance_to_be_planned` (
  `precedent` int NOT NULL,
  `successeur` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_dependance_sequence`
--

CREATE TABLE `INFO_dependance_sequence` (
  `id_squence_prev` int NOT NULL,
  `id_squence_next` int NOT NULL,
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
-- Structure de la table `INFO_enseignant`
--

CREATE TABLE `INFO_enseignant` (
  `id_enseignant` int NOT NULL,
  `prenom` varchar(25) NOT NULL,
  `nom` varchar(25) NOT NULL,
  `fullName` varchar(50) DEFAULT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `statut` enum('permanent','vacataire') NOT NULL DEFAULT 'permanent',
  `id_discipline` int DEFAULT NULL,
  `composante` varchar(25) DEFAULT NULL,
  `service statutaire` int NOT NULL,
  `décharge` int NOT NULL,
  `service effectif` float NOT NULL DEFAULT '192',
  `HCAutorisees` tinyint(1) NOT NULL DEFAULT '1',
  `commentaire` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_filiere`
--

CREATE TABLE `INFO_filiere` (
  `nom_filiere` varchar(11) NOT NULL,
  `nom_long` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_groupe`
--

CREATE TABLE `INFO_groupe` (
  `id_groupe` int NOT NULL,
  `nom_groupe` varchar(20) NOT NULL,
  `id_promo` int NOT NULL,
  `groupe_type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_groupe_type`
--

CREATE TABLE `INFO_groupe_type` (
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
  `learning_unit_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module`
--

CREATE TABLE `INFO_module` (
  `id_module` int NOT NULL,
  `code_module` varchar(10) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `id_discipline` int DEFAULT NULL,
  `id_semestre` tinyint NOT NULL,
  `id_learning_unit` int DEFAULT NULL,
  `hCM` float DEFAULT NULL,
  `hTD` float DEFAULT NULL,
  `hTP` float DEFAULT NULL,
  `hTPTD` float DEFAULT NULL,
  `hPROJ` float DEFAULT NULL,
  `hPersonnelle` float DEFAULT NULL,
  `type` enum('Specialite','Transverse') DEFAULT 'Specialite',
  `id_responsable` int DEFAULT NULL,
  `commentaire` text,
  `modifiable` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module_as_promo`
--

CREATE TABLE `INFO_module_as_promo` (
  `id_module` int NOT NULL,
  `id_promo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_module_sequencage`
--

CREATE TABLE `INFO_module_sequencage` (
  `id_module_sequencage` int NOT NULL,
  `id_module` int NOT NULL,
  `seanceType` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `groupe_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'CM',
  `numero_ordre` int DEFAULT NULL,
  `duree_h` decimal(10,1) NOT NULL,
  `id_responsable` int DEFAULT NULL,
  `commentaire` text,
  `modifiable` tinyint(1) NOT NULL DEFAULT '1'
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
  `code_module` int DEFAULT NULL,
  `id_discipline` int DEFAULT NULL,
  `fullname` int DEFAULT NULL,
  `nom_filiere` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_promo`
--

CREATE TABLE `INFO_promo` (
  `id_promo` int NOT NULL,
  `nom_filiere` varchar(11) NOT NULL,
  `statut` enum('FISE','FISA','FISEA','FISECP') DEFAULT 'FISE',
  `annee` int NOT NULL,
  `parcour` varchar(25) DEFAULT NULL,
  `site` varchar(25) NOT NULL,
  `nbGroupeCM` int NOT NULL DEFAULT '1',
  `nbGroupeTD` int NOT NULL,
  `nbGroupeTP` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seanceType`
--

CREATE TABLE `INFO_seanceType` (
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
-- Structure de la table `INFO_seance_to_be_planned`
--

CREATE TABLE `INFO_seance_to_be_planned` (
  `id_seance_to_be_planned` int NOT NULL,
  `lieu` varchar(25) NOT NULL,
  `type` varchar(10) NOT NULL,
  `heure` float NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_module` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_seance_to_be_planned_as_promo`
--

CREATE TABLE `INFO_seance_to_be_planned_as_promo` (
  `id_seance_to_be_planned` int NOT NULL,
  `id_promo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_semestre`
--

CREATE TABLE `INFO_semestre` (
  `id_semestre` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `INFO_view`
--

CREATE TABLE `INFO_view` (
  `id_view` int NOT NULL,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `INFO_dependances`
--
ALTER TABLE `INFO_dependances`
  ADD PRIMARY KEY (`id_dependances`),
  ADD KEY `FK_dependances_as_module_prev` (`id_module precedant`),
  ADD KEY `FK_dependances_as_module_next` (`id_module suivant`),
  ADD KEY `FK_dependances_as_seanceType_prev` (`type precedant`),
  ADD KEY `FK_dependances_as_seanceType_next` (`type suivant`);

--
-- Index pour la table `INFO_dependances_seance_to_be_planned`
--
ALTER TABLE `INFO_dependances_seance_to_be_planned`
  ADD PRIMARY KEY (`precedent`,`successeur`);

--
-- Index pour la table `INFO_dependance_sequence`
--
ALTER TABLE `INFO_dependance_sequence`
  ADD PRIMARY KEY (`id_squence_prev`,`id_squence_next`),
  ADD KEY `FK_dependance_sequence_as_module_sequencage_next` (`id_squence_next`),
  ADD KEY `FK_dependance_sequence_as_enseignant` (`id_responsable`);

--
-- Index pour la table `INFO_discipline`
--
ALTER TABLE `INFO_discipline`
  ADD PRIMARY KEY (`id_discipline`),
  ADD UNIQUE KEY `SECONDARY` (`nom`);

--
-- Index pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  ADD PRIMARY KEY (`id_enseignant`),
  ADD UNIQUE KEY `mail` (`mail`),
  ADD UNIQUE KEY `SECONDARY` (`fullName`) USING BTREE,
  ADD KEY `FK_enseignant_as_discipline` (`id_discipline`);

--
-- Index pour la table `INFO_filiere`
--
ALTER TABLE `INFO_filiere`
  ADD PRIMARY KEY (`nom_filiere`),
  ADD UNIQUE KEY `SECONDARY` (`nom_filiere`) USING BTREE;

--
-- Index pour la table `INFO_groupe`
--
ALTER TABLE `INFO_groupe`
  ADD PRIMARY KEY (`id_groupe`),
  ADD UNIQUE KEY `SECONDARY` (`nom_groupe`),
  ADD KEY `FK_groupe_as_promo` (`id_promo`),
  ADD KEY `FK_groupe_as_groupe_type` (`groupe_type`);

--
-- Index pour la table `INFO_groupe_type`
--
ALTER TABLE `INFO_groupe_type`
  ADD PRIMARY KEY (`groupe_type`),
  ADD UNIQUE KEY `SECONDARY` (`groupe_type`) USING BTREE;

--
-- Index pour la table `INFO_learning_unit`
--
ALTER TABLE `INFO_learning_unit`
  ADD PRIMARY KEY (`id_learning_unit`),
  ADD UNIQUE KEY `SECONDARY` (`learning_unit_code`);

--
-- Index pour la table `INFO_module`
--
ALTER TABLE `INFO_module`
  ADD PRIMARY KEY (`id_module`),
  ADD UNIQUE KEY `SECONDARY` (`code_module`) USING BTREE,
  ADD KEY `FK_module_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_as_semestre` (`id_semestre`),
  ADD KEY `FK_module_as_learning_unit` (`id_learning_unit`),
  ADD KEY `FK_module_as_discipline` (`id_discipline`);

--
-- Index pour la table `INFO_module_as_promo`
--
ALTER TABLE `INFO_module_as_promo`
  ADD PRIMARY KEY (`id_module`,`id_promo`),
  ADD KEY `FK_promo` (`id_promo`);

--
-- Index pour la table `INFO_module_sequencage`
--
ALTER TABLE `INFO_module_sequencage`
  ADD PRIMARY KEY (`id_module_sequencage`),
  ADD UNIQUE KEY `SECONDARY` (`id_module`,`seanceType`,`numero_ordre`) USING BTREE,
  ADD KEY `FK_module_sequencage_as_seanceType` (`seanceType`),
  ADD KEY `FK_module_sequencage_as_module` (`id_module`),
  ADD KEY `FK_module_sequencage_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_sequencage_as_groupe_type` (`groupe_type`);

--
-- Index pour la table `INFO_parameters_of_views`
--
ALTER TABLE `INFO_parameters_of_views`
  ADD PRIMARY KEY (`id_parameters_of_views`),
  ADD UNIQUE KEY `sessionId` (`sessionId`),
  ADD KEY `FK_parameters_of_views_as_semestre` (`id_semestre`),
  ADD KEY `FK_parameters_of_views_as_module` (`code_module`),
  ADD KEY `FK_parameters_of_views_as_enseignant` (`fullname`),
  ADD KEY `FK_parameters_of_views_as_filiere` (`nom_filiere`),
  ADD KEY `FK_parameters_of_views_as_discipline` (`id_discipline`);

--
-- Index pour la table `INFO_promo`
--
ALTER TABLE `INFO_promo`
  ADD PRIMARY KEY (`id_promo`),
  ADD UNIQUE KEY `SECONDARY` (`nom_filiere`,`statut`,`annee`,`site`,`parcour`) USING BTREE;

--
-- Index pour la table `INFO_seanceType`
--
ALTER TABLE `INFO_seanceType`
  ADD PRIMARY KEY (`type`),
  ADD UNIQUE KEY `SECONDARY` (`type`);

--
-- Index pour la table `INFO_seance_planned`
--
ALTER TABLE `INFO_seance_planned`
  ADD PRIMARY KEY (`id_seance_planned`),
  ADD UNIQUE KEY `date` (`date`,`id_enseignant`),
  ADD KEY `FK_seance_seanceType` (`type`);

--
-- Index pour la table `INFO_seance_to_be_planned`
--
ALTER TABLE `INFO_seance_to_be_planned`
  ADD PRIMARY KEY (`id_seance_to_be_planned`),
  ADD KEY `FK_module_seance_to_be_planned` (`id_module`),
  ADD KEY `FK_enseignant_seance_to_be_planned` (`id_enseignant`),
  ADD KEY `FK_seance_to_be_planned_seanceType` (`type`);

--
-- Index pour la table `INFO_seance_to_be_planned_as_promo`
--
ALTER TABLE `INFO_seance_to_be_planned_as_promo`
  ADD PRIMARY KEY (`id_seance_to_be_planned`,`id_promo`),
  ADD KEY `INFO_seance_to_be_planned_as_promo_ibfk_2` (`id_promo`);

--
-- Index pour la table `INFO_semestre`
--
ALTER TABLE `INFO_semestre`
  ADD PRIMARY KEY (`id_semestre`),
  ADD UNIQUE KEY `SECONDARY` (`id_semestre`) USING BTREE;

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
-- AUTO_INCREMENT pour la table `INFO_discipline`
--
ALTER TABLE `INFO_discipline`
  MODIFY `id_discipline` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  MODIFY `id_enseignant` int NOT NULL AUTO_INCREMENT;

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
-- AUTO_INCREMENT pour la table `INFO_seance_to_be_planned`
--
ALTER TABLE `INFO_seance_to_be_planned`
  MODIFY `id_seance_to_be_planned` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_view`
--
ALTER TABLE `INFO_view`
  MODIFY `id_view` int NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `INFO_dependances`
--
ALTER TABLE `INFO_dependances`
  ADD CONSTRAINT `FK_dependances_as_module_next` FOREIGN KEY (`id_module suivant`) REFERENCES `INFO_module` (`id_module`),
  ADD CONSTRAINT `FK_dependances_as_module_prev` FOREIGN KEY (`id_module precedant`) REFERENCES `INFO_module` (`id_module`),
  ADD CONSTRAINT `FK_dependances_as_seanceType_next` FOREIGN KEY (`type suivant`) REFERENCES `INFO_seanceType` (`type`),
  ADD CONSTRAINT `FK_dependances_as_seanceType_prev` FOREIGN KEY (`type precedant`) REFERENCES `INFO_seanceType` (`type`);

--
-- Contraintes pour la table `INFO_dependance_sequence`
--
ALTER TABLE `INFO_dependance_sequence`
  ADD CONSTRAINT `FK_dependance_sequence_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_next` FOREIGN KEY (`id_squence_next`) REFERENCES `INFO_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_prev` FOREIGN KEY (`id_squence_prev`) REFERENCES `INFO_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_enseignant`
--
ALTER TABLE `INFO_enseignant`
  ADD CONSTRAINT `FK_enseignant_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_groupe`
--
ALTER TABLE `INFO_groupe`
  ADD CONSTRAINT `FK_groupe_as_groupe_type` FOREIGN KEY (`groupe_type`) REFERENCES `INFO_groupe_type` (`groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_groupe_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `INFO_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_module`
--
ALTER TABLE `INFO_module`
  ADD CONSTRAINT `FK_module_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`),
  ADD CONSTRAINT `FK_module_as_learning_unit` FOREIGN KEY (`id_learning_unit`) REFERENCES `INFO_learning_unit` (`id_learning_unit`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `INFO_semestre` (`id_semestre`);

--
-- Contraintes pour la table `INFO_module_as_promo`
--
ALTER TABLE `INFO_module_as_promo`
  ADD CONSTRAINT `FK_module` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`),
  ADD CONSTRAINT `FK_promo` FOREIGN KEY (`id_promo`) REFERENCES `INFO_promo` (`id_promo`);

--
-- Contraintes pour la table `INFO_module_sequencage`
--
ALTER TABLE `INFO_module_sequencage`
  ADD CONSTRAINT `FK_module_sequencage_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `INFO_enseignant` (`id_enseignant`),
  ADD CONSTRAINT `FK_module_sequencage_as_groupe_type` FOREIGN KEY (`groupe_type`) REFERENCES `INFO_groupe_type` (`groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_module` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_seanceType` FOREIGN KEY (`seanceType`) REFERENCES `INFO_seanceType` (`type`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_parameters_of_views`
--
ALTER TABLE `INFO_parameters_of_views`
  ADD CONSTRAINT `FK_parameters_of_views_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `INFO_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_enseignant` FOREIGN KEY (`fullname`) REFERENCES `INFO_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_filiere` FOREIGN KEY (`nom_filiere`) REFERENCES `INFO_filiere` (`nom_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_module` FOREIGN KEY (`code_module`) REFERENCES `INFO_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `INFO_semestre` (`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `INFO_promo`
--
ALTER TABLE `INFO_promo`
  ADD CONSTRAINT `FK_filiere` FOREIGN KEY (`nom_filiere`) REFERENCES `INFO_filiere` (`nom_filiere`);

--
-- Contraintes pour la table `INFO_seance_planned`
--
ALTER TABLE `INFO_seance_planned`
  ADD CONSTRAINT `FK_seance_seanceType` FOREIGN KEY (`type`) REFERENCES `INFO_seanceType` (`type`);

--
-- Contraintes pour la table `INFO_seance_to_be_planned`
--
ALTER TABLE `INFO_seance_to_be_planned`
  ADD CONSTRAINT `FK_enseignant_seance_to_be_planned` FOREIGN KEY (`id_enseignant`) REFERENCES `INFO_enseignant` (`id_enseignant`),
  ADD CONSTRAINT `FK_module_seance_to_be_planned` FOREIGN KEY (`id_module`) REFERENCES `INFO_module` (`id_module`),
  ADD CONSTRAINT `FK_seance_to_be_planned_seanceType` FOREIGN KEY (`type`) REFERENCES `INFO_seanceType` (`type`);

--
-- Contraintes pour la table `INFO_seance_to_be_planned_as_promo`
--
ALTER TABLE `INFO_seance_to_be_planned_as_promo`
  ADD CONSTRAINT `INFO_seance_to_be_planned_as_promo_ibfk_1` FOREIGN KEY (`id_seance_to_be_planned`) REFERENCES `INFO_seance_to_be_planned` (`id_seance_to_be_planned`),
  ADD CONSTRAINT `INFO_seance_to_be_planned_as_promo_ibfk_2` FOREIGN KEY (`id_promo`) REFERENCES `INFO_promo` (`id_promo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;