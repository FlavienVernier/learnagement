<link rel="stylesheet" href="css/page_rendus.inc.css"/>


<?php
$ajout=false;
echo "<h1> Enseignants </h1>";
/* Afficher la liste des rendus qu'un enseignant a rentré */
echo "<h2>Liste des rendus vous concernant : </h2> ";
$sql="SELECT r.date, r.description, p.parcour AS promo
    FROM LNM_rendu_module r 
        JOIN LNM_rendu_module_as_enseignant e ON r.id_rendu_module = e.id_rendu_module 
        JOIN LNM_rendu_module_as_etudiant retu ON retu.id_rendu_module = r.id_rendu_module
        JOIN LNM_etudiant etu ON etu.id_etudiant = retu.id_etudiant
        JOIN LNM_promo p ON p.id_promo = etu.id_promo
    WHERE e.id_enseignant = " . $_SESSION['id_enseignant'] . "
        AND r.date >= NOW()
    ORDER BY date ASC";
$result=mysqli_query($conn, $sql) or die ("Problème lors de la connexion");


echo "<div id='listerenduseleves'><ul> ";
while ($row=mysqli_fetch_array($result)) {
    echo"<li>".$row['date']. " - ". $row['description']. " [". $row['promo']."] ";
}
echo "</ul></div>";

//    /* Permettre à un enseignants de rajouter un rendus*/
//    echo "<h2>Rentrer un nouveau rendu </h2>";
//
//    echo "<form action='?page=accueil&section=rendus_enseignants' method='post'>";
//    echo "<label>Sélectionner une promo : </label>";
//    echo "<select name='promo'>";
//    $sql="SELECT parcour AS nom FROM LNM_promo";
//    $result=mysqli_query($conn, $sql) or die("Problème lors de la connexion"); // on envoie la requête dans la base de donnée
//    while ($row=mysqli_fetch_array($result)) {
//        echo "<option value'". $row["nom"]."'>".$row["nom"]. "</option>";
//    }
//    echo "</select><br>";
//    // echo "<br><label>Sélectionner un groupe</label><br>";
//    // echo "<select name='groupe'>";
//    // $sql="SELECT nom_groupe AS nom FROM LNM_groupe";
//    // $result=mysqli_query($conn, $sql) or die("Problème lors de la connexion"); // on envoie la requête dans la base de donnée
//    // while ($row=mysqli_fetch_array($result)) {
//    //     echo "<option value'". $row["nom"]."'>".$row["nom"]. "</option>";
//    // }
//    // echo "</select>";
//    echo "<br>Description : <input type='text' name='description' value='...'></br>";
//    echo "<br>Date de rendu : <input type='date' name='date_saisie' value='OFF'>";
//    echo "<br><button class='bouton' type='submit'>Valider</button>";
//    echo "</form>";
//
//    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
//        // On récupère les données du formulaire pour les ajouter à la base de donnée
//        $promo=$_POST["promo"];
//        //$groupe=$_POST["groupe"];
//        $description=$_POST["description"];
//        $date_saisie=$_POST["date_saisie"];
//
//        // Vérification que la description n'est pas 'OFF'
//        if ($description !== '...' && $date_saisie !== '') {
//            $sql="INSERT INTO LNM_rendu_module(id_rendu_module, description, date) VALUES (NULL, \"".$description."\", \"".$date_saisie."\");";
//            $result=mysqli_query($conn, $sql); // on envoie la requête dans la base de donnée
//
//            $sql_id_rendu = "SELECT id_rendu_module FROM LNM_rendu_module WHERE description LIKE \"".$description."\" AND date LIKE \"".$date_saisie."\"";
//            $result1 = mysqli_query($conn, $sql_id_rendu);
//            $id_rendu=mysqli_fetch_array($result1);
//
//            $sql_id_enseignant = "SELECT id_enseignant FROM LNM_enseignant WHERE mail LIKE '".$_SESSION["mail"]."'";
//            $result1 = mysqli_query($conn, $sql_id_enseignant);
//            $id_enseignant=mysqli_fetch_array($result1);
//
//            $sql_enseignant = "INSERT INTO LNM_rendu_module_as_enseignant(id_rendu_module, id_enseignant) VALUES ('".$id_rendu['id_rendu_module']."','".$id_enseignant['id_enseignant']."')";
//            $result2 =mysqli_query($conn, $sql_enseignant);
//
//            //Créer une entrée dans la table LNM_rendu_as_etudiant avec l'id du rendu et la date NULL pour tous les étudiants de la promo
//            $sql_etudiants = "INSERT INTO LNM_rendu_module_as_etudiant(id_rendu_module, id_etudiant)
//            SELECT ".$id_rendu['id_rendu_module'].", id_etudiant FROM LNM_etudiant WHERE id_promo LIKE (SELECT id_promo FROM LNM_promo WHERE parcour LIKE '".$promo."')";
//            $result3 = mysqli_query($conn, $sql_etudiants);
//            if($result && $result2 && $result3){
//                $ajout=true;
//            }
//        } else {
//            echo "Données manquantes ou invalides. Veuillez entrer des données valides.";
//        }
//    }
//
//    /* Afficher un message si l'élément a bien été rajouté */
//    if ($ajout) {
//        // On vérifie qu'il y a bien un élément ajouté
//        if (mysqli_affected_rows($conn) > 0) {
//            echo "L'élément a été ajouté avec succès à la liste.";
//            echo "<script>window.location.href='?page=accueil&section=rendus_enseignants'</script>";
//        } else {
//            echo "Erreur : Aucune ligne n'a été insérée dans la base de données.";
//        }
//    } else if($ajout = FALSE && $conn != NULL){
//        // Erreur lors de l'ajout de l'élément
//        //On stocke dans $errorCode le type d'erreur qui a été soulevé
//        $errorCode = mysqli_errno($conn);
//        // On affiche l'erreur en question, du moins le message qu'elle retourne
//        echo "Erreur lors de l'ajout de l'élément : " . mysqli_error($conn);
//
//    }
    

?>