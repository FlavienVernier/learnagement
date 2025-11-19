import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

export default function SemesterFilter({ selectedSemester, setSelectedSemester }) {
  const style = {
    padding: "8px",
    marginBottom: "4px",
    background: "#ffffff",
    borderRadius: "4px",
    cursor: "grab",
    justifyContent: "space-between",
  };
  return (
    <FormControl style={style} component="fieldset" sx={{ color: '#009bda' }} >
      <FormLabel sx={{ color: '#009bda' }}>Semestre</FormLabel>
      <RadioGroup
        row
        value={selectedSemester}
        onChange={(e) => setSelectedSemester(e.target.value)}
      >
        <FormControlLabel value="S8" control={<Radio sx={{ color: '#009bda' }} />} label="S8" />
        <FormControlLabel value="S9" control={<Radio sx={{ color: '#009bda' }} />} label="S9" />
      </RadioGroup>
    </FormControl>
  );
}
