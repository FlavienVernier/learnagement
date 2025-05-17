<?php

function selectAPCbyIdComp($conn, $id_competence){
    $sql = "SELECT 
                `APC_niveau`.`id_competence`,
                `APC_niveau`.`niveau`,
                `APC_apprentissage_critique`.`id_apprentissage_critique`,
                `APC_apprentissage_critique`.`libelle_apprentissage`
            FROM `APC_apprentissage_critique`
            JOIN `APC_niveau` ON `APC_apprentissage_critique`.`id_niveau` = `APC_niveau`.`id_niveau`
            WHERE `APC_niveau`.`id_competence` = $id_competence;";

    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}


