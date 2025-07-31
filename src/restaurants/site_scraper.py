import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import os

def scrape_restaurant_data(city):
    print("sitescraper : ", city)

    output_file_path = "swiggy/data/restaurants/intermediate/{}/swiggy_{}.html".format(
        city, city
    )
    # s3.head_object(Bucket=bucket, Key=output_file_path)
    if os.path.exists(output_file_path):
        print("File already exists: {}".format(output_file_path))
        return

    url = f"https://www.swiggy.com/city/{city}/order-online"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options, )
    # driver = webdriver.Chrome()
    print(url)
    driver.get(url)

    while True:
        try:
            time.sleep(3)
            show_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Show more')]")
                )
            )
            show_more_button.click()
            time.sleep(2)
        except:
            print("No more 'Show more' button.")
            break

    show_more_button = driver.find_element(
        By.XPATH, '//button[contains(., "Show More")]'
    )
    show_more_button.click()
    for _ in range(10):
        driver.execute_script("window.scrollBy(0, window.innerHeight)")
        time.sleep(2)

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")
    html_page = soup.prettify()
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(html_page)

    # s3.upload_file(output_file_path, bucket, output_file_path)

    driver.quit()

if __name__ == "__main__":
    scrape_restaurant_data()
