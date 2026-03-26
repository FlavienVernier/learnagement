<?php
    require '../vendor/autoload.php';

    require './utils/session.php';
    require './utils/render.php';
    include "./utils/connectDB.php";
    include "./utils/router.php";

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Active les logs phpCAS dans un fichier
//phpCAS::setDebug('/var/www/html/cas_debug.log');
phpCAS::setVerbose(true);
// autoload DOIT être en premier, avant tout output

    create_session();

    // Configuration phpCAS
    phpCAS::client(CAS_VERSION_2_0, 'cas-uds.grenet.fr', 443, '/login', 'http://192.168.168.34:40080/APP_2026/learnagementCAS.php');

    // Désactiver la validation du certificat SSL (à activer en production avec le bon certificat)
    phpCAS::setNoCasServerValidation();
    // prod code : phpCAS::setCasServerCACert('/chemin/vers/certificat.pem');

    // Forcer l'authentification CAS
    phpCAS::forceAuthentication();

    // L'utilisateur est authentifié, récupérer son login
    $_SESSION["connecte"] = true;
    $_SESSION["login"] = phpCAS::getUser();

    $defaultPage = "home";
    $page = !isset($_GET["page"]) ? $defaultPage : $_GET["page"];
    $section = !isset($_GET["section"]) ? "home" : $_GET["section"];

    echo("<!-- Rendering page: $page, section: $section, user: {$_SESSION['login']} -->");
    if($page === "home")
        render("templates/dashboard", ["page" => $section, "conn" => $conn]);
    else
        render("templates/root", ["page" => $page, "conn" => $conn]);