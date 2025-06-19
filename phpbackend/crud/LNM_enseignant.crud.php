<?php
  //include('./function_acction_allowed.php');


function listLNM_enseignant($conn)
{
    $sql = "SELECT * FROM `LNM_enseignant`";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
