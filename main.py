import argparse
# import boto3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from secret_key import SecretKey
from src.restaurants.site_scraper import scrape_restaurant_data
# from src.restaurants.html_to_items import convert_html_to_items
from src.restaurants.parse_items import parse_menu_items
from src.restaurants.local_restaurants import local_restaurants
from src.restaurants.local_html import local_html
# from src.restaurants.local_item import local_item
from src.restaurants.parse_local_items import parse_local_items
from src.restaurants.Merged_local_restaurants import Merged_local_restaurants
# from src.menu.site_scraper import site_scraper_json
from src.menu.site_scraper_requests import site_scraper_json
from src.menu.restaurant_json_parser import rest_json_parser

class Scrape:
    # def __init__(self):
    #     self.aws_access_key_id = SecretKey.AWS_ACCESS_KEY_ID
    #     self.aws_secret_access_key = SecretKey.AWS_SECRET_ACCESS_KEY
    print("Scrape class initialized.")
    def main(self,city):
        # s3 = boto3.client(
        #     "s3",
        #     region_name="ap-south-1",
        #     aws_access_key_id=self.aws_access_key_id,
        #     aws_secret_access_key=self.aws_secret_access_key,
        # )

        bucket = "swiggy-zomato-scraper"
        city = city.capitalize()
        priority_order = [
            "site_scraper1",
            # "html_to_items",
            # "parse_items",
            # "local_restaurants",
            # "local_html",
            # # "local_item",
            # "parse_local_items",
            # "Merged_local_restaurants",
            "site_scraper2",
            "rest_json_parser",
        ]

        for priority in priority_order:
            if priority == "site_scraper1":
                # scrape_restaurant_data(city, s3, bucket)  example for se integration
                scrape_restaurant_data(city)
            # elif priority == "html_to_items":
            #     convert_html_to_items(city)
            elif priority == "parse_items":
                parse_menu_items(city)
            elif priority == "local_restaurants":
                local_restaurants(city)
            elif priority == "local_html":
                local_html(city)
            # elif priority == "local_item":
            #     local_item(city)
            elif priority == "parse_local_items":
                parse_local_items(city)
            elif priority == "Merged_local_restaurants":
                Merged_local_restaurants(city)
            elif priority == "site_scraper2":
                site_scraper_json(city)
            elif priority == "rest_json_parser":
                rest_json_parser(city)

        print("Scraping completed for city: {}".format(city))
        
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restaurant Data Scraper")
    parser.add_argument(
        "city", type=str, help="City for which to scrape restaurant data"
    )
    # parser.add_argument("item_count", type=int, default=10, help="Number of items to process for item_html")
    args = parser.parse_args()
    scraper = Scrape()
    scraper.main(args.city)
