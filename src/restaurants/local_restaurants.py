from bs4 import BeautifulSoup
import pandas as pd
import os


def local_restaurants(city):
    print("Extracting local restaurants for city '{}'".format(city))

    read_file_path = "swiggy/data/restaurants/intermediate/{}/swiggy_{}.html".format(
        city, city
    )
    # html_object = s3.get_object(Bucket=bucket, Key=read_file_path)
    # html_content = html_object["Body"].read().decode("utf-8")
    with open(read_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # info_container = soup.find("div", class_="InfoList__InfoContainer-sc-s3b9ls-0")
    info_container = soup.select('[class*="InfoList__InfoAnchor"]')
    # print("Info container found:", info_container)
    # Extract link and name information
    links_and_names = []
    for info in info_container:
        link=info.__getitem__("href")
        name = info.get_text(strip=True)
        links_and_names.append([name, link])

    # Print the extracted information
    local = pd.DataFrame(links_and_names, columns=["name", "Link"])

    output_file_path = (
        f"swiggy/data/restaurants/output/{city}/swiggy_locality_{city}.csv"
    )
    output_dir = os.path.dirname(output_file_path)

    os.makedirs(output_dir, exist_ok=True)
    local.to_csv(output_file_path, index=False)
    # s3.upload_file(output_file_path, bucket, output_file_path)


if __name__ == "__main__":
    local_restaurants()
