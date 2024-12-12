<link rel="stylesheet" href="css/page_liste_personnel.inc.css"/>

<?php
// Affichage des élèves
echo "<p> Liste des élèves : </p>";
//Affichage de la barre de tri
echo "<form method='post' action='?page=accueil&section=liste_etu'>";
echo "<label id='formulaire' for='choix'>Sélectionnez la filière et/ou l'année à afficher : </label>";
// selection de la filiere
echo "<select name='filiere' id='form'>";
    $sql="SELECT DISTINCT nom_filiere from LNM_filiere";
    $res=mysqli_query($conn, $sql);
    echo "<option value=pas_filiere>    </option>";
    while ($row = mysqli_fetch_array($res)) { // tant qu'on a une ligne de résultat
        echo "<option value=".$row['nom_filiere'].">".$row['nom_filiere']."</option>"; // on affiche l'option correspondante
    }
echo "</select>";
// selection de l'année
echo "<select name='annee' id='form'>";
    $sql="SELECT DISTINCT annee from LNM_promo";
    $res=mysqli_query($conn, $sql);
    echo "<option value=pas_annee>    </option>";
    while ($row = mysqli_fetch_array($res)) { // tant qu'on a une ligne de résultat
        echo "<option value=".$row['annee'].">".$row['annee']."</option>"; // on affiche l'option correspondante
    }
echo "</select>";
echo "<input type='hidden' name='valider' value='true'>"; // Ajout de la variable cachée pour indiquer que le formulaire a été soumis
echo "<button class='bouton_retour' type='valider'>Valider</button>";
echo "<a href='?page=accueil&section=liste_personnel' class='bouton_retour'>Retour</a>";
echo "</form>";

// Affichage de la liste
if (isset($_POST['valider'])) {
    $filiere=$_POST['filiere'];
    $annee=$_POST['annee'];
    
    // si on a pas de filiere :
    if ($filiere=="pas_filiere" && $annee!="pas_annee"){
        //affichage des élèves en fonction de l'année selectionnée
        echo "<p>Elèves en ".$annee." : </p> ";
        $sql = "SELECT e.prenom AS etu_prenom, e.nom AS etu_nom, f.nom_filiere AS etu_filiere FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            WHERE p.annee = '{$annee}'";
        $result=mysqli_query($conn, $sql);
        echo "<div id='etudiants'>";
        while ($row=mysqli_fetch_array($result)){ 
            echo "<div id='etudiant'> <div id='nom_prenom'> ".$row['etu_nom']." ".$row['etu_prenom']."</div> <div id='annee_filiere'> ".$row['etu_filiere']." </div> </div>"; 
            }
        echo "</div>";
        
    }

    // si on a pas d'année :
    elseif ($annee=="pas_annee" && $filiere!="pas_filiere"){
        //affichage des élèves en fonction de la filière selectionnée
        echo "<p>Elèves de ".$filiere." : </p>";
        $sql = "SELECT e.prenom AS etu_prenom, e.nom AS etu_nom, p.annee AS etu_annee FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            WHERE f.nom_filiere = '{$filiere}'";
        $result=mysqli_query($conn, $sql);
        echo "<div id='etudiants'>";
        while ($row=mysqli_fetch_array($result)){ 
            echo "<div id='etudiant'> <div id='nom_prenom'> ".$row['etu_nom']." ".$row['etu_prenom']."</div> <div id='annee_filiere'> ".$row['etu_annee']." </div> </div>"; 
            }
        echo "</div>";
        
    }

    elseif($annee!="pas_annee" && $filiere!="pas_filiere"){
        $sql = "SELECT e.prenom AS etu_prenom, e.nom AS etu_nom, f.nom_filiere AS etu_filiere FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere
            WHERE p.annee = '{$annee}' 
            AND f.nom_filiere = '{$filiere}'";
        $result=mysqli_query($conn, $sql);
        if (mysqli_num_rows($result)>0) {
            echo "<p>Elèves de ".$filiere." en ".$annee." : </p>";
            echo "<div id='etudiants'>";
            while ($row=mysqli_fetch_array($result)){ 
                echo "<div id='etudiant'>".$row['etu_nom']." ".$row['etu_prenom']."</div>"; 
                }
            echo "</div>";
            }
        else{
            echo "<p id='erreur_recherche'>Il n'y a pas d'étudiants correspondant à la recherche : ".$filiere." en ".$annee.".</p>";
        }
    }
        
    

}
// si on a pas de confidion on affiche toute la liste
else {
    $sql = "SELECT e.prenom AS etu_prenom, e.nom AS etu_nom, f.nom_filiere AS etu_filiere, p.annee AS etu_annee FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere";
    $result=mysqli_query($conn, $sql);
    echo "<div id='etudiants'>";
    while ($row = mysqli_fetch_array($result)){ 
        echo "<div id='etudiant'> <div id='nom_prenom'> ".$row['etu_nom']." ".$row['etu_prenom']."</div> <div id='annee_filiere'> " .$row['etu_annee']." " .$row['etu_filiere']."</div> </div>"; 
    }
    echo "</div>";
} 

?>