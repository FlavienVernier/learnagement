import {
  DndContext,
  closestCenter,
  useSensor,
  useSensors,
  PointerSensor
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  useSortable,
  verticalListSortingStrategy
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import CancelIcon from '@mui/icons-material/Cancel';
import { IconButton } from '@mui/material';

function SortableItem({ id, name, handleRemove }) {
  const { attributes, listeners, setNodeRef, setActivatorNodeRef, transform, transition } = useSortable({ id });
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    padding: "8px",
    marginBottom: "4px",
    background: "#ebebeb",
    borderRadius: "4px",
    cursor: "grab",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes}>
      <div ref={setActivatorNodeRef} {...listeners} style={{ flex: 1 }}>
        <Typography 
          variant="body1"
          sx={{ 
            fontFamily: 'Roboto, sans-serif', 
            color: '#000000',
          }}
        >
          {name}
        </Typography>
      </div>
      <IconButton
        onClick={(e) => {
          e.stopPropagation();
          handleRemove(id);
        }}
        sx={{ color: '#8d8d8d' }}
      >
        <CancelIcon />
      </IconButton>
    </div>
  );
}

export default function UnivSelection({ selectedUnivs, reorderUnivs }) {
  const sensors = useSensors(useSensor(PointerSensor));

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      const oldIndex = selectedUnivs.findIndex(u => u.nom_partenaire === active.id);
      const newIndex = selectedUnivs.findIndex(u => u.nom_partenaire === over.id);
      reorderUnivs(arrayMove(selectedUnivs, oldIndex, newIndex));
    }
  };

  const handleRemove = (universityName) => {
    const newList = selectedUnivs.filter(u => u.nom_partenaire !== universityName);
    reorderUnivs(newList);
  };

  return (
    <Box 
      sx={{
        padding:'1vw',
        marginY: '2vh',
        backgroundColor:'#ffffff',
        color: '#000000',
        borderRadius: '4px'
      }}
    >
      <Typography 
        variant="h5"
        fontSize={20}
        sx={{
          color: '#009bda',
          paddingBottom: '2vh'
        }}
      >
        Universités sélectionnées</Typography>
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={selectedUnivs.map(u => u.nom_partenaire)} strategy={verticalListSortingStrategy}>
          {selectedUnivs.map(u => (
            <SortableItem key={u.nom_partenaire} id={u.nom_partenaire} name={u.nom_partenaire} handleRemove={handleRemove} />
          ))}
        </SortableContext>
      </DndContext>
    </Box>
  );
}