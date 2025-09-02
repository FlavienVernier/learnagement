<link rel="stylesheet" type="text/css" href="css/page_dashboard.css">

<div id="dashboard-container">
    <iframe src=
    <?php
        require_once("../../config.php");
        loadEnv("../..");

        print("\"" . $_ENV['MOBILITY_URL'] . "\"");
    ?>
    width="100%" height="600px" style="border:none;"></iframe>
</div>
