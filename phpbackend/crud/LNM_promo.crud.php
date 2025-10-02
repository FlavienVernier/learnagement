<?php

function listLNM_promo($conn) {
     $sql = "
        SELECT LNM_promo.`id_promo`, ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS promo
        FROM `LNM_promo`
        JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo;
     ";
     $res = mysqli_query($conn, $sql);
     $rs = rs_to_table($res);
     return $rs;
}

