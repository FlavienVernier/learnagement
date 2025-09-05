<?php
    header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
    header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

    header("Content-Type: application/json");

    session_start();

    include("../db_connection/connectDB.php");
    include("../crud/MAQUETTE_module.crud.php");
    include("../crud/function_rs_to_table.php");

    function removeDuplicatesFromNestedArray($nestedArray)
    {
        // Sérialiser les sous-listes pour les rendre uniques
        $serialized = array_map('serialize', $nestedArray);

        // Utiliser array_unique pour supprimer les doublons
        $uniqueSerialized = array_unique($serialized);

        // Désérialiser les sous-listes pour obtenir le résultat original
        $uniqueArray = array_map('unserialize', $uniqueSerialized);

        // Réindexer le tableau pour garantir un encodage JSON correct
        return array_values($uniqueArray);
    }

    if (isset($_POST['code_module'])){
        $code_module = $_POST['code_module'];
        $rsMaquette = selectMAQUETTE_module($conn, $code_module);

        $maquette = removeDuplicatesFromNestedArray($rsMaquette); // Suppression des doublons existants

        echo json_encode($maquette);
    }else{
        echo json_encode("Error code_module undefined");
    }

