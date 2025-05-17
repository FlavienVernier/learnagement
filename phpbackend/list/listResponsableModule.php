<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");


    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module.crud.php");
    include("../crud/function_rs_to_table.php");

    session_start();

    $id = $_SESSION['userId'];
    $listeModules = listMAQUETTE_module_with_learning_unit($conn, $id);

    $indexedArray = [];
    foreach ($listeModules as $module) {
        $id_module = $module["id_module"];
        $indexedArray[$id_module] = $module;
    }
    echo json_encode($indexedArray, JSON_NUMERIC_CHECK);