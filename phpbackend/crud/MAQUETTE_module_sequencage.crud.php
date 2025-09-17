<?php

function createMAQUETE_module_sequencage($conn, $id_module, $nombre, $id_seance_type, $id_groupe_type, $duree_h, $id_intervenant_principal)
{
    if($id_intervenant_principal == "NULL"){
        $sql = "INSERT INTO `MAQUETTE_module_sequencage` (`id_module`, `nombre`, `id_seance_type`, `id_groupe_type`, `duree_h`) 
                             VALUES ('$id_module', '$nombre', '$id_seance_type', '$id_groupe_type', '$duree_h')";
    }else {
        $sql = "INSERT INTO `MAQUETTE_module_sequencage` (`id_module`, `nombre`, `id_seance_type`, `id_groupe_type`, `duree_h`, `id_intervenant_principal`) 
                             VALUES ('$id_module', '$nombre', '$id_seance_type', '$id_groupe_type', '$duree_h', '$id_intervenant_principal')";
    };
    if(mysqli_query($conn, $sql)){
        return "Data Inserted";
    }else{
        return "Insertion Failed";
    }
    //}else{
    //  return ['No permission to INSERT into MAQUETE_module_sequencage'];
    //}
}

function deleteMAQUETE_module_sequencage($conn, $id_module_sequencage)
{
    $sql = "DELETE FROM MAQUETTE_module_sequencage
            WHERE id_module_sequencage = '$id_module_sequencage'";

    if(mysqli_query($conn, $sql)){
        return "Data Deleted";
    }else{
        return "Delete Failed";
    }
    //}else{
    //  return ['No permission to INSERT into MAQUETE_module_sequencage'];
    //}
}

function setMAQUETE_module_sequencage_intervenant_principal($conn, $id_module_sequencage, $id_intervenant_principal){
    $sql = "UPDATE MAQUETTE_module_sequencage
            SET id_intervenant_principal = '$id_intervenant_principal'
            WHERE id_module_sequencage = '$id_module_sequencage'";

    if(mysqli_query($conn, $sql)){
        return "Data Updated";
    }else{
        return "Updat Failed";
    }
}

function listMAQUETTE_moduleSequencageByIdResp($conn, $id) {
    $sql = "SELECT MAQUETTE_module_sequencage.*, MAQUETTE_module.code_module, LNM_seanceType.type, LNM_groupe_type.groupe_type, ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant_principal
            FROM MAQUETTE_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = MAQUETTE_module_sequencage.id_intervenant_principal
            WHERE MAQUETTE_module.id_responsable = '$id'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function checkMAQUETTE_moduleSequencageVsMaquuetteByIdResp($conn, $id) {
    $sql = "SELECT DISTINCT
    MAQUETTE_module.id_module, 
    MAQUETTE_module.code_module, 
    IFNULL(hCM,0) - IFNULL(hCMCequenced,0) AS 'ecart_CM',  IFNULL(hTD,0)  - IFNULL(hTDCequenced,0) AS 'ecart_TD', IFNULL(hTP,0)  - IFNULL(hTPCequenced,0) AS 'ecart_TP',  IFNULL(hTPTD,0) - IFNULL(hTPTDCequenced,0) AS 'ecart_TPTD'
FROM MAQUETTE_module
LEFT JOIN (
    SELECT code_module, SUM(nombre * duree_h) as hCMCequenced
    FROM MAQUETTE_module_sequencage 
    JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
    JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
    JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
    WHERE LNM_seanceType.type = 'CM' AND LNM_groupe_type.groupe_type = 'PROMO' OR LNM_seanceType.type = 'Exam' AND LNM_groupe_type.groupe_type = 'PROMO' 
    GROUP BY code_module) CMsequenced ON  CMsequenced.code_module = MAQUETTE_module.code_module
LEFT JOIN (
    SELECT code_module, SUM(nombre * duree_h) as hTDCequenced
    FROM MAQUETTE_module_sequencage 
    JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
    JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
    JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
    WHERE LNM_seanceType.type = 'TD' AND LNM_groupe_type.groupe_type = 'TD'
    GROUP BY code_module) TDsequenced ON  TDsequenced.code_module = MAQUETTE_module.code_module
LEFT JOIN (
    SELECT code_module, SUM(nombre * duree_h) as hTPCequenced
    FROM MAQUETTE_module_sequencage 
    JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
    JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
    JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
    WHERE LNM_seanceType.type = 'TP' AND LNM_groupe_type.groupe_type = 'TP'
    GROUP BY code_module) TPsequenced ON  TPsequenced.code_module = MAQUETTE_module.code_module
LEFT JOIN (
    SELECT code_module, SUM(nombre * duree_h) as hTPTDCequenced
    FROM MAQUETTE_module_sequencage 
    JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
    JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
    JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
    WHERE LNM_seanceType.type = 'TP' AND LNM_groupe_type.groupe_type = 'TD'
    GROUP BY code_module) TPTDsequenced ON  TPTDsequenced.code_module = MAQUETTE_module.code_module
WHERE MAQUETTE_module.id_responsable = '$id';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function checkMAQUETTE_moduleSequencageVsMaquuette($conn) {
    $sql="SELECT 
            `MAQUETTE_module`.`code_module`, 
            IFNULL(`hCM`,0) + IFNULL(`hTD`,0) + IFNULL(`hTP`,0) + IFNULL(`hTPTD`,0) + IFNULL(`hPROJ`,0) AS `hMCCC`, 
            `hCequenced`, 
            IFNULL(`hCM`,0) + IFNULL(`hTD`,0) + IFNULL(`hTP`,0) + IFNULL(`hTPTD`,0) + IFNULL(`hPROJ`,0) - `hCequenced` AS `Reste à planifier`
        FROM `MAQUETTE_module`
        JOIN (
            SELECT `code_module`, SUM(`duree_h`) as hCequenced
            FROM `MAQUETTE_module_sequencage` 
            JOIN `MAQUETTE_module_sequence` ON `MAQUETTE_module_sequence`.id_module_sequencage = `MAQUETTE_module_sequencage`.id_module_sequencage
            JOIN `MAQUETTE_module` ON `MAQUETTE_module`.`id_module` = `MAQUETTE_module_sequencage`.`id_module`
            GROUP BY `code_module`) sequenced ON  sequenced.`code_module` = `MAQUETTE_module`.`code_module`;";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
