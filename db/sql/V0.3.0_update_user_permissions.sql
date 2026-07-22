-- La responsabilité "conteneur"
CREATE TABLE LNM_enseignant_responsabilites (
    id_enseignant_responsabilites          INT PRIMARY KEY AUTO_INCREMENT,
    id_enseignant               INT NOT NULL,
    type_objet                  VARCHAR(50) NOT NULL,  -- 'stage', 'semestre', 'filiere', 'all'
    FOREIGN KEY (id_enseignant) REFERENCES LNM_enseignant(id_enseignant),
    UNIQUE KEY SECONDARY (id_enseignant, type_objet)
);

-- Les dimensions du scope, une par ligne
CREATE TABLE LNM_enseignant_responsabilite_dimensions (
    id_enseignant_responsabilite_dimensions          INT PRIMARY KEY AUTO_INCREMENT,
    id_enseignant_responsabilites                    INT NOT NULL,
    dimension                             VARCHAR(50) NOT NULL,   -- 'filiere', 'niveau', 'semestre', ...
    valeur                                VARCHAR(100) NOT NULL,  -- 'IDU', 'FI4', 'S8', ...
    FOREIGN KEY (id_enseignant_responsabilites) REFERENCES LNM_enseignant_responsabilites(id_enseignant_responsabilites) ON DELETE CASCADE,
    UNIQUE KEY SECONDARY (id_enseignant_responsabilites, dimension)
);
