<?php
error_reporting(E_ALL & ~E_DEPRECATED & ~E_WARNING);

session_start();

$cookieFile = '/tmp/intranet_cookies_' . session_id() . '.txt';

function curl_get(string $url, string $cookieFile, array $extra = []): array
{
    $ch = curl_init($url);

    // Options de base séparées
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
    curl_setopt($ch, CURLOPT_COOKIEFILE,     $cookieFile);
    curl_setopt($ch, CURLOPT_COOKIEJAR,      $cookieFile);
    curl_setopt($ch, CURLOPT_USERAGENT,      'Mozilla/5.0');
    curl_setopt($ch, CURLOPT_HEADER,         true);

    // Options supplémentaires (POST, etc.)
    foreach ($extra as $opt => $val) {
        curl_setopt($ch, $opt, $val);
    }

    $response   = curl_exec($ch);
    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $finalUrl   = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);

    return [
        'status'    => $statusCode,
        'headers'   => substr($response, 0, $headerSize),
        'body'      => substr($response, $headerSize),
        'final_url' => $finalUrl,
    ];
}

function getRedirectLocation(string $headers): ?string
{
    preg_match('/Location:\s*(\S+)/i', $headers, $m);
    return $m[1] ?? null;
}

function getCsrfToken(string $html): ?string
{
    preg_match('/<input[^>]+name="execution"[^>]+value="([^"]+)"/i', $html, $m);
    return $m[1] ?? null;
}

// --- Étape 1 : accès intranet → redirige vers CAS ---
$step1  = curl_get('https://intranet.univ-smb.fr/', $cookieFile);
$casUrl = getRedirectLocation($step1['headers']);

if (!$casUrl) {
    if (str_contains($step1['body'], 'Wooclap')) {
        header('Content-Type: application/json');
        echo json_encode(['status' => 'authenticated', 'contains_wooclap' => true]);
        exit;
    }
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Pas de redirection CAS', 'body' => mb_substr($step1['body'], 0, 300)]);
    exit;
}

// --- Étape 2 : chargement du formulaire CAS ---
$step2     = curl_get($casUrl, $cookieFile);
$execution = getCsrfToken($step2['body']);

if (!$execution) {
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Token CAS "execution" introuvable', 'body' => mb_substr($step2['body'], 0, 300)]);
    exit;
}

// --- Étape 3 : POST des identifiants ---
$login    = $_POST['login']    ?? getenv('UNI_LOGIN');
$password = $_POST['password'] ?? getenv('UNI_PASSWORD');

$postData = http_build_query([
    'username'   => $login,
    'password'   => $password,
    'execution'  => $execution,
    '_eventId'   => 'submit',
    'geolocation'=> '',
]);

$step3 = curl_get($casUrl, $cookieFile, [
    CURLOPT_POST       => true,
    CURLOPT_POSTFIELDS => $postData,
]);

// --- Étape 4 : suivi des redirections post-auth ---
$redirectUrl  = getRedirectLocation($step3['headers']);
$maxRedirects = 5;
$current      = $step3;

while ($redirectUrl && $maxRedirects-- > 0) {
    $current     = curl_get($redirectUrl, $cookieFile);
    $redirectUrl = getRedirectLocation($current['headers']);
}

// --- Résultat ---
header('Content-Type: application/json');
echo json_encode([
    'status'           => $current['status'],
    'final_url'        => $current['final_url'],
    'contains_wooclap' => str_contains($current['body'], 'Wooclap'),
    'html_excerpt'     => mb_substr(strip_tags($current['body']), 0, 500),
]);