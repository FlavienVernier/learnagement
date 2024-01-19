<?php

require_once("functions_filter.php");


/**
 *
 */
function get_view($conn, $view_name, $request){

  $request = __addFiltersInRequest($conn, $request);

  //print($request . "\n");
  
  print("<button type=\"button\" class=\"collapsible\">$view_name</button>");
  
  print("
   <article class=\"content\">
      <table>");
  

  /*  on suppose, bien entendu, que la vue existe  */
  
  $result = query($conn, $request);

  if (mysqli_num_rows($result) > 0) {
    print("<thead><tr>");
    $fields = mysqli_fetch_fields($result);
    foreach($fields as $field){
      print("<th>".$field->name."</th>");
    }
    print("</tr></thead>\n");
  }

  print("    <tbody>"); 

  while($ligne = mysqli_fetch_row ($result)){
    print("<tr>");
    foreach($ligne as $k=>$v){
      print("<td>".$v."</td>");
    }
    print("</tr>\n");
  }
  
  print("</tbody>");

  print("
      </table>
    </article>");

  mysqli_free_result($result);
}

/**
 *
 */
function get_updatable($conn, $table_name_displayed, $request){
  
  $request = __addFiltersInRequest($conn, $request);
  $table_name = __getTableFromRequest($conn, $request)[0];

  //print($request . "\n");
  //print("Table name: $table_name \n");
  
  /*
   * get the table primary K field 
   */
  $primaryKeys = getPrimaryKeyFields($conn, $table_name);
  //dispDict("pk", $primaryKeys);
  
  print("<button type=\"button\" class=\"collapsible\">$table_name_displayed</button>");
  
  print("
   <article class=\"content\">
      <table>");

  $result = query($conn, $request);
  $fields_type = [];
	
  if (mysqli_num_rows($result) > 0) {
    
    print("<thead><tr>");
    
    $fields = mysqli_fetch_fields($result);
    
    foreach($fields as $field){

      $fields_type[$field->name] = $field->type;
      
      if($field->name == $primaryKeys[0] && !isLinkingTable($conn, $table_name)){	
	print(""); // do not display K for base Table (not linking table)
      }else if ($field->name == "modifiable"){
	print(""); //do not display "modifiable" field
      }else if ($field->name == "id_responsable"){
	print(""); //do not display "responsible" field
      }else{
	print("<th>" . $field->name . "</th>");
      }
    }
     
    print("</tr></thead>\n");
  }

  $options = [];
  $foreinKeyFields = getForeignKeys($conn, $table_name); // FK => FTable
  foreach($foreinKeyFields as $fk => $table){
    $optionArray = getSecondaryKeys($conn, $table);
    $options[$fk] = "";
    $optionsP2S[$fk] = [];
    foreach($optionArray as $row){
      $options[$fk] = $options[$fk] . "<option value=\"" . $row["id"] . "\">" . $row["ExplicitSecondaryK"] . "</option>";
      $optionsP2S[$fk][$row["id"]] = $row["ExplicitSecondaryK"];
    }
  }
	
  print("    <tbody>");
  while($line = mysqli_fetch_assoc($result)){
    print("<tr>");
    $pk = -1;
    foreach($line as $k=>$v){

      if(($k == $primaryKeys[0]) && (!isLinkingTable($conn, $table_name))){
	$pk=$v;

	print("<form id='$table_name$pk' action='update_table.php' method='post' class='form-row'></form>");
	print("<input form='$table_name$pk' type='hidden' name='table' value=\"$table_name\">");
	// save primary key of base table (cannot be modified), tagged with '__old_' to be easily find in the $POST array 
	print("<input form='$table_name$pk' type='hidden' name='__old_$primaryKeys[0]' value=\"$v\">");

      }else if(($k == $primaryKeys[0]) && (isLinkingTable($conn, $table_name))){

	$pk = $line[$primaryKeys[0]] . "_" . $line[$primaryKeys[1]];
	
	print("<form id='$table_name$pk' action='update_table.php' method='post' class='form-row'></form>");
	print("<input form='$table_name$pk' type='hidden' name='table' value=\"$table_name\">");
	//save old 1st foreign key of primary key for linking table
	print("<input form='$table_name$pk' type='hidden' name='__old_" . $primaryKeys[0] . "' value=\"" . $line[$primaryKeys[0]] . "\">");
	//save old 2nd foreign key of primary key for linking table
	print("<input form='$table_name$pk' type='hidden' name='__old_" . $primaryKeys[1] . "' value=\"" . $line[$primaryKeys[1]] . "\">");

      }else if((isLinkingTable($conn, $table_name) && ($k == $primaryKeys[1]))){

	print(""); // do nothing, already manage previously

      }else if($k == "modifiable"){ // do not display modifiable field
	$modifiable = $v;
	
      }else if($k ==  "id_responsable"){ // do not display responsible
	
	$id_resp = $v;
	print("<input form='" . $table_name . "_pk' type='hidden' name='$k' value=\"$v\">");

      }else if($fields_type[$k] == "text"){ // big text fields (cannot be primary or foreign K)

	print("<td><textarea form='$table_name$pk' name='$k'>$v</textarea></td>");
	
      }else if(in_array($k, array_keys($foreinKeyFields))){ // Foreign Key
	
	print("<td><select id='$pk$k' form='$table_name$pk' name='$k'>");
	print("<option value=\"" . $v . "\">" . $optionsP2S[$k][$v] . "</option>");
	print("<option value=\"NULL\"> </option>");
	print($options[$k]);
	print("</select></td>");
	//print("<script>selectElement('$pk$k', '$v');<\script>");
	  
      }else if (isLinkingTable($conn, $table_name) || ($k != 0)){ // display other fields except primary key of base table (not linking table)
	
	print("<td><input form='$table_name$pk' type='text' name='$k' value=\"$v\"></td>");

      }
    }
      
    
    if($modifiable && isset($_SESSION['loggedin']) && $_SESSION['userId'] == $id_resp){
      print("<td>");
      print("<button form='$table_name$pk' type='submit' name='action' value='update'>Update</button>");
      print("<button form='$table_name$pk' type='submit' name='action' value='delete'>Delete</button>");
      print("</td>");
    }else{
      print("<td>");
      print("<button form='$table_name$pk' type='submit' name='action' value='update' disabled>Update</button>");
      print("<button form='$table_name$pk' type='submit' name='action' value='delete' disabled>Delete</button>");
      print("</td>");
    }
    print("</tr>\n");
  }
  print("</tbody>");
  
  print("
      </table>
    </article>");

  mysqli_free_result($result);
  
}
	
?>
