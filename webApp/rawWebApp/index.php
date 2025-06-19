<?php
session_start();
require_once("../config.php");
loadEnv("..");
require_once("functions.php");
require_once("functions_filter.php");
if(!isset($_SESSION["loggedin"])){
  $_SESSION['loggedin'] = false;
  $_SESSION['start'] = time();
  
  $sessionId = session_id();
  include("connectDB.php");
  
  initFilter($conn, "NULL", $sessionId);
 
 }
$_SESSION['timeout'] = $_ENV["SESSION_TIMEOUT"];
?>
  
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Learnagement</title>
    <link href="inc/css/style.css" rel="stylesheet" type="text/css">
  </head>
  <body class="loggedin" onload="setMain(getCookie('mainPage')); setCollapsible();">
    <header>
      <h1>Learnagement</h1>
    </header>
    <nav class="navtop">
      <div>
    <a href="#" onclick="setMain('view.php');">View</a>
   <?php
    if($_SESSION['loggedin']){
      print("<a href=\"#\" onclick=\"setMain('modif.php');\">Manage</a>\n");
      print("<a href=\"profil.php\"><i class=\"fas fa-user-circle\"></i>" . $_SESSION['userFirstname'] . " " . $_SESSION['userLastname'] . "</a>\n");
      print("<a href=\"logout.php\"><i class=\"fas fa-sign-out-alt\"></i>Logout</a>\n");
    }else{
      // set view as main page
      print("<script>
	    document.cookie = 'mainPage='.concat('', 'view.php').concat('','; SameSite=Strict');
	    </script>");
      print("<a href=\"login.php\"><i class=\"fas fa-sign-in-alt\"></i>Login</a>\n");
    }
    
   ?>
    <a href="activateAccount.php">Activate Account</a>

	   </div>
    </nav>
    <aside>
      <?php include("filter.php"); ?> 
    </aside>
    <main class="tabs">
      <?php include("view.php"); ?> 
    </main>
    <footer>
    <a href='https://github.com/FlavienVernier/learnagement'>Lernagement GitHub</a>
    </footer>

    <script type="text/javascript">

    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }


   function setCollapsible(){
   var coll = document.getElementsByClassName("collapsible");
   var i;
   
   for (i = 0; i < coll.length; i++) {
     coll[i].addEventListener("click", function() {
	 this.classList.toggle("active");
	 var content = this.nextElementSibling;
	 if (content.style.display === "block") {
	   content.style.display = "none";
	 } else {
	   content.style.display = "block";
	 }
       });
   }
 }

   function setMain(fileName){
    
   
   var xhr = typeof XMLHttpRequest != 'undefined' ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
   xhr.open('get', fileName, true);
   xhr.onreadystatechange = function() {
     if (xhr.readyState == 4 && xhr.status == 200) { 
       document.getElementsByTagName('main')[0].innerHTML = xhr.responseText;
       setCollapsible();
     } 
   }
   xhr.send();
   document.cookie = 'mainPage='.concat('', fileName).concat('',"; SameSite=Strict");
 }
</script>
  </body>
    
</html>
