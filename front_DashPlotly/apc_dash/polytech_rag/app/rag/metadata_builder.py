from app.config import CATEGORY_KEYWORDS


class MetadataBuilder:
    def detect_category(self, file_name: str):
        name = file_name.lower()

        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in name:
                    return category

        return "general"

    def enrich_chunks(self, chunks):
        enriched = []

        for chunk in chunks:
            category = self.detect_category(chunk["file_name"])

            new_chunk = {
                **chunk,
                "category": category
            }

            enriched.append(new_chunk)

        return enriched