<?php
echo "<h1>Lancer une application Dash avec PHP</h1>";
echo "<form method='post'>";
echo    "<button type='submit' name='run_dash'>Lancer l'application Dash</button>";
echo "</form>";

if (isset($_POST['run_dash'])) {
    // Commande pour exécuter l'application Dash
    $command = 'python3 ../../visualisation/visus/main.py > /dev/null 2>&1 &';
    shell_exec($command);

    // Vérification que Dash est démarré
    $host = 'localhost';
    $port = 8050;

    // Petit délai pour laisser Dash s'initialiser
    sleep(2);

    if (@fsockopen($host, $port)) {
        echo "<p>Application Dash démarrée. Accédez à <a href='http://$host:$port' target='_blank'>http://$host:$port</a></p>";
    } else {
        echo "<p>Lancement de l'application Dash en cours. Veuillez patienter quelques secondes et réessayez <a href='http://$host:$port' target='_blank'>http://$host:$port</a></p>";
    }
}
?>
