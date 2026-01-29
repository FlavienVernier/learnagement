<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Learnagement Web Sites</title>
    <link rel="stylesheet" href="./style.css">
    <link rel="icon" href="./favicon.ico" type="image/x-icon">
  </head>
  <body>
    <main>
      <h1>Choose your app</h1>
      <a href="./rawWebApp">Raw Web App</a></br>
      <a href="./APP_2026/learnagement.php">APP 2026</a></br>
        <?php
            require_once("config.php");
            loadEnv(".");
            print("<a href=" . $_ENV["NEXTAUTH_URL"] . ">L3 INFO SCEM 2025</a></br>")
        ?>
    </main>
  </body>
</html>
