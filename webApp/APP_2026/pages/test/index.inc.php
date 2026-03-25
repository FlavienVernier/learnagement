<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Components - Test Page</title>

    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="../theme/theme.css">
    <link rel="stylesheet" href="../theme/tailwind.extension.css">

    <style>
        /* BASE RESET */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
            font-size: 14px;
            background: var(--c-bg);
            color: var(--c-text);
            line-height: 1.5;
            min-height: 100vh;
        }
        /* Add a little spacing between components for the test page */
        .test-section { margin-bottom: 40px; display: flex; flex-direction: column; gap: 16px; }
    </style>
</head>
<body>
<div class="page">

    <div class="page-title">Polytech — UI Components Test</div>
    <div class="page-sub">Test de tous les composants dynamiques PHP.</div>

    <div class="test-section">
        <h3>0. Alerts</h3>
        <div class="col" style="max-width:520px; gap: 16px;">
            <?= render("components/alert", [
                "type" => "info",
                "message" => "La période d'inscription se termine le 30 juin 2025."
            ]) ?>

            <?= render("components/alert", [
                "type" => "success",
                "message" => "Votre dossier a bien été soumis."
            ]) ?>

            <?= render("components/alert", [
                "type" => "warning",
                "message" => "Des pièces justificatives sont manquantes."
            ]) ?>

            <?= render("components/alert", [
                "type" => "error",
                "message" => "Impossible de se connecter. Vérifiez vos identifiants."
            ]) ?>
        </div>
    </div>

    <div class="test-section">
        <h3>1. Controls (Checkboxes, Radios, Toggles)</h3>
        <div class="row" style="align-items:flex-start; gap:32px; flex-wrap:wrap;">
            <div class="col">
                <?= render("components/checkbox", ["label" => "Option A", "checked" => true]) ?>
                <?= render("components/checkbox", ["label" => "Option B"]) ?>
                <?= render("components/checkbox", ["label" => "Désactivé", "disabled" => true]) ?>
            </div>

            <div class="col">
                <?= render("components/radio", ["label" => "Étudiant", "name" => "demo-radio", "checked" => true]) ?>
                <?= render("components/radio", ["label" => "Enseignant", "name" => "demo-radio"]) ?>
                <?= render("components/radio", ["label" => "Administrateur", "name" => "demo-radio"]) ?>
            </div>

            <div class="col">
                <?= render("components/toggle", [
                    "label" => "Notifications", 
                    "checked" => true, 
                    "onchange" => "syncToggle(this)"
                ]) ?>
                <?= render("components/toggle", [
                    "label" => "Mode sombre", 
                    "onchange" => "syncToggle(this)"
                ]) ?>
                <?= render("components/toggle", [
                    "label" => "Désactivé", 
                    "disabled" => true
                ]) ?>
            </div>
        </div>
    </div>

    <div class="test-section">
        <h3>2. Cards</h3>
        <div class="row" style="gap: 16px; align-items: flex-start;">
            <?= render("components/card", [
                "style" => "width:240px",
                "header" => 
                    '<span class="card-title">Cours du semestre</span>' . 
                    render("components/badge", ["label" => "Actif", "color" => "success", "dot" => true]),
                "body" => "Algorithmique avancée — 4 ECTS",
                "footer" => 
                    render("components/button", ["label" => "Voir", "variant" => "accent", "size" => "sm"]) . 
                    render("components/button", ["label" => "Ignorer", "variant" => "ghost", "size" => "sm"])
            ]) ?>

            <?= render("components/card", [
                "interactive" => true,
                "style" => "width:240px",
                "onclick" => "alert('Card clicked!')",
                "header" => 
                    '<span class="card-title">Projet tuteuré</span>' . 
                    render("components/badge", ["label" => "En cours", "color" => "warning", "dot" => true]),
                "body" => "Dépôt avant le 15 mai &middot; Groupe de 4",
                "footer" => '<span style="font-size:12px; color:var(--c-text-3)">Cliquez pour détails &rarr;</span>'
            ]) ?>
        </div>
    </div>

    <div class="test-section">
        <h3>3. Buttons & Badges</h3>
        <div class="row">
            <?= render("components/button", ["label" => "Small", "variant" => "primary", "size" => "sm"]) ?>
            <?= render("components/button", ["label" => "Medium", "variant" => "primary"]) ?>
            <?= render("components/button", ["label" => "Large", "variant" => "primary", "size" => "lg"]) ?>
        </div>
        <div class="row">
            <?= render("components/badge", ["label" => "Primary", "color" => "primary"]) ?>
            <?= render("components/badge", ["label" => "Accent", "color" => "accent"]) ?>
            <?= render("components/badge", ["label" => "Neutre", "color" => "neutral"]) ?>
            <?= render("components/badge", ["label" => "Actif", "color" => "success", "dot" => true]) ?>
            <?= render("components/badge", ["label" => "En attente", "color" => "warning", "dot" => true]) ?>
            <?= render("components/badge", ["label" => "Erreur", "color" => "error", "dot" => true]) ?>
        </div>
    </div>

    <div class="test-section">
        <h3>4. Avatars</h3>
        <div class="row">
            <?= render("components/avatar", ["initials" => "JD", "size" => "sm", "color" => "primary"]) ?>
            <?= render("components/avatar", ["initials" => "ML", "size" => "md"]) ?>
            <?= render("components/avatar", ["initials" => "AP", "size" => "lg", "color" => "success"]) ?>
            
            <?php 
            $groupData = [
                ["initials" => "JD", "size" => "md", "color" => "primary"],
                ["initials" => "ML", "size" => "md"],
                ["initials" => "AP", "size" => "md", "color" => "success"],
                ["initials" => "+4", "size" => "md", "color" => "warning", "tooltip" => "+4 autres"]
            ];
            ?>
            <?= render("components/avatar_group", ["avatars" => $groupData]) ?>
        </div>
    </div>

    <div class="test-section">
        <h3>5. Dividers</h3>
        <div class="col" style="max-width:400px; gap:16px">
            <?= render("components/divider") ?>
            <?= render("components/divider", ["label" => "ou"]) ?>
            <?= render("components/divider", ["label" => "Section suivante"]) ?>
        </div>
    </div>

    <div class="test-section">
        <h3>6. Inputs, Search & Select</h3>
        <div class="col" style="gap: 16px;">
            <?= render("components/search_bar", ["id" => "search-demo"]) ?>
            <?= render("components/search_bar", ["size" => "lg", "placeholder" => "Recherche globale…", "showClear" => false]) ?>

            <div class="row" style="align-items: flex-start;">
                <div class="col" style="max-width:300px;">
                    <?= render("components/input", [
                        "label" => "Nom complet",
                        "placeholder" => "ex. Marie Dupont",
                        "hint" => "Tel qu'il apparaît sur votre carte étudiant."
                    ]) ?>

                    <?= render("components/input", [
                        "label" => "Email",
                        "type" => "email",
                        "value" => "invalide@",
                        "error" => true,
                        "errorMsg" => "Adresse email invalide."
                    ]) ?>
                </div>

                <div class="col" style="max-width:300px;">
                    <?= render("components/input", [
                        "type" => "textarea",
                        "label" => "Description",
                        "placeholder" => "Décrivez votre projet…"
                    ]) ?>

                    <?= render("components/select", [
                        "label" => "Département",
                        "minWidth" => 180,
                        "options" => ["Informatique", "Mécanique", "Électronique", "Génie civil"]
                    ]) ?>
                </div>
            </div>
        </div>
    </div>

    <div class="test-section">
    <h3>7. Dropdown</h3>
        <?php
        $dropdownItems = [
            ["type" => "label", "label" => "Fichier"],
            ["label" => "Modifier", "icon" => "✎"],
            ["label" => "Dupliquer", "icon" => "⎘"],
            ["type" => "divider"],
            ["label" => "Supprimer", "icon" => "🗑", "danger" => true]
        ];

        // Notice we added the 'onclick' right here!
        $dropdownTrigger = render("components/button", [
            "label" => "Actions <span style='font-size:9px; opacity:.6'>▾</span>", 
            "variant" => "secondary",
            "onclick" => "toggleDropdown('dd1')" 
        ]);
        ?>

        <?= render("components/dropdown", [
            "id" => "dd1",
            "trigger" => $dropdownTrigger,
            "items" => $dropdownItems
        ]) ?>
    </div>

    <script>
        function toggleDropdown(id) {
            const menu = document.getElementById(id + '-menu');
            if (!menu) return; // Prevent errors if menu isn't found
            
            const isOpen = menu.classList.contains('open');
            document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
            if (!isOpen) menu.classList.add('open');
        }
        
        document.addEventListener('click', e => {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
            }
        });
    </script>

    <div class="test-section">
        <h3>8. Skeletons</h3>
        <div class="row" style="align-items:flex-start; gap:24px">
            <div class="col" style="width:220px; gap:8px">
                <?= render("components/skeleton", ["type" => "title"]) ?>
                <?= render("components/skeleton", ["type" => "text"]) ?>
                <?= render("components/skeleton", ["type" => "text", "style" => "width:75%"]) ?>
                <?= render("components/skeleton", ["type" => "text", "style" => "width:55%"]) ?>
            </div>
            
            <div class="col" style="gap:8px">
                <div class="row" style="gap:10px">
                    <?= render("components/skeleton", ["type" => "avatar"]) ?>
                    <div class="col" style="gap:6px; width:160px">
                        <?= render("components/skeleton", ["type" => "text", "style" => "width:120px; height:12px"]) ?>
                        <?= render("components/skeleton", ["type" => "text", "style" => "width:80px; height:10px"]) ?>
                    </div>
                </div>
                <?= render("components/skeleton", ["type" => "btn"]) ?>
            </div>
        </div>
    </div>

    <div class="test-section">
        <h3>9. Tabs</h3>
        <div class="col">
            <?= render("components/tabs", [
                "groupId" => "tabs-under",
                "tabs" => [
                    ["label" => "Présentation", "active" => true],
                    ["label" => "Documents"],
                    ["label" => "Planning"],
                    ["label" => "Notes"]
                ]
            ]) ?>

            <?= render("components/tabs", [
                "type" => "pill",
                "groupId" => "tabs-pill",
                "style" => "width:fit-content",
                "tabs" => [
                    ["label" => "Semaine", "active" => true],
                    ["label" => "Mois"],
                    ["label" => "Année"]
                ]
            ]) ?>
        </div>
    </div>

</div><script>
    /* ── Toggle ── */
    function syncToggle(input) { 
        // Logic depends on your CSS, but usually just needs to trigger onchange 
        console.log('Toggle state:', input.checked);
    }

    /* ── Dropdown ── */
    function toggleDropdown(id) {
        const menu = document.getElementById(id + '-menu');
        const isOpen = menu.classList.contains('open');
        document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
        if (!isOpen) menu.classList.add('open');
    }
    
    document.addEventListener('click', e => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
        }
    });

    /* ── Tabs ── */
    function setTab(btn, group) {
        const parent = btn.closest('[role="tablist"]');
        parent.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        btn.classList.add('active');
    }
</script>
</body>
</html>