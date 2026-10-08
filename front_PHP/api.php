<?php
require_once __DIR__ . '/vendor/autoload.php'; // Add this line
require_once __DIR__ . "/config.php";
require_once __DIR__ . '/utils/auth.php';
require_once __DIR__ . '/utils/apiProxy.php';

loadEnv(".");

$path = $_GET['path'] ?? '';
if (empty($path)) {
    http_response_code(400);
    header('Content-Type: application/json');
    exit(json_encode(['error' => 'Missing path']));
}

$user = getCurrentUser();
$authHeaders = ($user && !empty($user['jwt_token'])) ? ["Authorization: Bearer " . $user['jwt_token']] : [];
$result = forwardToBackend($path, $_SERVER['REQUEST_METHOD'], file_get_contents('php://input'), 'application/json', $authHeaders);

http_response_code($result['status']);
header('Content-Type: application/json');
echo $result['body'];