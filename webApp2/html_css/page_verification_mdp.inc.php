<link rel="stylesheet" type="text/css" href="css/connexion.css">


<?php
if( isset( $_POST["inscription_ok"])){

  //vérification si personne prof ou etu
  $sql1="SELECT mail, password, password_updated FROM LNM_etudiant WHERE mail LIKE'".$_POST["id"]."'";
  $result1 = mysqli_query($conn, $sql1) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql1);
  $val= mysqli_fetch_array($result1);
  if ($val){
    //Vérification mdp
    if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
      $_SESSION["connecte"]=true; 
      $_SESSION["mail"]=$_POST["id"];
      $_SESSION["type"]="etudiant";
    }
    //Mdp pas encore changé
    else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
      $mail = $_POST['id'];
      $_SESSION["type"]="etudiant";
      echo"<div id= principal>";
      echo "<div id='requete'><h1 id= textprincipal>Initialisation du mot de passe</h1>";
      echo "<form action='?page=verification_inscription' method='post'>";
      echo "<p>(Utilisateur : ".$mail.")</p>";
      echo "<input class=champRecherche type='password' name='mdp1' placeholder='Mot de passe' required><br>";
      echo "<input class =champRecherche type='password' name='mdp2' placeholder='Confirmer mot de passe' required><br>";
      echo "<input type='hidden' name='id' value='".$mail."'>";
      echo "<input id=bouton type='submit' value='Valider'>";
      echo "</div>";
      echo"</div>";
    }
    else{
      echo "<script>alert('Erreur - Identifiants incorrects !')</script>";
      echo "<script>window.location.href='?page=connexion'</script>";
    }
  }
  else{
    $sql2="SELECT mail, password FROM LNM_enseignant WHERE mail LIKE'".$_POST["id"]."'";
    $result2 = mysqli_query($conn, $sql2) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql2);
    $val= mysqli_fetch_array($result2);
    //Vérification mdp
    if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
      $_SESSION["connecte"]=true; 
      $_SESSION["mail"]=$_POST["id"];
      $_SESSION["type"]="enseignant";
    }
    //Mdp pas encore changé
    else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
      $mail = $_POST['id'];
      $_SESSION["type"]="enseignant";
      echo"<div id= principal>";
      echo "<div id='requete'><h1 id= textprincipal>Initialisation du mot de passe</h1>";
      echo "<form action='?page=verification_inscription' method='post'>";
      echo "<p>(Utilisateur : ".$mail.")</p>";
      echo "<input class=champRecherche type='password' name='mdp1' placeholder='Mot de passe' required><br>";
      echo "<input class =champRecherche type='password' name='mdp2' placeholder='Confirmer mot de passe' required><br>";
      echo "<input type='hidden' name='id' value='".$mail."'>";
      echo "<input id=bouton type='submit' value='Valider'>";
      echo "</div>";
      echo"</div>";
    }
    else{
      echo "<script>alert('Erreur - Identifiants incorrects !')</script>";
      echo "<script>window.location.href='?page=connexion'</script>";
    }
  }

  //redirection
  echo "<script>window.location.href='?page=accueil'</script>";
}
?>
