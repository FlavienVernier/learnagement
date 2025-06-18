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
    && isset($_POST['sujet'])
    && isset($_POST['mission'])
    && isset($_POST['ville'])
    && isset($_POST['start_date'])
    && isset($_POST['end_date'])
    && isset($_POST['id_etudiant'])){
    $entreprise = $_POST['entreprise'];
    $intitule = $_POST['sujet'];
    $description = $_POST['mission'];
    $ville = $_POST['ville'];
    $date_debut = $_POST['start_date'];
    $date_fin = $_POST['end_date'];
    $id_etudiant = $_POST['id_etudiant'];
    if (isset($_POST['id_enseignant']) && (trim($_POST['id_enseignant']) != "") && (strtoupper(trim($_POST['id_enseignant'])) != "NULL")) {
        $id_enseignant = $_POST['id_enseignant'];
    }else{
        $id_enseignant = "NULL";
    }

    $rsStage = createLNM_stage($conn, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, "", $id_etudiant, $id_enseignant);

    echo json_encode($rsStage);
}else{
    echo json_encode("Error at least one required data undefined");
}

