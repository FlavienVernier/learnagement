<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/CLASS_session.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");


    try{
        $rsModules =  checkCLASS_sessionWithoutIntervenant($conn);

        echo json_encode($rsModules);
    }catch (Exception $e) {
	    echo json_encode($e->getMessage());
    }


