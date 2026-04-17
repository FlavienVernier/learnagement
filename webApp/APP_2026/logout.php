<?php
error_reporting(E_ALL & ~E_DEPRECATED & ~E_WARNING);

session_start();

$cookieFile = '/tmp/intranet_cookies_' . session_id() . '.txt';

// Supprime le fichier de cookies
if (file_exists($cookieFile)) {
    unlink($cookieFile);
}

// Détruit la session PHP
session_destroy();

header('Content-Type: application/json');
echo json_encode(['status' => 'logged_out']);