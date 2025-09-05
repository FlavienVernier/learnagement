import { Box, Typography, Slider } from "@mui/material";

export default function NoteMinFilter({ maxNote, setMaxNote }) {
  return (
    <Box sx={{ color: 'white', mt: 2 }}>
      <Typography variant="subtitle1">Note minimale acceptée</Typography>
      <Slider
        value={maxNote}
        min={0}
        max={20}
        step={0.5}
        onChange={(e, value) => setMaxNote(value)}
        valueLabelDisplay="auto"
        sx={{ color: 'white' }}
      />
      <Typography variant="body2">
        Affiche les universités avec une note minimale ≤ {maxNote}
      </Typography>
    </Box>
  );
}
