<?php
try {
  loadEnv("..");

  [
    "email" => $email,
    "password" => $password,
  ] = $_POST;

  $sql = [
    "SELECT id_etudiant AS id, mail, password, password_updated, 'etudiant' AS type FROM LNM_etudiant WHERE mail LIKE '$email'",
    "SELECT id_enseignant AS id, mail, password, password_updated, 'enseignant' AS type FROM LNM_enseignant WHERE mail LIKE '$email'",
    "SELECT NULL AS id, mail, password, password_updated, 'administratif' AS type FROM LNM_administratif WHERE mail LIKE '$email'",
  ];
  $result = mysqli_query($conn, implode(" UNION ALL ", $sql)) or die("Requête invalide: ". mysqli_error( $conn )."\n".implode(" UNION ALL ", $sql));
  $val = mysqli_fetch_array($result);

  if (empty($val))
    redirect("login");

  [
    "id" => $id,
    "type" => $type,
    "password" => $encrypt_password,
    "password_updated" => $password_updated
  ] = $val;
  $password_updated = boolval($password_updated);

  if (!$password_updated && password_verify($password, $encrypt_password)){
    $_SESSION["connecte"] = true; 
    $_SESSION["email"] = $email;
    $_SESSION["type"] = $type;
    $_SESSION["id"] = $id;
    redirect("dashboad");
  } else if ($password_updated && $encrypt_password == $password){
    $_SESSION["type"] = $type;
    $_SESSION["id"] = $id;
    render("pages/init_password/index.inc", ["email" => $email]);
  } else {
    redirect("login");
  }
} catch (Exception $e) {
  #todo: add logs
  redirect("login");
}