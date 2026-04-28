from app.rag.retriever import Retriever
from app.rag.generator import SimpleGenerator


class QueryService:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = SimpleGenerator()

    def build_guided_query(self, formation, category):
        templates = {
            "competences": f"Quelles sont les compétences principales de la formation {formation} ?",
            "metiers": f"Quels sont les métiers et débouchés de la formation {formation} ?",
            "projets": f"Quels projets pratiques peut-on réaliser en formation {formation} ?",
            "techniques": f"Quelles compétences techniques faut-il maîtriser en formation {formation} ?",
            "bonnes_pratiques": f"Quelles sont les bonnes pratiques pour réussir en formation {formation} ?",
            "experiences": f"Quelles expériences pratiques sont utiles pour la formation {formation} ?",
            "general": f"Donne les informations importantes sur la formation {formation}."
        }

        return templates.get(category, templates["general"])

    def answer_guided(self, formation, category):
        formation = formation.lower()
        category = category.lower()

        query = self.build_guided_query(formation, category)

        chunks = self.retriever.retrieve(
            query=query,
            formation=formation,
            category=category,
            top_k=5
        )

        return self.generator.generate(query, chunks)