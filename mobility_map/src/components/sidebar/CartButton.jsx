import { ShoppingCartIcon } from '@heroicons/react/24/outline';
import Button from '@mui/material/Button';

export default function CartButton({ onButtonClick, active }) {
  return (
    <Button
      onClick={onButtonClick}
      variant="contained"
      sx={{
        boxShadow: 'none',
        backgroundColor: active ? '#ffffff' : '#009bda',
        color: active ? '#009bda' : '#ffffff',
        textTransform: 'none',
        justifyContent: 'flex-start',
        gap: 1,
        paddingY: 1.5,
        paddingX: 2,
        '&:hover': {
          backgroundColor: active ? '#f0f0f0' : '#007bb5',
        },
      }}
      fullWidth
      startIcon={
        <ShoppingCartIcon style={{ height: 24, width: 24 }} />
      }
    >
      Tableau Comparatif
    </Button>
  );
}