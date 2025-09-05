import { Autocomplete, TextField } from '@mui/material';
import Box from '@mui/material/Box';

export default function CountryFilter({ countries, selected, onChange }) {
  return (
    <Box 
      sx={{
          padding:'10px',
          backgroundColor:'#ffffff',
          color: '#000000',
          borderRadius: "4px"
        }}
    >
      <Autocomplete
        multiple
        options={countries}
        value={selected}
        onChange={(e, newValue) => onChange(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Filtrer par pays" placeholder="Choisissez des pays" />
        )}
      />
    </Box>
  );
}
