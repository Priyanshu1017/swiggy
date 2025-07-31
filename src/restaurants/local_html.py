import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def local_html(city):
    print("Extracting local html for city '{}'".format(city))

    # Read CSV directly from S3
    csv_key = (
        f"swiggy/data/restaurants/output/{city}/swiggy_locality_{city}.csv"
    )
    print(f"swiggy/data/restaurants/output/{city}/swiggy_locality_{city}.csv")
    # csv_object = s3.get_object(Bucket=bucket, Key=csv_key)
    # df = pd.read_csv(pd.io.common.BytesIO(csv_object["Body"].read()))
    df = pd.read_csv(csv_key)

    count_created = 0  # Counter for the number of files created
    for index, row in df.iterrows():
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=chrome_options)
            # driver = webdriver.Chrome()
            # try:
            link = row["Link"]
            restaurant_name = row["name"].strip()
            print("Processing link: {}".format(link))
            output_file_path ="swiggy/data/restaurants/intermediate/{}/localities/{}/{}_{}.html".format(
                    city,
                    restaurant_name.replace(".", ""),
                    city,
                    restaurant_name.replace(".", ""),
                )

            # if s3_object_exists(s3, bucket, output_file_path):
            #     print("File already exists: {}".format(output_file_path))
            #     continue
            if os.path.exists(output_file_path):
                print("File already exists: {}".format(output_file_path))
                count_created += 1  # Increment the counter when a file already exists
                continue

            driver.get(link)

            while True:
                try:
                    time.sleep(2)
                    show_more_button = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(text(), 'Show more')]")
                        )
                    )
                    show_more_button.click()
                    print("scrolling")
                    time.sleep(2)
                except:
                    print("No more 'Show more' button.")
                    break

            time.sleep(2)
            for _ in range(10):
                driver.execute_script("window.scrollBy(0, window.innerHeight)")

            response = driver.page_source
            soup = BeautifulSoup(response, "html.parser")
            html_page = soup.prettify()

            output_dir = os.path.dirname(output_file_path)
            os.makedirs(output_dir, exist_ok=True)
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(html_page)

            # s3.upload_file(output_file_path, bucket, output_file_path)
            print("New File Created: {}".format(output_file_path))
            count_created += 1  # Increment the counter when a new file is created

            driver.quit()
        except Exception as e:
            print("Error processing link {}: {}".format(index, str(e)))
            continue

def s3_object_exists(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    local_html()
