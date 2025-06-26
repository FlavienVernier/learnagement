<?php
function listCLASS_absence_anonymous($conn){
    $sql = "SELECT abs.id_session, abs.id_etudiant, id_promo, 
                    YEAR(sess.schedule) as 'annee' 
            FROM CLASS_absence as abs 
            INNER JOIN LNM_etudiant as etu ON abs.id_etudiant=etu.id_etudiant 
            INNER JOIN CLASS_session as sess ON abs.id_session=sess.id_session;";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

