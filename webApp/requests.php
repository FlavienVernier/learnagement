<?php

// get parameters according to the session
$param_req = "SELECT * FROM `INFO_vue_parameters` WHERE `sessionId` =  \"$sessionId\"";


// get all views
$vues_req = "SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_TYPE = \"VIEW\" AND TABLE_NAME LIKE \"INFO_vue_%\"";

// get all tables
$tables_req = "SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_TYPE = \"BASE TABLE\" AND TABLE_NAME LIKE \"INFO_%\"";


// get view column names
$columns_vue_req = "SHOW COLUMNS FROM $vue_name";

// get view column names
$columns_table_req = "SHOW COLUMNS FROM $table_name";

// get view content
$vue_req = " SELECT * FROM  $vue_name WHERE 1 ";

// get table content
$vue_req = " SELECT * FROM  $table_name WHERE 1 ";



// get explicit secondary Key
$secondaryK_req = "SHOW INDEXES FROM $table_name WHERE `Key_name`=\"SECONDARY\"";

// get foreign keys of a table
$foreignK_req = "SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = $mysql_db AND TABLE_NAME = $table_name";
?>
