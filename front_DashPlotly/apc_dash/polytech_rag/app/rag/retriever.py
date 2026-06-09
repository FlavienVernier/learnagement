from app.config import FAISS_INDEX_FILE, FAISS_METADATA_FILE
from app.rag.embedder import TextEmbedder
from app.rag.vectorstore import FAISSVectorStore


class Retriever:
    def __init__(self):
        self.embedder = TextEmbedder()
        self.store = FAISSVectorStore.load(
            FAISS_INDEX_FILE,
            FAISS_METADATA_FILE
        )

    def retrieve(self, query, formation=None, category=None, top_k=5):
        query_embedding = self.embedder.embed_texts([query])

        results = self.store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            formation=formation,
            category=category
        )

        return results