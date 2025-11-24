<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/MAQUETTE_module.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

if(isset($_POST["id_module"])
    && isset($_POST["id_responsable"])){
    $id_module = $_POST["id_module"];
    $id_responsable = $_POST["id_responsable"];

    $rs = setMAQUETTE_moduleResponsable($conn, $id_module,  $id_responsable);
    echo json_encode($rs);
}else{
    echo json_encode("Error at least one required data undefined");
}

