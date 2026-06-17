function getState(uid) {
    return window.MobilityMapState?.popupState?.get(String(uid)) ?? null;
}

async function findPlaceByUniversity(university) {
    const placesService = new google.maps.places.PlacesService(document.createElement('div'));

    const findPlace = (query) => new Promise((resolve) => {
        placesService.findPlaceFromQuery(
            {
                query,
                fields: ['name', 'photos', 'formatted_address', 'place_id']
            },
            (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && results?.length) {
                    resolve({ places: results, status });
                    return;
                }
                resolve({ places: [], status });
            }
        );
    });

    const getDetails = (placeId) => new Promise((resolve) => {
        placesService.getDetails(
            {
                placeId,
                fields: ['name', 'photos', 'formatted_address', 'place_id']
            },
            (place, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && place) {
                    resolve({ place, status });
                    return;
                }
                resolve({ place: null, status });
            }
        );
    });

    const textSearch = (query, location) => new Promise((resolve) => {
        placesService.textSearch(
            {
                query,
                location,
                radius: 6000
            },
            (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK && results?.length) {
                    resolve({ places: results, status });
                    return;
                }
                resolve({ places: [], status });
            }
        );
    });

    const photoMap = new Map();
    const statuses = [];

    const addPhotosFromPlace = (place) => {
        const photos = place?.photos || [];
        photos.forEach((photo) => {
            const thumbUrl = photo.getUrl({ maxWidth: 420, maxHeight: 260 });
            if (!photoMap.has(thumbUrl)) {
                photoMap.set(thumbUrl, {
                    thumbUrl,
                    fullUrl: photo.getUrl({ maxWidth: 1600, maxHeight: 1200 })
                });
            }
        });
    };

    const queries = [
        `${university.name} ${university.country}`,
        `${university.name} ${university.address}`,
        `${university.name} university`
    ];

    for (const query of queries) {
        const found = await findPlace(query);
        statuses.push(`findPlace:${found.status}`);
        for (const candidate of found.places.slice(0, 4)) {
            let place = candidate;
            if (place.place_id && (!place.photos || place.photos.length === 0)) {
                const details = await getDetails(place.place_id);
                statuses.push(`getDetails:${details.status}`);
                if (details.place) {
                    place = details.place;
                }
            }
            addPhotosFromPlace(place);
            if (photoMap.size >= 12) {
                return { photos: Array.from(photoMap.values()).slice(0, 12), status: statuses.join(' | ') };
            }
        }
    }

    const baseLocation = {
        lat: parseFloat(university.latitude),
        lng: parseFloat(university.longitude)
    };

    for (const query of queries) {
        const found = await textSearch(query, baseLocation);
        statuses.push(`textSearch:${found.status}`);
        for (const candidate of found.places.slice(0, 6)) {
            let place = candidate;
            if (place.place_id && (!place.photos || place.photos.length === 0)) {
                const details = await getDetails(place.place_id);
                statuses.push(`getDetails:${details.status}`);
                if (details.place) {
                    place = details.place;
                }
            }
            addPhotosFromPlace(place);
            if (photoMap.size >= 12) {
                return { photos: Array.from(photoMap.values()).slice(0, 12), status: statuses.join(' | ') };
            }
        }
    }

    return {
        photos: Array.from(photoMap.values()).slice(0, 12),
        status: statuses.length ? statuses.join(' | ') : 'ZERO_RESULTS'
    };
}

async function findStreetViewPosition(university) {
    const streetViewService = new google.maps.StreetViewService();
    const geocoder = new google.maps.Geocoder();

    const tryByLocation = (location, radius) => new Promise((resolve) => {
        streetViewService.getPanorama({ location, radius }, (data, status) => {
            if (status === 'OK' && data?.location?.latLng) {
                resolve(data.location.latLng);
                return;
            }
            resolve(null);
        });
    });

    const geocodeAddress = (address) => new Promise((resolve) => {
        geocoder.geocode({ address }, (results, status) => {
            if (status === 'OK' && results?.length) {
                resolve(results[0].geometry.location);
                return;
            }
            resolve(null);
        });
    });

    const nameQueries = [
        `${university.name}, ${university.country}`,
        `${university.name}, ${university.address}, ${university.country}`,
        `${university.name} university ${university.country}`
    ];

    const radii = [400, 800, 1400, 2200];

    for (const query of nameQueries) {
        const geocodedLocation = await geocodeAddress(query);
        if (!geocodedLocation) {
            continue;
        }
        for (const radius of radii) {
            const position = await tryByLocation(geocodedLocation, radius);
            if (position) {
                return position;
            }
        }
    }

    const base = {
        lat: parseFloat(university.latitude),
        lng: parseFloat(university.longitude)
    };

    for (const radius of radii) {
        const position = await tryByLocation(base, radius);
        if (position) {
            return position;
        }
    }

    return null;
}

