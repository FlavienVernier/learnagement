<?php
//Réinitialisation de la session
if (isset($_SESSION)){
    $_SESSION["connecte"] = false; 
    $_SESSION["email"] = null;
    $_SESSION["type"] = null;
    $_SESSION["id"] = null;
}
redirect("login");