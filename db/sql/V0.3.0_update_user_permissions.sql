-- La responsabilité "conteneur"
CREATE TABLE LNM_responsabilites (
    id_responsabilites          INT PRIMARY KEY AUTO_INCREMENT,
    id_enseignant               INT NOT NULL,
    type_objet                  VARCHAR(50) NOT NULL,  -- 'stage', 'semestre', 'filiere', 'all'
    FOREIGN KEY (id_enseignant) REFERENCES LNM_enseignant(id_enseignant)
);

-- Les dimensions du scope, une par ligne
CREATE TABLE LNM_responsabilite_dimensions (
    id_responsabilite_dimensions          INT PRIMARY KEY AUTO_INCREMENT,
    id_responsabilite                     INT NOT NULL,
    dimension                             VARCHAR(50) NOT NULL,   -- 'filiere', 'niveau', 'semestre', ...
    valeur                                VARCHAR(100) NOT NULL,  -- 'IDU', 'FI4', 'S8', ...
    FOREIGN KEY (id_responsabilite) REFERENCES LNM_responsabilites(id_responsabilites) ON DELETE CASCADE,
    UNIQUE KEY unique_dim (id_responsabilite, dimension)
);