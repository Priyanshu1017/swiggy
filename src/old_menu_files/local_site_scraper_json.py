from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time
import os

# Initialize the web driver
driver = webdriver.Chrome()

# Load the DataFrame containing links and names
city = "bangalore"

df = pd.read_csv(f"swiggy/data/restaurants/output/{city}/swiggy_locality_{city}.csv")
for index, row in df.iterrows():
    
        restaurant_name = row['name'].strip() 
        df = pd.read_csv(f"swiggy/data/restaurants/output/{city}/local/{restaurant_name}.csv")

        # Loop through the links and names
        for index, row in df.iterrows():
            try:
                link = row['link']
                restaurant_name = row['name'].strip()  # Strip leading and trailing spaces
                
                # Check if the output file already exists
                output_filename = "swiggy/data/menus/intermidiate/{}/Local_restaurant/{}.json".format(city,restaurant_name.replace(" ", "_"))
                
                output_dir = os.path.dirname(output_filename)
                os.makedirs(output_dir, exist_ok=True)
                if os.path.exists(output_filename):
                    print("File already exists: {}".format(output_filename))
                    continue  # Skip to the next iteration
                
                driver.get(link)
                time.sleep(10)  # Wait for the page to load (adjust this as needed)
                
                # Retrieve the initial state JSON data
                initial_state_script = "return window.___INITIAL_STATE__"
                initial_state_json = driver.execute_script(initial_state_script)
                
                with open(output_filename, 'w') as json_file:
                    json.dump(initial_state_json, json_file, indent=4)
                
                print("New file created and saved: {}".format(output_filename))
            
            except Exception as e:
                print("Error processing link {}: {}".format(restaurant_name, str(e)))

        # Close the web driver
        driver.quit()
