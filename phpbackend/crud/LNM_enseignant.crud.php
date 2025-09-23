<?php
  //include('./function_acction_allowed.php');


function listLNM_enseignant($conn)
{
    $sql = "SELECT * FROM `LNM_enseignant`";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listLNM_enseignant_responsabilite($conn)
{
    $sql = "SELECT 
        CONCAT(`LNM_enseignant`.`prenom`,' ',`LNM_enseignant`.`nom`) AS `responsable`,
        COUNT(`MAQUETTE_module`.`id_module`) AS `responsabilite`,
        GROUP_CONCAT(distinct `MAQUETTE_module`.`code_module` separator ', ') AS `modules` 
        FROM `LNM_enseignant` 
        JOIN `MAQUETTE_module` ON `MAQUETTE_module`.`id_responsable` = `LNM_enseignant`.`id_enseignant` 
        GROUP BY `LNM_enseignant`.`nom`, `LNM_enseignant`.`prenom`;";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function checkLNM_enseignant_sans_cours($conn)
{
    $sql = "SELECT `prenom`, `nom`, `mail`, `statut`, `composante`
            FROM LNM_enseignant
            WHERE LNM_enseignant.id_enseignant 
                      NOT IN (  SELECT CLASS_session.id_enseignant 
                                FROM CLASS_session 
                                WHERE CLASS_session.id_enseignant IS NOT null);";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}