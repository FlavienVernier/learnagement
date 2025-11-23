<?php
loadEnv("..");

[
  "inscription_ok" => $inscription,
  "id" => $mail,
  "mdp" => $password,
] = $_POST;

if(!isset($_POST["inscription_ok"])){
  redirect("login");
}

$sql = [
  "SELECT id_etudiant AS id, mail, password, password_updated, 'etudiant' AS type FROM LNM_etudiant WHERE mail LIKE '$mail'",
  "SELECT id_enseignant AS id, mail, password, password_updated, 'enseignant' AS type FROM LNM_enseignant WHERE mail LIKE '$mail'",
  "SELECT NULL AS id, mail, password, password_updated, 'administratif' AS type FROM LNM_administratif WHERE mail LIKE '$mail'",
];
$result = mysqli_query($conn, implode(" UNION ALL ", $sql)) or die("Requête invalide: ". mysqli_error( $conn )."\n".implode(" UNION ALL ", $sql));
$val= mysqli_fetch_array($result);

if (empty($val))
  redirect("login");

$password_updated = boolval($val['password_updated']);
if (!$password_updated && password_verify($_POST['mdp'], $val['password'])){
  $_SESSION["connecte"]=true; 
  $_SESSION["mail"]=$_POST["id"];
  $_SESSION["type"]=$val["type"];
  $_SESSION["id_".$val["type"]]=$val['id'];
  redirect("home");
} else if ($password_updated && $val['password'] == $_POST['mdp']){
  $mail = $_POST['id'];
  $_SESSION["type"]=$val["type"];
  $_SESSION["id_".$val["type"]]=$val['id'];
  render("pages/init_mdp/index.inc", ["mail" => $mail]);
} else{
  redirect("login");
}

// $2y$12$xf7wgqNCc1U3YM2KfLxAIeiAYLo.qtkzfm3j2jaaSRwh6tpTp72wm