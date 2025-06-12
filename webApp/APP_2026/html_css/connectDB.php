<?php
    require_once("../../config.php");

    $conn = mysqli_connect("$_ENV['MYSQL_SERVER']","$_ENV['MYSQL_USER']","$_ENV['MYSQL_PASSWD']","$_ENV['MYSQL_DB']","$_ENV['MYSQL_PORT']");

    if  ($conn === FALSE){
        echo "connexion au serveur impossible: ".myslq_error();

        exit;
    }
    mysqli_query($conn, 'SET NAMES utf8');
?>
