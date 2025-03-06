<?php

session_start();
require_once("config.php");
include("connectDB.php");
include("functions.php");

dispDict("_POST", $_POST);

if (isset($_POST['table'])) {

  $pk = getPrimaryKeyFields($conn, $_POST['table']);
  
  $updates = [];
  foreach($_POST as $field => $value){
    if($field != "table" && !str_starts_with($field, '__old_') && $field != "action"){
      if(empty($value)){
	array_push($updates, $field . " = NULL");
      }else if($value == "NULL"){
	array_push($updates, $field . " = NULL");	
      }else{
	array_push($updates, $field . " = \"$value\"");
      }
    }else{
      
    }
  }
  if(isLinkingTable($conn, $_POST['table'])){
    $pk0 = '__old_' . $pk[0];
    $pk1 = '__old_' . $pk[1];
    if($_POST['action'] == "update"){
      $query = "UPDATE " . $_POST['table'] . " SET " . implode(", ", $updates) . " WHERE " . $pk[0] . " = " . $_POST[$pk0] . " AND " . $pk[1] . " = " . $_POST[$pk1];
    }else if($_POST['action'] == "delete"){
      $query = "DELETE FROM ". $_POST['table'] . " WHERE " . $pk[0] . " = " . $_POST[$pk0] . " AND " . $pk[1] . " = " . $_POST[$pk1];
    }
  }else{
    $pk0 = '__old_' . $pk[0];
    if($_POST['action'] == "update"){
      $query = "UPDATE " . $_POST['table'] . " SET " . implode(", ", $updates) . " WHERE " . $pk[0] . " = " . $_POST[$pk0];
    }else if($_POST['action'] == "delete"){
      $query = "DELETE FROM ". $_POST['table'] . " WHERE " . $pk[0] . " = " . $_POST[$pk0];
    }
 }
  //print($query);
  mysqli_query($conn, $query);
  header('location: index.php');
}
?>
