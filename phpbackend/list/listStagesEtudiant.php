<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/LNM_stage.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_etudiant'])){
      try{
        $id_etudiant = $_POST['id_etudiant'];
        $rsStages = listLNM_stageByStudentId($conn, $id_etudiant);

        echo json_encode($rsStages);
      }catch (Exception $e) {
	echo json_encode($e->getMessage());
      }
    }else{
        echo json_encode("Error id_enseignant undefined");
    }

