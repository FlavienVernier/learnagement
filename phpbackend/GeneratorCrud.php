<?php
require_once("db_connection/connectDB.php");
include("./functions.php");
function ShowCreateCrud($conn, $name, $table, $columns)
{
  $pks=getPrimaryKeyFields($conn, $table);
  
    echo "include('./function_acction_allowed.php');\n";


    echo "\nfunction create$name(\$conn";
    echo (!empty($columns) ? ", $" . implode(", $", $columns) : "");
    echo "){";
    echo "\n  if(action_allowed('INSERT', '$table', NULL)){";
    echo "\n    \$sql = \"INSERT INTO `$table` (";
    echo (!empty($columns) ? "`" . implode("`, `", $columns) . "`" : "Array");;
    echo ") VALUES (";
    echo (!empty($columns) ? "'$" . implode("', '$", $columns) . "'" : "Array");
    echo ")\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    return \$res;";
    echo "\n  }else{";
    echo "\n    return ['No permission to INSERT into $table'];";
    echo "\n  }";
    echo "\n}\n";
    

    echo "\n/**";
    echo "\n* @\$conn data base connector";
    echo "\n* @\$primaryKeys array with primary key fields as keys and primary key values as values";
    echo "\n*/";    
    echo "\nfunction update$name(\$conn, \$primaryKeys, ";
    echo (!empty($columns) ? "\$" . implode(", \$", $columns) : "");
    echo "){";
    echo "\n  if(action_allowed('UPDATE', '$table', \$primaryKeys)){";

    $setClauses = [];
    foreach ($columns as $column) {
        $setClauses[] = " `$column`='\$$column'";
    }
    echo "\n    \$sql = \"UPDATE `$table` SET  ";
    echo   implode(',', $setClauses);
    echo " WHERE ";
    $setKeys = [];
    //for($i = 0; $i < count($pks); $i++) {
    foreach($pks as $pk){
      $setKeys[] = "`$pk` = '\$primaryKeys[\"$pk\"]'";
    }
    echo   implode(',', $setKeys);
    echo "\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    return \$res;";
    
    echo "\n  }else{";
    echo "\n    return ['No permission to UPDATE \$id line in $table'];";
    echo "\n  }";
    echo "\n}\n";

    echo "\n/**";
    echo "\n* @\$conn data base connector";
    echo "\n* @\$primaryKeys array with primary key fields as keys and primary key values as values";
    echo "\n*/";
    echo "\nfunction delete$name(\$conn,  \$primaryKeys){";
    echo "\n  if(action_allowed('DELETE', '$table', \$primaryKeys)){";
    echo "\n    \$sql = \"DELETE FROM `$table` WHERE ";
    $setKeys = [];
    //for($i = 0; $i < count($pks); $i++) {
    foreach($pks as $pk){
      $setKeys[] = "`$pk` = '\$primaryKeys[\"$pk\"]'";
    }
    echo   implode(',', $setKeys);
    echo "\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    return \$res;";

    echo "\n  }else{";
    echo "\n    return ['No permission to DELETE \$id line from $table'];";
    echo "\n  }";
    echo "\n}\n";

    
    echo "\nfunction list$name(\$conn){";
    echo "\n    \$sql = \"SELECT * FROM `$table`\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    \$rs = rs_to_table(\$res);";
    echo "\n    return \$rs;\n}\n";
}


//ShowCreateCrud("MAQUETTE_module", "MAQUETTE_module", ["id_module",
//    "code_module",
//    "nom",
//    "ECTS",
//    "id_discipline",
//    "id_semestre",
//    "hCM",
//    "hTD",
//    "hTP",
//    "hTPTD",
//    "hPROJ",
//    "hPersonnelle",
//    "id_responsable",
//    "id_etat_module",
//    "commentaire",
//    "modifiable"]);
/*ShowCreateCrud("LNM_filiere", "LNM_filiere", [
    "id_filiere",
    "nom_filiere",
    "nom_long",
    "id_responsable"
    ]);*/

ShowCreateCrud($conn, "LNM_stage", "LNM_stage", [
					 "entreprise", "intitule", "description", "ville", "date_debut", "date_fin", "nature", "id_etudiant", "id_enseignant"
    ]);
