<?php

function listLNM_statut($conn) {
     $sql = "SELECT * FROM `LNM_statut`";
     $res = mysqli_query($conn, $sql);
     $rs = rs_to_table($res);
     return $rs;
}

