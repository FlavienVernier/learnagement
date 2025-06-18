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


function listAPC_evaluationApprentissageCritiqueByStudentId($conn, $id_etudiant){
    $sql = "SELECT eval.id_etudiant, 
                   eval.evaluation, 
                   ac.libelle_apprentissage, 
                   niveau.libelle_niveau, 
                   competence.libelle_competence, 
                   competence.id_competence 
            FROM ETU_competence_evaluation as eval 
                INNER JOIN APC_apprentissage_critique as ac ON eval.id_apprentissage_critique=ac.id_apprentissage_critique 
                INNER JOIN APC_niveau as niveau ON ac.id_niveau=niveau.id_niveau 
                INNER JOIN APC_competence as competence ON niveau.id_competence=competence.id_competence 
            WHERE eval.id_etudiant = $id_etudiant;";

    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}