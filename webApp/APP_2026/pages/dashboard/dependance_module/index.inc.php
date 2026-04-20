<?php
require_once __DIR__ . "/../../../utils/endpoint.php";
$token = $_SESSION["jwt_token"];
$user_id = $_SESSION['id'];
$user_type = $_SESSION['type'];

$enseignants = get_enseignants($token);
$etudiants = get_etudiants($token);

$modulesResp = get_modules_responsables($token);
$promos = get_promos($token);
$filieres = get_filieres($token);
$modulesDepedencies = get_module_dependencies(61, $token);
$modulesResponsable = get_modules_responsable_by_id($user_id, $token);
$get_modules_intervenant_by_id = get_modules_intervenant_by_id($user_id, $token);
if ($user_type=== 'enseignant') {
    $dataGantt = get_data_gantt($user_id, $token);
} else {
    $dataGantt = get_data_gantt_etudiant($user_id, $token);
}
?>

<script src="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/frappe-gantt/0.6.1/frappe-gantt.min.css"/>
<script src="https://cdn.dhtmlx.com/gantt/edge/dhtmlxgantt.js"></script>
<link href="https://cdn.dhtmlx.com/gantt/edge/dhtmlxgantt.css" rel="stylesheet">

<link rel="stylesheet" href="pages/dashboard/dependance_module/dependance_module.css"/>
<script type="module" src="pages/dashboard/dependance_module/index.inc.js" defer></script>

<script>
    const token = "<?= htmlspecialchars($token) ?>";
    const userId = <?= json_encode($user_id) ?>;
    const userType = <?= json_encode($user_type) ?>;
    const dataGantt = <?php echo json_encode($dataGantt); ?>;

    
    const dataModules = <?php echo json_encode($modulesResp); ?>;
    const dataPromos = <?php echo json_encode($promos); ?>;
    const dataFilieres = <?php echo json_encode($filieres); ?>;
    const dataModulesDependencies = <?php echo json_encode($modulesDepedencies); ?>;
    const dataModulesResponsables = <?php echo json_encode($modulesResponsable); ?>;
    const dataModulesIntervenantById = <?php echo json_encode($get_modules_intervenant_by_id); ?>;
    const enseignants = <?php echo json_encode($enseignants); ?>;

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


            <div id = "gantt-chart" class="gantt-chart"></div>
            
        </div>

    </section>

    <dialog id="modal-ajout-module">
  <div class="modal-header">
    <h2>Nouveau module</h2>
    <button class="btn-close" id="btn-cancel-module-cross" aria-label="Fermer">×</button>
  </div>
  <div class="modal-body">
    <form id="form-ajout-module">
      <div class="form-grid">

        <div class="form-group">
          <label for="code_module">Code module</label>
          <input type="text" id="code_module" name="code_module" placeholder="ex: PROJ631" required>
        </div>

        <div class="form-group">
          <label for="nom">Nom du module</label>
          <input type="text" id="nom" name="nom" placeholder="ex: Projet Algorithmique" required>
        </div>

        <div class="form-group full">
          <label>Heures (CM · TD · TP)</label>
          <div class="input-row">
            <input type="number" name="hCM" placeholder="CM" min="0" step="0.5">
            <input type="number" name="hTD" placeholder="TD" min="0" step="0.5">
            <input type="number" name="hTP" placeholder="TP" min="0" step="0.5">
          </div>
        </div>

        <div class="form-group full">
          <label>Semestre</label>
          <div class="semestre-pills">
            <input class="pill-input" type="radio" name="semestre" id="s1" value="1">
            <label class="pill-label" for="s1">S1</label>
            <input class="pill-input" type="radio" name="semestre" id="s2" value="2">
            <label class="pill-label" for="s2">S2</label>
            <!-- ... S3 à S8 sur le même modèle -->
          </div>
        </div>

        <div class="form-group full">
          <label for="id_responsable">Responsable</label>
          <select name="id_responsable" id="id_responsable">
            <option value="">— Sélectionner —</option>
            <!-- options dynamiques -->
          </select>
        </div>

      </div>
      <div class="modal-footer" style="padding: 20px 0 0;">
        <button type="button" class="btn" id="btn-cancel-module">Annuler</button>
        <button type="submit" class="btn btn-primary">Créer le module</button>
      </div>
    </form>
  </div>
</dialog>

</div>