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
    $sql = "SELECT ETU_classical_evaluation.evaluation, concat(LNM_etudiant.nom, ' ', LNM_etudiant.prenom) as etudiant, MAQUETTE_module.nom,  ETU_classical_evaluation.date, concat(LNM_filiere.nom_filiere, '_', LNM_promo.annee, '_', LNM_statut.nom_statut) AS 'promo'
            FROM ETU_classical_evaluation
                 JOIN MAQUETTE_module ON ETU_classical_evaluation.id_module = MAQUETTE_module.id_module 
                 JOIN LNM_enseignant ON MAQUETTE_module.id_responsable = LNM_enseignant.id_enseignant
                 JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = ETU_classical_evaluation.id_etudiant
                 JOIN LNM_promo ON LNM_etudiant.id_promo = LNM_promo.id_promo
                 JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                 JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
            WHERE LNM_enseignant.id_enseignant='$idEnseignant'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}