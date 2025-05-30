<link rel="stylesheet" type="text/css" href="css/page_dashboard.css">

<div id="dashboard-container">
    <iframe src=
<?php
    require_once("../../config.php");
    $payload = [
        'id_enseignant' => $_SESSION['id_enseignant'],
        'expires' => time() + 300 // 5 minutes
    ];

    // Utilise une clé secrète partagée avec l'application Dash
    //ToDo
    $secret = 'Cle secrete a generer automatiquement au lancement de Learnagement';
    $token = base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', json_encode($payload), $secret);


    print("\"http://localhost:" . $python_web_server_port . "/enseignant/?auth_token=" . urlencode($token) . "\"");
?>
width="100%" height="600px" style="border:none;"></iframe>
</div>
