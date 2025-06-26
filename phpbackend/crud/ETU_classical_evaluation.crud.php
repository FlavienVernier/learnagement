<?php

/*
 * return anonymous evaluations (without student info)
 */
function listETU_classical_evaluation_byIdModule($conn, $idModule){
    $sql = "SELECT evaluation, module.nom, date  
            FROM ETU_classical_evaluation as eval 
                JOIN MAQUETTE_module as module ON eval.id_module=module.id_module 
            WHERE eval.id_module='$idModule'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}


/*
 * return anonymous evaluations (without student info)
 */
function listETU_classical_average_evaluation_byIdModule($conn, $idModule){
    $sql = "SELECT AVG(evaluation)  as 'evaluation'
            FROM ETU_classical_evaluation as eval 
                JOIN MAQUETTE_module as module ON eval.id_module=module.id_module 
            WHERE eval.id_module='$idModule'
            GROUP BY eval.id_etudiant";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
function listETU_classical_evaluation_byIdEtudiant($conn, $idEtudiant){
    $sql = "SELECT evaluation, module.id_module, module.code_module, module.nom,  date  
            FROM ETU_classical_evaluation as eval 
                JOIN MAQUETTE_module as module ON eval.id_module=module.id_module 
            WHERE eval.id_etudiant='$idEtudiant'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}


function listETU_classical_evaluation_byIdEnseignant($conn, $idEnseignant){
    $sql = "SELECT evaluation, module.nom  
            FROM ETU_classical_evaluation as eval 
                JOIN MAQUETTE_module as module ON eval.id_module=module.id_module 
            WHERE ...";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}