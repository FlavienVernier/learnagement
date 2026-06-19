from app.services.file_service import FileService


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

    print("=== Assistant d'orientation Polytech ===")

    print("\nChoisir une formation :")
    for i, formation in enumerate(formations, start=1):
        print(f"{i}. {formation.upper()}")

    formation_choice = int(input("\nVotre choix : "))
    formation = formations[formation_choice - 1]

    print("\nQue voulez-vous consulter ?")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    category_choice = int(input("\nVotre choix : "))
    category = categories[category_choice - 1]

    level = "tous"
    keyword = ""

    if category == "projets":
        levels = ["tous", "débutant", "intermédiaire", "avancé"]

        print("\nFiltrer par niveau :")
        for i, lvl in enumerate(levels, start=1):
            print(f"{i}. {lvl}")

        level_choice = int(input("\nVotre choix : "))
        level = levels[level_choice - 1]

        keyword = input(
            "\nMot-clé optionnel "
            "(ex: BIM, Kafka, ACV, CAO, IoT, signal, énergie) "
            "ou Entrée pour ignorer : "
        ).strip()

    print("\nGénération de la réponse...\n")

    answer = service.generate_answer(
        formation=formation,
        category=category,
        level=level,
        keyword=keyword
    )

    print(answer)


if __name__ == "__main__":
    main()
    