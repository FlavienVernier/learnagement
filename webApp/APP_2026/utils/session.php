<?php
function _session_start() {
    if (session_status() === PHP_SESSION_NONE) {
        session_start([
            'cookie_lifetime' => 86400,
        ]);
    }
}

function create_session() {
    _session_start();

    if (!isset($_SESSION["connecte"])){
        add_session("connect", false);
        add_session("email", null);
        add_session("type", null); //etudiant ou enseignant ou administration
    }
}

function add_session(string $key, $value) {
    _session_start();
    $_SESSION[$key] = $value;
}

function get_session(string $key) {
    _session_start();
    return $_SESSION[$key] ?? null;
}

function delete_session() {
    _session_start();

    // Vide toutes les variables de session
    $_SESSION = [];

    // Supprime le cookie de session si existant
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(
            session_name(), 
            '', 
            time() - 42000,
            $params["path"], 
            $params["domain"],
            $params["secure"], 
            $params["httponly"]
        );
    }
    session_destroy();
}