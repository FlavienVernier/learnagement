<link rel="stylesheet" href="css/page_rendus.inc.css"/>


<?php

?>
   
<script type="text/javascript" language="javascript">
   
const userAction = async () => {
   const response = await fetch('http://localhost:40081/list/listStagesEtudiant.php', {
				method: 'POST',
				id_etudiant: 503, // string or object
				headers: {
				  'Content-Type': 'application/x-www-form-urlencoded'
				}
				});
   const myJson = await response.json(); //extract JSON from the http response
  // do something with myJson

}
  document.getElementById("div").innerHTML = myJson;
</script>
   
<html>
<body id='bod'><button type="submit" onclick="javascript:send()">call</button>
<div id='div'>

</div></body>
</html>
