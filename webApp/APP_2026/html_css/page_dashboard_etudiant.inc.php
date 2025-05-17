<link rel="stylesheet" type="text/css" href="css/page_dashboard.css">

<div id="dashboard-container">
    <iframe src=
<?php
    require_once("../../config.php");
    print("\"http://localhost:" . $python_web_server_port . "/etudiant\"");
?>
  width="100%" height="600px" style="border:none;"></iframe>
</div>
