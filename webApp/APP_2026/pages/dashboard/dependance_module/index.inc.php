<?php
require_once __DIR__ . "/../../../utils/endpoint.php";

$token = $_SESSION["jwt_token"];
$user_id = $_SESSION['id'];
$user_type = $_SESSION['type'];


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (ob_get_length()) ob_clean();
    header('Content-Type: application/json');

    $body = json_decode(file_get_contents('php://input'), true);

    if ($body) {
        $sql = "INSERT INTO MAQUETTE_module (
                    code_module, nom_module, hCM, hTD, hTP, hProj, hPerso, ECTS, id_semestre, id_responsable, id_discipline
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        $stmt = mysqli_prepare($conn, $sql);

        if ($stmt) {
            $code = $body['code_module'] ?? '';
            $nom = $body['nom_module'] ?? ''; // ou 'nom' selon ce que vous envoyez
            $hCM = $body['hCM'] ?? 0;
            $hTD = $body['hTD'] ?? 0;
            $hTP = $body['hTP'] ?? 0;
            $hProj = $body['hProj'] ?? 0; // ou 'hProjet'
            $hPerso = $body['hPerso'] ?? 0;
            $ects = $body['ECTS'] ?? 0;
            $semestre = $body['semestre'] ?? 0;
            $resp = $body['id_responsable'] ?? 0;
            $disc = $body['id_discipline'] ?? 0;

            mysqli_stmt_bind_param($stmt, "ssddddddiii", 
                $code, $nom, $hCM, $hTD, $hTP, $hProj, $hPerso, $ects, $semestre, $resp, $disc
            );

            if (mysqli_stmt_execute($stmt)) {
                echo json_encode(["status" => "success", "message" => "Module créé en dur avec succès."]);
            } else {
                http_response_code(400);
                echo json_encode(["detail" => "Erreur SQL : " . mysqli_stmt_error($stmt)]);
            }
            mysqli_stmt_close($stmt);
        } else {
            http_response_code(500);
            echo json_encode(["detail" => "Erreur de préparation SQL : " . mysqli_error($conn)]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["detail" => "Aucune donnée reçue."]);
    }
    
    exit;
}

if ($user_type=== 'enseignant') {
    $dataGantt = get_data_gantt($user_id, $token);
    $enseignants = get_enseignants($token);
    $disciplines = get_disciplines($token);
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

    if (!empty($item['prv_discipline'])) $filieres[] = $item['prv_discipline'];
    if (!empty($item['nxt_discipline'])) $filieres[] = $item['nxt_discipline'];
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
            <?php if ($user_type === 'enseignant') { ?>
              <div class="button-section">
                  <?= render("components/button", [
                      "id" => "btn-add-module", 
                      "label" => "Ajouter module", 
                      "variant" => "primary", 
                      "size" => "sm"
                  ]) ?>
                  <?= render("components/button", [
                      "id" => "btn-add-sequence", 
                      "label" => "Ajouter séquence", 
                      "variant" => "primary", 
                      "size" => "sm"
                  ]) ?>
              </div>
            <?php } ?>


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
          <label for="nom_module">Nom du module</label>
          <input type="text" id="nom_module" name="nom_module" placeholder="ex: Projet Algorithmique" required>
        </div>

        <div class="form-group full">
          <label>Heures (CM · TD · TP· Proj· Perso) et ECTS</label>
          <div class="input-row">
            <input type="number" name="hCM" placeholder="CM" min="0" step="0.5">
            <input type="number" name="hTD" placeholder="TD" min="0" step="0.5">
            <input type="number" name="hTP" placeholder="TP" min="0" step="0.5">
            <input type="number" name="hProjet" placeholder="Projet" min="0" step="0.5">
            <input type="number" name="hPerso" placeholder="Perso" min="0" step="0.5">
            <input type="number" name="ECTS" placeholder="ECTS" min="0" step="0.5">
            
          </div>
        </div>

        <div class="form-group full">
          <label>Semestre</label>
          <div class="semestre-pills">
            <input class="pill-input" type="radio" name="semestre" id="s1" value="1">
            <label class="pill-label" for="s1">S1</label>
            <input class="pill-input" type="radio" name="semestre" id="s2" value="2">
            <label class="pill-label" for="s2">S2</label>
            <input class="pill-input" type="radio" name="semestre" id="s3" value="3">
            <label class="pill-label" for="s3">S3</label>
            <input class="pill-input" type="radio" name="semestre" id="s4" value="4">
            <label class="pill-label" for="s4">S4</label>
            <input class="pill-input" type="radio" name="semestre" id="s5" value="5">
            <label class="pill-label" for="s5">S5</label>
            <input class="pill-input" type="radio" name="semestre" id="s6" value="6">
            <label class="pill-label" for="s6">S6</label>
            <input class="pill-input" type="radio" name="semestre" id="s7" value="7">
            <label class="pill-label" for="s7">S7</label>
            <input class="pill-input" type="radio" name="semestre" id="s8" value="8">
            <label class="pill-label" for="s8">S8</label>
            <input class="pill-input" type="radio" name="semestre" id="s9" value="9">
            <label class="pill-label" for="s9">S9</label>
            <input class="pill-input" type="radio" name="semestre" id="s10" value="10">
            <label class="pill-label" for="s10">S10</label>
          </div>
        </div>

        <div class="form-group full">
          <label for="id_responsable">Responsable</label>
          <select name="id_responsable" id="id_responsable">
            <option value="">— Sélectionner —</option>
            <?php foreach ($enseignants as $enseignant) { ?>
              <option value="<?= htmlspecialchars($enseignant['id_enseignant']) ?>">
                <?= htmlspecialchars($enseignant['prenom'] . ' ' . $enseignant['nom'] . ' ('. $enseignant['statut']. ') ') ?>
              </option>
            <?php } ?>

          </select>

          <label for="id_responsable">Discipline</label>
          <select name="id_discipline" id="id_discipline">
            <option value="">— Sélectionner —</option>
            <?php foreach ($disciplines as $discipline) { ?>
              <option value="<?= htmlspecialchars($discipline['id_discipline']) ?>">
                <?= htmlspecialchars($discipline['nom']) ?>
              </option>
            <?php } ?>

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