<?php
    require_once("../../config.php");

    $conn = mysqli_connect("$mysql_server","$mysql_user","$mysql_passwd","$mysql_db","$mysql_port");

    if  ($conn === FALSE){
        echo "connexion au serveur impossible: ".myslq_error();

        exit;
    }
    mysqli_query($conn, 'SET NAMES utf8');
?>
