import os
import json
import pandas as pd


def rest_json_parser(city):
    print("Parsing restaurant JSON files for city '{}'".format(city))
    folder_path = f"swiggy/data/menus/intermediate/{city}/"
    json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]

    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)

        output_csv_file = "swiggy/data/menus/output/{}/{}.csv".format(city, json_file)
        output_csv_file=output_csv_file.replace(".json", "")
        if os.path.exists(output_csv_file):
            print(
                "CSV file already exists for {}: {}".format(json_file, output_csv_file)
            )
            continue

        with open(file_path, "r") as file:
            data = json.load(file)

        if data.get("statusCode") != 0 :
            print(
                f"Deleting file {file_path} due to status code {data.get('statusCode')}"
            )
            os.remove(file_path)
            continue
        
        try:
            card_info = data.get("data")["cards"][2]
        except :
            print(f"file {file_path} does not contain expected card structure.")
            os.remove(file_path)
            continue
        
        
        print(file_path)
        rest_info = parse_rest_info(data)
        final_data = parse_menu_info(data, rest_info)
        save_to_csv(final_data, output_csv_file)
    return "Parsing completed for all files."

def item_card(rest_info,item_cards):
    """_summary_

    Args:
        item_cards (list of menu item cards): _list of dictionaries containing menu item details_

    Returns:
        _type_: list of menu item details
    """
    
    all_items = []

    for item_card in item_cards:
        item_info = item_card.get("card").get("info")
        item_name = item_info.get("name")
        item_id = item_info.get("id")
        item_category = item_info.get("category")
        item_description = item_info.get("description")
        item_image_id = item_info.get("imageId")
        if item_image_id:
            item_image_url = f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_208,h_208,c_fit/{item_image_id}"
        else:
            item_image_url = None
        item_price = item_info.get("price")
        addons = item_info.get("addons")
        try:
            ribbon = item_info.get("ribbon")
        except :
            ribbon = "None"
        try:
            vegClassifier = item_info.get("itemAttribute").get("vegClassifier")
        except:
            vegClassifier = "None"
        all_items.append(
            [   *rest_info,
                item_category,
                item_id,
                item_name,
                item_description,
                item_image_url,
                item_price,
                addons,
                ribbon,
                vegClassifier,
            ]
        )

    return all_items

def parse_rest_info(data): 
 
    card_info = data.get("data")["cards"][2].get("card").get("card").get("info")
    resId= card_info.get('id')
    resName= card_info.get('name')
    city = card_info.get("city")
    slugs = card_info.get("slugs").get("restaurant")
    uniqueId = card_info.get("uniqueId")
    cloudinaryImageId = card_info.get("cloudinaryImageId")
    locality = card_info.get("locality")
    areaName = card_info.get("areaName")
    costForTwo = card_info.get("costForTwo")
    costForTwoMessage = card_info.get("costForTwoMessage")
    cuisines = card_info.get("cuisines")
    resavgRating = card_info.get("avgRating")
    restotalRatingsString = card_info.get("totalRatingsString")
    restotalRatings = card_info.get("totalRatings")
    latLong = card_info.get("latLong")
    return [resId, resName, city, slugs, uniqueId, cloudinaryImageId, locality, areaName, costForTwo, costForTwoMessage, cuisines, resavgRating, restotalRatingsString, restotalRatings, latLong]

def parse_menu_info(data, rest_info):   
    Final_list=[]
    menu_loc = data.get("data")["cards"]
    try:
        menu_info = ( menu_loc[4].get("groupedCard").get("cardGroupMap").get("REGULAR").get("cards"))
        
    except:
        for i in range(2,len(menu_loc)):
            try:
                menu_info = (menu_loc[i].get("groupedCard").get("cardGroupMap").get("REGULAR").get("cards"))
                break
            except:
                continue
    for i in range(1,len(menu_info)-2):
        try:
            menu_items = menu_info[i].get("card").get("card").get("categories")
            for j in range(len(menu_items)):
                item_cards = menu_items[j].get("itemCards")
                item_list = item_card(rest_info,item_cards)
                Final_list.extend(item_list)

        except:
            menu_items = menu_info[i].get("card").get("card").get("itemCards")
            item_list=item_card(rest_info,menu_items)
            Final_list.extend(item_list)

    return Final_list

def save_to_csv(final_data, output_file):
    columns = [
        "resId", "resName", "city", "slugs", "uniqueId", "cloudinaryImageId",
        "locality", "areaName", "costForTwo", "costForTwoMessage", "cuisines",
        "resavgRating", "restotalRatingsString", "restotalRatings", "latLong",
        "item_category", "item_id", "item_name", "item_description",
        "item_image_url", "item_price", "addons", "ribbon", "vegClassifier"
    ]
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df = pd.DataFrame(final_data, columns=columns)
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
    return "Data saved successfully"

if __name__ == "__main__":

    # city = "Jabalpur"
    rest_json_parser()
