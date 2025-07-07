<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_etudiant'])){
      try{
        $id_etudiant = $_POST['id_etudiant'];
        $rsModules = listMAQUETTE_moduleChargeBuIdEtudiant($conn, $id_etudiant);

        echo json_encode($rsModules);
      }catch (Exception $e) {
	echo json_encode($e->getMessage());
      }
    }else{
        echo json_encode("Error id_etudiant undefined");
    }

