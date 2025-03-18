<?php
  session_start();
  require_once("config.php");
  require_once("functions.php");
  require_once("functions_filter.php");
  include("connectDB.php");

  // Now we check if the data from the login form was submitted, isset() will check if the data exists.
  if ( !isset($_POST['username'], $_POST['password']) ) {
    // Could not get the data that should have been sent.
    exit('Please fill both the username and password fields!');
  }

  $userlogin = $_POST['username'];

  /*
   * get user id and hashed password
   */
  $login_req = "SELECT id_enseignant, prenom, nom, password FROM LNM_enseignant WHERE mail = \"$userlogin\"";
  $result = mysqli_query($conn, $login_req);

  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $req;
    echo 'error ' . mysqli_error($conn);
    exit;
  }


  if (mysqli_num_rows($result) > 0) {
    $row = mysqli_fetch_assoc($result);
    $id = $row["id_enseignant"];
    $firstname = $row["prenom"];
    $lastname = $row["nom"];
    $hashedPassword = $row["password"];
    // Account exists, now we verify the password.
    // Note: remember to use password_hash in your registration file to store the hashed passwords.
    if (password_verify($_POST['password'], $hashedPassword)) {
      // Verification success! User has logged-in!
      // Create sessions, so we know the user is logged in, they basically act like cookies but remember the data on the server.
      session_regenerate_id();
      $sessionId = session_id();
      $_SESSION['loggedin'] = true;
      $_SESSION['userLogin'] = $_POST['username'];
      $_SESSION['userId'] = $id;
      $_SESSION['userFirstname'] = $firstname;
      $_SESSION['userLastname'] = $lastname;
      $_SESSION['start'] = time();
    
      initFilter($conn, $id, $sessionId);
      
      header("Location: index.php");
      exit();
    }else {
      // Incorrect password
      echo 'Incorrect  password!';
      print('Incorrect username and/or password!');
    }
  }else{
    // Incorrect username
    echo 'Incorrect username!';
    print('Incorrect username and/or password!');
  }
?>
