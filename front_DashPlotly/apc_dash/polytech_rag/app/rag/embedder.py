from sentence_transformers import SentenceTransformer
import numpy as np

from app.config import EMBEDDING_MODEL_NAME


class TextEmbedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings.astype("float32")

    def embed_chunks(self, chunks):
        texts = [chunk["text"] for chunk in chunks]
        return self.embed_texts(texts)