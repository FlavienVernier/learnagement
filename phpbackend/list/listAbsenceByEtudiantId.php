<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json; charset=utf-8");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/CLASS_absence.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

if (isset($_POST['id_etudiant'])){
    $id_etudiant = $_POST['id_etudiant'];
    $rsStages = listCLASS_absenceByStudentId($conn, $id_etudiant);

    echo json_encode($rsStages, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}else{
    echo json_encode("Error id_etudiant undefined");
}

