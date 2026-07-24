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

    <!-- Quota Display (Bottom Left) -->
    <div id="studentQuotaContainer" class="hidden absolute bottom-6 left-4 z-[1000] bg-white/95 border border-indigo-100 rounded-lg shadow-lg p-4 backdrop-blur-sm pointer-events-none">
        <p class="text-[10px] uppercase font-bold text-indigo-700 tracking-wide mb-1">Quota - <span id="quotaFiliereName">...</span></p>
        <div class="flex gap-4">
            <div class="flex items-center gap-1">
                <span class="text-xs font-semibold text-indigo-600">S8:</span>
                <span class="text-sm font-bold text-indigo-900" id="quotaS8Count">-</span>
            </div>
            <div class="flex items-center gap-1">
                <span class="text-xs font-semibold text-indigo-600">S9:</span>
                <span class="text-sm font-bold text-indigo-900" id="quotaS9Count">-</span>
            </div>
        </div>
    </div>

    <!-- Contrôles et panneaux superposés -->
    <div class="absolute top-[10px] left-[55px] z-[1000] flex max-w-[92vw] flex-col items-start gap-2.5">
        <div id="mapControls" class="flex items-center gap-2">
            <button onclick="document.getElementById('filterForm').classList.toggle('hidden')"
                class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                Filtres
            </button>
            <button id="wishesBtn" onclick="document.getElementById('wishesPanel').classList.toggle('hidden')"
                class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                Voeux
            </button>
            <div id="campaignOpenBadge" class="hidden bg-blue-50 text-blue-800 font-semibold py-2 px-4 border border-blue-200 rounded shadow text-sm flex items-center gap-2 pointer-events-none">
                <span class="text-blue-500">ℹ️</span> Campagne en cours
            </div>
            <div id="wishesSubmittedBadge" class="hidden bg-green-50 text-green-800 font-semibold py-2 px-4 border border-green-200 rounded shadow text-sm flex items-center gap-2 pointer-events-none">
                <span class="text-green-500">✅</span> Vœux soumis
            </div>
        </div>

        <form id="filterForm" onsubmit="return false;" class="hidden bg-white p-4 rounded-lg shadow-lg border border-gray-200">
            <div class="flex flex-wrap justify-center items-center gap-4">
                <div class="flex flex-col">
                    <label for="semestreSelect" class="text-xs font-semibold text-gray-600 mb-1">Semestre</label>
                    <select name="semestre" id="semestreSelect" onchange="updateMap()" class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary min-w-24">
                    <option>Tous</option>
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

        <aside id="wishesPanel" class="hidden w-[min(92vw,22rem)] max-h-[80vh] overflow-y-auto bg-white/95 p-4 rounded-lg shadow-lg border border-gray-200 backdrop-blur-sm">
            <div class="mb-3 flex items-center justify-between">
                <h2 class="text-sm font-semibold text-gray-800">Mes voeux</h2>
                <span id="wishesCount" class="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-semibold text-primary">0/5</span>
            </div>
            <div id="campaignClosedNotice" class="hidden mb-3 bg-amber-50 border border-amber-200 rounded-lg p-3">
                <p class="text-xs font-bold text-amber-800">Inscriptions non disponibles.</p>
                <p class="text-xs text-amber-700 mt-0.5">La campagne n'est pas encore lancée. Revenez après l'annonce
                    officielle pour soumettre vos vœux.</p>
            </div>
            <p id="wishesEmpty" class="text-sm text-gray-500">Aucun voeu pour le moment.</p>
            <ul id="wishesList" class="space-y-2"></ul>
        </aside>
    </div>
    <!-- Bannière campagne non ouverte -->
    <div id="campaignClosedBanner" class="hidden absolute top-3 left-1/2 -translate-x-1/2 z-[1100] w-max max-w-[90vw] pointer-events-none">
        <div class="bg-white border border-amber-300 rounded-xl shadow-lg px-5 py-3 flex items-center gap-3">
            <span class="text-amber-500 text-xl">⏳</span>
            <div>
                <p class="text-sm font-bold text-gray-800">La procédure de mobilité n'a pas encore commencé.</p>
                <p class="text-xs text-gray-500 mt-0.5">Vous pouvez explorer les universités. L'inscription aux vœux sera disponible après le lancement officiel de la campagne.</p>
            </div>
        </div>
    </div>
