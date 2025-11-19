import { FormControl, FormLabel, Select, MenuItem } from '@mui/material';

const specialties = ["MM", "MC", "SNI", "BAT", "EIT", "IDU"];

export default function SpecialtyFilter({ selectedSpecialty, setSelectedSpecialty }) {
  const style = {
    padding: "8px",
    marginBottom: "4px",
    background: "#ffffff",
    borderRadius: "4px",
    cursor: "grab",
    justifyContent: "space-between",
  };
  return (
    <FormControl style={style} sx={{ color: '#009bda', marginTop: 2 }}>
      <FormLabel sx={{ color: '#009bda' }}>Spécialité</FormLabel>
      <Select
        value={selectedSpecialty}
        onChange={(e) => setSelectedSpecialty(e.target.value)}
        displayEmpty
        sx={{ color: '#009bda' }}
      >
        <MenuItem value="">
          <em>Toutes</em>
        </MenuItem>
        {specialties.map((spec) => (
          <MenuItem key={spec} value={spec}>
            {spec}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
