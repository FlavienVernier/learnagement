import re


class ProjectService:
    def extract_projects(self, text):
        pattern = r"(Projet #\d+.*?)(?=Projet #\d+|Ressources|Données :|Comment présenter|$)"
        blocks = re.findall(pattern, text, flags=re.DOTALL)

        projects = []

        for block in blocks:
            clean = self.clean_text(block)

            title = self.extract_title(clean)
            duration = self.extract_duration(clean)
            level = self.detect_level(clean, duration)

            context = self.extract_between(clean, "Contexte", "Objectifs")
            objectives = self.extract_objectives(clean)
            tools = self.extract_between_any(clean, ["Outils", "Stack technique", "Stack"], ["Livrable"])
            deliverable = self.extract_between(clean, "Livrable", "Bonus")
            bonus = self.extract_between_any(clean, ["Bonus"], ["ACs", "Blocs", "Bloc", "Projet #"])
            skills = self.extract_after_any(clean, ["ACs IDU", "ACs EIT", "ACs SNI", "Blocs BEE", "Bloc MECA", "Blocs MECA", "Bloc SNI"])

            domain = self.detect_domain(clean)

            projects.append({
                "title": title,
                "duration": duration,
                "level": level,
                "domain": domain,
                "context": context,
                "objectives": objectives,
                "tools": tools,
                "deliverable": deliverable,
                "bonus": bonus,
                "skills": skills
            })

        return projects

    def filter_projects(self, projects, level="tous", keyword=""):
        results = projects

        if level and level.lower() != "tous":
            results = [
                p for p in results
                if p["level"].lower() == level.lower()
            ]

        if keyword:
            keyword = keyword.lower()
            results = [
                p for p in results
                if keyword in (
                    p["title"] + " " +
                    p["domain"] + " " +
                    p["context"] + " " +
                    p["tools"] + " " +
                    p["deliverable"] + " " +
                    p["skills"]
                ).lower()
            ]

        return results

    def format_projects(self, projects, formation):
        response = f"## Projets pratiques pour {formation.upper()}\n\n"

        if not projects:
            return response + "Aucun projet ne correspond aux filtres choisis."

        for p in projects:
            response += f"### {p['title']}\n"
            response += f"- **Niveau :** {p['level']}\n"

            if p["domain"]:
                response += f"- **Domaine :** {p['domain']}\n"

            if p["duration"]:
                response += f"- **Durée :** {p['duration']}\n"

            if p["context"]:
                response += f"- **Contexte :** {p['context'][:350]}...\n"

            if p["objectives"]:
                response += "- **Objectifs :**\n"
                for obj in p["objectives"][:4]:
                    response += f"  - {obj}\n"

            if p["tools"]:
                response += f"- **Outils / Stack :** {p['tools']}\n"

            if p["deliverable"]:
                response += f"- **Livrable :** {p['deliverable']}\n"

            if p["bonus"]:
                response += f"- **Idée bonus :** {p['bonus']}\n"

            if p["skills"]:
                response += f"- **Compétences / blocs :** {p['skills'][:200]}\n"

            response += "\n"

        return response

    def extract_title(self, text):
        match = re.search(r"(Projet #\d+)\s+(.*?)(?:\s+[■I]\s+|\s+\d+\s*[–-]?\s*\d*\s*semaines?|$)", text)
        if match:
            return f"{match.group(1)} — {match.group(2).strip()}"
        return text[:80]

    def extract_duration(self, text):
        match = re.search(r"(\d+\s*[–-]?\s*\d*\s*semaines?)", text)
        return match.group(1).replace(" ", "") if match else ""

    def detect_level(self, text, duration):
        text = text.lower()

        if "niveau 1" in text or "3a" in text or "débutant" in text:
            return "débutant"

        if "niveau 2" in text or "4a" in text or "intermédiaire" in text:
            return "intermédiaire"

        if "niveau 3" in text or "5a" in text or "avancé" in text:
            return "avancé"

        numbers = re.findall(r"\d+", duration)

        if numbers:
            max_week = max(int(n) for n in numbers)
            if max_week <= 3:
                return "débutant"
            if max_week <= 5:
                return "intermédiaire"
            return "avancé"

        return "non précisé"

    def detect_domain(self, text):
        text = text.lower()

        domains = {
            "Data / IA": ["data", "machine learning", "ia", "ml", "classification", "rag", "spark", "kafka"],
            "BIM / Bâtiment": ["bim", "revit", "re2020", "thermique", "chantier", "cvc", "acv bâtiment"],
            "Écologie / EIT": ["territoire", "flux", "déchets", "eit", "symbiose", "bilan carbone", "eau"],
            "Mécanique / CAO": ["cao", "solidworks", "catia", "fea", "ansys", "mécanique", "composite", "usinage"],
            "SNI / Embarqué": ["arduino", "stm32", "capteur", "iot", "signal", "pid", "raspberry", "freertos", "embarqué"]
        }

        found = []

        for domain, keywords in domains.items():
            if any(keyword in text for keyword in keywords):
                found.append(domain)

        return ", ".join(found)

    def extract_between(self, text, start, end):
        pattern = rf"{re.escape(start)}(.*?){re.escape(end)}"
        match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
        return self.clean_text(match.group(1)) if match else ""

    def extract_between_any(self, text, starts, ends):
        for start in starts:
            for end in ends:
                value = self.extract_between(text, start, end)
                if value:
                    return value
        return ""

    def extract_after_any(self, text, labels):
        for label in labels:
            pattern = rf"{re.escape(label)}(.*)"
            match = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
            if match:
                return self.clean_text(match.group(1))
        return ""

    def extract_objectives(self, text):
        objectives_text = self.extract_between_any(
            text,
            ["Objectifs"],
            ["Outils", "Stack technique", "Stack", "Livrable"]
        )

        if not objectives_text:
            return []

        objectives_text = objectives_text.replace("•", "\n•")
        lines = [line.strip() for line in objectives_text.splitlines() if line.strip()]

        objectives = []

        for line in lines:
            if line.startswith("•"):
                objectives.append(line.replace("•", "").strip())

        if not objectives:
            objectives.append(objectives_text[:300])

        return objectives

    def clean_text(self, text):
        text = text.replace("■", "")
        text = text.replace("I", "")
        text = re.sub(r"\s+", " ", text)
        return text.strip()