<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />

<!-- Import Leaflet JS -->
 <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
     integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
     crossorigin="">
</script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- ToDo : Déplacer dans un fichier global ex db.js -->
<script>
    window.ENV = {
        BACKEND_URL: "http://127.0.0.1",
        BACKEND_PORT: "44000",
        USER_TOKEN: "<?= $_SESSION["jwt_token"] ?>"
    };
    console.log("Environnement chargé :", window.ENV);
</script>

<script type="module" src="pages/dashboard/mobility_map/map.js" defer></script>

<!-- Map component -->
<div id="map" style="height: 100%; width: 100%;"></div>

<!-- Filtres -->
<div class="absolute top-[120px] left-1/2 -translate-x-1/2 z-[1000] flex flex-col items-center gap-2.5">
    <button onclick="document.getElementById('filterForm').classList.toggle('hidden')" class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
        Filtres
    </button>

    <form id="filterForm" onsubmit="return false;" class="hidden bg-white p-4 rounded-lg shadow-lg border border-gray-200">
        <div class="flex flex-wrap justify-center items-center gap-4">
            <div class="flex flex-col">
                <label for="filiereSelect" class="text-xs font-semibold text-gray-600 mb-1">Filière</label>
                <select name="filiere" id="filiereSelect" onchange="updateMap()" class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary">
                <option value="">Toutes</option>
                <option value="BAT">BAT</option>
                <option value="EIT">EIT</option>
                <option value="IDU">IDU</option>
                <option value="MC">MC</option>
                <option value="MM">MM</option>
                <option value="SNI">SNI</option>
                </select>
            </div>
            <div class="flex flex-col">
                <label for="semestreSelect" class="text-xs font-semibold text-gray-600 mb-1">Semestre</label>
                <select name="semestre" id="semestreSelect" onchange="updateMap()" class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary">
                <option value="S8">S8</option>
                <option value="S9">S9</option>
                </select>
            </div>
            <div class="flex flex-col">
                <div class="flex justify-between items-center mb-1">
                    <label for="noteMinRange" class="text-xs font-semibold text-gray-600">Note minimale</label>
                    <span id="noteMinValue" class="text-xs font-bold text-gray-700">20</span>
                </div>
                <input type="range" name="notemin" id="noteMinRange" min="0" max="20" value="20" class="w-32 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary" oninput="document.getElementById('noteMinValue').innerText = this.value; updateMap()">
            </div>
        </div>
    </form>
</div>