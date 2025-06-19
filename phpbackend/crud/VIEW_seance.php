<?php
function viewSeance($conn, $input, $code_module)
{
    preg_match('/([A-Za-z]+)(\d+)/', $input, $matches);
    if (count($matches) < 3) {
        return ["error" => "Format invalide"];
    }

    $type = $matches[1];
    $nombre = intval($matches[2]);

    $stmt = $conn->prepare("SELECT id_seance_type FROM LNM_seanceType WHERE type = ?");
    $stmt->bind_param("s", $type);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $id_seance_type = $row['id_seance_type'];
    } else {
        return ["error" => "Type de séance non trouvé"];
    }

    $stmt = $conn->prepare("SELECT id_module FROM MAQUETTE_module WHERE code_module = ?");
    $stmt->bind_param("s", $code_module);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $id_module = $row['id_module'];
    } else {
        return ["error" => "Module non trouvé"];
    }

    $stmt = $conn->prepare("SELECT duree_h, nombre FROM MAQUETTE_module_sequencage WHERE id_seance_type = ? AND id_module = ?");
    $stmt->bind_param("ii", $id_seance_type, $id_module);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $duree_h = $row['duree_h'];
        $totalNumber = $row['nombre'];

        return [
            "duree_h" => $duree_h,
            "typeCourse" => $type,
            "currentNumber" => $nombre,
            "moduleName" => $code_module,
            "moduleCode" => $code_module,
            "totalNumber" => $totalNumber
        ];
    } else {
        return ["error" => "Aucune donnée trouvée"];
    }
}