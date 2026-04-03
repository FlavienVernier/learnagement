const map = L.map('map').setView([48.85, 2.35], 4);

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

const universities = await fetchUniversities();

function popupText(university) {
    return `
        <b>${university.name}</b> (${university.code})<br/>
        <em class="text-[0.75rem]">${university.address}, ${university.country}</em><br/>
        Langue${university.languages.includes(',') ? 's' : ''}: ${university.languages}<br/>
        ${university.note_min !== null ? `Note min : ${university.note_min}<br/>` : ''}
        <a href="${university.website}" target="_blank">${university.website}</a><br/>
        <button
            type="button"
            onclick='window.addUniversityToWishes(${JSON.stringify(university)})'
            class="mt-2 inline-flex items-center rounded bg-primary px-3 py-1.5 text-sm font-semibold text-white hover:opacity-90"
        >
            Ajouter aux voeux
        </button>
    `;
}

async function addUniversityToWishes(university) {
    console.warn('Endpoint des voeux non défini.');
    return;

    try {
        const response = await fetch(wishesEndpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_etudiant: window.ENV.USER_ID,
                id_partner_university: university.id_partner_university,
            })
        });

        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        console.log('Université ajoutée aux voeux :', university);
    } catch (error) {
        console.error('Impossible d\'ajouter l\'université aux voeux :', error.message);
    }
}

window.addUniversityToWishes = addUniversityToWishes;

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
        markers.addLayer(marker);
    });
    map.addLayer(markers);
}

window.updateMap = updateMap; // Pour pouvoir appeler depuis le PHP
updateMap();