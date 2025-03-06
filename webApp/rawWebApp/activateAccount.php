<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Learnagement</title>
    <link href="inc/css/style.css" rel="stylesheet" type="text/css">
    
  </head>
  <body>
    <p>
   
   To activate (or change your password of) your account, send the hash of your password to Learnagement admin. </br>
   WARNING! Communications are not crypted, do not use a main password.
    </p>
   <form action="activateAccount.php" method='post'>
    <input type="password" id="pwd" name="password" autocomplete="off" /></br>
    <input type="submit" value="hash" /></br>
    <?php
     if ( isset($_POST['password']) && $_POST['password'] != "") {
       print(password_hash($_POST['password'], PASSWORD_DEFAULT));
     }
     ?>
</form>
  </body>
</html>
