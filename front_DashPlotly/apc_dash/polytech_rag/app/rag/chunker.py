class TextChunker:
    def __init__(self, chunk_size=800, overlap=150):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str):
        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk.strip())

            start = end - self.overlap

        return chunks

    def chunk_pages(self, pages):
        all_chunks = []
        chunk_id = 0

        for page in pages:
            text_chunks = self.chunk_text(page["text"])

            for chunk_text in text_chunks:
                all_chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "formation": page["formation"],
                    "source": page["source"],
                    "file_name": page["file_name"],
                    "page": page["page"],
                    "text": chunk_text
                })

                chunk_id += 1

        return all_chunks