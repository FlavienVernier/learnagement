<?php

header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/APC_apprentissage_critique.crud.php");

if (isset($_POST["idCompetence"])) {
    $idCompetence = $_POST["idCompetence"];
    $apprentissagesCritiques = selectAPCbyIdComp($conn, $idCompetence);

    $apprentissagesCritiquesByLevel = [];

    // Regrouper par niveau
    foreach ($apprentissagesCritiques as $APC) {
        $niveau = $APC['niveau'];
        if (!isset($apprentissagesCritiquesByLevel[$niveau])) {
            $apprentissagesCritiquesByLevel[$niveau] = [];
        }
        $apprentissagesCritiquesByLevel[$niveau][] = $APC;
    }

    echo json_encode($apprentissagesCritiquesByLevel, JSON_NUMERIC_CHECK);
}
