import MapView from "./MapView";

export default function MapPage({ universities, onAddUniv, popupFields, selectedSemester, selectedSpecialty }) {
  return (
    <div>
      <MapView 
        universities={universities} 
        onAddUniv={onAddUniv} 
        popupFields={popupFields} 
        selectedSemester={selectedSemester}   
        selectedSpecialty={selectedSpecialty} 
      />
    </div>
  );
}
