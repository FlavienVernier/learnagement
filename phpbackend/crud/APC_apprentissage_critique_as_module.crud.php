<?php

function selectModulesOfAllAPC($conn)
{
    $sql = "SELECT 
                `id_apprentissage_critique`,
                `MAQUETTE_module`.`id_module`,
                `MAQUETTE_module`.`code_module`,
                `MAQUETTE_module`.`nom`,
                `MAQUETTE_module`.`id_responsable`
            FROM `APC_apprentissage_critique_as_module`
            JOIN `MAQUETTE_module` ON `APC_apprentissage_critique_as_module`.`id_module` = `MAQUETTE_module`.`id_module`;";

    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}

function selectAPCbyIdModule($conn, $id_module){
    $sql = "SELECT 
                `APC_apprentissage_critique_as_module`.`id_apprentissage_critique`,
                `APC_apprentissage_critique`.`libelle_apprentissage`
            FROM `APC_apprentissage_critique_as_module`
            JOIN `APC_apprentissage_critique` ON `APC_apprentissage_critique_as_module`.`id_apprentissage_critique` = `APC_apprentissage_critique`.`id_apprentissage_critique`
            WHERE `APC_apprentissage_critique_as_module`.`id_module` = $id_module;";

    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}