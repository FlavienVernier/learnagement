<?php
loadEnv("..");

if(!isset($_POST["inscription_ok"])){
  redirect("login");
}

$sql = [
  "SELECT id_etudiant AS id, mail, password, password_updated, 'etudiant' AS type FROM LNM_etudiant WHERE mail LIKE'".$_POST["id"]."'",
  "SELECT id_enseignant AS id, mail, password, password_updated, 'enseignant' AS type FROM LNM_enseignant WHERE mail LIKE'".$_POST["id"]."'",
  "SELECT NULL AS id, mail, password, password_updated, 'administratif' AS type FROM LNM_administratif WHERE mail LIKE'".$_POST["id"]."'",
];
$result = mysqli_query($conn, implode(" UNION ALL ", $sql)) or die("Requête invalide: ". mysqli_error( $conn )."\n".implode(" UNION ALL ", $sql));
$val= mysqli_fetch_array($result);

if ($val['password_updated'] != NULL && password_verify($_POST['mdp'], $val['password'])){
  $_SESSION["connecte"]=true; 
  $_SESSION["mail"]=$_POST["id"];
  $_SESSION["type"]=$val["type"];
  $_SESSION["id_".$val["type"]]=$val['id'];
  redirect("home");
} else if ($val['password_updated'] == NULL && $val['password'] == $_POST['mdp']){
  $mail = $_POST['id'];
  $_SESSION["type"]=$val["type"];
  $_SESSION["id_".$val["type"]]=$val['id'];
  redirect("init_mdp", ["mail" => $mail]);
}
else{
  redirect("login");
}