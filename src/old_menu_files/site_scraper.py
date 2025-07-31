from selenium import webdriver
import pandas as pd
import json
import time
import os

#NO need to work here
def site_scraper_json(city):
    print("Creating jsons for '{}'".format(city))
    print(1)

    folder_path = f"swiggy/data/restaurants/output/{city}/Merged_list.csv"
    df = pd.read_csv(folder_path)

    files_created = 0

    for index, row in df.iterrows():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options)
        # try:
        link = row["link"]
        links_part = link.split("restaurants/")
        restaurant_name = links_part[1]

        output_filename = f"swiggy/data/menus/intermediate/{city}/{restaurant_name.replace(' ', '_')}.json"

        # Check if the file exists
        if os.path.exists(output_filename):
            if os.path.getsize(output_filename) == 0:
                print("File is empty, deleting: {}".format(output_filename))
                os.remove(output_filename)
                continue

            try:
                with open(output_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if len(data.get("data").get("cards")) < 2:
                        print("File is empty, deleting: {}".format(output_filename))
                        os.remove(output_filename)
                        continue

                print(
                    "File already exists and has valid data: {}".format(output_filename)
                )
                continue

            except json.JSONDecodeError:
                print(
                    "JSON data is null or malformed. Deleting file: {}".format(
                        output_filename
                    )
                )
                os.remove(output_filename)
                continue
        # If we reached this point, either the file doesn't exist or it has null data

        driver.get(link)
        time.sleep(4)

        # Retrieve the initial state JSON data
        initial_state_script = "return window.___INITIAL_STATE__"
        initial_state_json = driver.execute_script(initial_state_script)

        if initial_state_json is not None:
            output_dir = os.path.dirname(output_filename)
            os.makedirs(output_dir, exist_ok=True)
            with open(output_filename, "w") as json_file:
                json.dump(initial_state_json, json_file, indent=4)

            print("New file created and saved: {}".format(output_filename))

            files_created += 1  # Increment the counter
            time.sleep(2)

        else:
            print("JSON data is null. Deleting file: {}".format(output_filename))
            
        driver.quit()
        # except Exception as e:
        #     print("Error processing link {}: {}".format(restaurant_name, str(e)))
        #     pass


if __name__ == "__main__":
    site_scraper_json()
