<?php
    require_once("../config.php");
    loadEnv("..");
    /*
    $pdo = mysqli_connect($_ENV['MYSQL_SERVER'], $_ENV['MYSQL_USER_LOGIN'], $_ENV['MYSQL_USER_PASSWORD'], $_ENV['MYSQL_DB'], $_ENV['MYSQL_PORT']);

    if  ($pdo === FALSE){
        echo "connexion au serveur impossible: ".mysqli_error();
        exit;
    }
    mysqli_query($pdo, 'SET NAMES utf8');
    */