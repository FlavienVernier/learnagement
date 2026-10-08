<?php

require __DIR__ . '/../../../vendor/autoload.php';
require_once __DIR__ . '/../../../utils/apiProxy.php'; // adapte le chemin selon ta structure réelle
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

try {
    loadEnv(".");

    [
        "email" => $email,
        "password" => $password,
    ] = $_POST;

    $data = http_build_query([
        'username' => $email,
        'password' => $password,
        'grant_type' => "password"
    ]);

    $result = forwardToBackend(
        path: 'token',
        method: 'POST',
        body: $data,
        contentType: 'application/x-www-form-urlencoded'
    );

    $response_json = json_decode($result['body'], true);

    if (!$response_json || !array_key_exists("access_token", $response_json)) {
        echo "<script type='text/javascript'>window.alert('Incorrect login or password.');</script>" . PHP_EOL;
        Alert::error("Incorrect login or password.");
        $t->router->redirect('login');
        exit;
    }

    $jwt = $response_json["access_token"];
    $secretKey = $_ENV["INSTANCE_SECRET"];
    try {
        $decoded = JWT::decode(
            $jwt,
            new Key($secretKey, 'HS256')
        );

        echo "Utilisateur : " . $decoded->email . " " . $decoded->firstname . " " . $decoded->lastname . PHP_EOL;
        echo "Expire à : " . date('Y-m-d H:i:s', $decoded->exp) . PHP_EOL;
        getLogger()->info("Utilisateur : " . $decoded->email . " " . $decoded->firstname . " " . $decoded->lastname . PHP_EOL);
        getLogger()->info("Expire à : " . date('Y-m-d H:i:s', $decoded->exp) . PHP_EOL);

        if ($decoded->exp < time()) {
            $t->router->redirect('login');
            throw new Exception("Token expiré");
        }

    } catch (Exception $e) {
        // ToDo manage expired token, expired password...
        echo "Token invalide : " . $e->getMessage();
        $t->router->redirect('login');
        exit;
    }

    $types = array("enseignant", "etudiant", "administratif");

    if (!boolval($decoded->password2update)){
        login(
            $decoded->id,
            $decoded->email,
            array_values(array_intersect($decoded->roles,$types))[0],
            $jwt
        );
        $t->router->redirect('dashboard');
    } else if (boolval($decoded->password2update)){
        $_SESSION["type"] = array_values(array_intersect($decoded->roles,$types))[0];
        $_SESSION["id"] = $decoded->id;
        echo $t->render('base/init_password', ['email' => $email]);
    } else {
        // theoriquement ce point ne doit jamais être atteint
        $t->router->redirect('login');
    }
} catch (Exception $e) {
    #todo: add logs
    $t->router->redirect('login');
}