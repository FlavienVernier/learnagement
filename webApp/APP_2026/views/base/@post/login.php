<?php

require __DIR__ . '/../../../../vendor/autoload.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

try {
  loadEnv("..");

  [
    "email" => $email,
    "password" => $password,
  ] = $_POST;


  $url = $_ENV["PYTHON_BACKEND_DOCKER_URL"] . ":" . $_ENV["PYTHON_BACKEND_DOCKER_PORT"] . "/token";
  $data = http_build_query(['username' => $email,
           'password' => $password,
           'grant_type' => "password"
  ]);

  $headers = [
    "Content-Type: application/x-www-form-urlencoded",
    "Content-Length: " . strlen($data)
  ];

  // use key 'http' even if you send the request to https://...
  $options = [
    'http' => [
        'header' => $headers,
        'method' => 'POST',
        'content' =>  $data,
        'ignore_errors' => true,
    ],
  ];
  $context = stream_context_create($options);
  $response = file_get_contents($url, false, $context);

  $response_json = json_decode($response, true);

  if(!array_key_exists("access_token", $response_json)){
      echo "<script type='text/javascript'>window.alert('Incorrect login or password.');</script>". PHP_EOL;
      $t->router->redirect('login');
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

    if ($decoded->exp < time()) {
        $t->router->redirect('login');
        throw new Exception("Token expiré");
    }

  } catch (Exception $e) {
      // ToDo manage expired token, expired password...
      echo "Token invalide : " . $e->getMessage();
      $t->router->redirect('login');
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
      // theriticaly this point must never be accessed
      $t->router->redirect('login');
  }
} catch (Exception $e) {
  #todo: add logs
  $t->router->redirect('login');
}