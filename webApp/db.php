<?php

    require_once("config.php");
    require_once("functions.php");


/*
 * wrap  mysqli_query and check result
 */

function query($conn, $req){
  //print($req);
  $result = mysqli_query($conn, $req);
  
  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $req;
    echo 'error ' . mysqli_error($conn);
    exit;
  }
  
  return $result;
}

/*
 * return array of table names extracted from SQL request
 */
function __getTableFromRequest($conn, $request){
  
  $req = "EXPLAIN " . $request;
  $result = query($conn, $req);

  $tables = [];
  while ($row = mysqli_fetch_assoc($result)) {
    array_push($tables, $row["table"]);
  }
  return $tables;
}

// return request splitted in a dictionnary
function __buidSecondaryKeyRequest($conn, $table){

  global $mysql_db;

  //get primary K fields  
  $primaryKsFields = getPrimaryKeyFields($conn, $table);

  //get foreign K fields
  $foreignKsFields = getForeignKeys($conn, $table);

  // get secondary K fields
  $secondaryk_fields_req = "SELECT column_name FROM information_schema.statistics WHERE table_schema = \"$mysql_db\" AND table_name = \"$table\" AND INDEX_NAME = \"SECONDARY\"";

  $result = query($conn, $secondaryk_fields_req);

  $secondaryKFields = [];
  if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_row($result)) {
      array_push($secondaryKFields, $row[0]);
    }
  }

  $requestAsDict["SELECT"] = [];
  $requestAsDict["SELECT_PRIM"] = [];
  foreach($primaryKsFields as $primaryKField){
    array_push($requestAsDict["SELECT_PRIM"], $table . "." . $primaryKField);
  }
  $requestAsDict["FROM"] = "";
  $requestAsDict["MAINTABLE"] = "$table";
  foreach($secondaryKFields as $secondaryKField){
    // if the secondary K field is a foreignK
    if(in_array($secondaryKField, array_keys($foreignKsFields))){
      
      $subRequestAsDict = __buidSecondaryKeyRequest($conn, $foreignKsFields[$secondaryKField]);
      
      $requestAsDict["SELECT"] = array_merge($requestAsDict["SELECT"], $subRequestAsDict["SELECT"]);
      $requestAsDict["SELECT_PRIM"] = array_merge($requestAsDict["SELECT_PRIM"], $subRequestAsDict["SELECT_PRIM"]);
      //dispDICT("requestAsDict after SELECT", $requestAsDict);  
      $requestAsDict["FROM"] = $requestAsDict["FROM"] . " JOIN " . $subRequestAsDict["MAINTABLE"] . " ON " . $subRequestAsDict["MAINTABLE"] . "." . getPrimaryKeyFields($conn, $foreignKsFields[$secondaryKField])[0] . " = " . $table . "." . $secondaryKField . $subRequestAsDict["FROM"];
      //dispDICT("requestAsDict AFTER FROM", $requestAsDict);  
    }else{  
      $requestAsDict["SELECT"] = array_merge($requestAsDict["SELECT"], [$table . "." . $secondaryKField]);
    }
  }
  
  //dispDICT("requestAsDict", $requestAsDict);  
  return $requestAsDict;
}

function buidSecondaryKeyRequest($conn, $table){
  //print("</br>TABLE: " . $table . "</br>");

    $primaryKeyField = getPrimaryKeyFields($conn, $table)[0];

    $secondaryKeyRequestAsDict = __buidSecondaryKeyRequest($conn, $table);
    
  $secondaryKeyRequestAsDict["SELECT"] = implode(", ", $secondaryKeyRequestAsDict["SELECT"]);
  $secondaryKeyRequestAsDict["SELECT_PRIM"] = implode(", ", $secondaryKeyRequestAsDict["SELECT_PRIM"]);
  $secondaryKeyRequestAsDict["FROM"] = $table . " " . $secondaryKeyRequestAsDict["FROM"];

 
    $secondaryKeyRequest = "CREATE OR REPLACE VIEW ExplicitSecondaryKs_" . $table . " AS SELECT $primaryKeyField AS id, CONCAT_WS(\" \", " . $secondaryKeyRequestAsDict["SELECT"] . ") AS ExplicitSecondaryK, " . $secondaryKeyRequestAsDict["SELECT_PRIM"] . " FROM " . $secondaryKeyRequestAsDict["FROM"];

    //print($secondaryKeyRequest . "</br>");
    query($conn, $secondaryKeyRequest);
}
/*
 * create view of FK for each table updatable
 * an updatable table is 1st table of each requeste of VIEW_updatable
 * created view contains following fields:
 * (table_name, fk_fields, fk_table, fk_values, fk_explicit)
 * fk_values contains all primary keys of fk_table
 * fk_explici contains coresponding concatened secondary keys of fk_table
 */
function initViewOfExplicitFKOfUpdatable($conn){

  // for each foreign table of updatable table, generate the explicit (human readable) secondary keys views
  
  $request = "SELECT table_name, request FROM VIEW_updatable";

  $result = query($conn, $request);

  $tables = [];
  while ($row = mysqli_fetch_assoc($result)) {
    $request =  $row["request"];
    //$table = __getTableFromRequest($conn, $request)[0];
    $table = $row["table_name"];

    //get foreign Ks fields
    $foreignKeysFields = getForeignKeys($conn, $table);

    //dispDict($table, $foreignKsFields);
    foreach($foreignKeysFields as $foreignTable){
      buidSecondaryKeyRequest($conn, $foreignTable);
    }
  }

  

  
}


?>
