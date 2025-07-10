<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json; charset=utf-8");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/NONAME_framework.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

if (isset($_POST['table'])){
    $table = $_POST['table'];
    $rs = NONAME_framework_explicit_secondary_key($conn, $table);

    echo json_encode($rs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}else{
    echo json_encode("Error table undefined");
}

