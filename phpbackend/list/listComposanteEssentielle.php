<?php

header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/APC_composante_essentielle.crud.php");

if(isset($_POST["idCompetence"])){
    $idCompetence = $_POST["idCompetence"];
    $composantes_essentielles  = selectComposantesEssentiellesByIdCompetence($conn, $idCompetence);

    echo json_encode($composantes_essentielles, JSON_NUMERIC_CHECK);
}
