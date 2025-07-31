import pandas as pd
import json
import urllib
import requests
import os , re


def site_scraper_json(city):
    
    print("Scraping restaurant JSON files for city '{}'".format(city))
    folder_path = f"swiggy/data/restaurants/output/{city}/Merged_list.csv"
    # html_object = s3.get_object(Bucket=bucket, Key=folder_path)
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

        # Check if the file exists
        # s3.head_object(Bucket=bucket, Key=output_filename)
        # try:
        #     json_data = json.loads(
        #         s3.get_object(Bucket=bucket, Key=output_filename)["Body"].read()
        #     )
        # except json.JSONDecodeError:
        #     # JSON data is null or malformed
        #     print(
        #         "JSON data is null or malformed. Deleting file: {}".format(
        #             output_filename
        #         )
        #     )
        #     s3.delete_object(Bucket=bucket, Key=output_filename)
        #     continue

        if os.path.exists(output_filename):
            if os.path.getsize(output_filename) == 0:
                print("File is empty, deleting: {}".format(output_filename))
                os.remove(output_filename)
                continue
        if os.path.exists(output_filename):
            print("File already exists: {}".format(output_filename))
            continue

        # try:
        #     with open(output_filename, "r", encoding="utf-8") as f:
        #         data=json.load(f)
                
        #         try:
        #             if len(data.get("data").get("cards")) <2:
        #                 print("File is empty, deleting: {}".format(output_filename))
        #                 os.remove(output_filename)
        #                 continue
        #         except:
        #             print(data)
                    


        # except :
        #     print("JSON data is null or malformed. Deleting file: {}".format(output_filename))
        #     os.remove(output_filename)
            

        json_url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=12.9715987&lng=77.5945627&restaurantId={restaurant_id}"

        target_url = urllib.parse.quote(json_url)
        url = f"http://api.scrape.do?token=bca9ee10d0894330b715ab903eb80cef8d18a07ec7e&url={target_url}"
        response_json = requests.request("GET", url)

        swiggy_data = response_json.json()
        # if len(swiggy_data.get('data').get("cards")) <2:
        #     continue
        # print(len(swiggy_data.get('data').get("cards")))
        if swiggy_data.get("statusCode") != 0:
            print("No data found for restaurant: {}".format(restaurant_name))
            # print(
            #     f"Deleting file {file_path} due to status code {data.get('statusCode')}"
            # )
            # os.remove(file_path)
            continue
        if swiggy_data is not None:
            output_dir = os.path.dirname(output_filename)
            os.makedirs(output_dir, exist_ok=True)
            with open(output_filename, "w", encoding="utf-8") as json_file:
                json.dump(swiggy_data, json_file, indent=4)

            # s3.upload_file(output_filename, bucket, output_filename)

            print("New file created and saved: {}".format(output_filename))

        else:
            print("No data found")
            continue


if __name__ == "__main__":
    site_scraper_json()
