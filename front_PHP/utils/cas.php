<?php


function _mockCasResponse(string $ticket): ?array
{
    // Tickets de test prédéfinis
    $mocks = [
        "ST-MOCK-ENSEIGNANT" => [
            "login"      => "tartampion",
            "attributes" => [
                "sn"          => "tartampion",
                "givenName"   => "Pierre",
                "email"       => "pierre.tartampion@lnm.fr",
                "displayName" => "Pierre Tartampion",
            ],
            "members" => [
                "cn=enseignants,ou=groups,dc=lnm,dc=fr",
                "cn=permanents,ou=groups,dc=lnm,dc=fr",
            ],
        ],
        "ST-MOCK-ETUDIANT" => [
            "login"      => "titgoute",
            "attributes" => [
                "sn"          => "titgoute",
                "givenName"   => "Corine",
                "email"       => "Corine.Titgoute@etu.lnm.fr",
                "displayName" => "Corine Titgoute",
            ],
            "members" => [
                "cn=etudiants-idu4,ou=groups,dc=lnm,dc=fr",
                "cn=etudiants,ou=groups,dc=lnm,dc=fr",
            ],
        ],
        "ST-MOCK-INCONNU" => null,  // ticket invalide
    ];

    return $mocks[$ticket] ?? null;
}
function validateCasTicket(string $ticket, string $serviceUrl): ?array
{
    // Mode mock pour les tests sans serveur CAS
    if (getenv("CAS_MOCK_ENABLED") === "true") {
        return _mockCasResponse($ticket);
    }

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
        'email'  => $casData['attributes']['email']      ?? '',
        'nom'    => $casData['attributes']['sn']         ?? '',
        'prenom' => $casData['attributes']['givenName']  ?? '',
        'members' => $casData['members'],
    ];
    //getLogger()->info('Backend data: ' . json_encode($data));
    return cas_endpoint("POST", $url, $data);
}