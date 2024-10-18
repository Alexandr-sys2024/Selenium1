from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Функция для инициализации браузера
def init_browser():
    options = webdriver.ChromeOptions()
    # Укажите путь к вашему WebDriver для Яндекс.Браузера
    browser = webdriver.Chrome(executable_path='/path/to/yandexdriver', options=options)
    return browser

# Функция для поиска статьи по запросу
def search_wikipedia(query, browser):
    browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(2)

# Функция для перечисления параграфов
def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.CSS_SELECTOR, "p")
    for i, p in enumerate(paragraphs):
        print(f"Параграф {i+1}:\n{p.text}\n")
        if i % 5 == 4:  # Пауза каждые 5 параграфов
            input("Нажмите Enter, чтобы продолжить...")

# Функция для выбора связанной статьи
def choose_linked_article(browser):
    print("Связанные статьи:")
    links = browser.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    for i, link in enumerate(links):
        print(f"[{i+1}] {link.get_attribute('title') or link.text}")
    choice = int(input("Введите номер связанной статьи для перехода: ")) - 1
    if 0 <= choice < len(links):
        links[choice].click()
        time.sleep(2)
        return True
    else:
        print("Неправильный выбор.")
        return False

# Основная функция
def main():
    browser = init_browser()
    try:
        initial_query = input("Введите ваш запрос: ")
        search_wikipedia(initial_query, browser)

        while True:
            print("Выберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            choice = input("Ваш выбор: ")

            if choice == '1':
                list_paragraphs(browser)
            elif choice == '2':
                if not choose_linked_article(browser):
                    continue
                while True:
                    print("Выберите действие:")
                    print("1. Листать параграфы текущей статьи")
                    print("2. Перейти на одну из внутренних статей")
                    print("3. Вернуться назад к предыдущей статье")

                    sub_choice = input("Ваш выбор: ")

                    if sub_choice == '1':
                        list_paragraphs(browser)
                    elif sub_choice == '2':
                        if not choose_linked_article(browser):
                            continue
                    elif sub_choice == '3':
                        browser.back()
                        time.sleep(2)
                        break
                    else:
                        print("Неправильный выбор.")
            elif choice == '3':
                print("Завершение программы.")
                break
            else:
                print("Неправильный выбор.")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()