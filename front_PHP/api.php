<?php
/*
 * Accept only absolute path
 */

require_once __DIR__ . '/vendor/autoload.php';
require_once __DIR__ . "/config.php";
require_once __DIR__ . '/utils/auth.php';
require_once __DIR__ . '/utils/apiProxy.php';

loadEnv(".");

// --- En-têtes de sécurité ---
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store, private');

// --- 1. Méthode HTTP ---
$method = $_SERVER['REQUEST_METHOD'] ?? '';
$allowedMethods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'];
if (!in_array($method, $allowedMethods, true)) {
    getLogger()->error("Method not allowed: " . $method);
    http_response_code(405);
    header('Allow: ' . implode(', ', $allowedMethods));
    exit(json_encode(['error' => 'Method not allowed']));
}

// --- 2. Path ---
$path = $_GET['path'] ?? '';
if (!is_string($path) || !preg_match('#^/[a-zA-Z0-9_\-/]{1,255}$#', $path)) {
    getLogger()->error('Invalid path');
    // Si besoin de logger partiellement le path ATTENTION !!! Jamais en entier !!!
    // $safePath = substr(preg_replace('/[^\x20-\x7E]/', '?', $path), 0, 200);
    // getLogger()->error('Invalid path: ' . $safePath);
    http_response_code(400);
    exit(json_encode(['error' => 'Invalid path']));
}

// --- 3. Content-Length (première barrière, si présent) ---
$maxBytes = 1_000_000;
$declared = (int)($_SERVER['CONTENT_LENGTH'] ?? 0);
if ($declared > $maxBytes) {
    getLogger()->error("Content length too large");
    http_response_code(413);
    exit(json_encode(['error' => 'Content length too large']));
}

// --- 4. Lecture streaming du body (vraie barrière) ---
$body = '';
if (in_array($method, ['POST', 'PATCH', 'PUT', 'DELETE'], true)) {
    $in = fopen('php://input', 'rb');
    if ($in !== false) {
        while (!feof($in)) {
            $chunk = fread($in, 8192);
            if ($chunk === false) break;
            $body .= $chunk;
            if (strlen($body) > $maxBytes) {
                fclose($in);
                getLogger()->error("Payload too large");
                http_response_code(413);
                exit(json_encode(['error' => 'Payload too large']));
            }
        }
        fclose($in);
    }
}

// --- 5. Authentification + CSRF ---
$user = getCurrentUser();
$authHeaders = ($user && !empty($user['jwt_token']))
    ? ["Authorization: Bearer " . $user['jwt_token']]
    : [];

// CSRF : requis pour toute méthode d'écriture si auth par cookie
if (in_array($method, ['POST', 'PATCH', 'PUT', 'DELETE'], true)) {
    // ToDo adapter selon futur implémentation ou supprimer si les méthodes d'écriture sont bloquées par le proxy php :
    // $csrf = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    // if (!verifyCsrfToken($csrf)) {
    //     http_response_code(403);
    //     exit(json_encode(['error' => 'Invalid CSRF token']));
    // }
}

// --- 6. Appel backend ---
try {
    $result = forwardToBackend($path, $method, $body, 'application/json', $authHeaders);
} catch (\Throwable $e) {
    getLogger()->error('[proxy] backend error: ' . $e->getMessage());
    http_response_code(502);
    exit(json_encode(['error' => 'Backend unavailable']));
}

$status = (int)($result['status'] ?? 502);
if ($status < 100 || $status > 599) $status = 502;
http_response_code($status);
echo $result['body'] ?? '';