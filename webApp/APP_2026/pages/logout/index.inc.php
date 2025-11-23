<?php
//Réinitialisation de la session
if (isset($_SESSION)){
    $_SESSION["connecte"]=false;
    $_SESSION["mail"]="";
    $_SESSION["type"]="";
}
redirect("login");