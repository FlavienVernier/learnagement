<link rel="stylesheet" href="css/page_rendus.inc.css"/>

<?php

    echo "<h1> Etudiants </h1>";
    
//if($_SESSION["etudiant"]){
    $ajoute=false;
    /* Afficher la liste des rendus qu'un élèves a à faire*/
    echo "<h2>Devoirs à rendre </h2> ";

    /* Permettre a un élève de valider le dépôt d'un rendu */
    $sql="SELECT re.id_rendu_module AS id, r.description AS description, r.date AS date FROM `LNM_rendu_module_as_etudiant` re
    JOIN LNM_rendu_module r ON r.id_rendu_module=re.id_rendu_module WHERE re.date_depot is NULL 
    ORDER BY date ASC";
    $result=mysqli_query($conn, $sql); //or //die ("Problème lors de la connexion");
    echo "<form method='post' action='?page=accueil&section=rendus_etudiants'> ";

    while ($row=mysqli_fetch_array($result)) {
        echo "<input type='checkbox' name='checkbox[]' value=".$row['id']." class='rendu'>
        <label for='choix".$row['id']."'>". $row['date']. " -  ".$row['description'] ."</label><br>";
    }
    echo "<button class='bouton' type='submit'>Valider les éléments finis</button>";
    echo "</form>";

    if (isset($_POST['checkbox']) && is_array($_POST['checkbox'])) {
        foreach ($_POST['checkbox'] as $selectedCheckbox) {
            $sql="UPDATE LNM_rendu_module_as_etudiant SET date_depot = NOW() WHERE id_rendu_module =". $selectedCheckbox . ";";
            $result=mysqli_query($conn, $sql) ; // on envoie la requête dans la base de donnée
            if ($result) {
                echo "Le travail a bien été rendu.<br>";
                echo "<script>window.location.href='?page=accueil&section=rendus_etudiants'</script>";
            } else {
                echo "Erreur lors de la mise à jour : ".mysqli_error($conn)."<br>";
            }
        }

    }


    
?>