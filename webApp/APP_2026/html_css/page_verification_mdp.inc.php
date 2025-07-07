<link rel="stylesheet" type="text/css" href="css/connexion.css">


<?php

loadEnv("../..");

if( isset( $_POST["inscription_ok"])){

  //vérification si personne prof ou etu
  $sql1="SELECT id_etudiant, mail, password, password_updated FROM LNM_etudiant WHERE mail LIKE'".$_POST["id"]."'";
  $result1 = mysqli_query($conn, $sql1) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql1);
  $val= mysqli_fetch_array($result1);

  if ($val){
    //Si étudiant
    //Vérification mdp
    if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
      $_SESSION["connecte"]=true; 
      $_SESSION["mail"]=$_POST["id"];
      $_SESSION["type"]="etudiant";
      $_SESSION["id_etudiant"]=$val['id_etudiant'];
      //redirection
      echo "<script>window.location.href='?page=accueil'</script>";
    }
    //Mdp pas encore changé
    else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
      $mail = $_POST['id'];
      $_SESSION["type"]="etudiant";
      $_SESSION["id_etudiant"]=$val['id_etudiant'];
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
  else if ($val == NULL) {
      $sql2="SELECT id_enseignant, mail, password, password_updated FROM LNM_enseignant WHERE mail LIKE'".$_POST["id"]."'";
      $result2 = mysqli_query($conn, $sql2) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql2);
      $val= mysqli_fetch_array($result2);

      /*$url = $_ENV['PHP_BACKEND_DOCKER_URL'] . "/connection/authenticate.php";
      $data = ['username' => $_POST["id"], 'password' => $_POST['mdp']];

      // use key 'http' even if you send the request to https://...
      $options = [
          'http' => [
              'header' => "Content-type: application/x-www-form-urlencoded\r\n",
              'method' => 'POST',
              'content' => http_build_query($data),
          ],
      ];

      $context = stream_context_create($options);
      $result = file_get_contents($url, false, $context);
      if ($result === false) {
          // Handle error
      }

      var_dump($result);
  }*/


      if($val){
      //Si enseignant
      //Vérification mdp
      if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
        $_SESSION["connecte"]=true; 
        $_SESSION["mail"]=$_POST["id"];
        $_SESSION["type"]="enseignant";
        $_SESSION["id_enseignant"]=$val['id_enseignant'];
        //redirection
        echo "<script>window.location.href='?page=accueil'</script>";
      }
      //Mdp pas encore changé
      else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
        $mail = $_POST['id'];
        $_SESSION["type"]="enseignant";
        $_SESSION["id_enseignant"]=$val['id_enseignant'];
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
    else {
      //Sinon c'est un administratif
      $sql3="SELECT mail, password, password_updated FROM LNM_administratif WHERE mail LIKE'".$_POST["id"]."'";
      $result3 = mysqli_query($conn, $sql3) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql3);
      $val= mysqli_fetch_array($result3);

      //Vérification mdp
      if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
        $_SESSION["connecte"]=true; 
        $_SESSION["mail"]=$_POST["id"];
        $_SESSION["type"]="administratif";
        $_SESSION["id_administratif"]=$val['id_administratif'];
        //redirection
        echo "<script>window.location.href='?page=accueil'</script>";
      }
      //Mdp pas encore changé
      else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
        $mail = $_POST['id'];
        $_SESSION["type"]="administratif";
        $_SESSION["id_administratif"]=$val['id_administratif'];
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
  }
    
  else{
    echo "<script>alert('Erreur - Identifiants incorrects !')</script>";
    echo "<script>window.location.href='?page=connexion'</script>";
  }

}
?>
