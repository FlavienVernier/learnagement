<?php
    require_once("../config.php");

 /**
  * get the table primary K fields. Only 1 for base table, 2 for linking table
   *
   * @param
   *
   * @param string $table_name table 
   *
   * @return array Return the primary key fields as array of string
   */
function getPrimaryKeyFields($conn, $table_name){

  global $mysql_db;
  
  $primaryKeyField_req = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \"$mysql_db\" AND COLUMN_KEY = 'PRI' AND table_name = \"$table_name\"";

  $table = mysqli_query($conn, $primaryKeyField_req);
  if (!$table) {
    echo 'Impossible d\'exécuter la requête : ' . $req;
    echo 'error '.mysqli_error();
    exit;
  }

  /*
   * get K
   */
  $primaryKFields = [];
  if (mysqli_num_rows($table) > 0) {
    while($fieldRow = mysqli_fetch_row($table)){
      array_push($primaryKFields, $fieldRow[0]);
    }
  }

  mysqli_free_result($table); // free result memory space

  return $primaryKFields;
  }


  /**
   * @deprecated get the table primary K field (use getPrimaryKeyFields instead)
   *
   * @param
   *
   * @param string $table_name table 
   *
   * @return string Return the primary key
   */
function getPrimaryKeyField($conn, $table_name){

  return getPrimaryKeyFields($conn, $table_name)[0];
}

/**
   * get the table primary K values
   *
   * @param
   *
   * @param string $table_name table 
   *
   * @return array Return the primary key values as array of string
   */
function getPrimaryKeyValues($conn, $table_name){
  $primaryKFields = implode( ", ", getPrimaryKeyFields($conn, $table_name));
  
  $primaryKeyValues_req = "SELECT $primaryKFields FROM $table_name";
  $result = mysqli_query($conn, $primaryKeyValues_req);
  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $primaryKeyValues_req;
    echo 'error '.mysqli_error();
    exit;
  }
  $primaryKeyValues = [];
  if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_row($result)) {
      array_push($primaryKeyValues,$row[0]);
    }
  }
  return $primaryKeyValues;
}


/**
 * return a array of row, each row is a dictionnary:
 * row["id"] => primariKeyValue
 * row["ExplicitSecondaryK"]=> explitSecondaryKeyValue
 * only for foreign tables of updatable tables
 */
function getSecondaryKeys($conn, $table){
  
  $table_name = "ExplicitSecondaryKs_" . $table;

  $table_fields = getFields($conn, $table_name);
  $parameters = getParameters($conn);
  $filterFields =  array_intersect($table_fields, array_keys($parameters));

  $table_req = "SELECT * FROM $table_name WHERE 1 ";
  foreach($filterFields as $filterField){
    if($parameters[$filterField] != ""){
      $table_req = $table_req . " AND $table_name.$filterField = \"$parameters[$filterField]\" ";
    }
  }

  //print("</br>" . $table_req . "</br>");
    
  $result = query($conn, $table_req);

  $secondaryKeys = mysqli_fetch_all($result, MYSQLI_ASSOC);

  return $secondaryKeys;
}

/**
 * DEPRECATED
 * return explicit secondary K values as a string for a given primary K.
 */
function getSecondaryKeyValue($conn, $reference_table_name, $primary_value){

  global $mysql_db;

  // get primary K fields
  $primaryKFields = getPrimaryKeyFields($conn, $reference_table_name);
  // Theoriticaly there is only one field
  
  //get foreign Ksfields
  $foreignKsFields = getForeignKeys($conn, $reference_table_name);
   
  // get secondary K fields
  $secondaryk_fields_req = "SELECT column_name FROM information_schema.statistics WHERE table_schema = \"$mysql_db\" AND table_name = \"$reference_table_name\" AND INDEX_NAME = \"SECONDARY\"";

  $result = mysqli_query($conn, $secondaryk_fields_req);

  $secondaryKFields = [];
  if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_row($result)) {
      array_push($secondaryKFields, $row[0]);
    }
  }
    
  $secondaryKString = implode(", ", $secondaryKFields);
    
  // get secondary K values
  $secondaryk_values_req = "SELECT $secondaryKString FROM $reference_table_name WHERE $primaryKFields[0] = \"$primary_value\"";
  
  $result = mysqli_query($conn, $secondaryk_values_req);
  $secondaryKValues = [];
  if (mysqli_num_rows($result) > 0) {
    $secondaryKValues = mysqli_fetch_row($result); //get secondary K values of given primary K
  }
  
  foreach($secondaryKFields as $index => $secondaryKField){
    if (in_array($secondaryKField, array_keys($foreignKsFields))){
      $secondaryKValues[$index] = getSecondaryKeyValue($conn, $foreignKsFields[$secondaryKField], $secondaryKValues[$index]);
    }
  }
  
  return implode(", ", $secondaryKValues);
}

