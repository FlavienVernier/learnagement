<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/LNM_stage.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    $rsStages = listLNM_stageWithSupervisorId($conn);

    echo json_encode($rsStages);


