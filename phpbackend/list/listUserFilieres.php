<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies

header("Content-Type: application/json");

include("../db_connection/connectDB.php");
include("../crud/LNM_filiere.crud.php");
include("../crud/VIEW_display.crud.php");
include("../crud/function_rs_to_table.php");
include("../functions_filter.php");


session_start();


if (isset($_SESSION["userId"])) {
    $userId = $_SESSION["userId"];
    $filieres = [];

    // Toutes les filières dont l'utilisateur connecté est responsable
    $filieresUserResponsable = listLNM_filiereByUserId($conn, $userId);
    foreach ($filieresUserResponsable as $filiereUser) {
        $filieres[] = $filiereUser["nom_filiere"];
    }

    // Execution de MCCC par module (id : 4) et filtrage par l'utilisateur connecté
    $request = selectVIEW_display($conn, 4)["request"];
    $request = __addFiltersInRequest($conn, $request);

    $result = mysqli_query($conn, $request);
    $result = rs_to_table($result);

    // On récupère le nom des filières où l'utilisateur connecté intervient
    foreach ($result as $row) {
        $name_filieres = explode(", ", $row["filieres"]);
        if (sizeof($name_filieres) > 1) {
            foreach ($name_filieres as $name_filiere) {
                $filieres[] = $name_filiere;
            }
        }else{
            $filieres[] = $name_filieres[0];
        }
    }

    $filieres = array_values(array_unique($filieres)); //array_unique supprime tout les doublons mais garde les index d'origine de ceux-ci, array_values reindex le tableau de manière continue

    // Construction du tableau contenant les informations des filières (id_filiere, nom_filiere...)
    for ($i = 0; $i < sizeof($filieres); $i++) {
        $nom_filiere = $filieres[$i];
        $filiere = listLNM_filiereByName($conn, $nom_filiere);

        $filieres[$i] = $filiere;
    }

    sort($filieres); # ordre alphabétique
    echo json_encode($filieres, JSON_NUMERIC_CHECK);
}



