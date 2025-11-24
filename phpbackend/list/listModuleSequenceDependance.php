<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module_dependance.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_module'])) {
      try{
        $id_module = $_POST['id_module'];
        $rsModules = listMAQUETTE_moduleSequenceDependancesByIdModule($conn, $id_module);

        echo json_encode($rsModules);
      }catch (Exception $e) {
	echo json_encode($e->getMessage());
      }
    }else{
        echo json_encode("Error id_module undefined");
    }

