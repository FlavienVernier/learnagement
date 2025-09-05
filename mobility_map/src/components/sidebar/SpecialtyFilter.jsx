import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

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
    <FormControl style={style} component="fieldset" sx={{ color: '#009bda', marginTop: 2 }}>
      <FormLabel sx={{ color: '#009bda' }}>Spécialité</FormLabel>
      <RadioGroup
        row
        value={selectedSpecialty}
        onChange={(e) => setSelectedSpecialty(e.target.value)}
      >
        {specialties.map((spec) => (
          <FormControlLabel
            key={spec}
            value={spec}
            control={<Radio sx={{ color: '#009bda' }} />}
            label={spec}
          />
        ))}
        <FormControlLabel
          value=""
          control={<Radio sx={{ color: '#009bda' }} />}
          label="Toutes"
        />
      </RadioGroup>
    </FormControl>
  );
}
