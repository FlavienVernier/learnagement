<?php

$list = $_GET['list'] ?? null;

if ($list === 'prof') {
    // -------------------------------------------------------------------------
    // LOGIQUE ENSEIGNANTS
    // -------------------------------------------------------------------------
    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';
    echo '<script type="module" src="pages/dashboard/liste_personnel/index.inc.js" defer></script>';
    
    // Affichage de la barre de recherche
    echo "<form method='post' action='?page=home&section=liste_personnel&list=prof'>";
    echo "<input type='text' name='query' placeholder='Entrez une recherche'>";
    echo "<input class='bouton' type='submit' name='bouton_recherche' value='Rechercher'>";
    echo "<a href='?page=home&section=liste_personnel' class='bouton'>Retour</a>";
    echo "</form>";

    // Traitement de la recherche
    $sql = "SELECT id_enseignant as prof_id, prenom as prof_prenom, nom as prof_nom, mail as prof_mail FROM LNM_enseignant";
    if (isset($_POST['bouton_recherche']) && !empty($_POST['query'])) {
        $query = $_POST["query"];
        $sql .= " WHERE mail LIKE '%$query%'";
    }

    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        echo "<div class='conteneur_grid'>";
        echo "<div id='enseignants'>";
        while ($row = mysqli_fetch_array($result)) {
            echo "<div class='enseignant'> <a id='info_prof' href='?page=home&section=info_enseignant&id=" . $row['prof_id'] . "'>" . $row['prof_nom'] . " " . $row['prof_prenom'] . "</a> <a id='mail_prof' href='mailto:" . $row['prof_mail'] . "'>" . $row['prof_mail'] . "</a></div>";
        }
        echo "</div>";
        echo "</div>";
        
        echo "<div id='pagination'>
                <button id='btn_prev' class='bouton'>Précédent</button>
                <span id='page_info'></span>
                <button id='btn_next' class='bouton'>Suivant</button>
              </div>";

    } else {
        echo "<p id='erreur_recherche'>Il n'y a pas de professeurs correspondant à la recherche.</p>";
    }

} elseif ($list === 'etu') {
    // -------------------------------------------------------------------------
    // LOGIQUE ETUDIANTS
    // -------------------------------------------------------------------------
    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';
    echo '<script type="module" src="pages/dashboard/liste_personnel/index.inc.js" defer></script>';
    
    // Barre de tri/recherche
    echo "<form method='post' action='?page=home&section=liste_personnel&list=etu'>";
    echo "<label id='formulaire' for='choix'>Rechercher un étudiant par promotion/filière ou nom/prénom : </label>";
    echo "<div id='conteneur_recherche'>
            <div id='barre_recherche'>
                <input type='text' id='search_input' placeholder='ex : info/meca ou 2/3'>
                <button type='button' id='btn_recherche' class='bouton'>Rechercher</button>
                <a href='?page=home&section=liste_personnel' class='bouton'>Retour</a>
            </div>
            <div id='filtres_actifs'></div>
          </div>";
    echo "</form>";

    // Construction de la requête SQL de base
    $sql = "SELECT e.prenom AS etu_prenom, e.nom AS etu_nom, f.nom_filiere AS etu_filiere, p.annee AS etu_annee 
            FROM LNM_etudiant e
            JOIN LNM_promo p ON e.id_promo = p.id_promo
            JOIN LNM_filiere f ON p.id_filiere = f.id_filiere";
    
    $conditions = [];

    if (isset($_POST['valider'])) {
        $filiere = $_POST['filiere'];
        $annee = $_POST['annee'];

        if ($annee != "pas_annee") {
            $conditions[] = "p.annee = '{$annee}'";
        }
        if ($filiere != "pas_filiere") {
            $conditions[] = "f.nom_filiere = '{$filiere}'";
        }
    }

    if (!empty($conditions)) {
        $sql .= " WHERE " . implode(' AND ', $conditions);
    }

    $result = mysqli_query($conn, $sql);
    
    if (mysqli_num_rows($result) > 0) {
        echo "<div class='conteneur_grid'>";
        echo "<div id='etudiants'>";
        while ($row = mysqli_fetch_array($result)) {
            echo "<div class='etudiant'> <div id='nom_prenom'> " . $row['etu_nom'] . " " . $row['etu_prenom'] . "</div> <div id='annee_filiere'> " . $row['etu_annee'] . " " . $row['etu_filiere'] . "</div> </div>";
        }
        echo "</div>";
        echo "</div>";
        
        echo "<div id='pagination'>
                <button id='btn_prev' class='bouton'>Précédent</button>
                <span id='page_info'></span>
                <button id='btn_next' class='bouton'>Suivant</button>
              </div>";
    } else {
        echo "<p id='erreur_recherche'>Il n'y a pas d'étudiants correspondant à la recherche.</p>";
    }

} else {
    // -------------------------------------------------------------------------
    // PAGE D'ACCUEIL (CHOIX DE LA LISTE)
    // -------------------------------------------------------------------------
    
    // Link to the specific CSS for this page
    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';

    echo "<div id='choix_liste'>";
        echo "<label id='formulaire' for='choix'>Sélectionnez la liste à afficher</label>";
        
        echo "<div class='choice-container'>";
            echo "<a href='?page=home&section=liste_personnel&list=prof' class='choice-card'>";
                echo "<span>Enseignants</span>";
            echo "</a>";
            
            echo "<a href='?page=home&section=liste_personnel&list=etu' class='choice-card'>";
                echo "<span>Etudiants</span>";
            echo "</a>";
        echo "</div>";
    echo "</div>";
}
?>