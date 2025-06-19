<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");


// Inclusion des fichiers nécessaires
include("../db_connection/connectDB.php");
include("../crud/LNM_filiere.crud.php");
include("../crud/function_rs_to_table.php");

$filieres = listLNM_filiere($conn);

sort($filieres); # ordre alphabétique
echo json_encode($filieres, JSON_NUMERIC_CHECK);