<?php

    $token = $user["jwt_token"];
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

        patch_stage($token,
            $idStage,
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
            $_POST['id_etudiant'],
            $idEnseignant);
        Alert::success("Stage mis à jour avec succès.");
    } catch (\Throwable $th) {
        if (!isset($params['error']))
            $params['error'] = "Une erreur est survenue lors de la mise à jour du stage."; # TODO: Create system log
        Alert::error($params['error']); 
    }
    $t->router->redirect('dashboard-stage');