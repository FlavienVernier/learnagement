<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Carte de Mobilité — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
<section class="relative flex-1 min-h-[70vh]">
    <!-- Map component -->
    <div id="map" class="absolute inset-0" style="height: 100%; width: 100%;"></div>

    <!-- Street View Modal (grand format) -->
    <div id="streetViewModal" class="streetview-modal">
        <div class="streetview-content">
            <div class="streetview-header">
                <h2 id="streetViewTitle" class="text-lg font-semibold"></h2>
                <button class="streetview-close" onclick="window.closeStreetViewModal()">x</button>
            </div>
            <div id="streetViewPanoramaModal" style="width: 100%; height: 100%;"></div>
        </div>
    </div>

    <!-- Contrôles et panneaux superposés -->
    <div class="absolute top-[100px] left-4 z-[1000] flex max-w-[92vw] flex-col items-start gap-2.5">
        <div class="flex items-center gap-2">
            <button onclick="document.getElementById('filterForm').classList.toggle('hidden')" class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                Filtres
            </button>
            <button onclick="document.getElementById('wishesPanel').classList.toggle('hidden')" class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                Voeux
            </button>
        </div>

        <form id="filterForm" onsubmit="return false;" class="hidden bg-white p-4 rounded-lg shadow-lg border border-gray-200">
            <div class="flex flex-wrap justify-center items-center gap-4">
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

        <aside id="wishesPanel" class="hidden w-[min(92vw,22rem)] max-h-[60vh] overflow-y-auto bg-white/95 p-4 rounded-lg shadow-lg border border-gray-200 backdrop-blur-sm">
            <div class="mb-3 flex items-center justify-between">
                <h2 class="text-sm font-semibold text-gray-800">Mes voeux</h2>
                <span id="wishesCount" class="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-semibold text-primary">0/5</span>
            </div>
            <p id="wishesEmpty" class="text-sm text-gray-500">Aucun voeu pour le moment.</p>
            <ul id="wishesList" class="space-y-2"></ul>
        </aside>
    </div>
</section>
<?php $t->endSlot(); ?>


<?php $t->startSlot('style.top'); ?>
<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
<link rel="stylesheet" href="/APP_2026/theme/mobility-map.css" />
<?php $t->endSlot(); ?>


<?php $t->startSlot('script.top'); ?>
<?php
    $googleMapsApiKey = getenv('GOOGLE_MAPS_API_KEY') ?: ($_ENV['GOOGLE_MAPS_API_KEY'] ?? '');
?>
<!-- Import Leaflet JS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin="">
</script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- Google Maps API pour Street View interactif -->
<script src="https://maps.googleapis.com/maps/api/js?key=<?= urlencode($googleMapsApiKey) ?>&libraries=places"></script>

<!-- Logic map dédiée -->
<script src="/APP_2026/theme/mobility-map-carousel.js"></script>
<script src="/APP_2026/theme/mobility-map-streetview.js"></script>

<!-- ToDo : Déplacer dans un fichier global ex db.js -->
<script>
    window.ENV = {
        BACKEND_URL: "http://127.0.0.1",
        BACKEND_PORT: "44000",
        USER_TOKEN: "<?= $_SESSION["jwt_token"] ?>",
        USER_ID: "<?= $_SESSION["id"] ?>"
    };
    console.log("Environnement chargé :", window.ENV);
</script>
<?php $t->endSlot(); ?>

