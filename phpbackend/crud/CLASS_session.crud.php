<?php
function listCLASS_sessionByStudentId($conn, $id_etudiant){
    $sql = "SELECT etu.nom, session.schedule as date_prevue, promo.annee, sequencage.duree_h, module.nom 
                FROM CLASS_session as session 
                JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe 
                JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo 
                JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo 
                JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence 
                JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage 
                JOIN MAQUETTE_module as module ON sequencage.id_module = module.id_module 
                WHERE session.schedule < CURRENT_DATE and etu.id_etudiant = '$id_etudiant';";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function listCLASS_sessionByIdResp($conn, $id) {
    $sql = "SELECT CLASS_session.id_session, CLASS_session.id_groupe, LNM_groupe.nom_groupe, LNM_promo.id_promo, 'ExplicitSecondaryPromoKs not yet generated' as promo,
MAQUETTE_module_sequence.numero_ordre, MAQUETTE_module_sequence.id_intervenant_principal, MAQUETTE_module_sequence.commentaire,
                    MAQUETTE_module_sequencage.id_module, MAQUETTE_module_sequencage.id_seance_type, MAQUETTE_module_sequencage.duree_h,
                    MAQUETTE_module.code_module, 
                    LNM_seanceType.type, 
                    ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK as intervenant
            FROM CLASS_session
            	LEFT JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session.id_groupe
                LEFT JOIN LNM_promo ON LNM_promo.id_promo = LNM_groupe.id_promo
            	LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
            WHERE MAQUETTE_module.id_responsable = '$id'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}
function listCLASS_sessionByIdIntervenant($conn, $id) {
    $sql = "SELECT CLASS_session.id_groupe, LNM_groupe.nom_groupe, LNM_promo.id_promo, 'ExplicitSecondaryPromoKs not yet generated' as promo,
MAQUETTE_module_sequence.numero_ordre, MAQUETTE_module_sequence.id_intervenant_principal, MAQUETTE_module_sequence.commentaire,
                    MAQUETTE_module_sequencage.id_module, MAQUETTE_module_sequencage.id_seance_type, MAQUETTE_module_sequencage.duree_h,
                    MAQUETTE_module.code_module, MAQUETTE_module.nom as nom_module,
                    LNM_seanceType.type,
                    LNM_semestre.semestre
            FROM CLASS_session
            	LEFT JOIN LNM_groupe ON LNM_groupe.id_groupe = CLASS_session.id_groupe
                LEFT JOIN LNM_promo ON LNM_promo.id_promo = LNM_groupe.id_promo
            	LEFT JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
            	LEFT JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                LEFT JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                LEFT JOIN MAQUETTE_module_as_learning_unit ON MAQUETTE_module_as_learning_unit.id_module = MAQUETTE_module.id_module
                LEFT JOIN MAQUETTE_learning_unit ON MAQUETTE_learning_unit.id_learning_unit = MAQUETTE_module_as_learning_unit.id_learning_unit AND MAQUETTE_learning_unit.id_promo = LNM_promo.id_promo
                LEFT JOIN LNM_semestre ON LNM_semestre.id_semestre = MAQUETTE_module.id_semestre
                LEFT JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type
                LEFT JOIN LNM_groupe_type ON LNM_groupe_type.id_groupe_type = MAQUETTE_module_sequencage.id_groupe_type
                LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = CLASS_session.id_enseignant
            WHERE CLASS_session.id_enseignant = '$id'";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function setCLASS_session_enseignant($conn, $id_session,  $id_enseignant){
    $sql = "UPDATE CLASS_session
            SET id_enseignant = '$id_enseignant'
            WHERE id_session = '$id_session'";

    if(mysqli_query($conn, $sql)){
        return "Data Updated";
    }else{
        return "Updat Failed";
    }
}