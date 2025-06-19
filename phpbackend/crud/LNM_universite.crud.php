<?php
function listLNM_universite($conn){
    $sql = "SELECT * FROM `LNM_universite`";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

