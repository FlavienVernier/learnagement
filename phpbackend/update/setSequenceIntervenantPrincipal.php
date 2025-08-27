<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/MAQUETTE_module_sequence.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

if(isset($_POST["id_module_sequence"])
    && isset($_POST["id_intervenant_principal"])){
    $id_module_sequence = $_POST["id_module_sequence"];
    $id_intervenant_principal = $_POST["id_intervenant_principal"];

    $rs = setMAQUETE_module_sequence_intervenant_principal($conn, $id_module_sequence,  $id_intervenant_principal);
    echo json_encode($rs);
}else{
    echo json_encode("Error at least one required data undefined");
}

