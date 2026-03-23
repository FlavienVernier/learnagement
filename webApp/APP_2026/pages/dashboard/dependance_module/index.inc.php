<?php
require_once __DIR__ . "/../../../utils/endpoint.php";
$token = $_SESSION["jwt_token"];

echo "<!-- DEBUG: dependency module index.inc.php loaded -->\n";
echo "<!-- DEBUG: jwt_token = $token -->\n";

echo '<link rel="stylesheet" href="pages/dashboard/dependance_module/dependance_module.css"/>';
echo '<script type="module" src="pages/dashboard/dependance_module/index.inc.js" defer></script>';
?>

<div class="dependance-module-container">

    <header class="top-bar">
        <a href="formulaire.php" class="btn-form">⬅ Aller au formulaire</a>
    </header>

    <section class="main-content">
        <div class="filters-section">
            <select id="filiere" class="filter-dropdown">
                <option value="">Sélectionner une Filière...</option>
                <option value="informatique">Informatique</option>
                <option value="design">Design</option>
                <option value="commerce">Commerce</option>
            </select>

            <select id="temps" class="filter-dropdown">
                <option value="">Sélectionner une Période...</option>
                <option value="semestre1">Semestre 1</option>
                <option value="semestre2">Semestre 2</option>
                <option value="annee">Année complète</option>
            </select>

            <select id="module" class="filter-dropdown">
                <option value="">Sélectionner un Module...</option>
                <option value="maths">Mathématiques</option>
                <option value="dev_web">Développement Web</option>
                <option value="marketing">Marketing</option>
            </select>
        </div>

        <div id="active-tags-container" class="tags-container"></div>

        <div class="gantt-wrapper">
            <div id="gantt-chart">
                <p class="placeholder-text">Le diagramme de Gantt s'affichera ici</p>
            </div>
        </div>
</section>

</div>
</html>