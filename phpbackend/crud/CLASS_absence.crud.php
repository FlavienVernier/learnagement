<?php
function listCLASS_absenceByResponsableId($conn, $id){
    $sql = "SELECT concat(LNM_etudiant.prenom, ' ', LNM_etudiant.nom), concat(LNM_filiere.nom_filiere, '_', LNM_promo.annee, '_', LNM_statut.nom_statut), MAQUETTE_module.code_module, CLASS_session.schedule
            FROM `CLASS_absence` 
            JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
            JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
            JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
            JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
            JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
            JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
            JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
            WHERE MAQUETTE_module.id_responsable = '$id';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listCLASS_absenceByEnseignantId($conn, $id){
    $sql = "SELECT concat(LNM_etudiant.prenom, ' ', LNM_etudiant.nom), concat(LNM_filiere.nom_filiere, '_', LNM_promo.annee, '_', LNM_statut.nom_statut), MAQUETTE_module.code_module, CLASS_session.schedule
            FROM `CLASS_absence` 
            JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
            JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
            JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
            JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
            JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
            JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
            JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
            WHERE CLASS_session.id_enseignant = '$id';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
function listCLASS_absenceByStudentId($conn, $id){
    $sql = "...";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}


function listCLASS_absence($conn, $id){
    $sql = "...";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}