import re


class TextCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        return text