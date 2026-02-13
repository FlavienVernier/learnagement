<?php
    require_once("../config.php");
    loadEnv("..");

    $type = $_SESSION['type'];
error_log('Your message here');
    /*$payload = [
        'id_' . $type => $_SESSION['id'],
        'expires' => time() + 300 // 5 minutes
    ];*/

    //$secret = $_ENV["INSTANCE_SECRET"];
    //$token = base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', json_encode($payload), $secret);
?>

<!--<iframe src="<?php /*= 'http://'. $_SERVER['SERVER_NAME'] . ':' . $_ENV['DASH_PORT'] . '/'. $type . '/' .
        '?auth_old_token=' . urlencode($token) .
        '&jwt_token=' . $_SESSION["jwt_token"]
        */?>"
    class="h-full w-full" style="border:none;"></iframe>-->

<iframe src="<?= 'http://'. $_SERVER['SERVER_NAME'] . ':' . $_ENV['DASH_PORT'] . '/'. $type . '/' .
'?jwt_token=' . $_SESSION["jwt_token"]
?>"
        class="h-full w-full" style="border:none;"></iframe>