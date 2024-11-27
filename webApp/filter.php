<?php
require_once("config.php");
require_once("functions.php");
   
$sessionId = session_id();


include("connectDB.php");


$parameterFieldsAndValues = getParameters($conn);
//dispDICT("parameterFieldsAndValues", $parameterFieldsAndValues);

/*
 * Get all foreign keys with their secondary keys values
 */
$forefnK_fields_values_dic = [];
$foreignKs = getForeignKeys($conn,  "VIEW_parameters_of_views");
foreach($foreignKs as $foreignK => $foreignTable){
  $psK_values_dic = getPrimarySecondaryKeyValues($conn, $foreignTable);
  $forefnK_fields_values_dic += [$foreignK => $psK_values_dic];
}
//dispDICT("forefnK_fields_values_dic", $forefnK_fields_values_dic);

/*
 * Diplay form
 */
print("
        <div class=\"paramview\">
            <form action=\"setViewParameters.php\" method=\"post\">
    ");


foreach($parameterFieldsAndValues as $parameter_field => $parameter_value){
  if($parameter_field != "id_parameters_of_views" && $parameter_field != "sessionId" && $parameter_field != "userId"){
    print("
	  <div class=\"form-group\">
              <div class=\"dropdown\">
                <label for=\"$parameter_field-select\">$parameter_field :</label>
                <select name=\"$parameter_field\" id=\"$parameter_field-select\">
	        <option value=\"\"></option>
          ");
    //<option value='$parameter_values[$parameter_field]'>$parameter_values[$parameter_field]</option>
    foreach($forefnK_fields_values_dic[$parameter_field] as $key => $value){
	    if($key == $parameterFieldsAndValues[$parameter_field]){
	      print("<option selected=\"selected\" value=\"$key\">$value</option>");
	    }else{
	      print("<option value=\"$key\">$value</option>");
	    }
	  }
     
	  print("
            </select>
          </div>
        </div>
	  ");
			}
    }
    print("
      <button type=\"submit\" name=\"submit\" value=\"Submit\" class=\"btn-validate\">Valider</button>
    </form>
  </div>
    ");	
?>