/**
 * return explicit secondary K values for all primary Ks as dictionary primaryKValue => secondaryKvalue.
 */
function getPrimarySecondaryKeyValues($conn, $reference_table_name){

  $primaryKValues = getPrimaryKeyValues($conn, $reference_table_name);
  
  $primarySecondaryKeyValues = [];
  foreach($primaryKValues as $primaryKValue){
    $primarySecondaryKeyValues[$primaryKValue] = getSecondaryKeyValue($conn, $reference_table_name, $primaryKValue);
  }
  //dispDict("primarySecondaryKeyValues", $primarySecondaryKeyValues);
  asort($primarySecondaryKeyValues);
  return $primarySecondaryKeyValues;
}

/**
 * @return array Return the dictionnary FK => table of reference for a given table
 */
function getForeignKeys($conn, $table_name){

  global $mysql_db;

  $foreignK_req = "SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = \"$mysql_db\" AND TABLE_NAME = \"$table_name\"";

  $result = mysqli_query($conn, $foreignK_req);
  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $foreignK_req;
    echo 'error '.mysqli_error();
    exit;
  }

  $foreignKeys = [];
  if (mysqli_num_rows($result) > 0) {
    while ($foreignKey = mysqli_fetch_row($result)) {
      $foreignKeys += [$foreignKey[1] => $foreignKey[3]]; // add entry FK => ref table
    }
  }
  return $foreignKeys;
}



/**
 * @return array of field names ordered according db server order
 */
