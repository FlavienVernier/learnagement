function getState(uid) {
    return window.MobilityMapState?.popupState?.get(String(uid)) ?? null;
}

function setPhotoSlide(uid, photoIndex) {
    const state = getState(uid);
    const image = document.getElementById(`photo-image-${uid}`);
    const caption = document.getElementById(`photo-caption-${uid}`);
    const status = document.getElementById(`photo-status-${uid}`);
    const prevBtn = document.getElementById(`photo-prev-${uid}`);
    const nextBtn = document.getElementById(`photo-next-${uid}`);

    if (!state || !image || !caption || !status || !prevBtn || !nextBtn) {
        return;
    }

    if (!state.photos || state.photos.length === 0) {
        image.style.display = 'none';
        caption.innerText = '';
        status.innerText = 'Aucune photo trouvee pour cette universite';
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        return;
    }

    const safeIndex = Math.max(0, Math.min(photoIndex, state.photos.length - 1));
    state.photoIndex = safeIndex;

    const photo = state.photos[safeIndex];
    image.style.display = 'block';
    image.src = photo.thumbUrl;
    image.onclick = () => window.open(photo.fullUrl, '_blank');
    caption.innerText = `Photo ${safeIndex + 1}/${state.photos.length}`;
    status.innerText = '';
    prevBtn.disabled = safeIndex === 0;
    nextBtn.disabled = safeIndex === state.photos.length - 1;
}

function setPopupPhotos(uid, photos) {
    const state = getState(uid);
    if (!state) {
        return;
    }

    state.photos = Array.isArray(photos) ? photos : [];
    setPhotoSlide(uid, 0);
}

function prevPopupPhoto(uid) {
    const state = getState(uid);
    if (!state || !state.photos || state.photos.length === 0) {
        return;
    }
    setPhotoSlide(uid, state.photoIndex - 1);
}

function nextPopupPhoto(uid) {
    const state = getState(uid);
    if (!state || !state.photos || state.photos.length === 0) {
        return;
    }
    setPhotoSlide(uid, state.photoIndex + 1);
}

window.MobilityMapCarousel = {
    setPhotoSlide,
    setPopupPhotos,
    prevPopupPhoto,
    nextPopupPhoto,
};

window.setPhotoSlide = setPhotoSlide;
window.prevPopupPhoto = prevPopupPhoto;
window.nextPopupPhoto = nextPopupPhoto;