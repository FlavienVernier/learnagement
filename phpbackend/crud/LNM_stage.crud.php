<?php
  //include('./function_acction_allowed.php');

function createLNM_stage($conn, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant)
{
  if(action_allowed('INSERT', 'LNM_stage', NULL)){
    $sql = "INSERT INTO `LNM_stage` (`entreprise`, `intitule`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`, `id_enseignant`) VALUES ('$entreprise', '$intitule', '$description', '$ville', '$date_debut', '$date_fin', '$nature', '$id_etudiant', '$id_enseignant')";
    $res = mysqli_query($conn, $sql);
    return $res;
  }else{
    return ['No permission to INSERT into LNM_stage'];
  }
}

function updateLNM_stage($conn, $id, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant)
{
  if(action_allowed('UPDATE', 'LNM_stage', '$id')){
    $sql = "UPDATE `LNM_stage` SET   `entreprise`='$entreprise', `intitule`='$intitule', `description`='$description', `ville`='$ville', `date_debut`='$date_debut', `date_fin`='$date_fin', `nature`='$nature', `id_etudiant`='$id_etudiant', `id_enseignant`='$id_enseignant' WHERE `id` = $id";
    $res = mysqli_query($conn, $sql);
    return $res;
  }else{
    return ['No permission to UPDATE $id line in LNM_stage'];
  }
}

function deleteLNM_stage($conn,  $id)
{
  if(action_allowed('DELETE', 'LNM_stage', $id)){
    $sql = "DELETE FROM `LNM_stage` WHERE `id`=$id";
    $res = mysqli_query($conn, $sql);
    return $res;
  }else{
    return ['No permission to DELETE $id line from LNM_stage'];
  }
}

function listLNM_stage($conn)
{
    $sql = "SELECT * FROM `LNM_stage`";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listLNM_stageBy($conn, $field, $value){
    $sql = "SELECT * FROM `LNM_stage` WHERE `$field`='$value';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}


function listLNM_stageBySupervisorId($conn, $supervisor_id) {
  return listLNM_stageBy($conn, "id_enseignant", $supervisor_id);
}

function listLNM_stageByStudentId($conn, $student_id) {
  return listLNM_stageBy($conn, "id_etudiant", $student_id);
}
