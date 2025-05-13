
<link rel="stylesheet" type="text/css" href="css/page_accueil.css">

<div id="container">
<div id="menu">
    <h2 id="titre">Learnagement</h2>
    <ul id="lemenu">
        <li><a href="?page=accueil&section=agenda" class="btn_menu ">Agenda</a></li>
        <?php if ($_SESSION["type"]=="etudiant"){
            echo "<li><a href='?page=accueil&section=etudiant' class='btn_menu'>Mon Compte</a></li>";
            echo "<li><a href='?page=accueil&section=rendus_etudiants' class='btn_menu'>Mes Rendus</a></li>";
            echo "<li><a href='?page=accueil&section=dashboard_etudiant' class='btn_menu'>Tableau de bord</a></li>";
        }
        else if ($_SESSION["type"]=="enseignant"){
            echo "<li><a href='?page=accueil&section=info_enseignant' class='btn_menu'>Mon Compte</a></li>";
            echo "<li><a href='?page=accueil&section=rendus_enseignants' class='btn_menu'>Mes Rendus</a></li>"; 
            echo "<li><a href='?page=accueil&section=dashboard_enseignant' class='btn_menu'>Tableau de bord</a></li>";
        }
        else{
            echo "<li><a href='?page=accueil&section=dashboard_administration' class='btn_menu'>Tableau de bord</a></li>";
        }
        ?>
        <li><a href="?page=accueil&section=liste_personnel" class="btn_menu ">Liste</a></li>
        <li><a href="?page=accueil&section=ressources" class="btn_menu ">Ressources</a></li>
        <li><br><br></li>
        <li><a href="?page=deconnexion" class="btn_menu ">Deconnexion</a></li>
    </ul>
</div>
<div id="contenu_section">

<?php
if(!isset($_GET["section"]) ) { 
    $section="agenda";
} else {
    $section=$_GET["section"];
}

if (file_exists("page_".$section.".inc.php")){
    include("page_".$section.".inc.php");
}
else{
    echo "Page non trouvée";
}
?>
</div>
</div>

