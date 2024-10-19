from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import webbrowser  # Для открытия в браузере

# Инициализация драйвера
driver = webdriver.Chrome()


def search_wikipedia(query):
    """Функция для поиска по запросу на Википедии."""
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    driver.get(url)
    time.sleep(2)  # Ждем загрузки страницы

    # Проверяем, существует ли статья
    try:
        title_element = driver.find_element(By.ID, "firstHeading")
        print(f"--- Статья: {title_element.text} ---\n")
    except:
        print(f"Статья по запросу '{query}' не найдена. Попробуйте снова.")
        return None

    return url


def print_paragraphs():
    """Функция для листания параграфов статьи."""
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")

    for i, paragraph in enumerate(paragraphs):
        try:
            if paragraph.text.strip():
                print(paragraph.text.strip())
                if (i + 1) % 2 == 0:  # Показываем по два параграфа за раз
                    user_input = input("\n[Enter - продолжить, q - выход]: ")
                    if user_input.lower() == 'q':
                        return
        except Exception as e:
            print(f"Ошибка при доступе к параграфу: {e}")


def list_related_links():
    """Вывод связанных статей на странице."""
    links = driver.find_elements(By.CSS_SELECTOR, "a")
    related_links = {idx + 1: link for idx, link in enumerate(links) if "/wiki/" in link.get_attribute("href")}

    if not related_links:
        print("Связанных страниц не найдено.")
        return None

    for idx, link in related_links.items():
        print(f"{idx}. {link.text}")

    return related_links


def browse_wiki():
    """Основной цикл программы для поиска и навигации по Википедии."""
    while True:
        # 1. Спрашиваем запрос пользователя
        query = input("Введите запрос для поиска в Википедии или 'q' для выхода: ")
        if query.lower() == 'q':
            break

        # 2. Переход по запросу на Википедию
        url = search_wikipedia(query)
        if not url:
            continue

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
                print_paragraphs()

            elif choice == '2':
                # Переход на связанные страницы
                print("\n--- Связанные страницы ---")
                related_links = list_related_links()
                if not related_links:
                    continue

                # Выбираем связанную статью для перехода
                try:
                    link_choice = int(input("\nВведите номер статьи для перехода или 0 для отмены: "))
                    if link_choice == 0:
                        continue
                    selected_link = related_links[link_choice]
                    new_url = selected_link.get_attribute("href")
                    driver.get(new_url)
                    time.sleep(2)  # Ждем загрузки новой страницы
                    print(f"\n--- Переход на статью: {selected_link.text} ---\n")
                except (ValueError, KeyError):
                    print("Некорректный ввод. Попробуйте снова.")

            elif choice == '3':
                # Открываем статью в браузере
                print(f"Открываем статью в браузере: {url}")
                webbrowser.open(url)

            elif choice == '4':
                # Выход из программы
                print("Выход из программы.")
                return
            else:
                print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    try:
        browse_wiki()
    finally:
        driver.quit()  # Закрываем браузер после завершения программы