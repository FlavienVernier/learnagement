<?php
if (!isset($_SESSION)){
    session_start([
        'cookie_lifetime' => 86400,
    ]);

    if (!isset($_SESSION["connecte"])){
        $_SESSION["connecte"] = false;
        $_SESSION["mail"] = "";
        $_SESSION["type"]=""; //etudiant ou enseignant ou administration
    }
}
?>

<!DOCTYPE html>

<html>
<head>
    <title>Learnagement</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" type="text/css" href="css/learnagment.css">
</head>

<?php 
  include("connectDB.php");
?>

    <body>
        <div id="contenu">
                <?php
                if(!isset($_GET["page"]) ) { 
                    $page="connexion";
                } else {
                    $page=$_GET["page"];
                }

                if (file_exists("page_".$page.".inc.php")){
                    include("page_".$page.".inc.php");
                }
                else{
                    echo "Page non trouvée";
                }
        ?>
        
    </div>
    <div id="piedpage">

        <footer> 
        <?php
        if($_SESSION["connecte"]){
            echo "Connecté en tant que : ".$_SESSION["mail"]." - ";
        }
        else {
            echo "Non connecté - ";
        }
        ?>
        <a href="https://www.univ-smb.fr/polytech/formation/informatique-donnees-usages/" target="_blank">IDU Polytech Annecy-Chambéry</a> /
            <a href="https://www.univ-smb.fr/scem/formations/departement-dinformatique/" target="_blank">Info SCEM</a>
            - APP -
            <a href="https://github.com/FlavienVernier/learnagement" target="_blank">Learnagement</a></footer>
        </div>
</body>