function getFields($conn, $table_name){
  $fieldsName_req = "SHOW COLUMNS FROM $table_name";

  $result = mysqli_query($conn, $fieldsName_req);
  
  if (!$result) {
    echo 'Impossible d\'exécuter la requête : ' . $foreignK_req;
    echo 'error '.mysqli_error();
    exit;
  }

  $fields = [];
  if (mysqli_num_rows($result) > 0) {
    while ($row = mysqli_fetch_row($result)) {
      array_push($fields, $row[0]);
    }
  }
  return $fields;
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

/*
 * WORK IN PROGRESS
 */
function getFilteredDependencies($conn, $table_name){

  $table_fields = getFields($conn, $table_name);
  $parameters = getParameters($conn);
  $filterFields =  array_intersect($table_fields, array_keys($parameters));

  $depedencies = [];
  foreach($filterFields as $field){
    $depedencies[$field] = $table_name;
  }

  $foreignKs = getForeignKeys($conn, $table_name);

  foreach($foreignKs as $foreignK => $foreignTable){
    $depedencies[$foreignK] = getFilteredDependencies($conn, $foreignTable);
  }

  return $dependencies;
}

/*
 * WORK IN PROGRESS
 *
 * return formated request
 */
function __dependencies2request($select, $dependencies, $parameters){
  $request = $select;
  $request = $request . " FROM ";
}


/**
 * DEPRECATED ?
 */
function getTableData($conn, $table_name, $fields, $id_responsable){

  $table_fields = getFields($conn, $table_name);
  //dispDICT("table_fields", $table_fields);
  
  $parameters = getParameters($conn);
  //dispDICT("parameters", $parameters);
  //dispDICT("parametersK", array_keys($parameters));

  $filterFields =  array_intersect($table_fields, array_keys($parameters));
  //dispDICT("filterFields", $filterFields);

  
  // get table content
  $table_req = " SELECT $fields FROM  $table_name WHERE id_responsable='$id_responsable' ";
  foreach($filterFields as $filterField){
    if($parameters[$filterField] != ""){
      $table_req = $table_req . " AND $table_name.$filterField = \"$parameters[$filterField]\" ";
    }
  }
  
  //print($table_req);
  
  $result  =   mysqli_query($conn, $table_req);  
    
  if ($result === FALSE){
    echo "la requ&ecirc;te a &eacute;chou&eacute; : ".mysqli_error();
    exit; // inutile de poursuivre le traitement dans ce cas
  }

  return $result; 
}

/**
 *
 */
function getKeysValuesResponsibles($conn, $table_name){

  global $mysql_db;

  $fields = getFields($conn, $table_name);

  //dispDict("fields", $fields);
  
  $keysValuesResponsibles = [];
  if(in_array("id_responsable", $fields)){
  
      $primaryKeyField = getPrimaryKeyField($conn, $table_name); // string of primary key field

      //$secondaryKeyFields = getSecondaryKeyFields($conn, $table_name); // array of string of secondary key fields
      
      $keysValuesResponsibles_req = "SELECT $primaryKeyField , id_responsable FROM $table_name";

      $result = mysqli_query($conn, $keysValuesResponsibles_req);
      if (!$result) {
	echo 'Impossible d\'exécuter la requête : ' . $keysValuesResponsibles_req;
	echo 'error '.mysqli_error();
	exit;
      }
  
      
      if (mysqli_num_rows($result) > 0) {
	while ($row = mysqli_fetch_row($result)) {
	  
 
	  //dispDict("row", $row);
	  $keysValuesResponsibles += [$row[0] => $row[1]]; // add entry FK => ref table
	}
      }
    }
    return $keysValuesResponsibles;
}

/**
 *
 
 *
 * reurn a dictionary  foreignK => id_responsible
 */
function getResponsibleIdsToInsert($conn, $table_name){

  $foreignKeys = getForeignKeys($conn, $table_name);

  //dispDict("foreignKeys", $foreignKeys);

  $inheritenceResponsability = [];
  foreach($foreignKeys as $foreignKey => $table){
    $keysValuesResponsibles = getKeysValuesResponsibles($conn, $table);
    //print("$foreignKey => $table :</br>");
    //dispDict("keysValuesResponsibles", $keysValuesResponsibles);
    if(!empty($keysValuesResponsibles)){
      $inheritenceResponsability += [ $foreignKey => $keysValuesResponsibles];
    }
  }
  return  $inheritenceResponsability;
}


/*
 *
 */
function __getReponsibles($conn, $table_name, $primaryK_value){
  $fields = getFields($conn, $table_name);
  //dispDICT("fields", $fields);
  $responsibles = [];

  $primaryKField = getPrimaryKeyFields($conn, $table_name)[0]; //$table_name is logicaly a base table, so there is only one primary K 
  if(in_array("id_responsable", $fields)){ // If the table defines a responsible for each tuple
    $req="SELECT id_responsable FROM $table_name WHERE $primaryKField =" . __quoteValue($primaryK_value);
    //print("</br> $req </br>");
    $result = mysqli_query($conn, $req);
    if (!$result) {
      echo 'Impossible d\'exécuter la requête : ' . $req;
      echo 'error '.mysqli_error();
      exit;
    }
    
    if (mysqli_num_rows($result) > 0) {
      $responsibles += mysqli_fetch_row($result);
    }
  }else{ // If the table does not define a responsible for each tuple, look for a responsible in foreign table
    $req="SELECT * FROM $table_name WHERE $primaryKField = " . __quoteValue($primaryK_value);
    //print("</br> $req </br>");
    $result = mysqli_query($conn, $req);
    if (!$result) {
      echo 'Impossible d\'exécuter la requête : ' . $req;
      echo 'error '.mysqli_error();
      exit;
    }
    
    if (mysqli_num_rows($result) > 0) {
      $dict_fields_values = mysqli_fetch_assoc($result);
      $responsibles += getForeignResponsibleIds($conn, $table_name, $dict_fields_values);
    }
  }

  return $responsibles;
}
/**
 * Get recursively the responsible ids from foreign tables for a given tuple.
 * The recursivity is cross recursivity with "__getResponsible()".
 *
 * @return list of foreign responsible ids for a given tuple of a table
 */
function getForeignResponsibleIds($conn, $table_name, $dict_fields_values){
  //dispDict("dict_fields_values", $dict_fields_values);
  
  $foreignKeys = getForeignKeys($conn, $table_name);
  //dispDICT("foreignKeys", $foreignKeys);
  
  $reponsibleIds = [];
  foreach($foreignKeys as $foreignKey => $foreignTable){
    //print("</br>$foreignKey -> $foreignTable , \n");
    //print($dict_fields_values[$foreignKey] . "\n</br>");print("---\n");
    $reponsibleIds += __getReponsibles($conn, $foreignTable, $dict_fields_values[$foreignKey]);
  }

  return $reponsibleIds;
}

/**
 *
 */
function isInsertAllowed($conn, $table_name, $dict_fields_values, $userId){
  return in_array($userId, getForeignResponsibleIds($conn, $table_name, $dict_fields_values));
}

/**
 *
 *
 * @return Boolean Return true if the table is a linking table (more than one field in the primary key)
 */
function isLinkingTable($conn, $table_name){
  $primayK = getPrimaryKeyFields($conn, $table_name);

  return count($primayK) > 1;
}

/*
* @return return quoted value 
*/
function __quoteValue($value){
  if($value[0] != "\"" && $value[strlen($value)-1] != "\""){
    return "\"$value\"";
  }
  return $value;
}

function dispDict($dicName, $d){
  return(0); //comment to debug, uncomment for prod
  print("</br>$dicName:</br>");
  foreach($d as $k => $v){
    if(gettype($v) == "string")
      print($k . "=>" . $v ."</br>\n");
    else if(gettype($v) == "array")
      print($k . "=>" . dispDict($dicName."_SUB", $v) ."</br>\n");
  }print("</br>");
}


?>
