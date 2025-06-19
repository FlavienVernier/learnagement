<?php
function listCLASS_absence_anonymous($conn){
    $sql = "SELECT abs.id_seance_to_be_affected_as_enseignant, abs.id_etudiant, id_promo, YEAR(sess.schedule) as 'annee' FROM CLASS_absence as abs INNER JOIN LNM_etudiant as etu ON abs.id_etudiant=etu.id_etudiant INNER JOIN CLASS_session_to_be_affected_as_enseignant as sess ON abs.id_seance_to_be_affected_as_enseignant=sess.id_seance_to_be_affected_as_enseignant;";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

