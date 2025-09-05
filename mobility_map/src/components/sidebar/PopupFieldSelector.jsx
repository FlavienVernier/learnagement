import React from 'react';
import { FormGroup, FormControlLabel, Checkbox, Typography } from '@mui/material';
import { CSS } from "@dnd-kit/utilities";

const fieldOptions = [
  { label: 'Pays', key: 'pays' },
  { label: 'Adresse', key: 'adresse' },
  { label: 'Critères Academiques', key: 'criteres_academiques' },
  { label: 'Intégration et Vie Sociale', key: 'integration_et_vie_sociale' },
  { label: 'Logement et Vie Quotidienne', key: 'logement_et_vie_quotidienne' },
  { label: 'Organisation et Démarches', key: 'organisation_et_demarches' },
  { label: 'Expérience Globale', key: 'experience_globale' },
  { label: 'Commentaire', key: 'commentaire' }
  // Ajoute d'autres champs ici si besoin
];

export default function PopupFieldSelector({ selectedFields, onChange }) {
  const style = {
    padding: "8px",
    marginBottom: "4px",
    background: "#ffffff",
    borderRadius: "4px",
    cursor: "grab",
    justifyContent: "space-between",
    alignItems: "center",
  };
  const handleToggle = (key) => {
    if (selectedFields.includes(key)) {
      onChange(selectedFields.filter(f => f !== key));
    } else {
      onChange([...selectedFields, key]);
    }
  };

  return (
    <div style={style}>
      <Typography variant="subtitle1" sx={{ color: '#009bda', fontWeight: 'bold' }}>
        Champs à afficher dans la popup
      </Typography>
      <FormGroup>
        {fieldOptions.map(({ label, key }) => (
          <FormControlLabel
            key={key}
            control={
              <Checkbox
                checked={selectedFields.includes(key)}
                onChange={() => handleToggle(key)}
                sx={{ color: '#009bda' }}
              />
            }
            label={<span style={{ color: '#009bda' }}>{label}</span>}
          />
        ))}
      </FormGroup>
    </div>
  );
}
