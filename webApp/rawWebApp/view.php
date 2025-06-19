<?php
session_start();
require_once("../config.php");
require_once("functions_db.php");
require_once("get_data.php"); 
require_once("db.php");
include("connectDB.php"); 



if (isset($_SESSION['start']) && (time() - $_SESSION['start'] > $_SESSION['timeout'])) {
  include("logout.php"); 
 }else if(isset($_SESSION['start'])){
  $_SESSION['start'] = time();
 }

$sessionId = session_id();
  
initViewOfExplicitFKOfUpdatable($conn);

//print("<section>");
print("<div id=\"tabsselector\">");

$groups = get_group_of_views($conn);
while ($group = mysqli_fetch_row($groups)) {
  print("<a href=\"#" . $group[0] . "\">" . $group[0] . "</a>&nbsp;");
 }
print("</div>");

$views = get_views($conn);

print("<div class=\"items\">");
$group_of_views = "No group";
print("<div id=\"defaulttab\class =\"tabcontent\" <!-- by default, show no section --> ");

while ($view = mysqli_fetch_row($views)) {
  $view_name = $view[0];
  $request = $view[2];
  if($group_of_views != $view[1]){
    $group_of_views = $view[1];
    print("</div>");
    print("<div id=\"" .  $group_of_views . "\" class=\"tabcontent\">");
  }
  $request = sprintf($request, $sessionId);
  //print($request);
  get_view($conn,  $view_name, $request);
}

mysqli_close($conn);
print("</div></div>");

	  
?>
