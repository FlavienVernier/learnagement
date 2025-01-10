-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : mysql
-- Généré le : jeu. 12 déc. 2024 à 10:18
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
-- Structure de la table `APC_apprentissage_critique`
--

CREATE TABLE `APC_apprentissage_critique` (
  `id_apprentissage_critique` int NOT NULL,
  `id_niveau` int NOT NULL,
  `libelle_apprentissage` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_apprentissage_critique_as_module`
--

CREATE TABLE `APC_apprentissage_critique_as_module` (
  `id_apprentissage_critique` int NOT NULL,
  `id_module` int NOT NULL,
  `type_lien` enum('Requis','Recommandé','Complémentaire') CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'Requis'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_competence`
--

CREATE TABLE `APC_competence` (
  `id_competence` int NOT NULL,
  `libelle_competence` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `code_competence` varchar(25) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_competence_as_filiere_as_statut`
--

CREATE TABLE `APC_competence_as_filiere_as_statut` (
  `id_competence` int NOT NULL,
  `is_filiere` int NOT NULL,
  `id_status` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_composante_essentielle`
--

CREATE TABLE `APC_composante_essentielle` (
  `id_composante_essentielle` int NOT NULL,
  `id_competence` int NOT NULL,
  `libelle_composante_essentielle` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_niveau`
--

CREATE TABLE `APC_niveau` (
  `id_niveau` int NOT NULL,
  `id_competence` int NOT NULL,
  `niveau` int NOT NULL,
  `libelle_niveau` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `APC_situation_professionnelle`
--

CREATE TABLE `APC_situation_professionnelle` (
  `id_situation_professionnelle` int NOT NULL,
  `id_competence` int NOT NULL,
  `libelle_situation` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Structure de la table `CLASS_session_to_be_affected`
--

CREATE TABLE `CLASS_session_to_be_affected` (
  `id_seance_to_be_affected` int NOT NULL,
  `id_module_sequence` int DEFAULT NULL,
  `id_groupe` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `CLASS_session_to_be_affected_as_enseignant`
--

CREATE TABLE `CLASS_session_to_be_affected_as_enseignant` (
  `id_seance_to_be_affected_as_enseignant` int NOT NULL,
  `id_seance_to_be_affected` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `CLASS_session_type_to_be_affected`
--

CREATE TABLE `CLASS_session_type_to_be_affected` (
  `id_type_seance_to_be_affected` int NOT NULL,
  `id_module_sequencage` int NOT NULL,
  `id_groupe` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `CLASS_session_type_to_be_affected_as_enseignant`
--

CREATE TABLE `CLASS_session_type_to_be_affected_as_enseignant` (
  `id_type_seance_to_be_affected_as_enseignant` int NOT NULL,
  `id_type_seance_to_be_affected` int NOT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `ETU_polypoint`
--

CREATE TABLE `ETU_polypoint` (
  `id_polypoint` int NOT NULL,
  `intitule` varchar(100) NOT NULL,
  `tache` varchar(50) NOT NULL,
  `nb_point` int NOT NULL,
  `annee_universitaire` varchar(9) NOT NULL,
  `id_etudiant` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `EXT_seance_planned`
--

CREATE TABLE `EXT_seance_planned` (
  `id_seance_planned` int NOT NULL,
  `type` varchar(10) NOT NULL,
  `date` datetime NOT NULL,
  `duree_h` time NOT NULL,
  `id_module` int NOT NULL,
  `id_enseignant` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Data extracted from calendar system';

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
-- Structure de la table `LNM_enseignant`
--

CREATE TABLE `LNM_enseignant` (
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
-- Structure de la table `LNM_etudiant`
--

CREATE TABLE `LNM_etudiant` (
  `id_etudiant` int NOT NULL,
  `nom` varchar(25) NOT NULL,
  `prenom` varchar(25) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_promo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_filiere`
--

CREATE TABLE `LNM_filiere` (
  `id_filiere` int NOT NULL,
  `nom_filiere` varchar(11) NOT NULL,
  `nom_long` varchar(50) DEFAULT NULL,
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_groupe`
--

CREATE TABLE `LNM_groupe` (
  `id_groupe` int NOT NULL,
  `nom_groupe` varchar(20) NOT NULL,
  `id_promo` int NOT NULL,
  `id_groupe_type` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_groupe_type`
--

CREATE TABLE `LNM_groupe_type` (
  `id_groupe_type` int NOT NULL,
  `groupe_type` varchar(10) NOT NULL,
  `commentaire` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_promo`
--

CREATE TABLE `LNM_promo` (
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
-- Structure de la table `LNM_rendu_module`
--

CREATE TABLE `LNM_rendu_module` (
  `id_rendu_module` int NOT NULL,
  `description` varchar(100) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_rendu_module_as_enseignant`
--

CREATE TABLE `LNM_rendu_module_as_enseignant` (
  `id_rendu_module` int NOT NULL,
  `id_enseignant` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_rendu_module_as_etudiant`
--

CREATE TABLE `LNM_rendu_module_as_etudiant` (
  `id_rendu_module` int NOT NULL,
  `id_etudiant` int NOT NULL,
  `date_depot` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_seanceType`
--

CREATE TABLE `LNM_seanceType` (
  `id_seance_type` int NOT NULL,
  `type` varchar(10) NOT NULL,
  `commentaire` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_semestre`
--

CREATE TABLE `LNM_semestre` (
  `id_semestre` tinyint NOT NULL,
  `semestre` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_stage`
--

CREATE TABLE `LNM_stage` (
  `id_stage` int NOT NULL,
  `entreprise` varchar(100) NOT NULL,
  `ville` varchar(50) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `nature` varchar(50) NOT NULL,
  `id_etudiant` int NOT NULL,
  `id_enseignant` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_statut`
--

CREATE TABLE `LNM_statut` (
  `id_statut` int NOT NULL,
  `nom_statut` varchar(10) NOT NULL,
  `Description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `LNM_universite`
--

CREATE TABLE `LNM_universite` (
  `id_universite` int NOT NULL,
  `nom` varchar(250) NOT NULL,
  `nom_court` varchar(50) NOT NULL,
  `ville` varchar(50) NOT NULL,
  `pays` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `MAQUETTE_dependance_sequence`
--

CREATE TABLE `MAQUETTE_dependance_sequence` (
  `id_sequence_prev` int NOT NULL,
  `id_sequence_next` int NOT NULL,
  `id_responsable` int NOT NULL,
  `modifiable` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `MAQUETTE_discipline`
--

CREATE TABLE `MAQUETTE_discipline` (
  `id_discipline` int NOT NULL,
  `nom` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `MAQUETTE_learning_unit`
--

CREATE TABLE `MAQUETTE_learning_unit` (
  `id_learning_unit` int NOT NULL,
  `learning_unit_code` varchar(10) NOT NULL,
  `learning_unit_name` varchar(50) NOT NULL,
  `id_promo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `MAQUETTE_module`
--

CREATE TABLE `MAQUETTE_module` (
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
-- Structure de la table `MAQUETTE_module_as_learning_unit`
--

CREATE TABLE `MAQUETTE_module_as_learning_unit` (
  `id_module` int NOT NULL,
  `id_learning_unit` int NOT NULL,
  `modifiable` tinyint(1) NOT NULL DEFAULT '0',
  `id_responsable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `MAQUETTE_module_sequencage`
--

CREATE TABLE `MAQUETTE_module_sequencage` (
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
-- Structure de la table `MAQUETTE_module_sequence`
--

CREATE TABLE `MAQUETTE_module_sequence` (
  `id_module_sequence` int NOT NULL,
  `id_module_sequencage` int DEFAULT NULL,
  `numero_ordre` int DEFAULT NULL,
  `commentaire` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- --------------------------------------------------------

--
-- Structure de la table `VIEW_check`
--

CREATE TABLE `VIEW_check` (
  `id_view` int NOT NULL,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `VIEW_display`
--

CREATE TABLE `VIEW_display` (
  `id_view` int NOT NULL,
  `sortIndex` int NOT NULL,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Unclassified',
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `VIEW_parameters_of_views`
--

CREATE TABLE `VIEW_parameters_of_views` (
  `id_parameters_of_views` int NOT NULL,
  `userId` int DEFAULT NULL,
  `sessionId` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_semestre` tinyint DEFAULT NULL,
  `id_module` int DEFAULT NULL,
  `id_discipline` int DEFAULT NULL,
  `id_enseignant` int DEFAULT NULL,
  `id_filiere` int DEFAULT NULL,
  `id_statut` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `VIEW_updatable`
--

CREATE TABLE `VIEW_updatable` (
  `id_updatable` int NOT NULL,
  `sortIndex` int NOT NULL,
  `table_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `table_name_displayed` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_of_views` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `allow_insert` tinyint NOT NULL,
  `allow_update` tinyint NOT NULL,
  `request` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `APC_apprentissage_critique`
--
ALTER TABLE `APC_apprentissage_critique`
  ADD PRIMARY KEY (`id_apprentissage_critique`),
  ADD UNIQUE KEY `SECONDARY` (`libelle_apprentissage`),
  ADD KEY `FK_apprentissage_critique_as_niveau` (`id_niveau`);

--
-- Index pour la table `APC_apprentissage_critique_as_module`
--
ALTER TABLE `APC_apprentissage_critique_as_module`
  ADD PRIMARY KEY (`id_apprentissage_critique`,`id_module`),
  ADD KEY `FK_apprentissage_critique_as_module_as_module` (`id_module`);

--
-- Index pour la table `APC_competence`
--
ALTER TABLE `APC_competence`
  ADD PRIMARY KEY (`id_competence`),
  ADD UNIQUE KEY `SECONDARY` (`code_competence`);

--
-- Index pour la table `APC_competence_as_filiere_as_statut`
--
ALTER TABLE `APC_competence_as_filiere_as_statut`
  ADD PRIMARY KEY (`id_competence`,`is_filiere`,`id_status`);

--
-- Index pour la table `APC_composante_essentielle`
--
ALTER TABLE `APC_composante_essentielle`
  ADD PRIMARY KEY (`id_composante_essentielle`),
  ADD UNIQUE KEY `SECONDARY` (`libelle_composante_essentielle`),
  ADD KEY `FK_composante_essentielle_as_competence` (`id_competence`);

--
-- Index pour la table `APC_niveau`
--
ALTER TABLE `APC_niveau`
  ADD PRIMARY KEY (`id_niveau`),
  ADD UNIQUE KEY `SECONDARY` (`id_competence`,`niveau`) USING BTREE;

--
-- Index pour la table `APC_situation_professionnelle`
--
ALTER TABLE `APC_situation_professionnelle`
  ADD PRIMARY KEY (`id_situation_professionnelle`),
  ADD KEY `FK_situation_professionnelle_as_competence` (`id_competence`);

--
-- Index pour la table `CLASS_session_to_be_affected`
--
ALTER TABLE `CLASS_session_to_be_affected`
  ADD PRIMARY KEY (`id_seance_to_be_affected`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequence`,`id_groupe`) USING BTREE,
  ADD KEY `FK_seance_to_be_affected_as_groupe` (`id_groupe`);

--
-- Index pour la table `CLASS_session_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_to_be_affected_as_enseignant`
  ADD PRIMARY KEY (`id_seance_to_be_affected_as_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`id_seance_to_be_affected`) USING BTREE,
  ADD KEY `FK_seance_to_be_affected_as_enseignant_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_seance_to_be_affected_as_enseignant_as_responsable` (`id_responsable`);

--
-- Index pour la table `CLASS_session_type_to_be_affected`
--
ALTER TABLE `CLASS_session_type_to_be_affected`
  ADD PRIMARY KEY (`id_type_seance_to_be_affected`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequencage`,`id_groupe`) USING BTREE,
  ADD KEY `FK_type_seance_to_be_affected_as_groupe` (`id_groupe`);

--
-- Index pour la table `CLASS_session_type_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_type_to_be_affected_as_enseignant`
  ADD PRIMARY KEY (`id_type_seance_to_be_affected_as_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`id_type_seance_to_be_affected`) USING BTREE,
  ADD KEY `FK_type_seance_to_be_affected_as_enseignant_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_type_seance_to_be_affected_as_enseignant_as_responsable` (`id_responsable`);

--
-- Index pour la table `ETU_polypoint`
--
ALTER TABLE `ETU_polypoint`
  ADD PRIMARY KEY (`id_polypoint`),
  ADD KEY `FK_polypoint_as_etudiant` (`id_etudiant`);

--
-- Index pour la table `EXT_seance_planned`
--
ALTER TABLE `EXT_seance_planned`
  ADD PRIMARY KEY (`id_seance_planned`),
  ADD UNIQUE KEY `date` (`date`,`id_enseignant`),
  ADD KEY `FK_seance_seanceType` (`type`);

--
-- Index pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  ADD PRIMARY KEY (`id_etat_module`),
  ADD UNIQUE KEY `SECONDARY` (`etat`),
  ADD KEY `FK_etat_module_as_responsable` (`id_responsable`);

--
-- Index pour la table `LNM_enseignant`
--
ALTER TABLE `LNM_enseignant`
  ADD PRIMARY KEY (`id_enseignant`),
  ADD UNIQUE KEY `SECONDARY` (`prenom`,`nom`) USING BTREE,
  ADD UNIQUE KEY `mail` (`mail`),
  ADD KEY `FK_enseignant_as_discipline` (`id_discipline`);

--
-- Index pour la table `LNM_etudiant`
--
ALTER TABLE `LNM_etudiant`
  ADD PRIMARY KEY (`id_etudiant`),
  ADD KEY `FK_etudiant_as_promo` (`id_promo`);

--
-- Index pour la table `LNM_filiere`
--
ALTER TABLE `LNM_filiere`
  ADD PRIMARY KEY (`id_filiere`),
  ADD UNIQUE KEY `SECONDARY` (`nom_filiere`) USING BTREE,
  ADD KEY `FK_filiere_as_responsable` (`id_responsable`);

--
-- Index pour la table `LNM_groupe`
--
ALTER TABLE `LNM_groupe`
  ADD PRIMARY KEY (`id_groupe`),
  ADD UNIQUE KEY `SECONDARY` (`nom_groupe`),
  ADD KEY `FK_groupe_as_promo` (`id_promo`),
  ADD KEY `FK_groupe_as_groupe_type` (`id_groupe_type`);

--
-- Index pour la table `LNM_groupe_type`
--
ALTER TABLE `LNM_groupe_type`
  ADD PRIMARY KEY (`id_groupe_type`),
  ADD UNIQUE KEY `SECONDARY` (`groupe_type`) USING BTREE;

--
-- Index pour la table `LNM_promo`
--
ALTER TABLE `LNM_promo`
  ADD PRIMARY KEY (`id_promo`),
  ADD UNIQUE KEY `SECONDARY` (`id_filiere`,`id_statut`,`annee`,`site`,`parcour`) USING BTREE,
  ADD KEY `FK_promo_as_statut` (`id_statut`),
  ADD KEY `FK_promo_as_responsable` (`id_responsable`);

--
-- Index pour la table `LNM_rendu_module`
--
ALTER TABLE `LNM_rendu_module`
  ADD PRIMARY KEY (`id_rendu_module`);

--
-- Index pour la table `LNM_rendu_module_as_enseignant`
--
ALTER TABLE `LNM_rendu_module_as_enseignant`
  ADD PRIMARY KEY (`id_rendu_module`,`id_enseignant`),
  ADD KEY `FK_rendu_module_as_enseignant_as_enseignant` (`id_enseignant`);

--
-- Index pour la table `LNM_rendu_module_as_etudiant`
--
ALTER TABLE `LNM_rendu_module_as_etudiant`
  ADD PRIMARY KEY (`id_rendu_module`,`id_etudiant`),
  ADD KEY `FK_rendu_module_as_etudiant_as_etudiant` (`id_etudiant`);

--
-- Index pour la table `LNM_seanceType`
--
ALTER TABLE `LNM_seanceType`
  ADD PRIMARY KEY (`id_seance_type`),
  ADD UNIQUE KEY `SECONDARY` (`type`);

--
-- Index pour la table `LNM_semestre`
--
ALTER TABLE `LNM_semestre`
  ADD PRIMARY KEY (`id_semestre`),
  ADD UNIQUE KEY `SECONDARY` (`semestre`) USING BTREE;

--
-- Index pour la table `LNM_stage`
--
ALTER TABLE `LNM_stage`
  ADD PRIMARY KEY (`id_stage`),
  ADD KEY `FK_stage_as_etudiant` (`id_etudiant`),
  ADD KEY `FK_stage_as_enseignant` (`id_enseignant`);

--
-- Index pour la table `LNM_statut`
--
ALTER TABLE `LNM_statut`
  ADD PRIMARY KEY (`id_statut`),
  ADD UNIQUE KEY `SECONDARY` (`nom_statut`);

--
-- Index pour la table `LNM_universite`
--
ALTER TABLE `LNM_universite`
  ADD PRIMARY KEY (`id_universite`),
  ADD UNIQUE KEY `SECONDARY` (`nom_court`) USING BTREE,
  ADD UNIQUE KEY `nom` (`nom`);

--
-- Index pour la table `MAQUETTE_dependance_sequence`
--
ALTER TABLE `MAQUETTE_dependance_sequence`
  ADD PRIMARY KEY (`id_sequence_prev`,`id_sequence_next`),
  ADD KEY `FK_dependance_sequence_as_module_sequencage_next` (`id_sequence_next`),
  ADD KEY `FK_dependance_sequence_as_enseignant` (`id_responsable`);

--
-- Index pour la table `MAQUETTE_discipline`
--
ALTER TABLE `MAQUETTE_discipline`
  ADD PRIMARY KEY (`id_discipline`),
  ADD UNIQUE KEY `SECONDARY` (`nom`);

--
-- Index pour la table `MAQUETTE_learning_unit`
--
ALTER TABLE `MAQUETTE_learning_unit`
  ADD PRIMARY KEY (`id_learning_unit`),
  ADD UNIQUE KEY `SECONDARY` (`learning_unit_code`,`id_promo`) USING BTREE,
  ADD KEY `FK_learning_unit_as_promo` (`id_promo`);

--
-- Index pour la table `MAQUETTE_module`
--
ALTER TABLE `MAQUETTE_module`
  ADD PRIMARY KEY (`id_module`),
  ADD UNIQUE KEY `SECONDARY` (`code_module`) USING BTREE,
  ADD KEY `FK_module_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_as_semestre` (`id_semestre`),
  ADD KEY `FK_module_as_discipline` (`id_discipline`),
  ADD KEY `FK_module_as_etat_module` (`id_etat_module`);

--
-- Index pour la table `MAQUETTE_module_as_learning_unit`
--
ALTER TABLE `MAQUETTE_module_as_learning_unit`
  ADD PRIMARY KEY (`id_module`,`id_learning_unit`),
  ADD KEY `FK_module_as_learning_unit_as_learning_unit` (`id_learning_unit`),
  ADD KEY `FK_module_sequencage_as_responsable` (`id_responsable`);

--
-- Index pour la table `MAQUETTE_module_sequencage`
--
ALTER TABLE `MAQUETTE_module_sequencage`
  ADD PRIMARY KEY (`id_module_sequencage`),
  ADD UNIQUE KEY `SECONDARY` (`id_module`,`id_seance_type`,`id_groupe_type`,`duree_h`) USING BTREE,
  ADD KEY `FK_module_sequencage_as_enseignant` (`id_responsable`),
  ADD KEY `FK_module_sequencage_as_intervenant_principal` (`intervenant_principal`),
  ADD KEY `FK_module_sequencage_as_groupe_type` (`id_groupe_type`),
  ADD KEY `FK_module_sequencage_as_seanceType` (`id_seance_type`);

--
-- Index pour la table `MAQUETTE_module_sequence`
--
ALTER TABLE `MAQUETTE_module_sequence`
  ADD PRIMARY KEY (`id_module_sequence`),
  ADD UNIQUE KEY `SECONDARY` (`id_module_sequencage`,`numero_ordre`) USING BTREE;

--
-- Index pour la table `VIEW_check`
--
ALTER TABLE `VIEW_check`
  ADD PRIMARY KEY (`id_view`),
  ADD UNIQUE KEY `SECONDARY` (`name`);

--
-- Index pour la table `VIEW_display`
--
ALTER TABLE `VIEW_display`
  ADD PRIMARY KEY (`id_view`),
  ADD UNIQUE KEY `SECONDARY` (`name`);

--
-- Index pour la table `VIEW_parameters_of_views`
--
ALTER TABLE `VIEW_parameters_of_views`
  ADD PRIMARY KEY (`id_parameters_of_views`),
  ADD UNIQUE KEY `sessionId` (`sessionId`),
  ADD KEY `FK_parameters_of_views_as_semestre` (`id_semestre`),
  ADD KEY `FK_parameters_of_views_as_module` (`id_module`),
  ADD KEY `FK_parameters_of_views_as_enseignant` (`id_enseignant`),
  ADD KEY `FK_parameters_of_views_as_discipline` (`id_discipline`),
  ADD KEY `FK_parameters_of_views_as_status` (`id_statut`),
  ADD KEY `FK_parameters_of_views_as_filiere` (`id_filiere`);

--
-- Index pour la table `VIEW_updatable`
--
ALTER TABLE `VIEW_updatable`
  ADD PRIMARY KEY (`id_updatable`),
  ADD UNIQUE KEY `SECONDARY` (`table_name`) USING BTREE,
  ADD UNIQUE KEY `table_name_displayed` (`table_name_displayed`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `APC_apprentissage_critique`
--
ALTER TABLE `APC_apprentissage_critique`
  MODIFY `id_apprentissage_critique` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `APC_competence`
--
ALTER TABLE `APC_competence`
  MODIFY `id_competence` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `APC_composante_essentielle`
--
ALTER TABLE `APC_composante_essentielle`
  MODIFY `id_composante_essentielle` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `APC_niveau`
--
ALTER TABLE `APC_niveau`
  MODIFY `id_niveau` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `APC_situation_professionnelle`
--
ALTER TABLE `APC_situation_professionnelle`
  MODIFY `id_situation_professionnelle` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `CLASS_session_to_be_affected`
--
ALTER TABLE `CLASS_session_to_be_affected`
  MODIFY `id_seance_to_be_affected` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `CLASS_session_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_to_be_affected_as_enseignant`
  MODIFY `id_seance_to_be_affected_as_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `CLASS_session_type_to_be_affected`
--
ALTER TABLE `CLASS_session_type_to_be_affected`
  MODIFY `id_type_seance_to_be_affected` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `CLASS_session_type_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_type_to_be_affected_as_enseignant`
  MODIFY `id_type_seance_to_be_affected_as_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `ETU_polypoint`
--
ALTER TABLE `ETU_polypoint`
  MODIFY `id_polypoint` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `EXT_seance_planned`
--
ALTER TABLE `EXT_seance_planned`
  MODIFY `id_seance_planned` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  MODIFY `id_etat_module` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_enseignant`
--
ALTER TABLE `LNM_enseignant`
  MODIFY `id_enseignant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_etudiant`
--
ALTER TABLE `LNM_etudiant`
  MODIFY `id_etudiant` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_groupe`
--
ALTER TABLE `LNM_groupe`
  MODIFY `id_groupe` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_promo`
--
ALTER TABLE `LNM_promo`
  MODIFY `id_promo` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_rendu_module`
--
ALTER TABLE `LNM_rendu_module`
  MODIFY `id_rendu_module` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_stage`
--
ALTER TABLE `LNM_stage`
  MODIFY `id_stage` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_statut`
--
ALTER TABLE `LNM_statut`
  MODIFY `id_statut` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `LNM_universite`
--
ALTER TABLE `LNM_universite`
  MODIFY `id_universite` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `MAQUETTE_discipline`
--
ALTER TABLE `MAQUETTE_discipline`
  MODIFY `id_discipline` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `MAQUETTE_learning_unit`
--
ALTER TABLE `MAQUETTE_learning_unit`
  MODIFY `id_learning_unit` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `MAQUETTE_module`
--
ALTER TABLE `MAQUETTE_module`
  MODIFY `id_module` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `MAQUETTE_module_sequencage`
--
ALTER TABLE `MAQUETTE_module_sequencage`
  MODIFY `id_module_sequencage` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `MAQUETTE_module_sequence`
--
ALTER TABLE `MAQUETTE_module_sequence`
  MODIFY `id_module_sequence` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `VIEW_check`
--
ALTER TABLE `VIEW_check`
  MODIFY `id_view` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `VIEW_display`
--
ALTER TABLE `VIEW_display`
  MODIFY `id_view` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `VIEW_parameters_of_views`
--
ALTER TABLE `VIEW_parameters_of_views`
  MODIFY `id_parameters_of_views` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `VIEW_updatable`
--
ALTER TABLE `VIEW_updatable`
  MODIFY `id_updatable` int NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `APC_apprentissage_critique`
--
ALTER TABLE `APC_apprentissage_critique`
  ADD CONSTRAINT `FK_apprentissage_critique_as_niveau` FOREIGN KEY (`id_niveau`) REFERENCES `APC_niveau` (`id_niveau`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `APC_apprentissage_critique_as_module`
--
ALTER TABLE `APC_apprentissage_critique_as_module`
  ADD CONSTRAINT `FK_apprentissage_critique_as_module_as_apprentissage_critique` FOREIGN KEY (`id_apprentissage_critique`) REFERENCES `APC_apprentissage_critique` (`id_apprentissage_critique`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_apprentissage_critique_as_module_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `APC_composante_essentielle`
--
ALTER TABLE `APC_composante_essentielle`
  ADD CONSTRAINT `FK_composante_essentielle_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `APC_niveau`
--
ALTER TABLE `APC_niveau`
  ADD CONSTRAINT `FK_niveau_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `APC_situation_professionnelle`
--
ALTER TABLE `APC_situation_professionnelle`
  ADD CONSTRAINT `FK_situation_professionnelle_as_competence` FOREIGN KEY (`id_competence`) REFERENCES `APC_competence` (`id_competence`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `CLASS_session_to_be_affected`
--
ALTER TABLE `CLASS_session_to_be_affected`
  ADD CONSTRAINT `FK_seance_to_be_affected_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `LNM_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_module_sequence` FOREIGN KEY (`id_module_sequence`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `CLASS_session_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_to_be_affected_as_enseignant`
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_seance_to_be_affected_as_enseignant_as_seance_to_be_affected` FOREIGN KEY (`id_seance_to_be_affected`) REFERENCES `CLASS_session_to_be_affected` (`id_seance_to_be_affected`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `CLASS_session_type_to_be_affected`
--
ALTER TABLE `CLASS_session_type_to_be_affected`
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_groupe` FOREIGN KEY (`id_groupe`) REFERENCES `LNM_groupe` (`id_groupe`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_module_sequence` FOREIGN KEY (`id_module_sequencage`) REFERENCES `MAQUETTE_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `CLASS_session_type_to_be_affected_as_enseignant`
--
ALTER TABLE `CLASS_session_type_to_be_affected_as_enseignant`
  ADD CONSTRAINT `FK_tseance_to_be_affected_as_enseignant_as_seance_to_be_affected` FOREIGN KEY (`id_type_seance_to_be_affected`) REFERENCES `CLASS_session_type_to_be_affected` (`id_type_seance_to_be_affected`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_type_seance_to_be_affected_as_enseignant_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `ETU_polypoint`
--
ALTER TABLE `ETU_polypoint`
  ADD CONSTRAINT `FK_polypoint_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `EXT_seance_planned`
--
ALTER TABLE `EXT_seance_planned`
  ADD CONSTRAINT `FK_seance_seanceType` FOREIGN KEY (`type`) REFERENCES `LNM_seanceType` (`type`);

--
-- Contraintes pour la table `INFO_etat_module`
--
ALTER TABLE `INFO_etat_module`
  ADD CONSTRAINT `FK_etat_module_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_enseignant`
--
ALTER TABLE `LNM_enseignant`
  ADD CONSTRAINT `FK_enseignant_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_etudiant`
--
ALTER TABLE `LNM_etudiant`
  ADD CONSTRAINT `FK_etudiant_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_filiere`
--
ALTER TABLE `LNM_filiere`
  ADD CONSTRAINT `FK_filiere_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_groupe`
--
ALTER TABLE `LNM_groupe`
  ADD CONSTRAINT `FK_groupe_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `LNM_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_groupe_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_promo`
--
ALTER TABLE `LNM_promo`
  ADD CONSTRAINT `FK_promo_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_promo_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_promo_as_statut` FOREIGN KEY (`id_statut`) REFERENCES `LNM_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_rendu_module_as_enseignant`
--
ALTER TABLE `LNM_rendu_module_as_enseignant`
  ADD CONSTRAINT `FK_rendu_module_as_enseignant_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_rendu_module_as_enseignant_as_rendu_module` FOREIGN KEY (`id_rendu_module`) REFERENCES `LNM_rendu_module` (`id_rendu_module`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_rendu_module_as_etudiant`
--
ALTER TABLE `LNM_rendu_module_as_etudiant`
  ADD CONSTRAINT `FK_rendu_module_as_etudiant_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_rendu_module_as_etudiant_as_rendu_module` FOREIGN KEY (`id_rendu_module`) REFERENCES `LNM_rendu_module` (`id_rendu_module`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `LNM_stage`
--
ALTER TABLE `LNM_stage`
  ADD CONSTRAINT `FK_stage_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_stage_as_etudiant` FOREIGN KEY (`id_etudiant`) REFERENCES `LNM_etudiant` (`id_etudiant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `MAQUETTE_dependance_sequence`
--
ALTER TABLE `MAQUETTE_dependance_sequence`
  ADD CONSTRAINT `FK_dependance_sequence_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_next` FOREIGN KEY (`id_sequence_next`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_dependance_sequence_as_module_sequencage_prev` FOREIGN KEY (`id_sequence_prev`) REFERENCES `MAQUETTE_module_sequence` (`id_module_sequence`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `MAQUETTE_learning_unit`
--
ALTER TABLE `MAQUETTE_learning_unit`
  ADD CONSTRAINT `FK_learning_unit_as_promo` FOREIGN KEY (`id_promo`) REFERENCES `LNM_promo` (`id_promo`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `MAQUETTE_module`
--
ALTER TABLE `MAQUETTE_module`
  ADD CONSTRAINT `FK_module_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`),
  ADD CONSTRAINT `FK_module_as_etat_module` FOREIGN KEY (`id_etat_module`) REFERENCES `INFO_etat_module` (`id_etat_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre` (`id_semestre`);

--
-- Contraintes pour la table `MAQUETTE_module_as_learning_unit`
--
ALTER TABLE `MAQUETTE_module_as_learning_unit`
  ADD CONSTRAINT `FK_module_as_learning_unit_as_learning_unit` FOREIGN KEY (`id_learning_unit`) REFERENCES `MAQUETTE_learning_unit` (`id_learning_unit`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_as_learning_unit_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `MAQUETTE_module_sequencage`
--
ALTER TABLE `MAQUETTE_module_sequencage`
  ADD CONSTRAINT `FK_module_sequencage_as_enseignant` FOREIGN KEY (`id_responsable`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_groupe_type` FOREIGN KEY (`id_groupe_type`) REFERENCES `LNM_groupe_type` (`id_groupe_type`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_intervenant_principal` FOREIGN KEY (`intervenant_principal`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_module_sequencage_as_seanceType` FOREIGN KEY (`id_seance_type`) REFERENCES `LNM_seanceType` (`id_seance_type`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Contraintes pour la table `MAQUETTE_module_sequence`
--
ALTER TABLE `MAQUETTE_module_sequence`
  ADD CONSTRAINT `FK_module_sequence_as_module_sequencage` FOREIGN KEY (`id_module_sequencage`) REFERENCES `MAQUETTE_module_sequencage` (`id_module_sequencage`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Contraintes pour la table `VIEW_parameters_of_views`
--
ALTER TABLE `VIEW_parameters_of_views`
  ADD CONSTRAINT `FK_parameters_of_views_as_discipline` FOREIGN KEY (`id_discipline`) REFERENCES `MAQUETTE_discipline` (`id_discipline`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_enseignant` FOREIGN KEY (`id_enseignant`) REFERENCES `LNM_enseignant` (`id_enseignant`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_filiere` FOREIGN KEY (`id_filiere`) REFERENCES `LNM_filiere` (`id_filiere`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_module` FOREIGN KEY (`id_module`) REFERENCES `MAQUETTE_module` (`id_module`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_semestre` FOREIGN KEY (`id_semestre`) REFERENCES `LNM_semestre` (`id_semestre`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `FK_parameters_of_views_as_status` FOREIGN KEY (`id_statut`) REFERENCES `LNM_statut` (`id_statut`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
