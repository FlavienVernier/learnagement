<?php
require_once __DIR__ . "/../../../utils/endpoint.php";
$token = $_SESSION["jwt_token"];
$user_id = $_SESSION['id'];

$enseignants = get_enseignants($token);
$etudiants = get_etudiants($token);

$modulesResp = get_modules_responsables($token);
$promos = get_promos($token);
$filieres = get_filieres($token);
$modulesDepedencies = get_module_dependencies(61, $token);
$modulesResponsable = get_modules_responsable_by_id($user_id, $token);
$get_modules_intervenant_by_id = get_modules_intervenant_by_id($user_id, $token);
?>

<script src="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.css"/>
<link rel="stylesheet" href="pages/dashboard/dependance_module/dependance_module.css"/>
<script type="module" src="pages/dashboard/dependance_module/index.inc.js" defer></script>

<script>
    const dataModules = <?php echo json_encode($modulesResp); ?>;
    const dataPromos = <?php echo json_encode($promos); ?>;
    const dataFilieres = <?php echo json_encode($filieres); ?>;
    const dataModulesDependencies = <?php echo json_encode($modulesDepedencies); ?>;
    const dataModulesResponsables = <?php echo json_encode($modulesResponsable); ?>;
    const dataModulesIntervenantById = <?php echo json_encode($get_modules_intervenant_by_id); ?>;
    const enseignants = <?php echo json_encode($enseignants); ?>;
    const token = "<?= htmlspecialchars($token) ?>";
    const userId = <?= json_encode($user_id) ?>;
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
                <?= render("components/button", ["id" => "btn-add-module", "label" => "Ajouter module", "variant" => "primary", "size" => "lg"]) ?>
            </div>


            <div class="gantt-wrapper">
                <svg id="gantt-chart"></svg>
            </div>
            
        </div>

    </section>

    <dialog id="modal-ajout-module" style="padding: 20px; border-radius: 8px; border: 1px solid #ccc; max-width: 500px;">
    <h3>Créer un nouveau module</h3>
    
    <form id="form-ajout-module">
        <div style="margin-bottom: 15px;">
            <label>Code du cours :</label>
            <input type="text" name="code_module" placeholder="Ex: M2101" required style="width: 100%;">
        </div>

        <div style="margin-bottom: 15px;">
            <label>Nom du cours :</label>
            <input type="text" name="nom" placeholder="Ex: Programmation Web" required style="width: 100%;">
        </div>

        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
            <div>
                <label>Heures CM :</label>
                <input type="number" step="0.5" name="hCM" placeholder="0" style="width: 100%;">
            </div>
            <div>
                <label>Heures TD :</label>
                <input type="number" step="0.5" name="hTD" placeholder="0" style="width: 100%;">
            </div>
            <div>
                <label>Heures TP :</label>
                <input type="number" step="0.5" name="hTP" placeholder="0" style="width: 100%;">
            </div>
        </div>

        <div style="margin-bottom: 15px;">
            <label>Semestre :</label>
            <input type="number" name="semestre" placeholder="Ex: 3" required style="width: 100%;">
        </div>

        <div style="margin-bottom: 15px;">
            <label>Enseignant associé :</label>
            <select name="id_responsable" required style="width: 100%;">
                <option value="">-- Sélectionner un enseignant --</option>
                <option value="1">M. Dupont</option> 
            </select>
        </div>

        <div style="margin-bottom: 15px;">
            <label>Promos associées :</label>
            <select name="promos[]" multiple style="width: 100%; height: 60px;">
                <option value="1">Promo 2024</option>
                <option value="2">Promo 2025</option>
            </select>
        </div>

        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
            <div style="flex: 1;">
                <label>Dépendances (Avant) :</label>
                <select name="dependances_avant[]" multiple style="width: 100%; height: 60px;">
                    <option value="10">M1101 - Intro</option>
                </select>
            </div>
            <div style="flex: 1;">
                <label>Dépendances (Après) :</label>
                <select name="dependances_apres[]" multiple style="width: 100%; height: 60px;">
                    <option value="15">M3101 - Avancé</option>
                </select>
            </div>
        </div>

        <div style="text-align: right; margin-top: 20px;">
            <button type="button" id="btn-cancel-module" style="margin-right: 10px;">Annuler</button>
            <button type="submit">Créer le module</button>
        </div>
    </form>
</dialog>

</div>