<?php

function ipInCidr(string $ip, string $cidr): bool
{
    if (strpos($cidr, '/') === false) {
        return $ip === $cidr;
    }
    [$subnet, $bits] = explode('/', $cidr, 2);
    $ipBin  = @inet_pton($ip);
    $subBin = @inet_pton($subnet);
    if ($ipBin === false || $subBin === false || strlen($ipBin) !== strlen($subBin)) {
        return false;
    }
    $bits  = (int)$bits;
    $bytes = intdiv($bits, 8);
    $rem   = $bits % 8;
    if ($bytes > 0 && substr($ipBin, 0, $bytes) !== substr($subBin, 0, $bytes)) {
        return false;
    }
    if ($rem > 0) {
        $mask = (0xFF << (8 - $rem)) & 0xFF;
        if ((ord($ipBin[$bytes]) & $mask) !== (ord($subBin[$bytes]) & $mask)) {
            return false;
        }
    }
    return true;
}

/**
 * IP réelle du client.
 * X-Forwarded-For n'est lu que si la requête vient d'un proxy de confiance (Traefik).
 */
function getClientIp(): string
{
    $remote  = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $trusted = array_filter(array_map('trim', explode(',', getenv('TRUSTED_PROXY_IPS') ?: '')));

    $fromTrustedProxy = false;
    foreach ($trusted as $cidr) {
        if (ipInCidr($remote, $cidr)) {
            $fromTrustedProxy = true;
            break;
        }
    }

    if ($fromTrustedProxy && !empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $parts     = array_map('trim', explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']));
        $candidate = end($parts); // ajouté par Traefik, non forgeable par le client
        if (filter_var($candidate, FILTER_VALIDATE_IP)) {
            return $candidate;
        }
    }
    return $remote;
}
function forwardToBackend(
    string $path,
    string $method,
    ?string $body,
    string $contentType = 'application/json',
    array $extraHeaders = [],
    array $query = []
): array {
    $backendUrl = getenv('INSTANCE_PROTOCOL') . '://' . getenv('BACKEND_PYTHON_DOCKER_URL')
        . ':' . getenv('BACKEND_PYTHON_DOCKER_PORT') . '/' . ltrim(rtrim($path,'/'), '/');

    if (!empty($query)) {
        $backendUrl .= '?' . http_build_query($query);
    }

    getLogger()->info("Forwarding to backend: " . $method . " " . strtok($backendUrl, '?'));

    $headers = array_merge(["Content-Type: " . $contentType], $extraHeaders);

    $ch = curl_init($backendUrl);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_FOLLOWLOCATION => false,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_CAINFO => rtrim(getenv('DOCKER_SSL_INTERNAL_DIR'), '/') . '/cert.pem',
    ]);

    if (in_array($method, ['POST', 'PUT', 'PATCH'], true) && $body !== null && $body !== '') {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }
    /*if (in_array($method, ['POST', 'PUT', 'PATCH']) && $body) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }*/

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    unset($ch);

    if ($response === false) {
        getLogger()->error("Forwarding to backend error: " . $curlError);
        return ['status' => 0, 'body' => null, 'error' => $curlError];
    }

    return ['status' => $httpCode, 'body' => $response, 'error' => null];
}