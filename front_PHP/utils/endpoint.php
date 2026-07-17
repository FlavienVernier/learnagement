<?php
require_once("./config.php");

function get_python_backend_url($endpoint) {
    $base_url = getenv("BACKEND_PYTHON_DOCKER_URL");
    $port = getenv("BACKEND_PYTHON_DOCKER_PORT");
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
    getLogger()->info("methode: " . $method . ", url: " . $url . ", data " . $data . ", token: " . $token);
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
        getLogger()->error("Connection error: " . curl_error($ch));
        curl_close($ch);
        throw new Exception("Connection error: " . curl_error($ch));
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
        getLogger()->error("JSON parsing error");
        return [];
    }

    return $data;
}


function cas_endpoint($method, $url, $data = null) {
    $casToken = getenv("INSTANCE_SECRET");
    $headers = [
        "X-Cas-Token: $casToken",
        "Content-Type: application/json",
    ];

    if ($method === "GET" && $data) {
        $url .= "?" . http_build_query($data);
    }

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    if ($method === "POST" && $data) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }

    $response = curl_exec($ch);
    $status   = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    unset($ch);

    if ($status === 404) return null;      // user inexistant → à provisionner
    if ($status >= 400) return null;

    return json_decode($response, true);
}


function get_enseignants($token) {
    $url = get_python_backend_url("enseignants/");
    return get_endpoint($url, $token);
}

function get_etudiants($token) {
    $url = get_python_backend_url("etudiants/");
    return get_endpoint($url, $token);
}
function get_etudiant($token, $id_etudiant) {
    $url = get_python_backend_url("etudiants/". $id_etudiant);
    return get_endpoint($url, $token);
}

function get_polypoints($token, $id_etudiant){
    $url = get_python_backend_url("etudiants/". $id_etudiant . "/polypoints/");
    return get_endpoint($url, $token);
}

function get_rendus_etudiant($token, $id_etudiant){
    $url = get_python_backend_url("etudiants/". $id_etudiant . "/rendus/");
    return get_endpoint($url, $token);
}

function get_stages($token){
$url = get_python_backend_url("etudiants/stages/");
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

function get_data_gantt($id_responsable, $token) {
    $url = get_python_backend_url("modules/gantt/" . $id_responsable . "/");
    return get_endpoint($url, $token);
}

function get_data_gantt_etudiant($id_etudiant, $token) {
    $url = get_python_backend_url("modules/gantt/etudiant/" . $id_etudiant . "/");
    return get_endpoint($url, $token);
}

function get_module_dependencies($id_module, $token) {
    $url = get_python_backend_url("modules/".$id_module."/dependencies/");
    return get_endpoint($url, $token);
}

function get_disciplines($token) {
    $url = get_python_backend_url("disciplines/");
    return get_endpoint($url, $token);
}

function post_module($data, $token) {
    $url = get_python_backend_url("modules/create/");
    return post_endpoint($url, $data, $token);
}

function get_stages_etudiant($token, $id_etudiant) {
    $url = get_python_backend_url("etudiants/" . $id_etudiant . "/stages/");
    return get_endpoint($url, $token);
}

function get_calendars($token, $id) {
    $url = get_python_backend_url("user/" . $id . "/calendars/");
    return get_endpoint($url, $token);
}

function post_calendar($token, $id, $url_name, $url_calendar) {
    $url = get_python_backend_url("user/" . $id . "/calendars/");
    $data = [
        "url_name" => $url_name,
        "url" => $url_calendar
    ];
    return post_endpoint($url, $data, $token);
}

function patch_calendar($token, $id, $id_calendar, $url_name, $url_calendar) {
    $url = get_python_backend_url("user/" . $id . "/calendars/" . $id_calendar);
    $data = [
        "url_name" => $url_name,
        "url" => $url_calendar
    ];
    return patch_endpoint($url, $data, $token);
}

function post_stage($token, $entreprise, $sujet, $mission, $adresse, $ville, $codePostal, $pays, $start_date, $end_date, $nature, $id_etudiant, $id_enseignant) {
    $url = get_python_backend_url("etudiants/" . $id_etudiant . "/stage");
    $data = [
        "entreprise" => $entreprise,
        "intitule" => $sujet,
        "description" => $mission,
        "adresse" => $adresse,
        "ville" => $ville,
        "codePostal" => $codePostal,
        "pays" => $pays,
        "date_debut" => $start_date,
        "date_fin" => $end_date,
        "nature" => $nature,
        "id_etudiant" => $id_etudiant,
        "id_enseignant" => $id_enseignant
    ];
    return post_endpoint($url, $data, $token);
}

function patch_stage($token, $id_stage, $entreprise, $sujet, $mission, $adresse, $ville, $codePostal, $pays, $start_date, $end_date, $nature, $id_etudiant, $id_enseignant) {
    $url = get_python_backend_url("etudiants/" . $id_etudiant . "/stages/" . $id_stage);
    $data = [
        "entreprise" => $entreprise,
        "intitule" => $sujet,
        "description" => $mission,
        "adresse" => $adresse,
        "ville" => $ville,
        "codePostal" => $codePostal,
        "pays" => $pays,
        "date_debut" => $start_date,
        "date_fin" => $end_date,
        "nature" => $nature,
        "id_enseignant" => $id_enseignant
    ];
    return patch_endpoint($url, $data, $token);
}