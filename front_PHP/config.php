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
               $_ENV[$key] = $value;
               $_SERVER[$key] = $value;
           }
       }
   }

use Monolog\Logger;
use Monolog\Level;
use Monolog\Handler\StreamHandler;

// create a log channel
function getLogger(): \Monolog\Logger {
    static $log = null;
    if ($log === null) {
        $log = new \Monolog\Logger('name');
        $log->pushHandler(new \Monolog\Handler\StreamHandler('php://stdout', Level::Info));
    }
    return $log;
}
//$log = new Logger('name');
//$log->pushHandler(new StreamHandler('php://stdout', Level::Info));

// predefined variable 
$sessionId = "None";
$vue_name = "None";
$table_name = "None";
$fields = "None";
$reference_table_name="";
$primaryk_and_secondaryK="";
$userlogin="";
?>
