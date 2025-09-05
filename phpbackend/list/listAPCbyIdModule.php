<?php

header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/APC_apprentissage_critique_as_module.crud.php");

if(isset($_POST["id_module"])){
    $id_module = $_POST["id_module"];
    $apc = selectAPCbyIdModule($conn, $id_module);

    echo json_encode($apc, JSON_NUMERIC_CHECK);
}

