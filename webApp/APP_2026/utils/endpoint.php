<?php

function get_python_backend_url($endpoint) {
    $base_url = getenv("PYTHON_BACKEND_DOCKER_URL");
    $port = getenv("PYTHON_BACKEND_DOCKER_PORT");
    return $base_url . ":" . $port . "/" . $endpoint;
}

function get_endpoint($url, $token, $data = null) {
    return python_endpoint("GET", $url, $data, $token);
}

function patch_endpoint($url, $data, $token) {
    return python_endpoint("PATCH", $url, $data, $token);
}

function post_endpoint($url, $data, $token) {
    return python_endpoint("POST", $url, $data, $token);
}

function delete_endpoint($url, $token) {
    return python_endpoint("DELETE", $url, null, $token);
}

function python_endpoint($method, $url, $data, $token) {

    $headers = [
        "Authorization: Bearer $token"
    ];

    if ($method === "GET" || $method === "DELETE") {
        $headers[] = "Content-Type: application/x-www-form-urlencoded";
    } else {
        $headers[] = "Content-Type: application/json";
    }

    if ($method === "GET" && $data) {
        $url .= "?" . http_build_query($data);
    }

    $ch = curl_init($url);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    if (($method === "POST" || $method === "PATCH") && $data) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }

    $response = curl_exec($ch);

    if ($response === false) {
        error_log("Connection error: " . curl_error($ch));
        curl_close($ch);
        return [];
    }

    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    //close curl (Warning curl_close($ch) is deprecated since 8.5)
    unset($ch);

    if ($status == 401) {
        throw new Exception("Invalid or expired token");
    }

    if ($status == 403) {
        throw new Exception("Access denied - missing required role");
    }

    if ($status >= 400) {
        throw new Exception("HTTP error: " . $status);
    }

    if ($response == "[]") {
        return [];
    }

    $data = json_decode($response, true);
    if ($data === null) {
        error_log("JSON parsing error");
        return [];
    }

    return $data;
}


function get_enseignants($token) {
    $url = get_python_backend_url("enseignants/");
    return get_endpoint($url, $token);
}

function get_etudiants($token) {
    $url = get_python_backend_url("etudiants/");
    return get_endpoint($url, $token);
}

function get_filieres($token) {
    $url = get_python_backend_url("filieres/");
    return get_endpoint($url, $token);
}

function get_statuts($token) {
    $url = get_python_backend_url("statuts/");
    return get_endpoint($url, $token);
}

function get_promos($token) {
    $url = get_python_backend_url("promos/");
    return get_endpoint($url, $token);
}

function get_groupe_types($token) {
    $url = get_python_backend_url("groupe_types/");
    return get_endpoint($url, $token);
}

function get_seance_types($token) {
    $url = get_python_backend_url("seance_types/");
    return get_endpoint($url, $token);
}

function get_modules_responsables($token) {
    $url = get_python_backend_url("modules/responsables/");
    return get_endpoint($url, $token);
}

function get_modules_intervenants($token) {
    $url = get_python_backend_url("modules/intervenants/");
    return get_endpoint($url, $token);
}

function get_modules_responsable_by_id($id_responsable, $token) {
    $url = get_python_backend_url("modules/responsables/" . $id_responsable);
    return get_endpoint($url, $token);
}

function get_modules_etudiant($id_etudiant, $token) {
    $url = get_python_backend_url("modules/etudiants/" . $id_etudiant . "/");
    return get_endpoint($url, $token);
}

function get_modules_intervenant_by_id($id_intervenant, $token) {
    $url = get_python_backend_url("modules/intervenants/" . $id_intervenant . "/");
    return get_endpoint($url, $token);
}


function get_modules_m2c3($id_filiere, $id_statut, $token) {
    $url = get_python_backend_url("m2c3/");
    $data = [
        "id_filiere" => $id_filiere,
        "id_statut" => $id_statut
    ];
    return get_endpoint($url, $token, $data);
}

function get_module_dependencies($id_module, $token) {
    $url = get_python_backend_url("modules/".$id_module."/dependencies/");
    return get_endpoint($url, $token);
}

function get_data_gantt($id_responsable, $token) {
    $url = get_python_backend_url("modules/" . $id_responsable . "/gantt/");
    return get_endpoint($url, $token);
}
