<?php
//require_once __DIR__ . '/vendor/autoload.php';
//require_once __DIR__ . '/auth.php';
//require_once __DIR__ . "/config.php";

function forwardToBackend(string $path, string $method, ?string $body): array {
    $backendUrl = getenv('INSTANCE_PROTOCOL') . '://' . getenv('BACKEND_PYTHON_DOCKER_URL')
        . ':' . getenv('BACKEND_PYTHON_DOCKER_PORT') . '/' . ltrim($path, '/');
    getLogger()->info("Forwarding to backend url: " . $backendUrl);
    $headers = ["Content-Type: application/json"];

    // On ajoute le JWT SEULEMENT s'il existe et n'est pas vide (cas CAS = jwt vide)
    $user = getCurrentUser();
    if ($user && !empty($user['jwt_token'])) {
        $headers[] = "Authorization: Bearer " . $user['jwt_token'];
    }

    $ch = curl_init($backendUrl);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_CAINFO => '/etc/ssl/learnagement-internal/cert.pem',
    ]);

    if (in_array($method, ['POST', 'PUT', 'PATCH']) && $body) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    // curl_close($ch); DEPRECATED

    if ($response === false) {
        return ['status' => 502, 'body' => json_encode(['error' => 'Backend unreachable', 'detail' => $curlError])];
    }

    return ['status' => $httpCode, 'body' => $response];
}