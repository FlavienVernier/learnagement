<?php

function forwardToBackend(
    string $path,
    string $method,
    ?string $body,
    string $contentType = 'application/json',
    array $extraHeaders = []
): array {
    $backendUrl = getenv('INSTANCE_PROTOCOL') . '://' . getenv('BACKEND_PYTHON_DOCKER_URL')
        . ':' . getenv('BACKEND_PYTHON_DOCKER_PORT') . '/' . ltrim($path, '/');
    getLogger()->info("Forwarding to backend url: " . $backendUrl);

    $headers = array_merge(["Content-Type: " . $contentType], $extraHeaders);

    $ch = curl_init($backendUrl);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_CAINFO => rtrim(getenv('DOCKER_SSL_INTERNAL_DIR'), '/') . '/cert.pem',
    ]);

    if (in_array($method, ['POST', 'PUT', 'PATCH']) && $body) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    unset($ch);

    if ($response === false) {
        return ['status' => 0, 'body' => null, 'error' => $curlError];
    }

    return ['status' => $httpCode, 'body' => $response, 'error' => null];
}