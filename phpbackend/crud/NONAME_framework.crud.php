<?php

function NONAME_framework_explicit_secondary_key($conn, $table) {
    $sql = "SELECT *
            FROM ExplicitSecondaryKs_" . $table;
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function NONAME_framework_explicit_secondary_key_by_PK($conn, $pk) {
   $secondaryKs = NONAME_framework_PKs($conn);
   $table_key = array_search($pk, array_column($secondaryKs, 'COLUMN_NAME'));
   $table = $secondaryKs[$table_key]['TABLE_NAME'];
   return NONAME_framework_explicit_secondary_key($conn, $table);
}
function NONAME_framework_PKs($conn) {
    $sql = "SELECT TABLE_NAME, COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'learnagement' AND COLUMN_KEY = 'PRI';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}