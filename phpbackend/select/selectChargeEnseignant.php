<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/CHARGE_enseignant.crud.php");

if (isset($_POST["user_id"])){
    $user_id = $_POST["user_id"];

    $chargeTotaleEnseignant = select_charge_totale($conn, $user_id);
    $chargeRepartEnseignant = select_charge_repart($conn, $user_id);
    $chargeEnseignant = array_merge($chargeTotaleEnseignant, $chargeRepartEnseignant);

    $strChargeEnseignant = json_encode($chargeEnseignant, JSON_NUMERIC_CHECK);
    echo $strChargeEnseignant;
}else{
    echo json_encode([False, "Error user_id undefined"]);
}


