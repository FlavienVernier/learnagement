<?php

function listMAQUETTE_moduleDependancesByIdModule($conn, $id) {
    $sql = "SELECT `id_sequence_prev`, `id_sequence_next`
            FROM `MAQUETTE_dependance_sequence` 
            JOIN MAQUETTE_module_sequence on MAQUETTE_module_sequence.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_prev 
            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
            JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
            JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module.id_module = '$id'
            UNION
            SELECT `id_sequence_prev`, `id_sequence_next`
            FROM `MAQUETTE_dependance_sequence` 
            JOIN MAQUETTE_module_sequence on MAQUETTE_module_sequence.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_next 
            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
            JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
            JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module.id_module = '$id';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listMAQUETTE_moduleSequenceDependancesByIdModule($conn, $id) {
    $sql = "SELECT MAQUETTE_module_sequence.id_module_sequence, LNM_seanceType.type, MAQUETTE_module.code_module, MAQUETTE_module.nom, MAQUETTE_module_sequence.commentaire 
			FROM MAQUETTE_module_sequence 
            JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
            JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
            JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type 
            WHERE MAQUETTE_module_sequence.id_module_sequence IN (SELECT MAQUETTE_module_sequence.id_module_sequence
                  FROM MAQUETTE_module_sequence
                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage 
                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module 
            	WHERE MAQUETTE_module.id_module = '$id')
            OR MAQUETTE_module_sequence.id_module_sequence IN
                (SELECT `id_sequence_next` 
            	FROM `MAQUETTE_dependance_sequence` 
            	JOIN MAQUETTE_module_sequence as sequence_prev on sequence_prev.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_prev 
            	JOIN MAQUETTE_module_sequencage  as sequencage_prev ON sequencage_prev.id_module_sequencage = sequence_prev.id_module_sequencage 
            	JOIN MAQUETTE_module as module_prev ON module_prev.id_module = sequencage_prev.id_module 
            	WHERE module_prev.id_module = '$id')
            OR MAQUETTE_module_sequence.id_module_sequence IN
                (SELECT `id_sequence_prev`
                FROM `MAQUETTE_dependance_sequence` 
                JOIN MAQUETTE_module_sequence as sequence_next on sequence_next.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_next
                JOIN MAQUETTE_module_sequencage  as sequencage_next ON sequencage_next.id_module_sequencage = sequence_next.id_module_sequencage 
                JOIN MAQUETTE_module as module_next ON module_next.id_module = sequencage_next.id_module 
                WHERE module_next.id_module = '$id');";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}