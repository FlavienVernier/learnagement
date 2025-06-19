<?php

function selectComposantesEssentiellesByIdCompetence($conn, $idCompetence){
    $sql="SELECT * FROM `APC_composante_essentielle` WHERE `id_competence` = $idCompetence;";
    $res = mysqli_query($conn, $sql);

    return rs_to_table($res);
}
