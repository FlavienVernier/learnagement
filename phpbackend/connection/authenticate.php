<?php
//header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Origin: " . $_ENV["INSTANCE_URL"] ); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies
header("Content-Type: application/json");

require_once("../db_connection/config.php");
require_once("../functions.php");
require_once("../functions_filter.php");
include("../db_connection/connectDB.php");


ini_set('session.use_cookies', 0); // Permet d'éviter d'envoyer au front deux PHPSESSID
session_start();

// Now we check if the data from the login form was submitted, isset() will check if the data exists.
if ( !isset($_POST['username'], $_POST['password']) ) {
    // Could not get the data that should have been sent.
    exit('Please fill both the username and password fields !');
}

$userlogin = $_POST['username'];

/*
* get user id and hashed password
*/
$login_req = "SELECT id_enseignant, prenom, nom, password FROM LNM_enseignant WHERE mail = \"$userlogin\"";
$result = mysqli_query($conn, $login_req);

if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $req;
    echo 'error ' . mysqli_error($conn);
    exit;
}


if (mysqli_num_rows($result) > 0) {
$row = mysqli_fetch_assoc($result);
$id = $row["id_enseignant"];
$firstname = $row["prenom"];
$lastname = $row["nom"];
$hashedPassword = $row["password"];
// Account exists, now we verify the password.
// Note: remember to use password_hash in your registration file to store the hashed passwords.
    if (password_verify($_POST['password'], $hashedPassword)) {
      // Verification success! User has logged-in!
      // Create sessions, so we know the user is logged in, they basically act like cookies but remember the data on the server.


        session_regenerate_id(true);
        $sessionId = session_id();
        setcookie('PHPSESSID', $sessionId, [
            'path' => '/',
            'secure' => false, // Valable uniquement pour HTTPS
            'httponly' => true,
            'samesite' => 'Lax'
        ]);

        initFilter($conn, $id, $sessionId);

        $_SESSION['userId'] = $id;
        $_SESSION['userFirstname'] = $firstname;
        $_SESSION['userLastname'] = $lastname;
        $_SESSION['start'] = time();

        $response = [
            "id" => $id,
            "email" => $_POST['username'],
            "firstname" => $firstname,
            "lastname" => $lastname,
        ];

        echo json_encode(['user' => $response, 'sessionId' => $sessionId], JSON_NUMERIC_CHECK);
        exit(0);
    }else {
          // Incorrect password
          echo json_encode([false, 'Incorrect  password !']);
    }
}else{
    // Incorrect username
    echo json_encode([false, 'Incorrect username !']);
}

