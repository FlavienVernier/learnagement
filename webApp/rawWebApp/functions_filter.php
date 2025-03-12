<?php

require_once("functions.php");
require_once("db.php");
/**
 *
 */
function initFilter($conn, $userId, $sessionId){

  // duote userId if not null
  if($userId != "NULL"){
    $userId = "\"" . $userId . "\"";
  }
  
  $req = "INSERT INTO `VIEW_parameters_of_views` (`id_parameters_of_views`, `userId`, `sessionId`) VALUES (NULL," . $userId . ",\"" . $sessionId . "\")";

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

/**
 * @return array of parameter field names
 */
function getParameterFields($conn){
  $fields = getFields($conn, "VIEW_parameters_of_views");

  // remove system parameter fields
  if (($key = array_search("id_parameters_of_views", $fields)) !== false) {
    unset($fields[$key]);
  }
  if (($key = array_search("userId", $fields)) !== false) {
    unset($fields[$key]);
  }
  if (($key = array_search("sessionId", $fields)) !== false) {
    unset($fields[$key]);
  }

  // return only parameter field names
  return fields;
}

/*
 * retrun dictionary paramField => paramValue
 */
function getParameters($conn){
  $sessionId = session_id();
  
  $param_req = "SELECT * FROM `VIEW_parameters_of_views` WHERE `sessionId` =  \"$sessionId\"";
  
  /*
   * get parameters fields
   */
  $result = mysqli_query($conn, $param_req);
  
  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $req;
    echo 'error ' . mysqli_error($conn);
    exit;
  }
  $parameters = mysqli_fetch_all($result, MYSQLI_ASSOC);

  return $parameters[0];
}
?>
