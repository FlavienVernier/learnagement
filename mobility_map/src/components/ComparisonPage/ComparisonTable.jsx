import { DataGrid } from '@mui/x-data-grid';
import { Typography, Box } from '@mui/material';

function ComparisonTable({ universities }) {
  if (universities.length === 0) {
    return <Typography variant="h3">Aucune université sélectionnée.</Typography>;
  }

  const columns = [
    //{ field: 'id', headerName: 'ID', flex: 0.3 },
    { field: 'nom_partenaire', headerName: 'Nom', flex: 1 },
    { field: 'pays', headerName: 'Pays', flex: 0.7 },
    { field: 'adresse', headerName: 'Adresse', flex: 0.7 },
    //{ field: 'latitude', headerName: 'Latitude', flex: 0.6, type: 'number' },
    //{ field: 'longitude', headerName: 'Longitude', flex: 0.6, type: 'number' },
    {field: 'site_web',
      headerName: 'Site Web',
      flex: 0.7,
      renderCell: (params) =>
        params.value ? (
          <a
            href={params.value}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#1976d2', textDecoration: 'underline' }}
          >
            {params.value}
          </a>
        ) : (
          "-"
        ),
    },
    { field: 'langue_des_cours', headerName: 'Langue des cours', flex: 0.7 },
    { field: 'S8_total_places', headerName: 'S8 Total Places', flex: 0.7 },
    { field: 'S9_total_places', headerName: 'S9 Total Places', flex: 0.7 },
    { field: 'criteres_academiques', headerName: 'Critères Academiques', description: "Qualité des cours, difficulté d'admission, etc.", flex: 0.7 },
    { field: 'integration_et_vie_sociale', headerName: 'Intégration et Vie Sociale', flex: 0.7 },
    { field: 'logement_et_vie_quotidienne', headerName: 'Logement et Vie Quotidienne', flex: 0.7 },
    { field: 'organisation_et_demarches', headerName: 'Organisation et Démarches', flex: 0.7 },
    { field: 'experience_globale', headerName: 'Expérience Globale', flex: 0.7 },
  ];

  const rows = universities.map((u, index) => ({
    id: index + 1,
    ...u,
  }));

  return (
    <Box sx={{ width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5]}
        sx={{
          '& .MuiDataGrid-columnSeparator': {
            display: 'none',
          },
          '& .MuiDataGrid-columnHeader': {
            cursor: 'default',
          },
        }}
      />
    </Box>
  );
}

export default ComparisonTable;
