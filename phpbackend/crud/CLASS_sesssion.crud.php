<?php
function listCLASS_sessionByStudentId($conn, $id_etudiant){
    $sql = "SELECT etu.nom, session.schedule as date_prevue, promo.annee, sequencage.duree_h, module.nom 
                FROM CLASS_session as session 
                JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe 
                JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo 
                JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo 
                JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence 
                JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage 
                JOIN MAQUETTE_module as module ON sequencage.id_module = module.id_module 
                WHERE session.schedule < CURRENT_DATE and etu.id_etudiant = '$id_etudiant';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

