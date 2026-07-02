<?php

function validateCasTicket(string $ticket, string $serviceUrl): ?array
{
    $casValidateUrl = "https://cas-uds.grenet.fr/serviceValidate"
        . "?service=" . urlencode($serviceUrl)
        . "&ticket=" . urlencode($ticket);

    $response = file_get_contents($casValidateUrl);
    if ($response === false) {
        return null;
    }

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
    $attributes = [];
    if (isset($cas->authenticationSuccess->attributes)) {
        foreach ($cas->authenticationSuccess->attributes->children() as $key => $value) {
            $attributes[$key] = (string) $value;
        }
    }

    return [
        'login' => $user,
        'attributes' => $attributes,
    ];
}

function casLogin(array $casData, string $serviceToken): ?array
{
    $url  = get_python_backend_url("token-cas/");
    $data = [
        'login'  => $casData['login'],
        'email'  => $casData['attributes']['mail']      ?? $casData['login'] . '@univ-savoie.fr',
        'nom'    => $casData['attributes']['sn']         ?? '',
        'prenom' => $casData['attributes']['givenName']  ?? '',
        'type'   => 'etudiant',
    ];
    return cas_endpoint("POST", $url, $data, $serviceToken);
}