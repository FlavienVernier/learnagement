<?php
  //include('./function_acction_allowed.php');

function createLNM_stage($conn, $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant)
{
  //if(action_allowed('INSERT', 'LNM_stage', NULL)){
    if($id_enseignant == "NULL"){
        $sql = "INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sssssssi", $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant);
    }else {
        $sql = "INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`, `id_enseignant`) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sssssssii", $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant);
    }
    if($stmt->execute()){
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
      $sql = "UPDATE `LNM_stage` 
                    SET  `entreprise`=?, 
                         `intitule`=?, 
                         `description`=?, 
                         `ville`=?, 
                         `date_debut`=?, 
                         `date_fin`=?, 
                         `nature`=?, 
                         `id_etudiant`=?, 
                         `id_enseignant`=? 
                   WHERE `id` = $id";
      $stmt = $conn->prepare($sql);
      $stmt->bind_param("sssssssii", $entreprise, $intitule, $description, $ville, $date_debut, $date_fin, $nature, $id_etudiant, $id_enseignant);
      if($stmt->execute()){
          return "Data Updated";
    }else{
          return "Update Failed";
    }
  }else{
    return ['No permission to UPDATE $id line in LNM_stage'];
  }
}

function deleteLNM_stage($conn,  $id_stage, $user_id)
{
  if(action_allowed('DELETE', 'LNM_stage', $user_id)){
    $sql = "DELETE FROM `LNM_stage` WHERE `id_stage`=?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $id_stage);
    if($stmt->execute()){
        return "Data Deleted";
    }else{
        return "Delete Failed";
    }
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
    $sql = "SELECT CONCAT(LNM_etudiant.prenom, ' ', LNM_etudiant.nom) AS 'etudiant', 
                LNM_stage.entreprise, 
                LNM_stage.`intitulé`, 
                LNM_stage.description, 
                LNM_stage.ville, 
                LNM_stage.date_debut, 
                LNM_stage.date_fin, 
                LNM_stage.nature, 
                CONCAT(LNM_enseignant.prenom, ' ', LNM_enseignant.nom) AS 'enseignant'
        FROM `LNM_stage` 
        JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
        JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
        WHERE $field='$value';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}


function listLNM_stageBySupervisorId($conn, $supervisor_id) {
  return listLNM_stageBy($conn, "LNM_enseignant.id_enseignant", $supervisor_id);
}

function listLNM_stageByStudentId($conn, $student_id) {
  return listLNM_stageBy($conn, "LNM_etudiant.id_etudiant", $student_id);
}

function listLNM_stageWithSupervisorId($conn){
    $sql = 'SELECT LNM_stage.`id_stage`, CONCAT(LNM_etudiant.nom, " ", LNM_etudiant.prenom) AS "étudiant", ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo", LNM_stage.`entreprise`, LNM_stage.`intitulé`, LNM_stage.`description`, LNM_stage.`ville`, LNM_stage.`date_debut`, LNM_stage.`date_fin`, LNM_stage.`nature`, CONCAT(LNM_enseignant.nom, " ", LNM_enseignant.prenom) AS enseignant
FROM `LNM_stage` 
JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
WHERE LNM_stage.`id_enseignant` IS NOT NULL;';
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listLNM_stageWithoutSupervisorId($conn){
    $sql = '

SELECT LNM_stage.`id_stage`, CONCAT(LNM_etudiant.nom, " ", LNM_etudiant.prenom) AS "étudiant", ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo", LNM_stage.`entreprise`,LNM_stage.`intitulé`,LNM_stage.`description`,LNM_stage.`ville`,LNM_stage.`date_debut`,LNM_stage.`date_fin`,`nature`
FROM `LNM_stage` 
JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
WHERE LNM_stage.`id_enseignant` IS NULL;';
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
function listLNM_stageStudentsWithoutStage($conn){
    $sql = 'SELECT `LNM_etudiant`.`id_etudiant`, `LNM_etudiant`.`nom`,`LNM_etudiant`.`prenom`, ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo"
FROM `LNM_etudiant` 
JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
WHERE `LNM_etudiant`.`id_etudiant` 
NOT IN ( SELECT `LNM_stage`.`id_etudiant` FROM `LNM_stage` WHERE 1);
';
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