async function hydratePopupContent(university) {
    const uid = String(university.id_partner_university);
    const state = window.MobilityMapState?.popupState?.get(uid);

    if (!state) {
        return;
    }

    state.university = university;
    state.photoIndex = 0;
    state.streetViewPosition = null;
    state.streetViewInitialized = false;
    state.photos = [];

    try {
        const found = await findPlaceByUniversity(university);
        const photos = Array.isArray(found.photos) ? found.photos.slice(0, 10) : [];
        window.MobilityMapCarousel?.setPopupPhotos(uid, photos);

        if (!photos.length) {
            const status = document.getElementById(`photo-status-${uid}`);
            if (status) {
                status.innerText = `Aucune photo trouvee (status API: ${found.status || 'UNKNOWN'}).`;
            }
        }
    } catch (error) {
        console.error('Erreur chargement photos:', error);
        const status = document.getElementById(`photo-status-${uid}`);
        if (status) {
            status.innerText = 'Impossible de charger les photos';
        }
    }

    state.streetViewPosition = await findStreetViewPosition(university);
    const streetStatus = document.getElementById(`street-status-${uid}`);
    const streetOpenBtn = document.getElementById(`street-open-${uid}`);

    if (streetStatus) {
        streetStatus.innerText = state.streetViewPosition
            ? 'Street View pret. Ouvrez l onglet StreetView.'
            : 'Street View indisponible a proximite';
    }
    if (streetOpenBtn) {
        streetOpenBtn.disabled = !state.streetViewPosition;
    }
}

function switchPopupTab(uid, tab) {
    const photosPanel = document.getElementById(`panel-photos-${uid}`);
    const streetPanel = document.getElementById(`panel-street-${uid}`);
    const photosTab = document.getElementById(`tab-photos-${uid}`);
    const streetTab = document.getElementById(`tab-street-${uid}`);

    if (!photosPanel || !streetPanel || !photosTab || !streetTab) {
        return;
    }

    const showPhotos = tab === 'photos';
    photosPanel.classList.toggle('hidden', !showPhotos);
    streetPanel.classList.toggle('hidden', showPhotos);
    photosTab.classList.toggle('active', showPhotos);
    streetTab.classList.toggle('active', !showPhotos);

    if (!showPhotos) {
        const state = getState(uid);
        const streetContainer = document.getElementById(`streetview-${uid}`);
        const streetStatus = document.getElementById(`street-status-${uid}`);
        console.log(uid, state, streetContainer, streetStatus);
        if (!state || !streetContainer || !streetStatus) {
            return;
        }

        if (!state.streetViewPosition) {
            streetStatus.innerText = 'Street View indisponible a proximite';
            return;
        }

        if (!state.streetViewInitialized) {
            new google.maps.StreetViewPanorama(streetContainer, {
                position: state.streetViewPosition,
                pov: { heading: 0, pitch: 0 },
                zoom: 1,
                addressControl: true,
                zoomControl: true,
                linksControl: true,
                fullscreenControl: false
            });
            state.streetViewInitialized = true;
            streetStatus.innerText = '';
        }
    }
}

function openStreetViewModal(uid) {
    const state = getState(uid);
    if (!state || !state.streetViewPosition) {
        return;
    }

    const modal = document.getElementById('streetViewModal');
    const title = document.getElementById('streetViewTitle');
    const container = document.getElementById('streetViewPanoramaModal');

    title.innerText = `${state.university.name} - Street View`;
    container.innerHTML = '';
    modal.classList.add('active');

    new google.maps.StreetViewPanorama(container, {
        position: state.streetViewPosition,
        pov: { heading: 0, pitch: 0 },
        zoom: 1,
        addressControl: true,
        zoomControl: true,
        linksControl: true,
        fullscreenControl: true
    });
}

function closeStreetViewModal() {
    const modal = document.getElementById('streetViewModal');
    modal.classList.remove('active');
}


document.getElementById('streetViewModal').addEventListener('click', (event) => {
    if (event.target.id === 'streetViewModal') {
        closeStreetViewModal();
    }
});

window.MobilityMapStreetView = {
    findPlaceByUniversity,
    findStreetViewPosition,
    hydratePopupContent,
    switchPopupTab,
    openStreetViewModal,
    closeStreetViewModal,
};

window.findPlaceByUniversity = findPlaceByUniversity;
window.findStreetViewPosition = findStreetViewPosition;
window.hydratePopupContent = hydratePopupContent;
window.switchPopupTab = switchPopupTab;
window.openStreetViewModal = openStreetViewModal;
window.closeStreetViewModal = closeStreetViewModal;