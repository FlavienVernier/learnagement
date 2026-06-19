<?php

header('Content-Type: application/json');
$body = json_decode(file_get_contents('php://input'), true);

if ($body) {
    /*
     * DEPRECATED Direct access to BD is forbiden
     */
    /*$sql = "INSERT INTO MAQUETTE_module (
                code_module, nom, hCM, hTD, hTP, hPROJ, hPersonnelle, ECTS, id_semestre, id_responsable, id_discipline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = mysqli_prepare($pdo, $sql);

    if ($stmt) {

        $code = $body['code_module'] ?? '';
        $nom = $body['nom'] ?? ''; // ou 'nom' selon ce que vous envoyez
        $hCM = $body['hCM'] ?? 0;
        $hTD = $body['hTD'] ?? 0;
        $hTP = $body['hTP'] ?? 0;
        $hProj = $body['hProj'] ?? 0; // ou 'hProjet'
        $hPerso = $body['hPerso'] ?? 0;
        $ects = $body['ECTS'] ?? 0;
        $semestre = $body['semestre'] ?? 0;
        $resp = $body['id_responsable'] ?? 0;
        $disc = $body['id_discipline'] ?? 0;

        mysqli_stmt_bind_param($stmt, "ssddddddiii", 
            $code, $nom, $hCM, $hTD, $hTP, $hProj, $hPerso, $ects, $semestre, $resp, $disc
        );

        if (mysqli_stmt_execute($stmt)) {
            echo json_encode(["status" => "success", "message" => "Module créé en dur avec succès."]);
        } else {
            http_response_code(400);
            echo json_encode(["detail" => "Erreur SQL : " . mysqli_stmt_error($stmt)]);
        }
        mysqli_stmt_close($stmt);
    } else {
        http_response_code(500);
        //echo json_encode(["detail" => "Erreur de préparation SQL : " . mysqli_error($pdo)]);
    }*/
    echo json_encode(["detail" => "Not implemented yet"]);
} else {
    http_response_code(400);
    echo json_encode(["detail" => "Aucune donnée reçue."]);
}