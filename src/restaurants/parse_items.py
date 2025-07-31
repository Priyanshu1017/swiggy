from bs4 import BeautifulSoup
import pandas as pd
import os , re

# Load the local HTML content using BeautifulSoup
def parse_menu_items(city):
    print("Parsing menu items for city '{}'".format(city))

    # html_file_path = "swiggy/data/restaurants/intermediate/{}/item_HTML_{}.html".format(
    #     city, city
    # )
    # Above path work with the html_to_items.py file
    
    html_file_path = "swiggy/data/restaurants/intermediate/{}/swiggy_{}.html".format(city, city)
    # html_object = s3.get_object(Bucket=bucket, Key=html_file_path)
    # html_content = html_object['Body'].read().decode('utf-8')
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    rest_elements = soup.select('[class*="RestaurantList__RestaurantAnchor"]')
    data = []
    for element in rest_elements:
        link = element["href"] 
        img_tags = element.select("img")
        img_url = img_tags[0]["src"] if img_tags else "N/A"
        res_info = element.select_one("div").text.split("      ")
        res = [item.strip() for item in res_info if item.strip()]

        if len(res) < 3:
            print("Insufficient data in row:", res)
            continue
        pattern = re.compile(r"^\d+(\.\d+)?[^a-zA-Z]*$")

        matches = [item for item in res if pattern.match(item)]
        if len(matches) > 0:
            rating = matches[0]
            ni=res.index(rating)
            name = res[ni-1]

        else:
            rating = "N/A"
            name = res[-4]
        if "•" in rating:
            rating = rating.split("•")[0].strip()

        discount = res[0]
        if discount == name:
            discount = "N/A"
        location = res[-1]
        cuisine = res[-2]
        duration = res[-3]
        # print("Name:", name, "Rating:", rating, "Discount:", discount," Cuisine:", cuisine, "Location:", location, "Duration:", duration)

        restaurant_data = {
            "link": link,
            "img_url": img_url,
            "name": name,
            "rating": rating,
            "discount": discount,
            "cuisine": cuisine,
            "location": location,
            "duration": duration
        }

        data.append(restaurant_data)

    df = pd.DataFrame(data)
    output_file_path = f"swiggy/data/restaurants/output/{city}/local/swiggy_{city}.csv"
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file_path, index=False)
    output_file_path = f"swiggy/data/restaurants/output/{city}/swiggy_{city}.csv"
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_file_path, index=False)
    # s3.upload_file(output_file_path, bucket, output_file_path)
    print("Data extracted and saved to", output_file_path)


if __name__ == "__main__":
    # city="mumbai"
    # s3 = boto3.client(
    #         "s3",
    #         region_name="ap-south-1",
    #         aws_access_key_id="AKIATWAW

    # bucket = "swiggy-zomato-scraper"
    # city = city.capitalize()
    # parse_menu_items(city, s3, bucket)
    parse_menu_items()
