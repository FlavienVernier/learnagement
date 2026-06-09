import json
import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []

    def add_embeddings(self, embeddings: np.ndarray, chunks):
        self.index.add(embeddings)
        self.metadata.extend(chunks)

    def search(self, query_embedding, top_k=5, formation=None, category=None):
        scores, indices = self.index.search(query_embedding, min(top_k * 20, len(self.metadata)))

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.metadata[idx]

            if formation and chunk.get("formation") != formation:
                continue

            if category and chunk.get("category") != category:
                continue

            results.append({
                "score": float(score),
                "chunk": chunk
            })

            if len(results) >= top_k:
                break

        return results

    def save(self, index_file, metadata_file):
        faiss.write_index(self.index, str(index_file))

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, index_file, metadata_file):
        index = faiss.read_index(str(index_file))

        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        store = cls(index.d)
        store.index = index
        store.metadata = metadata

        return store