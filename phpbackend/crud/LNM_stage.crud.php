<?php
  //include('./function_acction_allowed.php');

function createLNM_stage($conn, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant)
{
  //if(action_allowed('INSERT', 'LNM_stage', NULL)){
    if($id_enseignant == "NULL"){
        $sql = "INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`) 
                             VALUES ('$entreprise', '$intitule', '$description', '$ville', '$date_debut', '$date_fin', '$nature', '$id_etudiant')";
    }else {
        $sql = "INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`, `id_enseignant`) 
                             VALUES ('$entreprise', '$intitule', '$description', '$ville', '$date_debut', '$date_fin', '$nature', '$id_etudiant', '$id_enseignant')";
    };
    if(mysqli_query($conn, $sql)){
        return "Data Inserted";
    }else{
        return "Insertion Failed";
    }
  //}else{
  //  return ['No permission to INSERT into LNM_stage'];
  //}
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

function deleteLNM_stage($conn,  $id_stage, $user_id)
{
  if(action_allowed('DELETE', 'LNM_stage', $user_id)){
    $sql = "DELETE FROM `LNM_stage` WHERE `id_stage`=$id_stage";
    $res = mysqli_query($conn, $sql);
    return $res;
  }else{
    return ['No permission to DELETE $id_stage line from LNM_stage'];
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

function listLNM_stageWithSupervisorId($conn){
    $sql = 'SELECT LNM_stage.`id_stage`, CONCAT(LNM_etudiant.nom, " ", LNM_etudiant.prenom) AS "étudiant", LNM_stage.`entreprise`, LNM_stage.`intitulé`, LNM_stage.`description`, LNM_stage.`ville`, LNM_stage.`date_debut`, LNM_stage.`date_fin`, LNM_stage.`nature`, CONCAT(LNM_enseignant.nom, " ", LNM_enseignant.prenom) AS enseignant
FROM `LNM_stage` 
JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
WHERE LNM_stage.`id_enseignant` IS NOT NULL;';
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listLNM_stageWithoutSupervisorId($conn){
    $sql = 'SELECT LNM_stage.`id_stage`, CONCAT(LNM_etudiant.nom, " ", LNM_etudiant.prenom) AS "étudiant", LNM_stage.`entreprise`,LNM_stage.`intitulé`,LNM_stage.`description`,LNM_stage.`ville`,LNM_stage.`date_debut`,LNM_stage.`date_fin`,`nature`
FROM `LNM_stage` 
JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
WHERE LNM_stage.`id_enseignant` IS NULL;';
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
function listLNM_stageStudentsWithoutStage($conn){
    $sql = "SELECT `LNM_etudiant`.`id_etudiant`, `LNM_etudiant`.`nom`,`LNM_etudiant`.`prenom` FROM `LNM_etudiant` WHERE `LNM_etudiant`.`id_etudiant` NOT IN ( SELECT `LNM_stage`.`id_etudiant` FROM `LNM_stage` WHERE 1);";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function setLNM_stage_enseignant($conn, $id_stage,  $id_enseignant){
    $sql = "UPDATE LNM_stage
            SET id_enseignant = '$id_enseignant'
            WHERE id_stage = '$id_stage'";

    if(mysqli_query($conn, $sql)){
        return "Data Updated";
    }else{
        return "Updat Failed";
    }
}
