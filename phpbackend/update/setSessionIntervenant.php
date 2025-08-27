<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/CLASS_session.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

if(isset($_POST["id_session"])
    && isset($_POST["id_enseignant"])){
    $id_session = $_POST["id_session"];
    $id_enseignant = $_POST["id_enseignant"];

    $rs = setCLASS_session_enseignant($conn, $id_session,  $id_enseignant);
    echo json_encode($rs);
}else{
    echo json_encode("Error at least one required data undefined");
}

