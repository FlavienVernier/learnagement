import { useEffect, useState } from 'react';
import Sidebar from './components/sidebar/Sidebar';
import MapPage from './components/MapPage/MapPage';
import ComparisonPage from './components/ComparisonPage/ComparisonPage';
import WishPage from './components/WishPage/WishPage';
import * as XLSX from 'xlsx';
import Button from '@mui/material/Button';

function App() {
  const [activePage, setActivePage] = useState("map");

  const [universities, setUniversities] = useState([]);
  const [selectedCountries, setSelectedCountries] = useState([]);
  const [selectedUnivs, setSelectedUnivs] = useState([]);

  const [sidebarVisible, setSidebarVisible] = useState(true);
  
  const [selectedSemester, setSelectedSemester] = useState("S8");
  const [selectedSpecialty, setSelectedSpecialty] = useState("IDU");
  const [maxNote, setMaxNote] = useState(20);
  const [onlyEnglish, setOnlyEnglish] = useState(false);
  const [popupFields, setPopupFields] = useState([]);

  const [wishlist, setWishlist] = useState([]);
  const [s8Univs, setS8Univs] = useState([]);
  const [s9Univs, setS9Univs] = useState([]);

  useEffect(() => {
    setSelectedUnivs([]); // Réinitialise la sélection à chaque changement de semestre
  }, [selectedSemester]);

  useEffect(() => {
    const saved = sessionStorage.getItem("uploadedFile");
    if (saved) {
      const buffer = new Uint8Array(JSON.parse(saved));
      const workbook = XLSX.read(buffer, { type: 'array' });
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

      // Même logique de parsing/géocodage ici
      (async () => {
        const geocodedData = await Promise.all(jsonData.map(async (u) => {
          const hasLat = u.latitude && !isNaN(parseFloat(u.latitude));
          const hasLng = u.longitude && !isNaN(parseFloat(u.longitude));

          if (hasLat && hasLng) {
            return {
              ...u,
              latitude: parseFloat(u.latitude),
              longitude: parseFloat(u.longitude),
            };
          }

          const address = u.adresse?.trim();
          if (!address) return null;

          try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`, {
              headers: {
                'User-Agent': 'mobility-app/1.0 (contact@example.com)',
              }
            });
            const results = await response.json();
            if (results[0]) {
              return {
                ...u,
                latitude: parseFloat(results[0].lat),
                longitude: parseFloat(results[0].lon),
              };
            }
          } catch (error) {
            console.error(`Erreur de géocodage pour ${address}:`, error);
          }

          return null;
        }));

        const validData = geocodedData.filter(u => u && !isNaN(u.latitude) && !isNaN(u.longitude));
        setUniversities(validData);
      })();
    }
  }, []);

  const handleFileUpload = async (file) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        sessionStorage.setItem("uploadedFile", JSON.stringify(Array.from(new Uint8Array(e.target.result))));
        const workbook = XLSX.read(data, {type: 'array'});
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, {defval: ""});

        const geocodeCache = JSON.parse(localStorage.getItem("geocodeCache") || "{}");

        const geocodedData = await Promise.all(jsonData.map(async (u) => {
          const hasLat = u.latitude && !isNaN(parseFloat(u.latitude));
          const hasLng = u.longitude && !isNaN(parseFloat(u.longitude));

          console.log("lat, long: ", hasLat, hasLng);

          if (hasLat && hasLng) {
            return {
              ...u,
              latitude: parseFloat(u.latitude),
              longitude: parseFloat(u.longitude),
            };
          }

          const address = u.adresse?.trim();
          //console.log("address: ", address);
          if (!address) return null;

          if (geocodeCache[address]) {
            return {
              ...u,
              latitude: geocodeCache[address].lat,
              longitude: geocodeCache[address].lon,
            };
          }

          try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`, {
              headers: {
                'User-Agent': 'mobility-app/1.0 (contact@example.com)',
              }
            });

            const results = await response.json();
            if (results[0]) {
              const lat = parseFloat(results[0].lat);
              const lon = parseFloat(results[0].lon);
              geocodeCache[address] = { lat, lon };
              return {
                ...u,
                latitude: lat,
                longitude: lon,
              };
            }
          } catch (err) {
            console.error(`Erreur géocodage: ${address}`, err);
          }

          return null;
        }));

        // Sauvegarde du cache
        localStorage.setItem("geocodeCache", JSON.stringify(geocodeCache));

        const validData = geocodedData.filter(u => u && !isNaN(u.latitude) && !isNaN(u.longitude));
        setUniversities(validData);
      }catch (e) {
        console.error(e);
      }
    };

    reader.readAsArrayBuffer(file);
    
  };



  const countries = [...new Set(universities.map(u => u.pays).filter(Boolean))];
  const filtered = universities.filter(u => {
    const countryMatch = selectedCountries.length === 0 || selectedCountries.includes(u.pays);
    const semesterKey = `${selectedSemester}_total_places`;
    const specialtyKey = selectedSemester && selectedSpecialty ? `${selectedSemester}_${selectedSpecialty}` : null;
    const hasSemesterPlaces = u[semesterKey] > 0;
    const hasSpecialtyPlaces = specialtyKey ? u[specialtyKey] > 0 : true; 
    const noteOk = !u.note_min || parseFloat(u.note_min) <= maxNote; 
    const englishOk = !onlyEnglish || (
    !u.langue_des_cours ||  // garder les cases vides
    u.langue_des_cours.toLowerCase().includes("anglais")
    );

    return countryMatch && hasSemesterPlaces && hasSpecialtyPlaces && noteOk && englishOk;
  });

  const addUniv = (univ) => {
    if (selectedUnivs.some(u => u.nom_partenaire === univ.university) || selectedUnivs.length >= 5) return;
    setSelectedUnivs([...selectedUnivs, univ]);
  };

  const reorderUnivs = (reordered) => setSelectedUnivs(reordered);
  const geocodeAddress = async (address) => {
    const encoded = encodeURIComponent(address);
    const url = `https://nominatim.openstreetmap.org/search?q=${encoded}&format=json&limit=1`;
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'university-map-app', // requis par Nominatim
      }
    });
    const data = await res.json();
    if (data.length === 0) return null;
    return {
      latitude: parseFloat(data[0].lat),
      longitude: parseFloat(data[0].lon),
    };
  };

  return (
    <div className="relative flex min-h-screen bg-[#ffffff]">
      <Button
        onClick={() => setSidebarVisible(!sidebarVisible)}
        sx={{
          marginLeft: '100px',
          position: 'absolute',
          backgroundColor: '#009bda',
          color:  '#ffffff',
          textTransform: 'none',
          '&:hover': {
            backgroundColor: '#007bb5',
          },
        }}
        className="absolute top-4 left-4 z-50 bg-white text-black px-3 py-1 rounded shadow"
      >
        {sidebarVisible ? '⏴ Cacher' : '⏵ Afficher'}
      </Button>

      {sidebarVisible && (
        <Sidebar
          activePage={activePage}
          onSelectPage={setActivePage}
          countries={countries}
          selectedCountries={selectedCountries}
          setSelectedCountries={setSelectedCountries}
          selectedUnivs={selectedUnivs}
          setSelectedUnivs={setSelectedUnivs}
          reorderUnivs={reorderUnivs}
          onFileUpload={handleFileUpload}
          selectedSemester={selectedSemester}
          setSelectedSemester={setSelectedSemester}
          selectedSpecialty={selectedSpecialty}
          setSelectedSpecialty={setSelectedSpecialty}
          maxNote={maxNote} 
          setMaxNote={setMaxNote}
          onlyEnglish={onlyEnglish}
          setOnlyEnglish={setOnlyEnglish}
          popupFields={popupFields}
          setPopupFields={setPopupFields}
        />
      )}

      <main className="flex-1 p-6">
        {activePage === "map" && 
          <MapPage
          universities={filtered}
          onAddUniv={addUniv}
          popupFields={popupFields}
          selectedSemester={selectedSemester}
          selectedSpecialty={selectedSpecialty}
          sidebarVisible={sidebarVisible}
        />}
        {activePage === "comparison" && <ComparisonPage selectedUnivs={selectedUnivs} />}
        {activePage === "wish" && 
          <WishPage 
            sidebarUnivs={selectedUnivs} 
            selectedSemester={selectedSemester} 
            s8Univs={s8Univs}
            setS8Univs={setS8Univs}
            s9Univs={s9Univs}
            setS9Univs={setS9Univs}
          />
        }
      </main>
    </div>
  );
}

export default App;