class SimpleGenerator:
    def generate(self, query, retrieved_chunks):
        if not retrieved_chunks:
            return "Je n’ai pas trouvé d’information suffisante dans les documents."

        response = []
        response.append(f"Réponse basée sur les documents :\n")

        for i, item in enumerate(retrieved_chunks, start=1):
            chunk = item["chunk"]

            response.append(
                f"{i}. Source : {chunk['file_name']} — page {chunk['page']}\n"
                f"{chunk['text'][:700]}...\n"
            )

        return "\n".join(response)