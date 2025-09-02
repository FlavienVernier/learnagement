import { FormControlLabel, Checkbox, Box, Typography } from "@mui/material";

export default function EnglishLanguageFilter({ onlyEnglish, setOnlyEnglish }) {
  const style = {
    padding: "8px",
    marginBottom: "4px",
    background: "#ffffff",
    borderRadius: "4px",
    cursor: "grab",
    justifyContent: "space-between",
  };
  return (
    <Box style={style}>
      <Typography sx={{ color: '#009bda' }} variant="subtitle1">Langue des cours</Typography>
      <FormControlLabel  sx={{ color: '#009bda' }}
        control={
          <Checkbox
            checked={onlyEnglish}
            onChange={(e) => setOnlyEnglish(e.target.checked)}
            sx={{ color: '#009bda' }}
          />
        }
        label="Afficher uniquement les universités proposant des cours en anglais"
      />
    </Box>
  );
}
