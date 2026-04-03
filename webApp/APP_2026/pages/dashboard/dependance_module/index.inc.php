<?php
require_once __DIR__ . "/../../../utils/endpoint.php";
$token = $_SESSION["jwt_token"];

$modulesResp = get_modules_responsables($token);
$promos = get_promos($token);
$filieres = get_filieres($token);
$modulesDepedencies = get_module_dependencies(1, $token);
?>

<script src="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.css"/>
<link rel="stylesheet" href="pages/dashboard/dependance_module/dependance_module.css"/>
<script type="module" src="pages/dashboard/dependance_module/index.inc.js" defer></script>

<script>
    window.USER_TOKEN = "<?= htmlspecialchars($token) ?>";
    const dataModules = <?php echo json_encode($modulesResp); ?>;
    const dataPromos = <?php echo json_encode($promos); ?>;
    const dataFilieres = <?php echo json_encode($filieres); ?>;
    const dataModulesDependencies = <?php echo json_encode($modulesDepedencies); ?>;
</script>

<div class="dependance-module-container">

    <section class="main-content">
        
        <div class="filters-section">
            <?= render("components/select", [
                "label" => "Filière",
                "minWidth" => 180,
                "options" => ["Informatique", "Mécanique", "Électronique", "Génie civil"],
                "id" => "filiere-filter"
            ]) ?>

            <?= render("components/select", [
                "label" => "Période",
                "minWidth" => 180,
                "options" => ["Semestre 1", "Semestre 2", "Année complète"],
                "id" => "periode-filter", 
                "defaultText" => "Année complète"
            ]) ?>

            <?= render("components/select", [
                "label" => "Module",
                "minWidth" => 180,
                "options" => ["Mathématiques", "Chimie", "Management", "Sport"],
                "id" => "module-filter"
            ]) ?>
        </div>

        <div id="active-tags-container" class="tags-container"></div>

        <div class="gantt-container-with-button">
            
            <div class="button-section">
                <?= render("components/button", ["label" => "Ajouter module", "variant" => "primary", "size" => "lg"]) ?>
            </div>

            <div class="gantt-wrapper">
                <svg id="gantt-chart"></svg>
            </div>
            
        </div>

    </section>

</div>