<?php $t->startSlot('script.bottom'); ?>
<script type="module" defer>
    const map = L.map('map').setView([48.85, 2.35], 4);
    const wishedUniversities = new Map();
    const popupState = new Map();
    window.MobilityMapState = {
        popupState,
        wishedUniversities,
    };

    // In a flex layout, Leaflet can initialize before final dimensions are settled.
    requestAnimationFrame(() => map.invalidateSize());

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const markers = L.markerClusterGroup();

    const fetchUniversities = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/etudiant/" + window.ENV.USER_ID;
        let universities = [];
        try {
            const response = await fetch(url, {
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            universities = await response.json();
            console.log(universities);
        } catch (error) {
            console.error(error.message);
        }

        return universities;
    }

    const fetchWishes = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/etudiant/" + window.ENV.USER_ID + "/wishes";
        let wishes = [];
        try {
            const response = await fetch(url, {
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            wishes = await response.json();
        } catch (error) {
            console.error(error.message);
        }

        return wishes;
    }

    const universities = await fetchUniversities();
    const universitiesById = new Map(
        universities.map((u) => [String(u.id_partner_university), u])
    );
    window.MobilityMapState.universitiesById = universitiesById;

    async function refreshWishesFromServer() {
        const wishes = await fetchWishes();
        wishedUniversities.clear();
        wishes.forEach((wish) => {
            wishedUniversities.set(wish.id_partner_university, wish);
        });
    }
    await refreshWishesFromServer();

    function escapeHtml(value) {
        return String(value)
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    function renderWishesList() {
        const wishesList = document.getElementById('wishesList');
        const wishesEmpty = document.getElementById('wishesEmpty');
        const wishesCount = document.getElementById('wishesCount');
        const wishes = Array.from(wishedUniversities.values())
            .sort((a, b) => (a.priority ?? 999) - (b.priority ?? 999));

        wishesCount.innerText = String(wishes.length) + "/5";

        if (wishes.length === 0) {
            wishesList.innerHTML = '';
            wishesEmpty.classList.remove('hidden');
            return;
        }

        wishesEmpty.classList.add('hidden');
        wishesList.innerHTML = wishes
            .map((wish, index) => `
                <li class="rounded border border-gray-200 bg-gray-50 p-2">
                    <div class="flex items-center justify-between gap-2">
                        <div>
                            <p class="text-sm text-gray-800"><strong class="font-semibold">${escapeHtml(wish.name)}</strong> (${escapeHtml(wish.code)})</p>
                            <p class="text-xs text-gray-600">${escapeHtml(wish.country)}</p>
                        </div>
                        <div class="flex items-center gap-1">
                            <button
                                type="button"
                                onclick="window.moveWish(${wish.id_partner_university}, 'up')"
                                ${(index === 0) ? 'disabled' : ''}
                                class="h-7 w-7 text-base font-semibold text-gray-700 opacity-55 transition-opacity hover:opacity-100 disabled:cursor-not-allowed disabled:opacity-20"
                                title="Monter"
                            >
                                ↑
                            </button>
                            <button
                                type="button"
                                onclick="window.moveWish(${wish.id_partner_university}, 'down')"
                                ${(index === wishes.length - 1) ? 'disabled' : ''}
                                class="h-7 w-7 text-base font-semibold text-gray-700 opacity-55 transition-opacity hover:opacity-100 disabled:cursor-not-allowed disabled:opacity-20"
                                title="Descendre"
                            >
                                ↓
                            </button>
                            <button
                                type="button"
                                onclick="window.deleteWish(${wish.id_partner_university})"
                                class="h-7 w-7 text-base font-semibold text-gray-700 opacity-55 transition duration-150 hover:text-red-600 hover:opacity-100"
                                title="Supprimer"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                </li>
            `)
            .join('');
    }

    function popupText(university) {
        const alreadyInWishes = wishedUniversities.has(university.id_partner_university);
        const uid = String(university.id_partner_university);

        window.MobilityMapState.popupState.set(uid, {
            photos: null,
            photoIndex: 0,
            streetView: null
        });
        
        return `
            <div class="popup-tabs">
                <button id="tab-photos-${uid}" type="button" class="popup-tab" onclick="window.switchPopupTab('${uid}', 'photos')">Photos</button>
                <button id="tab-street-${uid}" type="button" class="popup-tab" onclick="window.switchPopupTab('${uid}', 'streetview')">StreetView</button>
            </div>
            <div id="panel-photos-${uid}" class="popup-panel hidden">
                <div class="popup-carousel">
                    <div class="popup-photo-frame">
                        <img id="photo-image-${uid}" class="popup-photo" alt="Photo universite" />
                        <button id="photo-prev-${uid}" type="button" class="popup-carousel-btn left" onclick="window.prevPopupPhoto('${uid}')" disabled>‹</button>
                        <button id="photo-next-${uid}" type="button" class="popup-carousel-btn right" onclick="window.nextPopupPhoto('${uid}')" disabled>›</button>
                    </div>
                </div>
                <p id="photo-caption-${uid}" class="popup-photo-caption"></p>
                <p id="photo-status-${uid}" class="popup-status">Chargement des photos...</p>
            </div>
            <div id="panel-street-${uid}" class="popup-panel hidden">
                <div id="streetview-${uid}" class="popup-streetview"></div>
                <p id="street-status-${uid}" class="popup-status">Chargement du Street View...</p>
                <div class="popup-streetview-actions">
                    <button id="street-open-${uid}" type="button" class="popup-streetview-expand" onclick="window.openStreetViewModal('${uid}')" disabled>Ouvrir en grand</button>
                </div>
            </div>
            <b>${escapeHtml(university.name)}</b> (${escapeHtml(university.code)})<br/>
            <em class="text-[0.75rem]">${escapeHtml(university.address)}, ${escapeHtml(university.country)}</em><br/>
            Langue${university.languages.includes(',') ? 's' : ''}: ${escapeHtml(university.languages)}<br/>
            ${university.note_min !== null ? `Note min : ${university.note_min}<br/>` : ''}
            <a href="${escapeHtml(university.website)}" target="_blank">${escapeHtml(university.website)}</a><br/>
            <button
                type="button"
                onclick="window.addUniversityToWishes('${uid}')"
                ${alreadyInWishes ? 'disabled' : ''}
                class="mt-2 inline-flex items-center rounded bg-primary px-3 py-1.5 text-sm font-semibold text-white hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
            >
                ${alreadyInWishes ? 'Déjà dans les voeux' : 'Ajouter aux voeux'}
            </button>
        `;
    }

    async function addUniversityToWishes(universityId) {
        const university = universitiesById.get(String(universityId));
        if (!university) {
            console.error('Universite introuvable pour id:', universityId);
            return;
        }

        if (wishedUniversities.has(university.id_partner_university)) {
            return;
        }

        try {
            const wishesEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wish/" + university.id_partner_university;

            const response = await fetch(wishesEndpoint, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok && response.status !== 409) {
                throw new Error(`Response status: ${response.status}`);
            }

            await refreshWishesFromServer();
            renderWishesList();
            updateMap();
            console.log('Université ajoutée aux voeux :', university);
        } catch (error) {
            console.error('Impossible d\'ajouter l\'université aux voeux :', error.message);
        }
    }

    async function deleteWish(idPartnerUniversity) {
        try {
            const deleteEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wish/" + idPartnerUniversity;

            const response = await fetch(deleteEndpoint, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            await refreshWishesFromServer();
            renderWishesList();
            updateMap();
        } catch (error) {
            console.error('Impossible de supprimer le voeu :', error.message);
        }
    }

    async function moveWish(idPartnerUniversity, direction) {
        try {
            const moveEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wish/" + idPartnerUniversity
                + "/move/" + direction;

            const response = await fetch(moveEndpoint, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            await refreshWishesFromServer();
            renderWishesList();
            updateMap();
        } catch (error) {
            console.error('Impossible de deplacer le voeu :', error.message);
        }
    }
    
    window.addUniversityToWishes = addUniversityToWishes;
    window.deleteWish = deleteWish;
    window.moveWish = moveWish;

    function updateMap() {
        markers.clearLayers();
        
        const selectedSemestre = document.getElementById('semestreSelect').value;
        const selectedNote = parseFloat(document.getElementById('noteMinRange').value);

        const filtered = universities.filter(u => {
            // Affiche univ si note_min <= selectedNote
            const uNote = u.note_min === null ? 0 : parseFloat(u.note_min);
            if (uNote > selectedNote) return false;

            // Filtre le semestre
            if (selectedSemestre === "S8") {
                return u.annee === 4;
            } else if (selectedSemestre === "S9") {
                return u.annee === 5;
            } else {
                return true;
            }
        });

        filtered.forEach(university => {
            const marker = L.marker([university.latitude, university.longitude])
                .bindPopup(popupText(university));

            marker.on('popupopen', () => {
                void window.hydratePopupContent(university);
            });

            markers.addLayer(marker);
        });
        map.addLayer(markers);
    }

    window.updateMap = updateMap; // Pour pouvoir appeler depuis le PHP
    renderWishesList();
    updateMap();
</script>
<?php $t->endSlot(); ?>