<?php

function loadEnv($path): void
{
  $lines = file($path . '/.env');
  foreach ($lines as $line) {
    if(substr(trim($line),0,1) != '#' && trim($line) != '') {
      [$key, $value] = explode('=', $line, 2);
      $key = trim($key);
      $value = trim($value);

      putenv(sprintf('%s=%s', $key, $value));
      //printf('%s=%s', $key, $value);
      $_ENV[$key] = $value;
      $_SERVER[$key] = $value;
    }
  }
}

loadEnv("..");

// Session timeout in second
  $session_timeout = $_ENV['SESSION_TIMEOUT'];

// MySQL server
$learnagement_instance = $_ENV['INSTANCE_NAME'];
$mysql_server = $_ENV['MYSQL_SERVER'];
//$mysql_user = "learnagement";
$mysql_user = $_ENV['MYSQL_USER_LOGIN'];
//$mysql_passwd = "toto";
$mysql_passwd = $_ENV['MYSQL_USER_PASSWORD'];
$mysql_db = $_ENV['MYSQL_DB'];
$mysql_port = $_ENV['MYSQL_PORT'];

// Python Dash serveur
#$python_web_server_port = "48050";

// predefined variable 
$sessionId = "None";
$vue_name = "None";
$table_name = "None";
$fields = "None";
$reference_table_name="";
$primaryk_and_secondaryK="";
$userlogin="";
?>
