from bs4 import BeautifulSoup
import pandas as pd
import os , re

def parse_local_items(city):
    print("Parsing local items for city '{}'".format(city))

    csv_key = "swiggy/data/restaurants/output/{}/swiggy_locality_{}.csv".format(
        city, city
    )
    # csv_object = s3.get_object(Bucket=bucket, Key=csv_key)
    # df = pd.read_csv(pd.io.common.BytesIO(csv_object["Body"].read()))
    df=pd.read_csv(csv_key)
    for index, row in df.iterrows():
        try:
            restaurant_name = row["name"].strip()

            # key = "swiggy/data/restaurants/intermediate/{}/localities/{}/{}_item_HTML.html".format(
            #     city,
            #     restaurant_name.replace(".", ""),
            #     restaurant_name.replace(".", ""),
            # )
            # above path work with the local_item.py file
            
            
            key = "swiggy/data/restaurants/intermediate/{}/localities/{}/{}_{}.html".format(
                city,
                restaurant_name.replace(".", ""),
                city,
                restaurant_name.replace(".", ""),
            )
            # html_object = s3.get_object(Bucket=bucket, Key=output_filename)
            with open(key, "r", encoding="utf-8") as f:
                html_content = f.read()
            output_file_path = (
                "swiggy/data/restaurants/output/{}/local/{}.csv".format(
                    city, restaurant_name
                )
            )

            soup = BeautifulSoup(html_content, "html.parser")

            # Find restaurant elements
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

            output_dir = os.path.dirname(output_file_path)

            os.makedirs(output_dir, exist_ok=True)
            df.to_csv(output_file_path, index=False)
            # s3.upload_file(output_file_path, bucket, output_file_path)
            print("Data extracted and saved to", output_file_path)
        except Exception as e:
            print("Error processing row {}: {}".format(index, str(e)))
            continue


if __name__ == "__main__":
    parse_local_items()
