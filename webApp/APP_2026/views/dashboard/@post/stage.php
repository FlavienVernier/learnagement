<?php
    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////
    $params = [];
    try {
        $dateDebut = new DateTime($_POST['date_debut']);
        $dateFin = new DateTime($_POST['date_fin']);
        if ($dateDebut > $dateFin) {
            $params['error'] = "La date de debut est après la date de fin";
            throw new Exception("La date de debut est après la date de fin");
        }

        $adresse      = $_POST['adresse'] !== '' ? $_POST['adresse'] : null;
        $codePostal   = $_POST['code_postal'] !== '' ? $_POST['code_postal'] : null;
        $pays         = $_POST['pays'] !== '' ? $_POST['pays'] : null;
        $idEnseignant = $_POST['id_enseignant'] !== '' ? (int) $_POST['id_enseignant'] : null;
        $idStage   = (int) $_POST['id_stage'];

        $sql = "UPDATE `LNM_stage`
            SET
                `entreprise`= ?,
                `intitulé`= ?,
                `description`= ?,
                `adresse`= ?,
                `ville`= ?,
                `code_postal`= ?,
                `pays`= ?,
                `date_debut`= ?,
                `date_fin`= ?,
                `nature`= ?,
                `id_enseignant`= ?
            WHERE id_stage = ?;";
        $stmt = mysqli_prepare($pdo, $sql);
        mysqli_stmt_bind_param($stmt, "ssssssssssii",
            $_POST['entreprise'],
            $_POST['intitulé'],
            $_POST['description'],
            $adresse,           // null si vide
            $_POST['ville'],
            $codePostal,        // null si vide
            $pays,              // null si vide
            $_POST['date_debut'],
            $_POST['date_fin'],
            $_POST['nature'],
            $idEnseignant,      // null si vide
            $idStage            // int, vient de l'URL
        );
        mysqli_stmt_execute($stmt);
        Alert::success("Stage mis à jour avec succès.");
    } catch (\Throwable $th) {
        if (!isset($params['error']))
            $params['error'] = "Une erreur est survenue lors de la mise à jour du stage."; # TODO: Create system log
        Alert::error($params['error']); 
    }
    $t->router->redirect('dashboard-stage');