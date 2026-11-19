import json

from app.config import RAW_PDF_DIR, PROCESSED_DIR, CHUNKS_FILE, ENRICHED_CHUNKS_FILE
from app.rag.loader import PDFLoader
from app.rag.cleaner import TextCleaner
from app.rag.chunker import TextChunker
from app.rag.metadata_builder import MetadataBuilder

from core.logging import logger

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    loader = PDFLoader()
    cleaner = TextCleaner()
    chunker = TextChunker()
    metadata_builder = MetadataBuilder()

    logger.info("Chargement des PDF...")
    pages = loader.load_all_pdfs(RAW_PDF_DIR)

    logger.info(f"Nombre de pages chargées : {len(pages)}")

    for page in pages:
        page["text"] = cleaner.clean(page["text"])

    logger.info("Découpage en chunks...")
    chunks = chunker.chunk_pages(pages)

    logger.info(f"Nombre de chunks créés : {len(chunks)}")

    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    logger.info("Ajout des métadonnées...")
    enriched_chunks = metadata_builder.enrich_chunks(chunks)

    with open(ENRICHED_CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched_chunks, f, ensure_ascii=False, indent=2)

    logger.info("Chunks enregistrés avec succès.")


if __name__ == "__main__":
    main()