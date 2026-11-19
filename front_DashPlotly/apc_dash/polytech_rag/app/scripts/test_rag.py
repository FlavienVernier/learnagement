from app.services.file_service import FileService

from mysql.connector.aio.logger import logger


def main():
    service = FileService()

    formations = ["idu", "eit", "meca", "sni", "bee"]

    categories = [
        "competences",
        "metiers",
        "projets",
        "techniques",
        "bonnes_pratiques",
        "experiences"
    ]

    logger.info("=== Assistant d'orientation Polytech ===")

    logger.info("\nChoisir une formation :")
    for i, formation in enumerate(formations, start=1):
        logger.info(f"{i}. {formation.upper()}")

    formation_choice = int(input("\nVotre choix : "))
    formation = formations[formation_choice - 1]

    logger.info("\nQue voulez-vous consulter ?")
    for i, category in enumerate(categories, start=1):
        logger.info(f"{i}. {category}")

    category_choice = int(input("\nVotre choix : "))
    category = categories[category_choice - 1]

    level = "tous"
    keyword = ""

    if category == "projets":
        levels = ["tous", "débutant", "intermédiaire", "avancé"]

        logger.info("\nFiltrer par niveau :")
        for i, lvl in enumerate(levels, start=1):
            logger.info(f"{i}. {lvl}")

        level_choice = int(input("\nVotre choix : "))
        level = levels[level_choice - 1]

        keyword = input(
            "\nMot-clé optionnel "
            "(ex: BIM, Kafka, ACV, CAO, IoT, signal, énergie) "
            "ou Entrée pour ignorer : "
        ).strip()

    logger.info("\nGénération de la réponse...\n")

    answer = service.generate_answer(
        formation=formation,
        category=category,
        level=level,
        keyword=keyword
    )

    logger.info(answer)


if __name__ == "__main__":
    main()
    