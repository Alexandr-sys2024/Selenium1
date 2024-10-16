from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import time

browser = webdriver.Chrome()
#browser.get("https://en.wikipedia.org/wiki/Document_Object_Model")
#browser.save_screenshot("dom.png")
#time.sleep(5)
#browser.quit()
#browser.get("https://ru.wikipedia.org/wiki/Selenium")
#browser.save_screenshot("selenium.png")
#time.sleep(3)
#browser.refresh()
browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
#Проверяем по заголовку, тот ли сайт открылся
assert "Википедия" in browser.title
time.sleep(5)
#Находим окно поиска
search_box = browser.find.element(By.ID, "searchInput")
#Прописываем ввод текста в поисковую строку. В кавычках тот текст, который нужно ввести
search_box.send_keys("Солнечная система Расширенный поиск")
#Добавляем не только введение текста, но и его отправку
search_box.send_keys(Keys.RETURN)
time.sleep(5)
