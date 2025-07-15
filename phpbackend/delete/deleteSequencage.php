<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/MAQUETTE_module_sequencage.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

/*if (isset($_POST['module'])
    && isset($_POST['nombre'])
    && isset($_POST['type'])
    && isset($_POST['duree_h'])
    && isset($_POST['groupe_type'])
    && isset($_POST['intervenant_principal'])){
    $id_module = $_POST['module'];
    $nombre = $_POST['nombre'];
    $id_seance_type = $_POST['type'];
    $duree_h = $_POST['duree_h'];
    $id_groupe_type = $_POST['groupe_type'];
    $id_intervenant_principal = $_POST['intervenant_principal'];*/
if(isset($_POST["id_module_sequencage"])){
    $id_module_sequencage = $_POST["id_module_sequencage"];

    $rs = deleteMAQUETE_module_sequencage($conn, $id_module_sequencage);
    echo json_encode($rs);
}else{
    echo json_encode("Error at least one required data undefined");
}

