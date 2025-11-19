import CartButton from "./CartButton";
import MapButton from "./MapButton";
import UnivSelection from "./UnivSelection";
import CountryFilter from "./CountryFilter";
import InputFileUpload from "./InputFileUpload";
import SemesterFilter from "./SemesterFilter";
import SpecialtyFilter from "./SpecialtyFilter";
import NoteMinFilter from "./NoteMinFilter";
import EnglishLanguageFilter from "./EnglishLanguageFilter";
import PopupFieldSelector from "./PopupFieldSelector";
import WishButton from "./WishButton";
import { useState } from "react";
import Button from '@mui/material/Button';
import { Typography, Box } from '@mui/material';
import { GlobeAltIcon } from '@heroicons/react/24/outline';

export default function Sidebar({
  activePage,
  onSelectPage,
  countries,
  selectedCountries,
  setSelectedCountries,
  selectedUnivs,
  setSelectedUnivs,
  reorderUnivs,
  onFileUpload,
  selectedSemester,
  setSelectedSemester,
  selectedSpecialty,
  setSelectedSpecialty,
  maxNote, 
  setMaxNote,
  onlyEnglish,
  setOnlyEnglish,
  popupFields,
  setPopupFields
}) {

  const handleSelect = (page) => {
    onSelectPage(page);
  };
  const handleResetFilters = () => {
    setSelectedCountries([]);
    setSelectedSemester("S8");
    setSelectedSpecialty("");
    setMaxNote(20);
    setOnlyEnglish(false);
  };
  const [filtersOpen, setFiltersOpen] = useState(true);
  const [popupFieldsSelectorOpen, setpopupFieldsSelectorOpen] = useState(true);
  
  return (
    <div className="bg-[#009bda] px-[2vh] max-w-[20vw] min-w-min pt-[32px]" style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
      <Box display="flex" alignItems="center" justifyContent="center" gap={1} m={2} style={{ width: '100%' }}>
        <GlobeAltIcon style={{ height: 30, width: 30, color: '#ffffff' }} />
        <Typography variant="h2" fontSize={25}
          sx={{ 
            fontFamily: 'Roboto, sans-serif', 
            color: '#ffffff' 
          }}
        >
          PARTIR UN JOUR
        </Typography>
      </Box>
      <MapButton
        onButtonClick={() => handleSelect("map")}
        active={activePage === "map"}
      />
      <CartButton
        onButtonClick={() => handleSelect("comparison")}
        active={activePage === "comparison"}
      />
      <WishButton
        onButtonClick={() => handleSelect("wish")}
        active={activePage === "wish"}
      />

      <InputFileUpload onFileUpload={onFileUpload} style={{ width: '100%' }} />
      <UnivSelection
        selectedUnivs={selectedUnivs}
        setSelectedUnivs={setSelectedUnivs}
        reorderUnivs={reorderUnivs}
      />
      <Button
        onClick={() => setFiltersOpen(prev => !prev)}
        sx={{
          boxShadow: 'none',
          backgroundColor:'#ffffff',
          color: '#009bda',
          textTransform: 'none',
          marginY: '2vh',
          width: '100%',
          '&:hover': {
            backgroundColor: '#8d8d8d',
            color: '#ffffff'
          },
        }}
      >
        {filtersOpen ? "Masquer les filtres" : "Afficher les filtres"}
      </Button>
      
      {filtersOpen && (
        <div className="space-y-2 mt-2">
          <SemesterFilter
            selectedSemester={selectedSemester}
            setSelectedSemester={setSelectedSemester}
          />
          <br />
          <SpecialtyFilter
            selectedSpecialty={selectedSpecialty}
            setSelectedSpecialty={setSelectedSpecialty}
          />
          <EnglishLanguageFilter onlyEnglish={onlyEnglish} setOnlyEnglish={setOnlyEnglish} />
          <NoteMinFilter maxNote={maxNote} setMaxNote={setMaxNote} />
          <CountryFilter
            countries={countries}
            selected={selectedCountries}
            onChange={setSelectedCountries}
          />
          <Button
            onClick={handleResetFilters}
            sx={{
              marginY: '2vh',
              boxShadow: 'none',
              backgroundColor:'#ffffff',
              color: '#009bda',
              textTransform: 'none',
              width: '100%',
              '&:hover': {
                backgroundColor: '#8d8d8d',
                color: '#ffffff'
              },
            }}
          >
            Réinitialiser les filtres
          </Button>
          <Button
          onClick={() => setpopupFieldsSelectorOpen(prev => !prev)}
          sx={{
            boxShadow: 'none',
            backgroundColor:'#ffffff',
            color: '#009bda',
            textTransform: 'none',
            marginY: '2vh',
            width: '100%',
            '&:hover': {
              backgroundColor: '#8d8d8d',
              color: '#ffffff'
            },
          }}
          >
            {popupFieldsSelectorOpen ? "Masquer les filtres des popups" : "Afficher les filtres des popups"}
          </Button>
          {popupFieldsSelectorOpen && (
            <PopupFieldSelector selectedFields={popupFields} onChange={setPopupFields} />
          )}
        </div>
      )}
    </div>
  );
}