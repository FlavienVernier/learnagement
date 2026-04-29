<?php

try {
    $params = [];
    if (!isset($_POST['url']) || empty($_POST['url'])) {
        $params['error'] = "L'url est requise."; 
        throw new Exception("L'url est requise.");
    }

    $url_name = uniqid(parse_url($_POST['url'], PHP_URL_HOST) . '-');
    $type = $user['type'];
    $id_etudiant = $type === 'etudiant' ? $user['id'] : null;
    $id_enseignant = $type === 'enseignant' ? $user['id'] : null;
    $id_administratif = $type === 'administratif' ? $user['id'] : null;
    $url = $_POST['url'];

    if ((bool)$_POST['hasAgenda']) {
        $sql = "UPDATE `LNM_calendar` SET `url_name`=?,`url`=? WHERE 
                        (id_etudiant = ? OR (? IS NULL AND id_etudiant IS NULL)) AND
                        (id_enseignant = ? OR (? IS NULL AND id_enseignant IS NULL)) AND
                        (id_administratif = ? OR (? IS NULL AND id_administratif IS NULL))";
        $stmt = mysqli_prepare($pdo, $sql);
        mysqli_stmt_bind_param($stmt, "ssiiiiii", $url_name, $url,
            $id_etudiant, $id_etudiant,
            $id_enseignant, $id_enseignant,
            $id_administratif, $id_administratif
        );
    } else {
        $sql = "INSERT INTO `LNM_calendar`(`url_name`, `id_etudiant`, `id_enseignant`, `id_administratif`, `url`) VALUES (?,?,?,?,?);";
        $stmt = mysqli_prepare($pdo, $sql);
        mysqli_stmt_bind_param($stmt, "siiis", $url_name, $id_etudiant, $id_enseignant, $id_administratif, $url);
    }
    mysqli_stmt_execute($stmt);
    Alert::success("L'agenda a été créé avec succès.");
} catch (\Throwable $th) {
    if (!isset($params['error']))
        $params['error'] = "Une erreur est survenue lors de l'ajout de l'agenda."; # TODO: Create system log
    Alert::error($params['error']);
    var_dump($th);
    var_dump($url_name);
}
$t->router->redirect('dashboard');