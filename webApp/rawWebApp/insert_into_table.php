<?php

session_start();
require_once("config.php");
include("connectDB.php");
require_once("functions.php");

if (isset($_POST['table'])) {
  
  //$responsibleIdsToInsert = getResponsibleIdsToInsert($conn, $_POST['table']);

  //dispDict("_POST", $_POST);
  //dispDict("responsibleIdsToInsert", $responsibleIdsToInsert);
  
  $insertAllowed = false;

  $fieldsAndValues = [];
  foreach($_POST as $field => $value){
    if($field != "table"){
      $fieldsAndValues += [$field => "\"$value\""];
      /*      if(array_key_exists($field, $responsibleIdsToInsert)){
	if(in_array($resp, $responsibleIdsToInsert[$field])){
	  $insertAllowed = true;
	}
	}*/
    }
  }

  $resp = $_POST['id_responsable'];
  $responsibleIdsToInsert = getForeignResponsibleIds($conn, $_POST['table'], $fieldsAndValues);
  dispDict("responsibleIdsToInsert", $responsibleIdsToInsert);
  if(in_array($resp, $responsibleIdsToInsert)){
    $insertAllowed = true;
  }
 
  if(!isset($_SESSION['loggedin']) || !$_SESSION['userId'] == $resp){
    $insertAllowed = false;
    print("Insert not allowed: No or bad loggin!");
    exit();
  }
    
  
  if($insertAllowed){
    $query = "INSERT INTO " . $_POST['table'] . "(" . implode(", ", array_keys($fieldsAndValues)) . ") VALUES ( " . implode(", ", $fieldsAndValues) . ")";
    $query = str_replace("\"\"", "Null", $query);
    //print($query);
    
    mysqli_query($conn, $query);
    header('location: index.php');
  }else{
    print("Insert not allowed: bad responsible!");
  }
}
?>
