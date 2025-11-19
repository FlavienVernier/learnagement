import React, { useEffect } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import L from 'leaflet';
import 'leaflet.markercluster';

function ClusterMarkers({ universities, onAddUniv, popupFields, selectedSemester, selectedSpecialty }) {
  const map = useMap();

  const popupFieldLabels = {
    nom_partenaire: "Nom du partenaire",
    pays: "Pays",
    adresse: "Adresse",
    site_web: "Site web",
    langue_des_cours: "Langue des cours",
    note_min: "Note minimale",
    criteres_academiques: "Critères Academiques",
    integration_et_vie_sociale: "Intégration et Vie Sociale",
    logement_et_vie_quotidienne: "Logement et Vie Quotidienne",
    organisation_et_demarches: "Organisation et Démarches",
    experience_globale: "Expérience Globale",
    commentaire: "Commentaire"
    // Ajoute d'autres labels ici si nécessaire
  };


  useEffect(() => {
    if (!map || !universities || universities.length === 0) return;

    const markerGroup = L.markerClusterGroup();

    universities.forEach((u) => {
      if (!u.latitude || !u.longitude) return;

      const lines = popupFields.map(field => {
        const value = u[field] ?? '-';
        return `<div><strong>${field.replace(/_/g, ' ')}:</strong> ${value}</div>`;
      });

      const fieldKey = `${selectedSemester}_${selectedSpecialty}`; // ex: "S8_IDU"
      const places = u[fieldKey] ?? 'Veuillez préciser la spécialité';
      const siteWebLink = u.site_web
        ? `<a href="${u.site_web}" target="_blank" rel="noopener noreferrer">${u.site_web}</a>`
        : '-';
        
      const popupContent = `
        <div>
          <div>${u.nom_partenaire || "-"}</div>
          <div><strong>Places (${fieldKey}):</strong> ${places}</div>
          ${popupFields.map(field => {
            const label = popupFieldLabels[field] || field;
            return `<div><strong>${label}:</strong> ${u[field] ?? '-'}</div>`;
          }).join('')}
          <div>Site Web: ${siteWebLink}</div>
          <button class="add-univ-btn">Ajouter</button>
        </div>
      `;
      const marker = L.marker([u.latitude, u.longitude], { university: u });
      marker.bindPopup(popupContent);
      markerGroup.addLayer(marker);
    });

    markerGroup.on('popupopen', (e) => {
      const marker = e.popup._source;
      const univ = marker.options.university;
      const btn = e.popup._contentNode.querySelector('.add-univ-btn');
      if (btn && univ) {
        btn.addEventListener('click', () => onAddUniv(univ));
      }
    });

    map.addLayer(markerGroup);

    return () => {
      map.removeLayer(markerGroup);
    };
  }, [map, universities, onAddUniv, popupFields]);

  return null;
}


export default function MapView({ universities, onAddUniv, popupFields, selectedSemester, selectedSpecialty, sidebarVisible }) {
  return (
    <div className={`h-[100vh] ${sidebarVisible ? 'w-[78vw]' : 'w-[100vw]'} fixed`}>
      <MapContainer center={[48.85, 2.35]} zoom={4} scrollWheelZoom className="h-full w-full">
        <TileLayer
          attribution="&copy; OpenStreetMap"
          url="https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}.png"
        />
        <ClusterMarkers
          universities={universities}
          onAddUniv={onAddUniv}
          popupFields={popupFields}
          selectedSemester={selectedSemester}
          selectedSpecialty={selectedSpecialty}
        />
      </MapContainer>
    </div>
  );
}