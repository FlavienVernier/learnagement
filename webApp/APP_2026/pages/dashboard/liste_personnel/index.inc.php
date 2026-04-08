<?php

require_once __DIR__ . "/../../../utils/endpoint.php";

$token = $_SESSION["jwt_token"];
$list = $_GET['list'] ?? null;

if ($list === 'prof') {

    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';
    echo '<script type="module" src="pages/dashboard/liste_personnel/index.inc.js" defer></script>';

    echo "<form method='post' action='?page=home&section=liste_personnel&list=prof'>";
    echo "<input type='text' name='query' placeholder='Entrez une recherche'>";
    echo "<input class='bouton' type='submit' name='bouton_recherche' value='Rechercher'>";
    echo "<a href='?page=home&section=liste_personnel' class='bouton'>Retour</a>";
    echo "</form>";

    // récupération via API
    $rows = get_enseignants($token);

    // filtrage éventuel
    if (isset($_POST['bouton_recherche']) && !empty($_POST['query'])) {
        $query = strtolower($_POST["query"]);

        $rows = array_filter($rows, function($row) use ($query) {
            return strpos(strtolower($row["mail"]), $query) !== false;
        });
    }

    if (!empty($rows)) {

        echo "<div class='conteneur_grid'>";
        echo "<div id='enseignants'>";

        foreach ($rows as $row) {

            echo "<div class='enseignant'>
                    <a id='info_prof' href='?page=home&section=info_enseignant&id=" . $row['id_enseignant'] . "'>
                        " . $row['nom'] . " " . $row['prenom'] . "
                    </a>
                    <a id='mail_prof' href='mailto:" . $row['mail'] . "'>
                        " . $row['mail'] . "
                    </a>
                 </div>";
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

    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';
    echo '<script type="module" src="pages/dashboard/liste_personnel/index.inc.js" defer></script>';

    echo "<form method='post' action='?page=home&section=liste_personnel&list=etu'>";
    echo "<label id='formulaire'>Rechercher un étudiant :</label>";

    echo "<div id='conteneur_recherche'>
            <div id='barre_recherche'>
                <input type='text' id='search_input' placeholder='ex : Dupont'>
                <button type='button' id='btn_recherche' class='bouton'>Rechercher</button>
                <a href='?page=home&section=liste_personnel' class='bouton'>Retour</a>
            </div>
          </div>";
    echo "</form>";

    // appel endpoint
    $url = get_python_backend_url("etudiants/");
    $rows = get_endpoint($url, $token);

    if (!empty($rows)) {

        echo "<div class='conteneur_grid'>";
        echo "<div id='etudiants'>";

        foreach ($rows as $row) {

            echo "<div class='etudiant'>
                    <div id='nom_prenom'>
                        " . $row['nom'] . " " . $row['prenom'] . "
                    </div>
                  </div>";
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

    echo '<link rel="stylesheet" href="pages/dashboard/liste_personnel/liste_personnel.css"/>';

    echo "<div id='choix_liste'>";

    echo "<label id='formulaire'>Sélectionnez la liste à afficher</label>";

    echo "<div class='choice-container'>";

    echo "<a href='?page=home&section=liste_personnel&list=prof' class='choice-card'>
            <span>Enseignants</span>
          </a>";

    echo "<a href='?page=home&section=liste_personnel&list=etu' class='choice-card'>
            <span>Etudiants</span>
          </a>";

    echo "</div>";
    echo "</div>";
}
