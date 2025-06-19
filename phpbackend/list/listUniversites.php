<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json; charset=utf-8");

session_start();

include("../db_connection/connectDB.php");
include("../crud/LNM_universite.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

$rsUniversite =listLNM_universite($conn);

echo json_encode($rsUniversite, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

