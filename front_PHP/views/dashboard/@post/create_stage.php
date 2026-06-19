<?php
    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////
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
        $idEtudiant   = (int) $_POST['id_etudiant'];

        post_stage($token,
            $_POST['entreprise'],
            $_POST['intitule'],
            $_POST['description'],
            $adresse,
            $_POST['ville'],
            $codePostal,
            $pays,
            $_POST['date_debut'],
            $_POST['date_fin'],
            $_POST['nature'],
            $idEtudiant,
            $idEnseignant );
        Alert::success("Stage créé avec succès.");
    } catch (\Throwable $th) {
        if (!isset($params['error']))
            $params['error'] = "Une erreur est survenue lors de la création du stage."; # TODO: Create system log
        Alert::error($params['error']); 
    }
    $t->router->redirect('dashboard-create-stage', query: $_POST);