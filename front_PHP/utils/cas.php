<?php

function validateCasTicket(string $ticket, string $serviceUrl): ?array
{
    $casValidateUrl = getenv("CAS_HOST") . "/serviceValidate"
        . "?service=" . urlencode($serviceUrl)
        . "&ticket=" . urlencode($ticket);

    $response = file_get_contents($casValidateUrl);
    if ($response === false) {
        return null;
    }
    //getLogger()->info("Prout" . json_encode($response));

    // Parse la réponse XML du CAS
    $xml = simplexml_load_string($response);
    if ($xml === false) {
        return null;
    }

    $ns = $xml->getNamespaces(true);
    $cas = $xml->children($ns['cas'] ?? 'cas');

    if (!isset($cas->authenticationSuccess)) {
        return null; // ticket invalide ou expiré
    }

    $user = (string) $cas->authenticationSuccess->user;

    // Attributs supplémentaires si ton CAS en renvoie
    $groups = getenv("CAS_ALLOWED_GROUPS");
    $allowedGroups = array_map('trim', explode(' ', $groups));
    $attributes = [];
    $members = [];
    if (isset($cas->authenticationSuccess->attributes)) {
        foreach ($cas->authenticationSuccess->attributes->children($ns['cas'] ?? 'cas') as $key => $value) {
            if ($key === 'member') {
                $members[] = (string) $value;  // collecte tous les cas:member
            } else {
                $attributes[$key] = (string) $value;
            }
        }
    }

    return [
        'login' => $user,
        'attributes' => $attributes,
        'members'    => $members,
    ];
}

function casLogin(array $casData): ?array
{
    $url  = get_python_backend_url("token-cas/");
    $data = [
        'login'  => $casData['login'],
        'email'  => $casData['attributes']['mail']      ?? $casData['login'] . '@univ-savoie.fr',
        'nom'    => $casData['attributes']['sn']         ?? '',
        'prenom' => $casData['attributes']['givenName']  ?? '',
        'members' => $casData['members'],
    ];
    //getLogger()->info('Backend data: ' . json_encode($data));
    return cas_endpoint("POST", $url, $data);
}