</section>
<?php $t->endSlot(); ?>


<?php $t->startSlot('stylesheet'); ?>
<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
<link rel="stylesheet" href="/theme/mobility-map.css" />
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
<script src="/theme/mobility-map-carousel.js"></script>
<script src="/theme/mobility-map-streetview.js"></script>

<!-- ToDo : Déplacer dans un fichier global ex db.js -->
<script>
    window.ENV = {
        BACKEND_URL: "<?= getenv('INSTANCE_PROTOCOL') . '://' . getenv('INSTANCE_URL') ?>",
        BACKEND_PORT: "<?= getenv('BACKEND_PYTHON_PORT') ?>",
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

    // Vérifier le statut de la campagne avant tout
    const campaignStatusUrl = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/etudiant/" + window.ENV.USER_ID + "/campaign-status";
    let campaignOpen = false;
    try {
        const statusRes = await fetch(campaignStatusUrl, {
            headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
        });
        if (statusRes.ok) {
            const statusData = await statusRes.json();
            campaignOpen = statusData.is_open === true;
        }
    } catch (e) {
        console.error("Impossible de récupérer le statut de la campagne", e);
    }
    window.MobilityMapState.campaignOpen = campaignOpen;

    // Afficher la bannière et le message dans le panel vœux si campagne fermée
    if (campaignOpen) {
        const badge = document.getElementById('campaignOpenBadge');
        if (badge) badge.classList.remove('hidden');
    } else {
        const banner = document.getElementById('campaignClosedBanner');
        const notice = document.getElementById('campaignClosedNotice');
        const wishesEmpty = document.getElementById('wishesEmpty');
        const wishesList = document.getElementById('wishesList');
        const wishesCount = document.getElementById('wishesCount');
        const wishesBtn = document.getElementById('wishesBtn');
        const wishesPanel = document.getElementById('wishesPanel');
        
        if (banner) banner.classList.remove('hidden');
        if (notice) notice.classList.remove('hidden');
        if (wishesEmpty) wishesEmpty.classList.add('hidden');
        if (wishesList) wishesList.classList.add('hidden');
        if (wishesCount) wishesCount.classList.add('hidden');
        if (wishesBtn) wishesBtn.classList.add('hidden');
        if (wishesPanel) wishesPanel.classList.add('hidden');
    }

    const universities = await fetchUniversities();
    const universitiesById = new Map(
        universities.map((u) => [String(u.id_partner_university), u])
    );
    window.MobilityMapState.universitiesById = universitiesById;

    const fetchAssignment = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/etudiant/" + window.ENV.USER_ID + "/assignment";
        try {
            const response = await fetch(url, {
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error(error.message);
        }
        return null;
    }
    
    let assignment = await fetchAssignment();
    window.MobilityMapState.assignment = assignment;

    async function refreshWishesFromServer() {
        const wishes = await fetchWishes();
        wishedUniversities.clear();
        wishes.forEach((wish) => {
            wishedUniversities.set(`${wish.id_partner_university}-${wish.id_semestre}`, wish);
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
            if (window.MobilityMapState.campaignOpen !== false) {
                wishesEmpty.classList.remove('hidden');
            }
            return;
        }

        wishesEmpty.classList.add('hidden');
        
        // OLD CODE (Buggy: ne gère pas bien undefined ou les chaînes "null"):
        // const isSubmitted = wishes.some(w => w.submission_date !== null);
        const isSubmitted = wishes.some(w => Boolean(w.submission_date) && w.submission_date !== 'null' && w.submission_date !== 'None');

        const campaignOpenBadge = document.getElementById('campaignOpenBadge');
        const wishesSubmittedBadge = document.getElementById('wishesSubmittedBadge');

        if (window.MobilityMapState.campaignOpen !== false) {
            if (isSubmitted) {
                if (campaignOpenBadge) campaignOpenBadge.classList.add('hidden');
                if (wishesSubmittedBadge) wishesSubmittedBadge.classList.remove('hidden');
            } else {
                if (campaignOpenBadge) campaignOpenBadge.classList.remove('hidden');
                if (wishesSubmittedBadge) wishesSubmittedBadge.classList.add('hidden');
            }
        }

        wishesList.innerHTML = wishes
            .map((wish, index) => `
            <li class="rounded border border-gray-200 bg-gray-50 p-2">
                <div class="flex items-center gap-4 mb-1">
                    <span class="font-semibold text-lg text-gray-800">${index + 1}</span>
                    <div class="flex items-center justify-between gap-2 w-full">
                        <div class="cursor-pointer flex-1 hover:text-primary transition-colors" onclick="window.flyToUniversity('${wish.id_partner_university}')" title="Voir sur la carte">
                            <p class="text-sm text-gray-800"><strong class="font-semibold">[S${escapeHtml(wish.id_semestre)}] ${escapeHtml(wish.name)}</strong> (${escapeHtml(wish.code)})</p>
                            <p class="text-xs text-gray-600">${escapeHtml(wish.country)}</p>
                        </div>
                        <div class="flex items-center gap-1 ${isSubmitted ? 'hidden' : ''}">
                            <button
                                type="button"
                                onclick="window.moveWish(${wish.id_partner_university}, ${wish.id_semestre}, 'up')"
                                ${(index === 0) ? 'disabled' : ''}
                                class="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent transition"
                                title="Monter le voeu"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"></path></svg>
                            </button>
                            <button
                                type="button"
                                onclick="window.moveWish(${wish.id_partner_university}, ${wish.id_semestre}, 'down')"
                                ${(index === wishes.length - 1) ? 'disabled' : ''}
                                class="p-1 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-700 disabled:opacity-30 disabled:hover:bg-transparent transition"
                                title="Descendre le voeu"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path></svg>
                            </button>
                            <button
                                type="button"
                                onclick="window.deleteWish(${wish.id_partner_university}, ${wish.id_semestre})"
                                class="p-1 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition ml-1"
                                title="Supprimer le voeu"
                            >
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </li>
            `)
            .join('');

        wishesList.innerHTML += `
            <button
                type="button"
                onclick="window.submitWishes()"
                class="mt-3 w-full rounded bg-primary px-3 py-2 text-sm font-semibold text-white cursor-pointer disabled:cursor-not-allowed disabled:bg-gray-400"
                ${wishes.length < 1 || isSubmitted ? 'disabled' : ''}
            >
                ${isSubmitted ? 'Voeux soumis' : 'Soumettre mes voeux'}
            </button>
        `;
    }

    function getLanguageFlags(languagesString) {
        if (!languagesString) return '';
        const flags = {
            'Allemand': '🇩🇪',
            'Anglais': '🇬🇧',
            'Espagnol': '🇪🇸',
            'Français': '🇫🇷',
            'Portugais': '🇵🇹',
            'Italien': '🇮🇹',
            'Japonais': '🇯🇵'
        };
        
        return languagesString.split(',').map(l => {
            const lang = l.trim();
            return flags[lang] ? `<span title="${escapeHtml(lang)}" class="text-base cursor-help">${flags[lang]}</span>` : escapeHtml(lang);
        }).join(' ');
    }

    function popupText(university) {
        const id_semestre = university.annee === 4 ? 8 : 9;
        const alreadyInWishes = wishedUniversities.has(`${university.id_partner_university}-${id_semestre}`);
        const uid = String(university.id_partner_university);
        // OLD CODE (Buggy: ne gère pas bien undefined ou les chaînes "null"):
        // const isSubmitted = Array.from(wishedUniversities.values()).some(w => w.submission_date !== null);
        const isSubmitted = Array.from(wishedUniversities.values()).some(w => Boolean(w.submission_date) && w.submission_date !== 'null' && w.submission_date !== 'None');

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
            ${getLanguageFlags(university.languages)}<br/>
            S${university.annee == 4 ? '8' : '9'} : 
            ${escapeHtml(university.number_of_places)} place${university.number_of_places > 1 ? 's' : ''}<br/>
            ${university.note_min !== null ? `Note min : ${university.note_min}<br/>` : ''}
            <a href="${escapeHtml(university.website)}" target="_blank">${escapeHtml(university.website)}</a><br/>
            ${
                (assignment && String(assignment.id_partner_university) === uid) ? 
                    (assignment.status === 'pending' ? `
                        <div class="mt-3 flex gap-2">
                            <button onclick="window.submitDecision('declined')" class="flex-1 px-2 py-1.5 bg-red-100 hover:bg-red-200 text-red-700 text-xs font-semibold rounded border border-red-200 transition">Refuser</button>
                            <button onclick="window.submitDecision('accepted')" class="flex-1 px-2 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-semibold rounded shadow-sm transition">Accepter</button>
                        </div>
                    ` : assignment.status === 'accepted' ? `
                        <div class="mt-3 text-xs font-semibold p-2 rounded text-center bg-green-50 text-green-700 border border-green-200">Affectation acceptée</div>
                    ` : `
                        <div class="mt-3 text-xs font-semibold p-2 rounded text-center bg-red-50 text-red-700 border border-red-200">Affectation refusée</div>
                    `)
                : window.MobilityMapState.campaignOpen === false ? `
                    <div class="mt-2 inline-flex items-center gap-1.5 rounded bg-gray-100 border border-gray-200 px-3 py-1.5 text-xs font-semibold text-gray-500 cursor-not-allowed">
                        <span>⏳</span> Disponible après le lancement de la campagne
                    </div>
                ` : `
                    <button
                        type="button"
                        onclick="window.addUniversityToWishes('${uid}', ${university.annee === 4 ? 8 : 9})"
                        ${alreadyInWishes || wishedUniversities.size >= 5 || isSubmitted ? 'disabled' : ''}
                        class="mt-2 inline-flex items-center rounded bg-primary px-3 py-1.5 text-sm font-semibold text-white hover:opacity-90 cursor-pointer disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        ${alreadyInWishes ? 'Déjà dans les voeux' : isSubmitted ? 'Voeux déjà soumis' : wishedUniversities.size < 5 ? 'Ajouter aux voeux' : 'Maximum de voeux atteint'}
                    </button>
                `
            }
        `;
    }

    async function addUniversityToWishes(universityId, id_semestre) {
        const university = universitiesById.get(String(universityId));
        if (!university) {
            console.error('Universite introuvable pour id:', universityId);
            return;
        }

        if (wishedUniversities.has(`${university.id_partner_university}-${id_semestre}`)) {
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
                },
                body: JSON.stringify({ id_semestre: id_semestre })
            });

            if (!response.ok && response.status !== 409) {
                throw new Error(`Response status: ${response.status}`);
            }

            await refreshWishesFromServer();
            renderWishesList();
            updateMap();
            document.getElementById('wishesPanel').classList.remove('hidden');
        } catch (error) {
            console.error('Impossible d\'ajouter l\'université aux voeux :', error.message);
        }
    }

    async function deleteWish(idPartnerUniversity, idSemestre) {
        try {
            const deleteEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wish/" + idPartnerUniversity
                + "/semestre/" + idSemestre;

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

    async function moveWish(idPartnerUniversity, idSemestre, direction) {
        try {
            const moveEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wish/" + idPartnerUniversity
                + "/semestre/" + idSemestre
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

    async function submitWishes() {
        if (!confirm("Êtes-vous sûr de vouloir soumettre vos voeux ? Cette action est définitive et vous ne pourrez plus les modifier par la suite.")) {
            return;
        }

        try {
            const submitEndpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/wishes/submit";

            const response = await fetch(submitEndpoint, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            alert('Voeux soumis avec succès !');
            await refreshWishesFromServer();
            renderWishesList();
            updateMap();
        } catch (error) {
            console.error('Impossible de soumettre les voeux :', error.message);
            alert('Erreur lors de la soumission des voeux.');
        }
    }
    
    window.addUniversityToWishes = addUniversityToWishes;
    window.deleteWish = deleteWish;
    window.moveWish = moveWish;
    window.submitWishes = submitWishes;

    window.submitDecision = async function(decision) {
        if (!confirm(`Êtes-vous sûr de vouloir ${decision === 'accepted' ? 'accepter' : 'refuser'} cette affectation ? Cette décision est définitive.`)) {
            return;
        }
        
        try {
            const endpoint = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT)
                + "/university/etudiant/" + window.ENV.USER_ID
                + "/assignment/decision";

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ decision })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || "Erreur inconnue");
            }

            // Mettre à jour l'état local
            assignment.status = decision;
            
            // Re-rendre la carte et ré-ouvrir la popup pour afficher le nouveau statut
            updateMap();
            setTimeout(() => {
                window.flyToUniversity(assignment.id_partner_university);
            }, 100);
            
        } catch (error) {
            console.error('Erreur lors de la décision :', error.message);
            alert("Une erreur est survenue : " + error.message);
        }
    }

    window.flyToUniversity = function(uid) {
        const university = universitiesById.get(String(uid));
        if (!university) return;

        const marker = window.MobilityMapState.markerInstances && window.MobilityMapState.markerInstances.get(String(uid));
        if (marker) {
            markers.zoomToShowLayer(marker, () => {
                marker.openPopup();
            });
            document.getElementById('wishesPanel').classList.add('hidden');
        } else {
            // Le marqueur est filtré : on désactive les filtres pour l'afficher
            document.getElementById('semestreSelect').value = 'Tous';
            const range = document.getElementById('noteMinRange');
            range.value = 20;
            document.getElementById('noteMinValue').innerText = 20;
            updateMap();
            
            // On retente la navigation et l'ouverture lorsque la carte est à jour
            setTimeout(() => {
                window.flyToUniversity(uid);
            }, 100);
        }
    };

    function updateMap() {
        markers.clearLayers();
        window.MobilityMapState.markerInstances = new Map();
        
        // Si l'étudiant a une affectation, on ne montre que cette université
        if (assignment) {
            const u = universitiesById.get(String(assignment.id_partner_university));
            if (u) {
                const marker = L.marker([u.latitude, u.longitude]).bindPopup(popupText(u));
                marker.on('popupopen', () => void window.hydratePopupContent(u));
                window.MobilityMapState.markerInstances.set(String(u.id_partner_university), marker);
                markers.addLayer(marker);
            }
            map.addLayer(markers);
            return;
        }
        
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

            window.MobilityMapState.markerInstances.set(String(university.id_partner_university), marker);
            markers.addLayer(marker);
        });
        map.addLayer(markers);
    }

    const fetchStudentQuota = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/etudiant/" + window.ENV.USER_ID + "/quota?annee_scolaire=2025-2026";
        try {
            const response = await fetch(url, { headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` } });
            if (response.ok) {
                const data = await response.json();
                if (data) {
                    const container = document.getElementById('studentQuotaContainer');
                    if (container) container.classList.remove('hidden');
                    
                    const filiereNameEl = document.getElementById('quotaFiliereName');
                    if (filiereNameEl) filiereNameEl.innerText = data.filiere || 'Filière';
                    
                    const s8El = document.getElementById('quotaS8Count');
                    if (s8El) s8El.innerText = data.S8 ?? 0;
                    
                    const s9El = document.getElementById('quotaS9Count');
                    if (s9El) s9El.innerText = data.S9 ?? 0;
                }
            }
        } catch (e) {
            console.error("Erreur quota", e);
        }
    };

    window.updateMap = updateMap; // Pour pouvoir appeler depuis le PHP
    renderWishesList();
    if (campaignOpen && !assignment) {
        fetchStudentQuota();
    }
    updateMap();
    if (assignment) {
        // Cacher les contrôles inutiles si affecté
        const mapControls = document.getElementById('mapControls');
        if(mapControls) mapControls.classList.add('hidden');
        document.getElementById('filterForm').classList.add('hidden');
        document.getElementById('wishesPanel').classList.add('hidden');
        
        // Ouvrir automatiquement la popup de la destination affectée
        setTimeout(() => {
            window.flyToUniversity(assignment.id_partner_university);
        }, 500);
    }
</script>
<?php $t->endSlot(); ?>