from bs4 import BeautifulSoup
import pandas as pd
import os


def local_restaurants(city):
    print("Extracting local restaurants for city '{}'".format(city))

    read_file_path = "swiggy/data/restaurants/intermediate/{}/swiggy_{}.html".format(
        city, city
    )
    with open(read_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    info_container = soup.select('[class*="InfoList__InfoAnchor"]')
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


if __name__ == "__main__":
    local_restaurants()
