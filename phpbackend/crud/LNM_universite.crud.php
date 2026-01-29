<?php
function listLNM_universite($conn){
    $sql = "SELECT LNM_universite.*, ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK, LNM_universite_as_promo.nombre_places 
            FROM LNM_universite
            JOIN LNM_universite_as_promo ON LNM_universite_as_promo.id_universite = LNM_universite.id_universite
            JOIN LNM_promo ON LNM_promo.id_promo = LNM_universite_as_promo.id_promo
            JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo;
        ";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

