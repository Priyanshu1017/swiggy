import pandas as pd
import json
import urllib
import requests
import os , re


def site_scraper_json(city):
    """_summary_ : Takes city as input and get the required file saved from the previous process using the input city. Using that file gets the json of the restaurant and save it locally.

    Args:
        city (_type_): Takes city which is entered as argument from main.py
    """
    
    
    print("Scraping restaurant JSON files for city '{}'".format(city))
    folder_path = f"swiggy/data/restaurants/output/{city}/Merged_list.csv"
    df = pd.read_csv(folder_path)

    for index, row in df.iterrows():
        link = row["link"]
        links_part = link.split("/")

        pattern = re.compile(r"rest\d+")
        restaurant_name = links_part[-1]
        if "dineout" in restaurant_name:
            restaurant_name=links_part[-2]
            print("Dineout link detected, currently not supported.")

        elif pattern.search(links_part[-1]):
            restaurant_name = links_part[-1]

        restaurant_id = restaurant_name.split("-")[-1].replace("rest", "")

        output_filename = f"swiggy/data/menus/intermediate/{city}/{restaurant_name.replace(' ', '_')}.json"

        if os.path.exists(output_filename):
            if os.path.getsize(output_filename) == 0:
                print("File is empty, deleting: {}".format(output_filename))
                os.remove(output_filename)
                continue
        if os.path.exists(output_filename):
            print("File already exists: {}".format(output_filename))
            continue


        json_url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=12.9715987&lng=77.5945627&restaurantId={restaurant_id}"

        target_url = urllib.parse.quote(json_url)
        url = f"http://api.scrape.do?token=bca9ee10d0894330b715ab903eb80cef8d18a07ec7e&url={target_url}"
        response_json = requests.request("GET", url)

        swiggy_data = response_json.json()
        if swiggy_data.get("statusCode") != 0:
            print("No data found for restaurant: {}".format(restaurant_name))
            continue
        if swiggy_data is not None:
            output_dir = os.path.dirname(output_filename)
            os.makedirs(output_dir, exist_ok=True)
            with open(output_filename, "w", encoding="utf-8") as json_file:
                json.dump(swiggy_data, json_file, indent=4)
            print("New file created and saved: {}".format(output_filename))

        else:
            print("No data found")
            continue


if __name__ == "__main__":
    site_scraper_json()
