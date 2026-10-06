INSERT INTO `LNM_role` (`id_role`, `role`)
VALUES (1, 'responsable_etudes'),
       (2, 'responsable_stages'),
       (3, 'relations_internationales');

INSERT INTO `LNM_administratif_as_role` (`id_administratif`, `id_role`)
VALUES ('1', '1'),
       ('2', '3');

INSERT INTO `LNM_enseignant_as_role` (`id_enseignant`, `id_role`)
VALUES ('6', '2');