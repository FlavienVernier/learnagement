<link rel="stylesheet" href="css/page_info_enseignant.inc.css"/>

<?php
/*
    Format table 'LNM_enseignant':
    id_enseignant INT,
    prenom VARCHAR(25),
    nom VARCHAR(25),
    mail VHARCHAR(50)
*/

if(isset($_GET["id"])){
    if (isset($_GET["id"])){
        $search = $_GET["id"];
        $sql = "SELECT prenom, nom, mail FROM LNM_enseignant WHERE id_enseignant = '".$search."'";
        $result = mysqli_query($conn, $sql);
    }
    else {
        echo "<div id='error-message'>";
        echo "<p>Erreur :(<br>Informations probablement erronées...</p>";
        echo "</div>";
        return;
    }
    if (mysqli_num_rows($result) == 0) {
        echo "<div id='error-message'>";
        echo "<p>Erreur :(<br>Informations probablement erronées...</p>";
        echo "</div>";
        return;
    }
    echo "<a href='?page=accueil&section=liste_prof' class='bouton_retour'>Retour</a>";
    echo "<div id=infos_enseignant>";
    $row = mysqli_fetch_assoc($result);
    echo "<h2>&#128100;".$row["prenom"]." ".$row["nom"]."</h2>";
    echo "<p>Mail : <a href='mailto:".$row['mail']."'>".$row['mail']."</a> </p>";
    echo "</div>";
    
}
else{
    $mail=$_SESSION["mail"];

        $sql = "SELECT * FROM LNM_enseignant WHERE mail LIKE '".$mail."'";
        $result = mysqli_query($conn, $sql);
        $row= mysqli_fetch_array($result);

    if (!$row["id_enseignant"]){ 
        echo "<div id='error-message'>";
        echo "<p>Erreur :(<br>Informations probablement erronées...</p>";
        echo "</div>";
        return;
    }
    echo "<div id=infos_enseignant>";
    echo "<h2>&#128100;".$row["prenom"]." ".$row["nom"]."</h2>";
    echo "<p>Mail : <a href='mailto:".$row['mail']."'>".$row['mail']."</a> </p>";
    echo "<p>Statut : ".$row['statut']." </p>";
    echo "</div>";
}
?>
