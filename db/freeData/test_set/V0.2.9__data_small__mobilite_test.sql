-- =============================================================================
-- Données de test — Mobilité internationale (années N et N+1)
-- Hash password commun : $2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm
--
-- 6 filières couvertes (toutes les filières réelles) :
--   Info (3) : IDU3=promo5  / IDU4=promo15   — Annecy
--   Meca (4) : MM3=promo17  / MM4=promo18    — Annecy
--   Sys  (5) : SNI3=promo20 / SNI4=promo21   — Annecy
--   Bat  (6) : BAT3=promo23 / BAT4=promo24   — Chambéry
--   Eco  (7) : EIT3=promo26 / EIT4=promo27   — Chambéry
--   Mat  (8) : MC3=promo29  / MC4=promo30    — Chambéry
--
-- Passage N→N+1 : UPDATE LNM_etudiant SET id_promo = <promo_annee4>
--                 WHERE id_etudiant IN (<ids annee=3>)
-- Après cet UPDATE, les anciens annee=3 soumettent leurs vœux (section N+1).
-- =============================================================================

SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================

-- =============================================================================
-- CRÉATION DES PROMOTIONS MANQUANTES (Statuts FISA, FISEA, FISECP pour annee=4)
-- =============================================================================
INSERT INTO LNM_promo (id_promo, id_filiere, id_statut, annee, parcour, site, nbGroupeCM, nbGroupeTD, nbGroupeTP, id_responsable) VALUES 
(1015, 3, 2, 4, NULL, 'Annecy', 1, 1, 2, NULL), (2015, 3, 3, 4, NULL, 'Annecy', 1, 1, 2, NULL), (3015, 3, 4, 4, NULL, 'Annecy', 1, 1, 2, NULL),
(1018, 4, 2, 4, NULL, 'Annecy', 1, 1, 2, NULL), (2018, 4, 3, 4, NULL, 'Annecy', 1, 1, 2, NULL), (3018, 4, 4, 4, NULL, 'Annecy', 1, 1, 2, NULL),
(1021, 5, 2, 4, NULL, 'Annecy', 1, 1, 2, NULL), (2021, 5, 3, 4, NULL, 'Annecy', 1, 1, 2, NULL), (3021, 5, 4, 4, NULL, 'Annecy', 1, 1, 2, NULL),
(1024, 6, 2, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (2024, 6, 3, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (3024, 6, 4, 4, NULL, 'Chambéry', 1, 1, 2, NULL),
(1027, 7, 2, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (2027, 7, 3, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (3027, 7, 4, 4, NULL, 'Chambéry', 1, 1, 2, NULL),
(1030, 8, 2, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (2030, 8, 3, 4, NULL, 'Chambéry', 1, 1, 2, NULL), (3030, 8, 4, 4, NULL, 'Chambéry', 1, 1, 2, NULL);

-- ÉTUDIANTS — ANNÉE N (annee=4, éligibles à la mobilité)
-- =============================================================================

-- IDU4 — Info, promo 15, Annecy (5 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9501, 'Durand',    'Camille',   'camille.durand@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 15, NULL, FALSE, 19),
(9502, 'Moreau',    'Lucas',     'lucas.moreau@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1015, NULL, TRUE, 16),
(9503, 'Bernard',   'Lea',       'lea.bernard@mob-test.local',       '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2015, NULL, FALSE, 13),
(9504, 'Petit',     'Antoine',   'antoine.petit@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 3015, NULL, FALSE, 11),
(9505, 'Martin',    'Sophie',    'sophie.martin@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 15, NULL, TRUE, 10);

-- MM4 — Meca, promo 18, Annecy (4 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9511, 'Rousseau',  'Maxime',    'maxime.rousseau@mob-test.local',   '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 18, NULL, TRUE, 18),
(9512, 'Garcia',    'Julie',     'julie.garcia@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1018, NULL, FALSE, 15),
(9513, 'Lefebvre',  'Thomas',    'thomas.lefebvre@mob-test.local',   '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2018, NULL, FALSE, 12),
(9514, 'Simon',     'Clara',     'clara.simon@mob-test.local',       '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 3018, NULL, TRUE, 10);

-- SNI4 — Sys, promo 21, Annecy (4 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9521, 'Laurent',   'Emma',      'emma.laurent@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 21, NULL, FALSE, 17),
(9522, 'Thomas',    'Nathan',    'nathan.thomas@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1021, NULL, TRUE, 14),
(9523, 'Robert',    'Ines',      'ines.robert@mob-test.local',       '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2021, NULL, FALSE, 11),
(9524, 'Richard',   'Alexis',    'alexis.richard@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 3021, NULL, TRUE, 10);

-- BAT4 — Bat, promo 24, Chambéry (4 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9531, 'Dupont',    'Marion',    'marion.dupont@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 24, NULL, FALSE, 18),
(9532, 'Leroy',     'Florian',   'florian.leroy@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1024, NULL, FALSE, 14),
(9533, 'Morel',     'Pauline',   'pauline.morel@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2024, NULL, TRUE, 11),
(9534, 'Fournier',  'Kevin',     'kevin.fournier@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 3024, NULL, FALSE, 10);

-- EIT4 — Eco, promo 27, Chambéry (4 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9541, 'Mercier',   'Lucie',     'lucie.mercier@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 27, NULL, FALSE, 17),
(9542, 'Leroux',    'Remy',      'remy.leroux@mob-test.local',       '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1027, NULL, FALSE, 14),
(9543, 'David',     'Celine',    'celine.david@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2027, NULL, FALSE, 11),
(9544, 'Bertrand',  'Victor',    'victor.bertrand@mob-test.local',   '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 3027, NULL, TRUE, 10);

-- MC4 — Mat, promo 30, Chambéry (3 étudiants)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9551, 'Nguyen',    'Alice',     'alice.nguyen@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 30, NULL, FALSE, 16),
(9552, 'Henry',     'Pierre',    'pierre.henry@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 1030, NULL, FALSE, 12),
(9553, 'Denis',     'Margot',    'margot.denis@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 2030, NULL, TRUE, 10);

-- =============================================================================
-- ÉTUDIANTS — ANNÉE N+1 (annee=3, passeront en annee=4 l'année suivante)
-- mobility_note NULL : les notes de mobilité ne sont pas encore calculées
-- =============================================================================

-- IDU3 → IDU4 (promo 5 → 15) : 4 étudiants (Wait, 3 etudiants: 9561-9563)
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9561, 'Girard',    'Manon',     'manon.girard@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 5, NULL, FALSE, NULL),
(9562, 'Bonnet',    'Quentin',   'quentin.bonnet@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 5, NULL, TRUE, NULL),
(9563, 'Vincent',   'Chloe',     'chloe.vincent@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 5, NULL, FALSE, NULL);

-- MM3 → MM4 (promo 17 → 18) : 3 étudiants
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9571, 'Lecomte',   'Laura',     'laura.lecomte@mob-test.local',     '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 17, NULL, TRUE, NULL),
(9572, 'Fontaine',  'Julien',    'julien.fontaine@mob-test.local',   '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 17, NULL, FALSE, NULL),
(9573, 'Chevalier', 'Sarah',     'sarah.chevalier@mob-test.local',   '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 17, NULL, FALSE, NULL);

-- SNI3 → SNI4 (promo 20 → 21) : 2 étudiants
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9581, 'Perrin',    'Elise',     'elise.perrin@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 20, NULL, FALSE, NULL),
(9582, 'Colin',     'Baptiste',  'baptiste.colin@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 20, NULL, FALSE, NULL);

-- BAT3 → BAT4 (promo 23 → 24) : 3 étudiants
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9591, 'Marchand',  'Elisa',     'elisa.marchand@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 23, NULL, TRUE, NULL),
(9592, 'Blanc',     'Arthur',    'arthur.blanc@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 23, NULL, TRUE, NULL),
(9593, 'Guerin',    'Lucie',     'lucie.guerin@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 23, NULL, FALSE, NULL);

-- EIT3 → EIT4 (promo 26 → 27) : 2 étudiants
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9601, 'Picard',    'Camille',   'camille.picard@mob-test.local',    '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 26, NULL, FALSE, NULL),
(9602, 'Muller',    'Noah',      'noah.muller@mob-test.local',       '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 26, NULL, FALSE, NULL);

-- MC3 → MC4 (promo 29 → 30) : 2 étudiants
INSERT INTO LNM_etudiant (id_etudiant, nom, prenom, mail, password, password_updated, id_promo, id_origine, mobility_completed, mobility_note) VALUES
(9611, 'Renard',    'Adele',     'adele.renard@mob-test.local',      '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 29, NULL, FALSE, NULL),
(9612, 'Faure',     'Theo',      'theo.faure@mob-test.local',        '$2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm', 0, 29, NULL, FALSE, NULL);

-- =============================================================================
-- VŒUX — ANNÉE N (étudiants en annee=4)
-- Règle : submission_date IS NOT NULL uniquement si l'étudiant a >= 5 voeux.
-- 1 étudiant brouillon par filière (< 5 voeux, submission_date NULL).
-- =============================================================================

-- --- IDU4 (promo 15, S8) ---
-- Camille Durand (9501, note=19) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9501,  1, 8, 1, '2026-04-02 09:00:00'),
(9501, 11, 9, 2, '2026-04-02 09:00:00'),
(9501,  3, 8, 3, '2026-04-02 09:00:00'),
(9501, 13, 9, 4, '2026-04-02 09:00:00'),
(9501, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-02 09:00:00');

-- Lucas Moreau (9502, note=16) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9502,  1, 9, 1, '2026-04-03 10:00:00'),
(9502, 34, 8, 2, '2026-04-03 10:00:00'),
(9502, 11, 9, 3, '2026-04-03 10:00:00'),
(9502,  3, 8, 4, '2026-04-03 10:00:00'),
(9502, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-03 10:00:00');

-- Lea Bernard (9503, note=13) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9503,  1, 8, 1, '2026-04-01 14:00:00'),
(9503, 11, 9, 2, '2026-04-01 14:00:00'),
(9503,  3, 8, 3, '2026-04-01 14:00:00'),
(9503, 45, 9, 4, '2026-04-01 14:00:00'),
(9503, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-01 14:00:00');

-- Antoine Petit (9504, note=11) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9504,  1, 9, 1, '2026-04-04 11:00:00'),
(9504, 45, 8, 2, '2026-04-04 11:00:00'),
(9504, 13, 9, 3, '2026-04-04 11:00:00'),
(9504, 34, 8, 4, '2026-04-04 11:00:00'),
(9504, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-04 11:00:00');

-- Sophie Martin (9505, note=10) — brouillon, 3 voeux, non soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9505,  1, 8, 1, NULL),
(9505, 11, 9, 2, NULL),
(9505,  3, 8, 3, NULL);

-- --- MM4 (promo 18, S8) ---
-- Maxime Rousseau (9511, note=18) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9511,  8, 9, 1, '2026-04-01 09:30:00'),
(9511, 10, 8, 2, '2026-04-01 09:30:00'),
(9511,  9, 9, 3, '2026-04-01 09:30:00'),
(9511,  1, 8, 4, '2026-04-01 09:30:00'),
(9511, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-01 09:30:00');

-- Julie Garcia (9512, note=15) — 5 voeux soumis (CHOIX MIXTES S8/S9)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9512,  8, 8, 1, '2026-04-02 10:00:00'),
(9512, 10, 9, 2, '2026-04-02 10:00:00'),
(9512,  9, 8, 3, '2026-04-02 10:00:00'),
(9512,  1, 9, 4, '2026-04-02 10:00:00'),
(9512, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-02 10:00:00');

-- Thomas Lefebvre (9513, note=12) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9513,  8, 9, 1, '2026-04-05 15:00:00'),
(9513, 10, 8, 2, '2026-04-05 15:00:00'),
(9513,  9, 9, 3, '2026-04-05 15:00:00'),
(9513,  1, 8, 4, '2026-04-05 15:00:00'),
(9513, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-05 15:00:00');

-- Clara Simon (9514, note=10) — brouillon
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9514,  8, 8, 1, NULL),
(9514, 10, 9, 2, NULL);

-- --- SNI4 (promo 21, S8) ---
-- Emma Laurent (9521, note=17) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9521, 11, 8, 1, '2026-04-02 10:00:00'),
(9521, 45, 9, 2, '2026-04-02 10:00:00'),
(9521, 68, 8, 3, '2026-04-02 10:00:00'),
(9521, 30, 9, 4, '2026-04-02 10:00:00'),
(9521, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-02 10:00:00');

-- Nathan Thomas (9522, note=14) — 5 voeux soumis (CHOIX MIXTES S8/S9)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9522, 45, 9, 1, '2026-04-04 14:00:00'),
(9522, 11, 8, 2, '2026-04-04 14:00:00'),
(9522, 68, 9, 3, '2026-04-04 14:00:00'),
(9522, 30, 8, 4, '2026-04-04 14:00:00'),
(9522, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-04 14:00:00');

-- Ines Robert (9523, note=11) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9523, 68, 8, 1, '2026-04-06 16:00:00'),
(9523, 45, 9, 2, '2026-04-06 16:00:00'),
(9523, 11, 8, 3, '2026-04-06 16:00:00'),
(9523, 30, 9, 4, '2026-04-06 16:00:00'),
(9523, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-06 16:00:00');

-- Alexis Richard (9524, note=10) — brouillon
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9524, 45, 9, 1, NULL),
(9524, 11, 8, 2, NULL);

-- --- BAT4 (promo 24, S8) ---
-- Marion Dupont (9531, note=18) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9531, 35, 9, 1, '2026-04-01 11:00:00'),
(9531, 37, 8, 2, '2026-04-01 11:00:00'),
(9531, 12, 9, 3, '2026-04-01 11:00:00'),
(9531, 78, 8, 4, '2026-04-01 11:00:00'),
(9531, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-01 11:00:00');

-- Florian Leroy (9532, note=14) — 5 voeux soumis (CHOIX MIXTES S8/S9)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9532, 37, 8, 1, '2026-04-03 13:00:00'),
(9532, 35, 9, 2, '2026-04-03 13:00:00'),
(9532, 12, 8, 3, '2026-04-03 13:00:00'),
(9532, 78, 9, 4, '2026-04-03 13:00:00'),
(9532, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-03 13:00:00');

-- Pauline Morel (9533, note=11) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9533, 12, 9, 1, '2026-04-05 09:00:00'),
(9533, 35, 8, 2, '2026-04-05 09:00:00'),
(9533, 37, 9, 3, '2026-04-05 09:00:00'),
(9533, 78, 8, 4, '2026-04-05 09:00:00'),
(9533, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-05 09:00:00');

-- Kevin Fournier (9534, note=10) — brouillon
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9534, 35, 8, 1, NULL),
(9534, 37, 9, 2, NULL),
(9534, 12, 8, 3, NULL);

-- --- EIT4 (promo 27, S8) ---
-- Lucie Mercier (9541, note=17) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9541, 22, 9, 1, '2026-04-02 09:00:00'),
(9541, 50, 8, 2, '2026-04-02 09:00:00'),
(9541, 26, 9, 3, '2026-04-02 09:00:00'),
(9541, 43, 8, 4, '2026-04-02 09:00:00'),
(9541, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-02 09:00:00');

-- Remy Leroux (9542, note=14) — 5 voeux soumis (CHOIX MIXTES S8/S9)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9542, 50, 8, 1, '2026-04-04 11:00:00'),
(9542, 22, 9, 2, '2026-04-04 11:00:00'),
(9542, 43, 8, 3, '2026-04-04 11:00:00'),
(9542, 26, 9, 4, '2026-04-04 11:00:00'),
(9542, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-04 11:00:00');

-- Celine David (9543, note=11) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9543, 43, 9, 1, '2026-04-06 15:00:00'),
(9543, 50, 8, 2, '2026-04-06 15:00:00'),
(9543, 22, 9, 3, '2026-04-06 15:00:00'),
(9543, 26, 8, 4, '2026-04-06 15:00:00'),
(9543, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-06 15:00:00');

-- Victor Bertrand (9544, note=10) — brouillon
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9544, 22, 8, 1, NULL),
(9544, 50, 9, 2, NULL);

-- --- MC4 (promo 30, S8) ---
-- Alice Nguyen (9551, note=16) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9551, 85, 8, 1, '2026-04-01 10:00:00'),
(9551, 32, 9, 2, '2026-04-01 10:00:00'),
(9551, 54, 8, 3, '2026-04-01 10:00:00'),
(9551, 46, 9, 4, '2026-04-01 10:00:00'),
(9551, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 8, 5, '2026-04-01 10:00:00');

-- Pierre Henry (9552, note=12) — 5 voeux soumis
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9552, 32, 9, 1, '2026-04-03 14:00:00'),
(9552, 85, 8, 2, '2026-04-03 14:00:00'),
(9552, 54, 9, 3, '2026-04-03 14:00:00'),
(9552, 46, 8, 4, '2026-04-03 14:00:00'),
(9552, (SELECT id_partner_university FROM MOB_partner_university WHERE code = 'MOB_STAGE'), 9, 5, '2026-04-03 14:00:00');

-- Margot Denis (9553, note=10) — brouillon
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9553, 85, 8, 1, NULL),
(9553, 32, 9, 2, NULL);

-- Les updates de passage de promo ont été retirés de ce script d'initialisation.
-- Ils restent en année 3 pour l'instant.


-- =============================================================================
-- VŒUX — ANNÉE N+1 (étudiants promus, soumettent leurs voeux après le passage)
-- =============================================================================

-- IDU3→IDU4 : Manon Girard (9561), Quentin Bonnet (9562), Chloe Vincent (9563)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9561,  1, 8, 1, NULL), (9561, 11, 8, 2, NULL), (9561,  3, 8, 3, NULL),
(9562,  1, 9, 1, NULL), (9562, 34, 9, 2, NULL), (9562, 45, 9, 3, NULL),
(9563, 11, 8, 1, NULL), (9563,  3, 8, 2, NULL);

-- MM3→MM4 : Laura Lecomte (9571), Julien Fontaine (9572), Sarah Chevalier (9573)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9571,  8, 9, 1, NULL), (9571, 10, 9, 2, NULL), (9571,  9, 9, 3, NULL),
(9572,  8, 8, 1, NULL), (9572,  1, 8, 2, NULL), (9572, 10, 8, 3, NULL),
(9573, 10, 9, 1, NULL), (9573,  9, 9, 2, NULL);

-- SNI3→SNI4 : Elise Perrin (9581), Baptiste Colin (9582)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9581, 45, 8, 1, NULL), (9581, 11, 8, 2, NULL), (9581, 68, 8, 3, NULL),
(9582, 68, 9, 1, NULL), (9582, 45, 9, 2, NULL);

-- BAT3→BAT4 : Elisa Marchand (9591), Arthur Blanc (9592), Lucie Guerin (9593)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9591, 35, 8, 1, NULL), (9591, 37, 8, 2, NULL), (9591, 12, 8, 3, NULL),
(9592, 37, 9, 1, NULL), (9592, 35, 9, 2, NULL), (9592, 78, 9, 3, NULL),
(9593, 12, 8, 1, NULL), (9593, 78, 8, 2, NULL);

-- EIT3→EIT4 : Camille Picard (9601), Noah Muller (9602)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9601, 22, 9, 1, NULL), (9601, 50, 9, 2, NULL), (9601, 43, 9, 3, NULL),
(9602, 50, 8, 1, NULL), (9602, 26, 8, 2, NULL);

-- MC3→MC4 : Adele Renard (9611), Theo Faure (9612)
INSERT INTO MOB_wishes (id_etudiant, id_partner_university, id_semestre, priority, submission_date) VALUES
(9611, 85, 9, 1, NULL), (9611, 32, 9, 2, NULL), (9611, 54, 9, 3, NULL),
(9612, 32, 8, 1, NULL), (9612, 46, 8, 2, NULL);

SET FOREIGN_KEY_CHECKS = 1;
