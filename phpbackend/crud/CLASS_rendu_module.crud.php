<?php
function listCLASS_renduByStudentId($conn, $id_etudiant){
    $sql = "SELECT rm.description, module.nom, ue.learning_unit_name, rm_etu.avancement
            FROM LNM_rendu_module as rm 
                JOIN LNM_rendu_module_as_etudiant as rm_etu ON rm_etu.id_rendu_module=rm.id_rendu_module 
                JOIN LNM_etudiant as etu ON etu.id_etudiant=rm_etu.id_etudiant 
                JOIN MAQUETTE_module_as_learning_unit as mue ON rm.id_module=mue.id_module 
                JOIN MAQUETTE_module as module ON mue.id_module=module.id_module 
                JOIN MAQUETTE_learning_unit as ue ON mue.id_learning_unit=ue.id_learning_unit 
            WHERE etu.id_etudiant = '$id_etudiant';";

    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

