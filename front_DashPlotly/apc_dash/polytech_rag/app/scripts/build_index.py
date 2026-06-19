import json

from app.config import ENRICHED_CHUNKS_FILE, INDEX_DIR, FAISS_INDEX_FILE, FAISS_METADATA_FILE
from app.rag.embedder import TextEmbedder
from app.rag.vectorstore import FAISSVectorStore


def main():
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    if not ENRICHED_CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {ENRICHED_CHUNKS_FILE}")

    print("Chargement des chunks...")
    with open(ENRICHED_CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Nombre de chunks : {len(chunks)}")

    print("Création des embeddings...")
    embedder = TextEmbedder()
    embeddings = embedder.embed_chunks(chunks)

    dimension = embeddings.shape[1]

    print(f"Dimension des embeddings : {dimension}")

    print("Création de l’index FAISS...")
    store = FAISSVectorStore(dimension=dimension)
    store.add_embeddings(embeddings, chunks)

    store.save(FAISS_INDEX_FILE, FAISS_METADATA_FILE)

    print("Index FAISS créé avec succès.")


if __name__ == "__main__":
    main()