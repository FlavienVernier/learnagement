<?php

try {


    $params = [];
    if (!isset($_POST['url']) || empty($_POST['url'])) {
        $params['error'] = "L'url est requise."; 
        throw new Exception("L'url est requise.");
    }

    $url_name = uniqid(parse_url($_POST['url'], PHP_URL_HOST) . '-');
    $type = $user['type'];
    $token = $user["jwt_token"];
    $id = $user['id'];

    $id_etudiant = $type === 'etudiant' ? $user['id'] : null;
    $id_enseignant = $type === 'enseignant' ? $user['id'] : null;
    $id_administratif = $type === 'administratif' ? $user['id'] : null;
    $url = $_POST['url'];
    $id_calendar = $_POST['idCalendar'];

    if ((bool)$_POST['hasAgenda']) {
        patch_calendar($token, $id, $id_calendar, $url_name, $url);
    } else {
        post_calendar($token, $id, $url_name, $url);
    }
    Alert::success("L'agenda a été créé avec succès.");
} catch (\Throwable $th) {
    if (!isset($params['error']))
        $params['error'] = "Une erreur est survenue lors de l'ajout de l'agenda."; # TODO: Create system log
    Alert::error($params['error']);
    var_dump($th);
    var_dump($url_name);
}
$t->router->redirect('dashboard');