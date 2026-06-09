import re
from urllib import response
import fitz
from numpy.strings import title

from apc_dash.polytech_rag.app.config import RAW_PDF_DIR
from apc_dash.polytech_rag.app.services.project_service import ProjectService

class FileService:
    def read_pdf(self, formation, category):
        formation = formation.lower()
        category = category.lower()

        pdf_path = RAW_PDF_DIR / formation / f"{category}.pdf"

        if not pdf_path.exists():
            return None, f"Fichier introuvable : {pdf_path}"

        doc = fitz.open(pdf_path)
        pages = []

        for page in doc:
            text = page.get_text().strip()
            if text:
                pages.append(text)

        doc.close()
        return "\n".join(pages), None

    def generate_answer(self, formation, category, level="tous", keyword=""):
        text, error = self.read_pdf(formation, category)

        if error:
            return error

        if category == "projets":
            return self.answer_projects(text, formation, level, keyword)

        if category == "competences":
            return self.answer_competences(text, formation)

        if category == "metiers":
            return self.answer_jobs(text, formation)

        if category == "techniques":
            return self.answer_sections(text, formation, "Compétences techniques à maîtriser")

        if category == "bonnes_pratiques":
            return self.answer_sections(text, formation, "Bonnes pratiques professionnelles")

        if category == "experiences":
            return self.answer_sections(text, formation, "Expériences pratiques et ressources")

        return self.answer_sections(text, formation, category)

    def answer_projects(self, text, formation, level="tous", keyword=""):
        service = ProjectService()
        projects = service.extract_projects(text)
        projects = service.filter_projects(projects, level=level, keyword=keyword)
        return service.format_projects(projects, formation)

    def answer_sections(self, text, formation, title):
        sections = self.extract_numbered_sections(text)
        response = f"## {title} — {formation.upper()}\n\n"

        if not sections:
            response += self.clean_text(text[:2500])
            return response

        for section in sections:
            response += f"### {section['title']}\n\n"

            bullets = self.extract_bullets(section["content"])

            if bullets:
                for bullet in bullets[:7]:
                    response += f"- {bullet}\n"
            else:
                content = self.clean_text(section["content"])
                response += content[:700] + "...\n"

            response += "\n"

        checklist = self.extract_checklist(text)
        if checklist:
            response += "## Checklist importante\n\n"
            for item in checklist[:10]:
                response += f"- {item}\n"

        return response

    def answer_jobs(self, text, formation):
        response = f"## Métiers et débouchés — {formation.upper()}\n\n"

        stop_words = ["Secteurs", "Tendances", "Conseils", "Sources"]

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        full_text = "\n".join(lines)

        pattern = (
            r"(?=(Data Engineer|Data Scientist|Data Analyst|"
            r"ML Engineer[^\n]*|Architecte Data[^\n]*|"
            r"Ingénieur [^\n]+|Chef de Projet[^\n]*|"
            r"Responsable [^\n]+|Chargé de Mission[^\n]+))"
        )

        parts = re.split(pattern, full_text)
        jobs = []

        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""

            for stop in stop_words:
                idx = content.find(stop)
                if idx != -1:
                    content = content[:idx]

            if len(content) < 80:
                continue

            competences = self.extract_after_label(content, "Compétences clés")
            salary = self.extract_salary(content)

            description = content.split("Compétences clés")[0].strip()
            description = self.clean_text(description)

            jobs.append({
                "title": title,
                "description": description[:450],
                "competences": competences[:300],
                "salary": salary
            })

        if not jobs:
            return response + self.clean_text(text[:2500])

        for job in jobs[:8]:
            response += f"### {job['title']}\n"

            if job["description"]:
                response += f"- **Description :** {job['description']}...\n"

            if job["competences"]:
                response += f"- **Compétences clés :** {job['competences']}\n"

            if job["salary"]:
                response += f"- **Salaire :** {job['salary']}\n"

            response += "\n"

        return response

    def answer_competences(self, text, formation):
        formation = formation.lower()

        if formation == "meca":
            return self.answer_meca_competences(text)

        if formation == "bee":
            return self.answer_bee_competences(text)

        response = f"## Compétences principales — {formation.upper()}\n\n"

        acs = re.findall(
            r"(AC\s*\d+\.\d+\s+.*?)(?=AC\s*\d+\.\d+|$)",
            text,
            flags=re.DOTALL
        )

        if not acs:
            return self.answer_sections(text, formation, "Compétences principales")

        grouped = {}

        for ac in acs:
            clean_ac = self.clean_text(ac)
            match = re.match(r"AC\s*(\d+)\.", clean_ac)

            bloc = f"Bloc {match.group(1)}" if match else "Autres compétences"
            grouped.setdefault(bloc, []).append(clean_ac)

        for bloc, items in grouped.items():
            response += f"### {bloc}\n"
            for item in items:
                response += f"- {item}\n"
            response += "\n"

        return response

    def answer_meca_competences(self, text):
        response = "## Compétences principales — MECA\n\n"

        pages = text.split("\f")
        clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(clean_lines)

        blocks = [
            "Concevoir des produits manufacturés",
        "Industrialiser des produits manufacturés",
        "Gérer un projet dans le domaine industriel",
        "Optimiser les procédés de fabrication",
        "Concevoir des systèmes mécatroniques",
        "Concevoir des produits en matériaux composites"
        ]

        for title in blocks:
            section = self.extract_section_around_title(clean_text, title, blocks)

            if not section:
                continue

            situations = self.extract_items_after(section, "Situations professionnelles")
            composantes = self.extract_items_after(section, "Composantes essentielles")

            response += f"### {title}\n\n"

            if situations:
                response += "**Situations professionnelles :**\n"
                for item in situations[:10]:
                    response += f"- {item}\n"
                response += "\n"

            if composantes:
                response += "**Composantes essentielles :**\n"
                for item in composantes[:8]:
                    response += f"- {item}\n"
                response += "\n"

        return response

    def answer_bee_competences(self, text):
        response = "## Compétences principales — BEE\n\n"

        clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(clean_lines)

        blocks = [
        "CONCEVOIR LE SYSTÈME CONSTRUCTIF",
        "GARANTIR LA PERFORMANCE",
        "INTÉGRER DES SOLUTIONS DURABLES ADAPTÉES",
        "PILOTER UN PROJET DE BÂTIMENT"
        ]

        for title in blocks:
            section = self.extract_section_around_title(clean_text, title, blocks)

            if not section:
                continue

            situations = self.extract_items_after(section, "Situations professionnelles")
            composantes = self.extract_items_after(section, "Composantes essentielles")

            response += f"### {title.title()}\n\n"

            if situations:
                response += "**Situations professionnelles :**\n"
                for item in situations[:10]:
                    response += f"- {item}\n"
                response += "\n"

            if composantes:
                response += "**Composantes essentielles :**\n"
                for item in composantes[:8]:
                    response += f"- {item}\n"
                response += "\n"

        return response

    def answer_block_competences(self, text, response, blocks):
        clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(clean_lines)

        lower_text = clean_text.lower()

        for title in blocks:
            start = lower_text.find(title.lower())

            if start == -1:
                continue

            next_positions = []

            for other in blocks:
                if other == title:
                    continue

                pos = lower_text.find(other.lower(), start + len(title))
                if pos != -1:
                    next_positions.append(pos)

            end = min(next_positions) if next_positions else len(clean_text)
            section = clean_text[start:end]

            response += f"### {title}\n\n"

            situations = self.extract_items_between(
                section,
                "Situations professionnelles",
                "Composantes essentielles"
            )

            composantes = self.extract_items_between(
                section,
                "Composantes essentielles",
                "APPRENTISSAGES"
            )

            if not situations:
                situations = self.extract_items_after(section, "Situations professionnelles")

            if not composantes:
                composantes = self.extract_items_after(section, "Composantes essentielles")

            if situations:
                response += "**Situations professionnelles :**\n"
                for item in situations[:10]:
                    response += f"- {item}\n"
                response += "\n"

            if composantes:
                response += "**Composantes essentielles :**\n"
                for item in composantes[:10]:
                    response += f"- {item}\n"
                response += "\n"

        return response

    def extract_items_between(self, text, start_label, end_label):
        start = text.lower().find(start_label.lower())

        if start == -1:
            return []

        end = text.lower().find(end_label.lower(), start + len(start_label))

        if end == -1:
            part = text[start:]
        else:
            part = text[start:end]

        return self.extract_bullet_items(part.replace(start_label, ""))

    def extract_items_after(self, text, label):
        start = text.lower().find(label.lower())

        if start == -1:
            return []

        part = text[start:]
        return self.extract_bullet_items(part.replace(label, ""))

    def extract_bullet_items(self, text):
        text = text.replace("•", "\n•")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        items = []

        for line in lines:
            if line.startswith("•"):
                item = line.replace("•", "").strip()
                if item and not item.startswith("…"):
                    items.append(self.clean_text(item))

        return items

    def extract_numbered_sections(self, text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        sections = []
        current_title = None
        current_content = []

        pattern = re.compile(r"^\d+\.\s+.+")

        for line in lines:
            if pattern.match(line):
                if current_title:
                    sections.append({
                        "title": current_title,
                        "content": "\n".join(current_content)
                    })

                current_title = line
                current_content = []
            else:
                if current_title:
                    current_content.append(line)

        if current_title:
            sections.append({
                "title": current_title,
                "content": "\n".join(current_content)
            })

        return sections

    def extract_bullets(self, text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        bullets = []

        for line in lines:
            if line.startswith("•"):
                bullets.append(line.replace("•", "").strip())
            elif line.startswith("■"):
                bullets.append(line.replace("■", "").strip())
            elif line.startswith("✓"):
                bullets.append(line.replace("✓", "").strip())
            elif line.startswith("→"):
                bullets.append(line.strip())

        return bullets

    def extract_checklist(self, text):
        if "Checklist" not in text:
            return []

        checklist_text = text.split("Checklist", 1)[1]
        lines = [line.strip() for line in checklist_text.splitlines() if line.strip()]

        items = []

        for line in lines:
            if line.startswith("■"):
                items.append(line.replace("■", "").strip())

        return items

    def extract_after_label(self, text, label):
        pattern = rf"{re.escape(label)}\s*:\s*(.*?)(?=Junior|Senior|ACs|Blocs|Bloc|$)"
        match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)

        if not match:
            return ""

        return self.clean_text(match.group(1))

    def extract_salary(self, text):
        match = re.search(
            r"(Junior\s*:\s*[^€]+€\s*Senior\s*:\s*[^€]+€)",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return self.clean_text(match.group(1))

        return ""
    def extract_section_around_title(self, text, title, all_titles):
        lower_text = text.lower()
        title_lower = title.lower()

        positions = []
        for t in all_titles:
            pos = lower_text.find(t.lower())
            if pos != -1:
                positions.append((pos, t))

        positions = sorted(positions)

        current_pos = lower_text.find(title_lower)

        if current_pos == -1:
            return ""

        start = current_pos

        for pos, t in reversed(positions):
            if pos < current_pos:
                previous_text = text[pos:current_pos]
                if len(previous_text) < 2500:
                    start = pos
                break

        end = len(text)

        for pos, t in positions:
            if pos > current_pos:
                end = pos
                break

        return text[start:end]

    def clean_text(self, text):
        text = text.replace("■", "")
        text = text.replace("I", "")
        text = re.sub(r"\s+", " ", text)
        return text.strip()