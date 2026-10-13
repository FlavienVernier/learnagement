UPDATE LNM_administratif SET login = mail WHERE login IS NULL;
UPDATE LNM_enseignant    SET login = mail WHERE login IS NULL;
UPDATE LNM_etudiant      SET login = mail WHERE login IS NULL;