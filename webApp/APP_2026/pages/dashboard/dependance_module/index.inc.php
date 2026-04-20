<?php
require_once __DIR__ . "/../../../utils/endpoint.php";
$token = $_SESSION["jwt_token"];
$user_id = $_SESSION['id'];
$user_type = $_SESSION['type'];

if ($user_type=== 'enseignant') {
    $dataGantt = get_data_gantt($user_id, $token);
} else {
    $dataGantt = get_data_gantt_etudiant($user_id, $token);
}

$semestres_bruts = [];
$modules_bruts = [];
$filieres=[];

foreach ($dataGantt as $item) {
    if (!empty($item['prv_semestre'])) $semestres_bruts[] = $item['prv_semestre'];
    if (!empty($item['nxt_semestre'])) $semestres_bruts[] = $item['nxt_semestre'];
    
    if (!empty($item['prv_nom'])) $modules_bruts[] = $item['prv_nom'];
    if (!empty($item['nxt_nom'])) $modules_bruts[] = $item['nxt_nom'];

    if (!empty($item['prv_filiere'])) $filieres[] = $item['prv_filiere'];
    if (!empty($item['nxt_filiere'])) $filieres[] = $item['nxt_filiere'];
}

$options_semestres = array_unique($semestres_bruts);
$options_modules = array_unique($modules_bruts);
$options_filieres = array_unique($filieres);

sort($options_semestres); 
sort($options_modules);
sort($options_filieres);

array_unshift($options_semestres, "Année complète");
?>

<script src="https://cdn.dhtmlx.com/gantt/edge/dhtmlxgantt.js"></script>
<link href="https://cdn.dhtmlx.com/gantt/edge/dhtmlxgantt.css" rel="stylesheet">
<script src="https://cdn.dhtmlx.com/gantt/edge/ext/dhtmlxgantt_grouping.js"></script>

<link rel="stylesheet" href="pages/dashboard/dependance_module/dependance_module.css"/>
<script type="module" src="pages/dashboard/dependance_module/index.inc.js" defer></script>

<script>
    const token = "<?= htmlspecialchars($token) ?>";
    const userId = <?= json_encode($user_id) ?>;
    const userType = <?= json_encode($user_type) ?>;
    const dataGantt = <?php echo json_encode($dataGantt); ?>;
</script>

<div class="dependance-module-container">

    <section class="main-content">
        
        <div class="filters-section">
            <?php if ($user_type === 'enseignant') {
                render("components/select", [
                    "label" => "Filière",
                    "minWidth" => 180,
                    "options" => $options_filieres,
                    "id" => "filiere-filter"
                ]);
            } ?>

            <?= render("components/select", [
                "label" => "Période",
                "minWidth" => 180,
                "options" => $options_semestres,
                "id" => "periode-filter", 
                "defaultText" => "Année complète"
            ]) ?>

            <?= render("components/select", [
                "label" => "Module",
                "minWidth" => 180,
                "options" => $options_modules,
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