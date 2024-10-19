import wikipediaapi
import webbrowser

# Инициализация объекта Википедии для русского языка
wiki = wikipediaapi.Wikipedia('ru')


def print_paragraphs(page, paragraphs_to_show=2):
    """Показывает по два параграфа из статьи."""
    paragraphs = page.summary.split('\n')
    for i in range(0, len(paragraphs), paragraphs_to_show):
        for paragraph in paragraphs[i:i + paragraphs_to_show]:
            print(paragraph)
        # Спрашиваем пользователя, хочет ли он продолжить листать
        user_input = input("\n[Enter - продолжить, q - выход]: ")
        if user_input.lower() == 'q':
            return


def browse_wiki():
    """Основной цикл программы для поиска и навигации по Википедии."""
    while True:
        # 1. Спрашиваем запрос пользователя
        query = input("Введите запрос для поиска в Википедии или 'q' для выхода: ")
        if query.lower() == 'q':
            break

        # 2. Находим страницу по запросу
        page = wiki.page(query)

        if not page.exists():
            print(f"Статья с названием '{query}' не найдена. Попробуйте снова.")
            continue

        print(f"\n--- Статья: {page.title} ---\n")

        # 3. Предлагаем три варианта действий
        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Открыть статью в браузере")
            print("4. Выйти из программы")

            choice = input("Ваш выбор: ")

            if choice == '1':
                # Листаем параграфы статьи
                print("\n--- Параграфы статьи ---")
                print_paragraphs(page)

            elif choice == '2':
                # Переход на связанные страницы
                print("\n--- Связанные страницы ---")
                links = page.links
                if not links:
                    print("Связанных страниц не найдено.")
                else:
                    related_pages = list(links.keys())
                    for idx, link_title in enumerate(related_pages, start=1):
                        print(f"{idx}. {link_title}")

                    # Выбираем связанную статью для перехода
                    try:
                        link_choice = int(input("\nВведите номер статьи для перехода или 0 для отмены: "))
                        if link_choice == 0:
                            continue
                        selected_page_title = related_pages[link_choice - 1]
                        new_page = wiki.page(selected_page_title)

                        # Внутреннее меню для связанной статьи
                        while True:
                            print(f"\n--- Статья: {new_page.title} ---")
                            print("1. Листать параграфы статьи")
                            print("2. Перейти на одну из связанных страниц")
                            print("3. Вернуться к предыдущей статье")

                            sub_choice = input("Ваш выбор: ")

                            if sub_choice == '1':
                                # Листаем параграфы выбранной статьи
                                print_paragraphs(new_page)
                            elif sub_choice == '2':
                                # Переход к связанным страницам выбранной статьи
                                new_links = new_page.links
                                if not new_links:
                                    print("Связанных страниц не найдено.")
                                else:
                                    new_related_pages = list(new_links.keys())
                                    for idx, new_link_title in enumerate(new_related_pages, start=1):
                                        print(f"{idx}. {new_link_title}")
                                    try:
                                        new_link_choice = int(
                                            input("\nВведите номер статьи для перехода или 0 для отмены: "))
                                        if new_link_choice == 0:
                                            continue
                                        selected_new_page_title = new_related_pages[new_link_choice - 1]
                                        new_page = wiki.page(selected_new_page_title)
                                    except (ValueError, IndexError):
                                        print("Некорректный ввод. Попробуйте снова.")
                            elif sub_choice == '3':
                                # Возврат к предыдущей статье
                                break
                            else:
                                print("Некорректный выбор.")
                    except (ValueError, IndexError):
                        print("Некорректный ввод. Попробуйте снова.")

            elif choice == '3':
                # Открываем статью в браузере
                url = page.fullurl
                print(f"Открываем статью в браузере: {url}")
                webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(url)

            elif choice == '4':
                # Выход из программы
                print("Выход из программы.")
                return
            else:
                print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    browse_wiki()