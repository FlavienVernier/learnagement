<?php
include("db_connection/connectDB.php");
function ShowCreateCrud($name, $table, $columns)
{
    echo "function create$name(\$conn";
    echo (!empty($columns) ? ", $" . implode(", $", $columns) : "");
    echo ")\n{";
    echo "\n    \$sql = \"INSERT INTO `$table` (";
    echo (!empty($columns) ? "`" . implode("`, `", $columns) . "`" : "Array");;
    echo ") VALUES (";
    echo (!empty($columns) ? "'$" . implode("', '$", $columns) . "'" : "Array");
    echo ")\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    return \$res;\n}\n";

    echo "\n function delete$name(\$conn,  \$id)\n{";
    echo "\n    \$sql = \"DELETE FROM `$table` WHERE `id`=\$id\";";
    echo "\n    \$res = mysqli_query(\$conn, \$sql);";
    echo "\n    return \$res;\n}\n";

    echo "function update$name(\$conn, \$id,";
    echo (!empty($columns) ? "\$" . implode(", \$", $columns) : "");
    echo ")\n{";

    $setClauses = [];
    foreach ($columns as $column) {
        $setClauses[] = " `$column`='\$$column'";
    }
    echo "    \$sql = \"UPDATE `$table` SET  ";
    echo   implode(',', $setClauses);
    echo " WHERE `id` = \$id\";";
    echo "    \$res = mysqli_query(\$conn, \$sql);";
    echo "    return \$res;";
    echo "}\n";

    echo "\nfunction list$name(\$conn)\n{";
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
ShowCreateCrud("LNM_filiere", "LNM_filiere", [
    "id_filiere",
    "nom_filiere",
    "nom_long",
    "id_responsable"
]);

