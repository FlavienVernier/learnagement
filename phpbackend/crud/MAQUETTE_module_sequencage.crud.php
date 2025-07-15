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
        return "Deletion Failed";
    }
    //}else{
    //  return ['No permission to INSERT into MAQUETE_module_sequencage'];
    //}
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
