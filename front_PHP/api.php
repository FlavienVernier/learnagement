<?php
require_once __DIR__ . '/utils/apiProxy.php';

$path = $_GET['path'] ?? '';
if (empty($path)) {
    http_response_code(400);
    header('Content-Type: application/json');
    exit(json_encode(['error' => 'Missing path']));
}

$result = forwardToBackend($path, $_SERVER['REQUEST_METHOD'], file_get_contents('php://input'));

http_response_code($result['status']);
header('Content-Type: application/json');
echo $result['body'];