from bs4 import BeautifulSoup
import pandas as pd
import os


def local_item(city):
    print("Extracting local items for city '{}'".format(city))

    # Read CSV directly from S3
    csv_key = "swiggy/data/restaurants/output/{}/swiggy_locality_{}.csv".format(
            city, city
        )
    # csv_object = s3.get_object(Bucket=bucket, Key=csv_key)
    # df = pd.read_csv(pd.io.common.BytesIO(csv_object["Body"].read()))
    df = pd.read_csv(csv_key)

    for index, row in df.iterrows():
        try:
            restaurant_name = row["name"].strip()
            # Construct the S3 key for the locality HTML file
            locality_key = "swiggy/data/restaurants/intermediate/{}/localities/{}/{}_{}.html".format(
                    city,
                    restaurant_name.replace(".", ""),
                    city,
                    restaurant_name.replace(".", ""),
                )

            # html_object = s3.get_object(Bucket=bucket, Key=locality_key)
            # html_content = html_object["Body"].read().decode("utf-8")
            with open(locality_key, "r", encoding="utf-8") as f:
                html_content = f.read()
            # Construct the S3 key for the item HTML file
            output_file_path = "swiggy/data/restaurants/intermediate/{}/localities/{}/{}_item_HTML.html".format(
                    city,
                    restaurant_name.replace(".", ""),
                    restaurant_name.replace(".", ""),
                )

            # try:
            #     s3.head_object(Bucket=bucket, Key=output_file_path)
            #     print("File already exists: {}".format(output_file_path))
            #     continue
            # except:
            #     pass
            if os.path.exists(output_file_path):
                print("File already exists: {}".format(output_file_path))
                continue

            soup = BeautifulSoup(html_content, "html.parser")
            restaurant_split_content = []

            all_restaurants = soup.find_all("div", class_="sc-blmETK jWsRRU")
            for restaurant in all_restaurants:
                html_content = restaurant.prettify()
                restaurant_split_content.append(html_content)

            output_dir = os.path.dirname(output_file_path)
            os.makedirs(output_dir, exist_ok=True)
            with open(output_file_path, "w", encoding="utf-8") as f:
                for item_content in restaurant_split_content:
                    f.write(item_content)

            # s3.upload_file(output_file_path, bucket, output_file_path)
            print(
                    "Output HTML file '{}' created successfully.".format(
                        output_file_path
                    )
                )
        except Exception as e:
            print("Error processing row {}: {}".format(index, str(e)))
            continue


if __name__ == "__main__":

    local_item("Jabalpur")
