<?php

header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/APC_competence_as_filiere_as_statut.crud.php");

if (isset($_POST["nom_filiere"])) {
    $nom_filiere = $_POST["nom_filiere"];
    $competences = selectCompetenceByNomFiliere($conn, $nom_filiere);
    echo json_encode($competences, JSON_NUMERIC_CHECK);
}

