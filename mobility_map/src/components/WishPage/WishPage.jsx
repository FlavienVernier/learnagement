import { useState } from "react";
import UnivSelection from "../sidebar/UnivSelection";
import { Typography, TextField, MenuItem, Select, FormControl, InputLabel, Button, Box } from '@mui/material';

const specialties = ["MM", "MC", "SNI", "BAT", "EIT", "IDU"];

export default function WishPage({ 
  sidebarUnivs, 
  selectedSemester, 
  s8Univs,
  setS8Univs,
  s9Univs,
  setS9Univs
}) {
  const [value, setValue] = useState("");
  const [error, setError] = useState(false);
  const [selectedSpecialty, setSelectedSpecialty] = useState("");

  const handleChange = (e) => {
    const newValue = e.target.value;
    // N'accepte que des chiffres
    if (/^\d*$/.test(newValue)) {
      setValue(newValue);
      setError(newValue.length > 0 && newValue.length !== 8);
    }
  };
  
  // Copier depuis la sidebar vers le sélecteur ciblé
  const copyFromSidebar = (semester) => {
    if (semester === "S8") {
      setS8Univs(sidebarUnivs);
    } else if (semester === "S9") {
      setS9Univs(sidebarUnivs);
    }
  };

  // Désactiver le bouton copier pour le semestre non sélectionné
  const isS8ButtonDisabled = selectedSemester !== "S8";
  const isS9ButtonDisabled = selectedSemester !== "S9";

  return (
    <Box>
      <Typography variant="h4" mb={2}>Wish List</Typography>

      <Box mb={4}>
        <Typography variant="h6">Semestre S8</Typography>
        <Button
          variant="contained"
          onClick={() => copyFromSidebar("S8")}
          disabled={isS8ButtonDisabled}
          sx={{ mb: 1 }}
        >
          Copier depuis la sidebar (S8)
        </Button>
        <UnivSelection
          selectedUnivs={s8Univs}
          setSelectedUnivs={setS8Univs}
          reorderUnivs={setS8Univs}
        />
      </Box>

      <Box mb={4}>
        <Typography variant="h6">Semestre S9</Typography>
        <Button
          variant="contained"
          onClick={() => copyFromSidebar("S9")}
          disabled={isS9ButtonDisabled}
          sx={{ mb: 1 }}
        >
          Copier depuis la sidebar (S9)
        </Button>
        <UnivSelection
          selectedUnivs={s9Univs}
          setSelectedUnivs={setS9Univs}
          reorderUnivs={setS9Univs}
        />
      </Box>

      <TextField
        label="Numéro étudiant"
        value={value}
        onChange={handleChange}
        error={error}
        helperText={error ? "L'entier doit contenir exactement 8 chiffres" : ""}
        inputProps={{ maxLength: 8 }}
      />
      <TextField
        select
        label="Spécialité"
        value={selectedSpecialty}
        onChange={(e) => setSelectedSpecialty(e.target.value)}
        fullWidth
      >
        {specialties.map((spec) => (
          <MenuItem key={spec} value={spec}>
            {spec}
          </MenuItem>
        ))}
      </TextField>
      <Button
        variant="contained"
        sx={{ backgroundColor: "#009bda", color: "#fff", '&:hover': { backgroundColor: "#007bb5" } }}
        onClick={() => console.log("Action future")}
      >
        Action à venir
      </Button>
    </Box>
  );
}
