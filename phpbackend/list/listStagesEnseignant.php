<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_enseignant'])){
        $id_enseignant = $_POST['id_enseignant'];
        $rsStages = listLNM_stageBySupervisorId($conn, $id_enseignant);

        echo json_encode($stages);
    }else{
        echo json_encode("Error id_enseignant undefined");
    }

