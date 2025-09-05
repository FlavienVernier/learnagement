<?php
function action_allowed($action, $table, $id){
  $user = $_SESSION['userId'];
  switch($action){
  case 'INSERT':
    // check if $user + $action + $table in  $_SESSION['permissions'];
    return true;
  case 'DELETE':
    // check if $user + $action + $table + $id in  $_SESSION['permissions'];
    return true;
  case 'UPDATE':
    // check if $user + $action + $table + $id in  $_SESSION['permissions'];
    return true;
  return false;
  }
}
