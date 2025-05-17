<?php

require_once("functions.php");
require_once("db_connection/db.php");
/**
 *
 */
function initFilter($conn, $userId, $sessionId){

  // duote userId if not null
  if($userId != "NULL"){
    $userId = "\"" . $userId . "\"";
  }
  
  $req = "INSERT INTO `VIEW_parameters_of_views` (`id_parameters_of_views`, `userId`, `sessionId`, `id_enseignant`) VALUES (NULL," . $userId . ",\"" . $sessionId . "\", $userId)";

  $result = query($conn, $req);
}

/*
 * add filters in request
 */
function __addFiltersInRequest($conn, $request){
  $parameters = getParameters($conn); //FK => Value
  $foreignParam = getForeignKeys($conn, "VIEW_parameters_of_views"); // FK => Table
  $tablesOfRequest = __getTableFromRequest($conn, $request);

  //dispDICT("parameters", $parameters);
  //dispDICT("foreignParam", $foreignParam);
  //dispDICT("tablesOfRequest", $tablesOfRequest);
  
  $filter = "";
  foreach($tablesOfRequest as $table){
    $fk = array_search($table, $foreignParam);
    //print("table: " . $table . " fk: " . $fk . "</br>\n");
    if($fk && $parameters[$fk] != ""){
      $filter = $filter . $table . "." . $fk . " = \"" . $parameters[$fk] . "\" AND ";
    }
  }
  //print("filter: " . $filter .  "</br>\n");
  
  $filteredRequest = strstr($request, 'WHERE', true) . " WHERE " . $filter . substr(strstr($request, 'WHERE'), 5);

  return $filteredRequest;
}
?>
