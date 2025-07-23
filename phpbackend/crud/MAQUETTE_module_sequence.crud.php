<?php

function listMAQUETTE_moduleSequenceByIdResp($conn, $id) {
    $sql = "SELECT  MAQUETTE_module_sequence.numero_ordre, MAQUETTE_module_sequence.id_intervenant_principal, MAQUETTE_module_sequence.commentaire,
                    MAQUETTE_module_sequencage.id_module, MAQUETTE_module_sequencage.id_seance_type, MAQUETTE_module_sequencage.id_groupe_type, MAQUETTE_module_sequencage.duree_h,
                    MAQUETTE_module.code_module, 
                    LNM_seanceType.type, 
                    LNM_groupe_type.groupe_type, 
                    ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant_principal
            FROM MAQUETTE_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = MAQUETTE_module_sequence.id_intervenant_principal
            WHERE MAQUETTE_module.id_responsable = '$id'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
