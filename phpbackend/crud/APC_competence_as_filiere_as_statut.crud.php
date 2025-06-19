<?php
function selectCompetenceByNomFiliere($conn, $nom_filiere){
    $sql = "SELECT
            `APC_competence`.`id_competence` AS `id_competence`,
            `APC_competence`.`code_competence` AS `code_competence`,
            `APC_competence`.`libelle_competence` AS `libelle_competence`,
            `APC_competence`.`description` AS `description_competence`
            FROM `APC_competence_as_filiere_as_statut`
            JOIN `APC_competence` ON `APC_competence_as_filiere_as_statut`.`id_competence` = `APC_competence`.`id_competence`
            JOIN `LNM_filiere` ON `APC_competence_as_filiere_as_statut`.`id_filiere` = `LNM_filiere`.`id_filiere`
            WHERE `nom_filiere` = '$nom_filiere';";

    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}
