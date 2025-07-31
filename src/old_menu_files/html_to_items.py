from bs4 import BeautifulSoup
import pandas as pd
import os


def convert_html_to_items(city):
    print("Converting HTML to items for city '{}'".format(city))
    output_file_path = (
        "swiggy/data/restaurants/intermediate/{}/item_HTML_{}.html".format(city, city)
    )
    # s3.head_object(Bucket=bucket, Key=output_file_path)
    if os.path.exists(output_file_path):
        print("File already exists: {}".format(output_file_path))
        return

    Key = "swiggy/data/restaurants/intermediate/{}/swiggy_{}.html".format(city, city)

    # html_object = s3.get_object(Bucket=bucket,Key=Key) )
    with open(Key, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    # soup=soup.body.prettify()
    # all_restaurants = soup.find_all("div", class_="sc-blmETK jWsRRU")
    all_restaurants = soup.select('[data-testid*="restaurant_list"]')
    
    for restaurant in all_restaurants:
        html_content = restaurant.prettify()

        output_dir = os.path.dirname(output_file_path)
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file_path, "w", encoding="utf-8") as f:
            print(
                "Output HTML file '{}' created successfully.".format(output_file_path)
            )
            f.write(html_content)
        # s3.upload_file(output_file_path, bucket, output_file_path)


if __name__ == "__main__":
    convert_html_to_items("Jabalpur")
