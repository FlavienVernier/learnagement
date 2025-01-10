<link rel="stylesheet" href="css/page_etudiant.inc.css"/>

<?php
// le mail de l'utilisateur est récupéré dans l'url 
$mail=$_SESSION["mail"];
$sql_etu = "(SELECT id_etudiant FROM LNM_etudiant e WHERE e.mail LIKE '".$mail."')";

/* Lancement du fichier de scraping des informations de l'étudiant */
/*$pythonScript='../python/scraping_polypoint_stage.py';
$output=shell_exec('python ' . $pythonScript);
 */

$sql="SELECT nom, prenom FROM LNM_etudiant e WHERE e.mail='".$mail."'"; //mail : correspond au mail universitaire entrée par la personne dans la page de connexion
$result=mysqli_query($conn, $sql);
$row=mysqli_fetch_array($result);

echo "<h2> Page étudiante - ".$row['nom']." ".$row['prenom']." </h2>";

//Menu pour les étudiants
echo "<ul id='menu'>";
echo "</ul>";

//Partie sur les polypoints
echo "<h3> Polypoints : </h3>";
// affichage par année
$sql_annee="SELECT DISTINCT annee_universitaire AS annee FROM ETU_polypoint WHERE id_etudiant= ".$sql_etu."";
$result=mysqli_query($conn, $sql_annee);
while($row = mysqli_fetch_array($result)){
    $annee=$row["annee"];
    $sql_somme="SELECT SUM(nb_point) AS somme_polypoint, annee_universitaire AS annee FROM ETU_polypoint WHERE annee_universitaire='".$annee."' AND id_etudiant=".$sql_etu."";
    $result_somme=mysqli_query($conn, $sql_somme); // on obtient un int
    $row_somme=mysqli_fetch_array($result_somme);
    $somme=strval($row_somme["somme_polypoint"]);
    if($somme>1){
        echo "<p id=polypoints_par_annee> Année ".$annee." : ".$somme." polypoints enregistrés </p>";
    }
    if($somme==1){
        echo "<p id=polypoint_par_annee> Année ".$annee." : ".$somme." polypoint enregistré </p>";
    }
}


// affichage de la liste de polypoints
$sql="SELECT intitule, tache, nb_point, annee_universitaire FROM ETU_polypoint p WHERE p.id_etudiant=".$sql_etu."";
$result=mysqli_query($conn, $sql);

//si on a des données associées à des polypoints :
if ($row = mysqli_fetch_array($result)){
    echo "<table id='polypoints'>";
    echo "<tr id='entete_polypoints'>
            <th>Action</th>
            <th>Détail</th>
            <th>Nombre</th>
            <th>Année concernée</th>
        </tr>";
    // insertions des données de polypoint dans un tableau
    do {
        echo "<tr>";
        echo "<td id='intitule_polypoints'>".$row['intitule']."</td>";
        echo "<td id='tache_polypoints'>".$row['tache']."</td>";
        echo "<td id='nb_polypoints'>".$row['nb_point']."</td>";
        echo "<td id='annee_polypoints'>".$row['annee_universitaire']."</td>";
        echo "</tr>";
    }
    while ($row = mysqli_fetch_array($result)); // tant qu'on a une ligne de résultat
    echo "</table>";
}
// si on a pas de polypoints :
else{
    echo  "<p id='pas_donnee'>Aucun polypoint enregistré. \nN'oubliez pas d'effectuer différentes actions dans l'année scolaire.</p>";
}




//Partie sur les stages
echo "<h3> Stages : </h3>";

$sql="SELECT date_debut, date_fin, entreprise, nature FROM LNM_stage s WHERE s.id_etudiant=".$sql_etu."";
$result=mysqli_query($conn, $sql);
// si on a déjà des stages d'enregistrés : 
if ($row = mysqli_fetch_array($result)){
    echo "<table id='stages'>";
    echo "<tr id='entete_stages'>
            <th>Dates </th>
            <th>Entreprise</th>
            <th>Nature</th>
        </tr>";
        // insertions des données des stages dans un tableau
        do{
            echo "<tr>";
            echo "<td id='dates_stage'>".$row['date_debut']." - ".$row['date_fin']."</td>";
            echo "<td id='entreprise_stage'>".$row['entreprise']."</td>";
            echo "<td id='nature_stage'>".$row['nature']."</td>";
            echo "</tr>";
        }
        while ($row = mysqli_fetch_array($result)) ;// tant qu'on a une ligne de résultat
        echo "</table>";
}
// si on a pas de stages enregistrés :
else{
    echo  "<p id='pas_donnee'>Aucun stage n'est connu du service. \nN'oubliez pas de faire vos demandes sur l'intranet.</p>";
}





?>