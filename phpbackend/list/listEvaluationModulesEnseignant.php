<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/ETU_classical_evaluation.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_enseignant'])){
      try{
        $id_enseignant = $_POST['id_enseignant'];
        $rsStages = listETU_classical_evaluation_byIdEtudiant($conn, $id_enseignant);

        echo json_encode($rsStages);
      }catch (Exception $e) {
	echo json_encode($e->getMessage());
      }
    }else{
        echo json_encode("Error id_enseignant undefined");
    }

