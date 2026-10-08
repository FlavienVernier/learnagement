-- La responsabilité "conteneur"
CREATE TABLE LNM_responsabilite (
    id_responsabilite          INT PRIMARY KEY AUTO_INCREMENT,
    type_objet                  VARCHAR(50) NOT NULL,  -- 'stage', 'semestre', 'filiere', 'all'
    UNIQUE KEY SECONDARY (type_objet)
);

INSERT INTO LNM_responsabilite (type_objet)
    SELECT DISTINCT type_objet FROM LNM_enseignant_responsabilites;

ALTER TABLE `LNM_enseignant_responsabilites` CHANGE `type_objet` `id_responsabilite` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL;

UPDATE LNM_enseignant_responsabilites
JOIN LNM_responsabilite ON LNM_responsabilite.type_objet = LNM_enseignant_responsabilites.id_responsabilite
SET LNM_enseignant_responsabilites.id_responsabilite = LNM_responsabilite.id_responsabilite;

ALTER TABLE `LNM_enseignant_responsabilites` CHANGE `id_responsabilite` `id_responsabilite` INT NOT NULL;
ALTER TABLE `LNM_enseignant_responsabilites` ADD CONSTRAINT FOREIGN KEY (`id_responsabilite`) REFERENCES `LNM_responsabilite` (`id_responsabilite`) ON DELETE RESTRICT ON UPDATE RESTRICT;
