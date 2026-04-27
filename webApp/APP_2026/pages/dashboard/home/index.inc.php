<link rel="stylesheet" href="./pages/dashboard/home/agenda.css" />
<script type="module" src="./pages/dashboard/home/agenda.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/ical.js/1.5.0/ical.min.js"></script>


<script>
    window.ENV = {
        BACKEND_URL: "<?= getenv('PYTHON_BACKEND_DOCKER_URL') ?: 'http://localhost' ?>",
        BACKEND_PORT: "<?= getenv('INSTANCE_NAME') . getenv('PYTHON_BACKEND_DOCKER_PORT') ?: '8000' ?>",
        USER_TOKEN: "<?= $_SESSION["jwt_token"] ?? '' ?>"
    };
    console.log("Environnement chargé :", window.ENV);
</script>

<script type="module" src="./pages/dashboard/home/agenda.js"></script>
<div class="max-w-7xl mx-auto p-8 space-y-12">
    <section class="space-y-2">
        <h1 class="text-4xl font-bold">
            Bienvenue sur l’intranet
        </h1>
        <p class="text-gray-500">
            Accès rapide à vos informations universitaires
        </p>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <a href="<?= router("home", ["section" => "rendus"]) ?>" class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
            <h2 class="text-xl font-semibold text-blue-700">
                📄 Rendus à venir
            </h2>
            <p class="text-gray-600">
                Consultez vos devoirs à rendre et leurs échéances.
            </p>
        </a>

        <? if ($_SESSION['type'] === 'etudiant') : ?>
            <a href="<?= router("home", ["section" => "etudiant"]) ?>"
            class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
                <h2 class="text-xl font-semibold text-green-700">
                    ⭐ Polypoints
                </h2>
                <p class="text-gray-600">
                    Suivez vos engagements et points acquis.
                </p>
            </a>
        <? endif; ?>

        <a href="<?= router("home", ["section" => "ressources"]) ?>"
           class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
            <h2 class="text-xl font-semibold text-purple-700">
                📚 Ressources
            </h2>
            <p class="text-gray-600">
                Accédez aux services et outils universitaires.
            </p>
        </a>

    </section>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-xl shadow p-6 space-y-4">
            <div class="flex items-center justify-between">
                <h2 class="text-2xl font-semibold text-indigo-700">
                    📅 Agenda
                </h2>
            </div>

            <div id="calendar-container" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-500">
                
                <div id="calendar-controls" class="flex items-center justify-between mb-4">
                    <button id="prev-week" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition">Semaine Précédente</button>
                    <div id="current-month" class="text-lg font-bold text-gray-700"></div>
                    <button id="next-week" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition">Semaine Suivante</button>
                </div>

                <div id="calendar-wrapper" class="py-8">
                    <div id="time-scale"></div>
                    </div>

                <div id="tooltip"></div>
            </div>

            <template id="calendar-setup-template">
                <div class="max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg border border-gray-100">
                    <div class="text-4xl mb-4">📅</div>
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Configuration du Planning</h3>
                    <p class="text-sm text-gray-600 mb-6">Collez votre lien <strong>iCal</strong> ou <strong>ADE</strong> pour synchroniser votre emploi du temps.</p>
                    
                    <input type="text" id="ade-url-input" 
                        class="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 outline-none"
                        placeholder="https://ade-usmb-ro.grenet.fr/...">

                    <input type="text" id="url-name-input" 
                        class="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-blue-500 outline-none"
                        placeholder="Nom du calendrier (ex: 'Planning des cours')">

                    <button id="save-calendar-btn" 
                            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors">
                        Enregistrer le lien
                    </button>
                    <p class="mt-4 text-xs text-gray-400 italic">
                        Besoin d'aide ? <a href="#" class="text-blue-500 underline">Où trouver mon lien ?</a>
                    </p>
                </div>
            </template>
        </div>

        <!-- ACTUALITÉS -->
        <div class="bg-white rounded-xl shadow p-6 space-y-4">

            <h2 class="text-2xl font-semibold text-orange-600">
                📰 Actualités
            </h2>

            <!-- Liste des actualités #idée -->
            <ul class="space-y-3">
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Ouverture des inscriptions sport</p>
                    <p class="text-sm text-gray-500">10 janvier 2025</p>
                </li>
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Fermeture exceptionnelle de la BU</p>
                    <p class="text-sm text-gray-500">18 janvier 2025</p>
                </li>
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Semaine de sensibilisation VSS</p>
                    <p class="text-sm text-gray-500">Du 22 au 26 janvier</p>
                </li>
            </ul>
        </div>
    </section>

</div>
