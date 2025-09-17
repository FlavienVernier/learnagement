<?php
    header("Access-Control-Allow-Origin: http://localhost:40081"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module.crud.php");
    include("../crud/function_rs_to_table.php");
    include("../crud/function_action_allowed.php");

    if (isset($_POST['id_filiere']) && isset($_POST['id_statut'])){
      try{
          $id_filiere = $_POST['id_filiere'];
          $id_statut = $_POST['id_statut'];
          $rsModules = getMAQUETTE_moduleM2C3($conn, $id_filiere, $id_statut);

          echo json_encode($rsModules);
      }catch (Exception $e) {
          echo json_encode($e->getMessage());
      }
    }else{
        echo json_encode("Error , id_filiere or id_status undefined");
    }

