import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException

# Настройка драйвера
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
url = "https://www.divan.ru/category/potolocnye-svetilniki"
driver.get(url)

# Ожидание загрузки элементов
try:
    # Увеличиваем время ожидания до 20 секунд
    svets = WebDriverWait(driver, 240).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.WdR1o'))
    )
except TimeoutException:
    print("Ошибка: Время ожидания истекло при загрузке элементов.")
    driver.quit()
    exit()
except WebDriverException as e:
    print(f"Ошибка WebDriver: {e}")
    driver.quit()
    exit()
except Exception as e:
    print(f"Ошибка при ожидании загрузки элементов: {e}")
    driver.quit()
    exit()

parsed_data = []

for svet in svets:
    try:
        # Правильные селекторы
        name_element = svet.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8.qUioe')  # Селектор для названия
        name = name_element.text
        link = name_element.get_attribute('href')  # Получаем ссылку на светильник
        price = svet.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU.KIkOH').text  # Селектор для цены

        # Добавление данных в список
        parsed_data.append([name, link, price])

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Закрытие драйвера
driver.quit()

# Сохранение данных в CSV файл
with open("divan_data.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Светильник', 'Ссылка', 'Стоимость'])
    writer.writerows(parsed_data)

print("Данные успешно сохранены в divan_data.csv")




