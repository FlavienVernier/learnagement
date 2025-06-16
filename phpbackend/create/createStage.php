<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

session_start();

include("../db_connection/connectDB.php");
include("../crud/LNM_stage.crud.php");
include("../crud/function_rs_to_table.php");
include("../crud/function_action_allowed.php");

if (isset($_POST['entreprise'])
    && isset($_POST['intitule'])
    && isset($_POST['description'])
    && isset($_POST['ville'])
    && isset($_POST['date_debut'])
    && isset($_POST['date_fin'])
    && isset($_POST['nature'])
    && isset($_POST['id_etudiant'])){
    $entreprise = $_POST['entreprise'];
    $intitule = $_POST['intitule'];
    $description = $_POST['description'];
    $ville = $_POST['ville'];
    $date_debut = $_POST['date_debut'];
    $date_fin = $_POST['date_fin'];
    $nature = $_POST['nature'];
    $id_etudiant = $_POST['id_etudiant'];
    if (isset($_POST['id_enseignant'])) {
        $id_enseignant = $_POST['id_enseignant'];
    }else{
        $id_enseignant = NULL;
    }

    $rsStage = createLNM_stage($conn, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant);

    echo json_encode($rsStage);
}else{
    echo json_encode("Error id_enseignant undefined");
}

