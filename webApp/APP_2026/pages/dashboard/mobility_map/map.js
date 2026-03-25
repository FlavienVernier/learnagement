const map = L.map('map').setView([48.85, 2.35], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const markers = L.markerClusterGroup();

let universities = [];

const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university";
console.log(url)
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

function popupText(university) {
    return `
        <b>${university.name}</b> (${university.code})<br/>
        <em class="text-[0.75rem]">${university.address}, ${university.country}</em><br/>
        Langue${university.languages.includes(',') ? 's' : ''}: ${university.languages}<br/>
        ${university.note_min !== null ? `Note min : ${university.note_min}<br/>` : ''}
        <a href="${university.website}" target="_blank">${university.website}</a><br/>
    `;
}

window.updateMap = updateMap;

function updateMap() {
    markers.clearLayers();
    
    const selectedFiliere = document.getElementById('filiereSelect').value;
    const selectedSemestre = document.getElementById('semestreSelect').value;
    const selectedNote = parseFloat(document.getElementById('noteMinRange').value);

    const filtered = universities.filter(u => {
        // Affiche univ si note_min <= selectedNote
        const uNote = u.note_min === null ? 0 : parseFloat(u.note_min);
        if (uNote > selectedNote) return false;
        
        let key = "";
        if (selectedFiliere) {
            key = selectedSemestre + "_" + selectedFiliere;
        } else {
            key = selectedSemestre + "_total_places";
        }

        return parseInt(u[key]) > 0;
    });

    filtered.forEach(university => {
        const marker = L.marker([university.latitude, university.longitude])
            .bindPopup(popupText(university));
        markers.addLayer(marker);
    });
    map.addLayer(markers);
}

updateMap();