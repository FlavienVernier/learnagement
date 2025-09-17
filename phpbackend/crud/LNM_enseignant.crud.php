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
        JOIN `MAQUETTE_module_as_learning_unit` ON `MAQUETTE_module_as_learning_unit`.`id_module` = `MAQUETTE_module`.`id_module`
        JOIN `MAQUETTE_learning_unit` ON `MAQUETTE_learning_unit`.`id_learning_unit` = `MAQUETTE_module_as_learning_unit`.`id_learning_unit`
        JOIN `LNM_promo` ON `MAQUETTE_learning_unit`.`id_promo` = `LNM_promo`.`id_promo`
        JOIN `LNM_statut` ON `LNM_statut`.`id_statut` = `LNM_promo`.`id_statut`
        JOIN `LNM_filiere` ON `LNM_filiere`.`id_filiere` = `LNM_promo`.`id_filiere`
        JOIN `LNM_semestre` ON `LNM_semestre`.`id_semestre` = `MAQUETTE_module`.`id_semestre`
        JOIN `MAQUETTE_discipline` ON `MAQUETTE_discipline`.`id_discipline` = `MAQUETTE_module`.`id_discipline`
        GROUP BY `LNM_enseignant`.`nom`, `LNM_enseignant`.`prenom`;";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}