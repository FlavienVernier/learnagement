<?php
    /*
     * Session initialisation
     */
    session_start();
    require_once("config.php");

if(isset($_SESSION['loggedin'])){
    if (isset($_SESSION['start']) && (time() - $_SESSION['start'] > $_ENV["SESSION_TIMEOUT"])) {
       session_unset(); 
       session_destroy(); 
       echo "you were disconnected due to a session timeout"; 
    }
    $_SESSION['start'] = time();


    /*
     * Check user connection
     */
    if(!isset($_SESSION["username"])){
        /*header("Location: registration/login.php");
        exit();*/
        $username="anonymous";
    }else{
        $username=$_SESSION["username"];
    }

    /*
     * db connection and load requests
     */
    require_once("functions_db.php");
    require_once("get_data.php");
    require("connectDB.php");

    
    $sessionId = session_id();
    //print("-".$sessionId.".");

    //require("requests.php");

    //print("<section>");
    print("<div id=\"tabsselector\">");
 
    $groups = get_group_of_updatables($conn);
    while ($group = mysqli_fetch_row($groups)) {
      print("<a href=\"#" . $group[0] . "\">" . $group[0] . "</a>&nbsp;");
    }
    print("</div>");

    $updatables = get_updatables($conn);

    print("<div class=\"items\">");
    $group_of_views = "No group";
    print("<div id=\"defaulttab\class =\"tabcontent\" <!-- by default, show no section --> ");

    while ($table = mysqli_fetch_assoc($updatables)) {
      $table_name = $table["table_name"];
      $table_name_displayed = $table["table_name_displayed"];
      $request = $table["request"];
      if($group_of_views != $table["group_of_views"]){
	$group_of_views = $table["group_of_views"];
	print("</div>");
	print("<div id=\"" .  $group_of_views . "\" class=\"tabcontent\">");
      }
      $request = sprintf($request, $sessionId);
      //print($request);
      get_updatable($conn,  $table_name, $table_name_displayed, $request);
    }
    
    mysqli_close($conn);
    print("</div></div>");
    
 }else{
  header('location: login.php');
 }
?>
