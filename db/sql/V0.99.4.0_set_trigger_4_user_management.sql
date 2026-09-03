
DELIMITER $$
CREATE TRIGGER trg_enseignant_id
BEFORE INSERT ON LNM_enseignant
FOR EACH ROW
BEGIN
    INSERT INTO LNM_user_id_generator () VALUES ();
    SET NEW.id_utilisateur = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_etudiant_id
BEFORE INSERT ON LNM_etudiant
FOR EACH ROW
BEGIN
    INSERT INTO LNM_user_id_generator () VALUES ();
    SET NEW.id_utilisateur = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_administratif_id
BEFORE INSERT ON LNM_administratif
FOR EACH ROW
BEGIN
    INSERT INTO LNM_user_id_generator () VALUES ();
    SET NEW.id_utilisateur = LAST_INSERT_ID();
END$$
DELIMITER ;