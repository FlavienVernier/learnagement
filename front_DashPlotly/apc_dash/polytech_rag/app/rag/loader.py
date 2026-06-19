import fitz
from pathlib import Path


class PDFLoader:
    def load_pdf(self, pdf_path: Path, formation: str):
        pages = []

        doc = fitz.open(pdf_path)

        for page_number, page in enumerate(doc, start=1):
            text = page.get_text()

            pages.append({
                "formation": formation,
                "source": str(pdf_path),
                "file_name": pdf_path.name,
                "page": page_number,
                "text": text
            })

        doc.close()
        return pages

    def load_all_pdfs(self, raw_pdf_dir: Path):
        all_pages = []

        for formation_dir in raw_pdf_dir.iterdir():
            if formation_dir.is_dir():
                formation = formation_dir.name.lower()

                for pdf_file in formation_dir.glob("*.pdf"):
                    pages = self.load_pdf(pdf_file, formation)
                    all_pages.extend(pages)

        return all_pages