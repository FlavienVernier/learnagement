<link rel="stylesheet" type="text/css" href="css/page_dashboard.css">

<div id="dashboard-container">
    <iframe src=
    <?php
        require_once("../../config.php");
        loadEnv("../..");

        $payload = [
            'id_etudiant' => $_SESSION['id_etudiant'],
            'expires' => time() + 300 // 5 minutes
        ];

        $secret = $_ENV["INSTANCE_SECRET"];
        $token = base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', json_encode($payload), $secret);

        print("\"http://" . $_SERVER['SERVER_NAME'] . ":" . $_ENV['DASH_PORT'] . "/etudiant/?auth_token=" . urlencode($token) . "\" ");
    ?>
    width="100%" height="600px" style="border:none;"></iframe>
</div>
