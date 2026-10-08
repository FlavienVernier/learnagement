INSERT INTO `LNM_enseignant_responsabilites` (`id_enseignant_responsabilites`, `id_enseignant`, `type_objet`)
VALUES (1, '14', 'stage'),
       (2, '6', 'stage');

INSERT INTO `LNM_enseignant_responsabilite_dimensions` (`id_enseignant_responsabilite_dimensions`, `id_enseignant_responsabilites`, `dimension`, `valeur`)
VALUES (NULL, '1', 'filiere', 'IDU'),
       (NULL, '1', 'annee', '4'),
       (NULL, '2', 'filiere', 'SEA'),
       (NULL, '2', 'annee', '4');