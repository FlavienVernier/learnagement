from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PDF_DIR = BASE_DIR / "data" / "raw_pdfs"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
INDEX_DIR = BASE_DIR / "data" / "indexes"

CHUNKS_FILE = PROCESSED_DIR / "chunks.json"
ENRICHED_CHUNKS_FILE = PROCESSED_DIR / "enriched_chunks.json"

FAISS_INDEX_FILE = INDEX_DIR / "faiss_index.bin"
FAISS_METADATA_FILE = INDEX_DIR / "faiss_metadata.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

FORMATIONS = ["idu", "eit", "meca", "sni", "bee"]

CATEGORY_KEYWORDS = {
    "competences": ["competence", "compétence"],
    "metiers": ["metier", "métier", "emploi", "marche", "marché"],
    "projets": ["projet", "pratique"],
    "techniques": ["technique", "outils", "technologie"],
    "bonnes_pratiques": ["bonne", "pratique"],
    "experiences": ["experience", "expérience"]
}