<?php
    require_once("../config.php");
    loadEnv("..");

    $type = $_SESSION['type'];

    $payload = [
        'id_' . $type => $_SESSION['id_' . $type],
        'expires' => time() + 300 // 5 minutes
    ];

    $secret = $_ENV["INSTANCE_SECRET"];
    $token = base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', json_encode($payload), $secret);
?>

<iframe src="<?= 'http://'. $_SERVER['SERVER_NAME'] . ':' . $_ENV['DASH_PORT'] . '/'. $type . '/?auth_token='. urlencode($token) ?>"
    class="h-full w-full" style="border:none;"></iframe>