<?php
header("Access-Control-Allow-Origin: http://localhost:40080"); // Activer CORS
header("Access-Control-Allow-Credentials: true"); // Autoriser le partage de cookies


// On demarre la session
session_start();

// Sécurité : on régénère l'ID pour éviter la fixation de session
session_regenerate_id(true);

// On vide le tableau $_SESSION proprement
$_SESSION = [];

// Supprime le cookie PHPSESSID (optionnel si déjà expiré, mais c'est mieux)
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(
        session_name(),    // Généralement "PHPSESSID"
        '',
        time() - 42000,    // Expire dans le passé
        $params["path"],
        $params["domain"],
        $params["secure"],
        $params["httponly"]
    );
}

// Détruit la session côté serveur
session_destroy();

