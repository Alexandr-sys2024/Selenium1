from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import webbrowser


class WikipediaBrowser:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def open_page(self, url):
        """Открывает страницу по указанному URL."""
        self.driver.get(url)
        time.sleep(2)  # Ожидаем загрузки страницы

    def search_wikipedia(self, query):
        """Возвращает URL статьи по запросу."""
        url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
        self.open_page(url)

        if self.article_exists():
            title = self.get_article_title()
            print(f"--- Статья: {title} ---\n")
            return url
        else:
            print(f"Статья по запросу '{query}' не найдена. Попробуйте снова.")
            return None

    def article_exists(self):
        """Проверяет существование статьи."""
        try:
            self.driver.find_element(By.ID, "firstHeading")
            return True
        except:
            return False

    def get_article_title(self):
        """Возвращает заголовок статьи."""
        title_element = self.driver.find_element(By.ID, "firstHeading")
        return title_element.text

    def print_paragraphs(self):
        """Печатает параграфы статьи с пошаговым просмотром."""
        paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "p")
        for i, paragraph in enumerate(paragraphs):
            if paragraph.text.strip():
                print(paragraph.text.strip())
                if (i + 1) % 2 == 0:
                    user_input = input("\n[Enter - продолжить, q - выход]: ")
                    if user_input.lower() == 'q':
                        return

    def list_related_links(self):
        """Возвращает словарь найденных связанных статей."""
        links = self.driver.find_elements(By.CSS_SELECTOR, "a")
        related_links = {}

        for idx, link in enumerate(links):
            href = link.get_attribute("href")
            if href and "/wiki/" in href:
                related_links[idx + 1] = (link.text, href)

        if not related_links:
            print("Связанных страниц не найдено.")
            return None

        for idx, (text, _) in related_links.items():
            print(f"{idx}. {text}")

        return related_links

    def browse_related_page(self, related_links):
        """Осуществляет переход на выбранную связанную страницу."""
        try:
            link_choice = int(input("\nВведите номер статьи для перехода или 0 для отмены: "))
            if link_choice == 0:
                return
            _, new_url = related_links[link_choice]
            self.open_page(new_url)
            new_title = self.get_article_title()
            print(f"\n--- Переход на статью: {new_title} ---\n")
        except (ValueError, KeyError):
            print("Некорректный ввод. Попробуйте снова.")

    def open_in_browser(self, url):
        """Открывает статью в системном браузере."""
        print(f"Открываем статью в браузере: {url}")
        webbrowser.open(url)

    def close(self):
        """Закрывает веб-драйвер."""
        self.driver.quit()


def main():
    wiki_browser = WikipediaBrowser()

    try:
        while True:
            query = input("Введите запрос для поиска в Википедии или 'q' для выхода: ")
            if query.lower() == 'q':
                break

            url = wiki_browser.search_wikipedia(query)
            if not url:
                continue

            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Открыть статью в браузере")
                print("4. Выйти из программы")

                choice = input("Ваш выбор: ")

                if choice == '1':
                    print("\n--- Параграфы статьи ---")
                    wiki_browser.print_paragraphs()

                elif choice == '2':
                    print("\n--- Связанные страницы ---")
                    related_links = wiki_browser.list_related_links()
                    if related_links:
                        wiki_browser.browse_related_page(related_links)

                elif choice == '3':
                    wiki_browser.open_in_browser(url)

                elif choice == '4':
                    print("Выход из программы.")
                    return

                else:
                    print("Некорректный выбор. Попробуйте снова.")

    finally:
        wiki_browser.close()


if __name__ == '__main__':
    main()