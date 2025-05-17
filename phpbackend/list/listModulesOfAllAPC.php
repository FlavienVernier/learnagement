<?php

header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/function_rs_to_table.php");
include("../crud/APC_apprentissage_critique_as_module.crud.php");

// Renvoie un tableau associatif où les éléments sont groupés par :
// - apprentissages critiques si indexBy = 'id_apprentissage_critique' (affiche la liste de modules pour un apprentissage critique)
// - modules si indexBy = 'id_module' (affiche la liste d'apprentissages critiques pour un module)


if(isset($_POST["indexBy"])){
    $indexBy = $_POST["indexBy"];

    $modulesOfAllAPC = selectModulesOfAllAPC($conn);
    $modulesOfAllAPCIndex = [];

    // groupement des modules par apprentissages critiques
    foreach ($modulesOfAllAPC as $item) {
        if($indexBy == "id_apprentissage_critique"){
            if(!isset($modulesOfAllAPCIndex[$item["id_apprentissage_critique"]])){
                $modulesOfAllAPCIndex[$item["id_apprentissage_critique"]] = [$item];
            }else{
                $modulesOfAllAPCIndex[$item["id_apprentissage_critique"]][] = $item;
            }
        }elseif ($indexBy == "id_module"){
            if(!isset($modulesOfAllAPCIndex[$item["id_module"]])){
                $modulesOfAllAPCIndex[$item["id_module"]] = [$item];
            }else{
                $modulesOfAllAPCIndex[$item["id_module"]][] = $item;
            }
        }


    }

    echo json_encode($modulesOfAllAPCIndex, JSON_NUMERIC_CHECK);
}
