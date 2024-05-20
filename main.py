import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

chrome_options = Options()
chrome_options.add_argument(f'user_agent={user_agent}')


driver = webdriver.Chrome(options=chrome_options)

try:

    driver.get("https://books.toscrape.com")
    pause_time = 2
    poetry_23 = driver.find_element(By.XPATH, '//ul/li/ul/li[1]/a')
    time.sleep(pause_time)

    poetry_23.click()
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(pause_time)

    poetry_23 = driver.find_element(By.XPATH, '//div[@class="col-sm-8 h1"]/a')
    poetry_23.click()
    time.sleep(pause_time)

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    driver.quit()


# parse
url = 'https://books.toscrape.com/catalogue/category/books/poetry_23'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

try:
    books_data = []

    for book in soup.find_all('h3'):
        title = book.a['title']
        book_url = book.a['href']
        full_book_url = f'https://books.toscrape.com/catalogue{book_url}'
        price = book.find_next('p', class_='price_color').text.strip()[2:]

        book_data = {
            'Title': title,
            'URL': full_book_url,
            'Price': price
        }

        books_data.append(book_data)

    output_file = 'poetry23.json'
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(books_data, json_file, ensure_ascii=False, indent=2)

    print(f'Готов файл {output_file}')

except Exception as e:
    print("Ошибочка!")
