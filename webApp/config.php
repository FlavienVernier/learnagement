<?php



function loadEnv($path): void
   {
       $lines = file($path . '/.env');
       foreach ($lines as $line) {
           [$key, $value] = explode('=', $line, 2);
           $key = trim($key);
           $value = trim($value);

           putenv(sprintf('%s=%s', $key, $value));
           //printf('%s=%s', $key, $value);
           $_ENV[$key] = $value;
           $_SERVER[$key] = $value;
       }
   }

loadEnv("..");

// Session timeout in second
//$session_timeout = 900;

// MySQL server
//$learnagement_instance = "dev";
//$mysql_server = "mysql_dev";
//$mysql_user = "learnagement";
//$mysql_user = "root";
//$mysql_passwd = "toto";
//$mysql_passwd = "toto";
//$mysql_db = "learnagement";
//$mysql_port = "3306";

// Python Dash serveur
//$python_web_server_port = "48050";

// predefined variable 
$sessionId = "None";
$vue_name = "None";
$table_name = "None";
$fields = "None";
$reference_table_name="";
$primaryk_and_secondaryK="";
$userlogin="";
?>
