import os
import json
import pandas as pd

city = "bangalore"
folder_path = f"swiggy/data/menus/intermidiate/{city}/"
json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]

for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)

    output_csv_file = "swiggy/data/menus/output/{}.csv".format(json_file)
    if os.path.exists(output_csv_file):
        print("CSV file already exists for {}: {}".format(json_file, output_csv_file))
        continue
    priceless_jsons=[]
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        xcards = data["menu"]["pl"]["data"]["data"]["cards"][2]["cards"]
        
        # avg = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['avgRatingString']
        
        restaurantId = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['id']
        
        totalratings = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['totalRatings']
        
        Resname = data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['name']
        
        Locality=data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['areaName']
                
        xlatLong = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['latLong']
        latlong=xlatLong.split(",")
        latitude=(latlong[0])
        longitude=(latlong[1])
        

        if xcards:
            cards = xcards
        else:
            print(json_file)
        Final_list = []

        for category in cards:
            chase = category.get('categories', "")
            if chase:
                chaser = category.get('categories', "")

                for itemcards in chaser:
                    item = itemcards.get("itemCards")
                    for card in item:
                        data = card.get('card')
                        info = data['info']
                        name = info['name']
                        id = info['id']
                        rating = info["ratings"]["aggregatedRating"].get('rating',None)
                        ratingcount = info["ratings"]["aggregatedRating"].get("ratingCount",None)
                        xdefaultPrice = info.get('defaultPrice')
                        if xdefaultPrice:
                            defaultPrice=xdefaultPrice
                        else:
                            defaultPrice=info['price']

                            
                        Final_list.append([Resname, name,totalratings,defaultPrice,Locality])
                        
                            

            else:
                chaser = category.get('itemCards', "")
                for card in chaser:
                    data = card.get('card')
                    info = data['info']
                    name = info['name']
                    id = info['id']
                    rating = info["ratings"]["aggregatedRating"].get('rating',None)
                    ratingcount = info["ratings"]["aggregatedRating"].get("ratingCount",None)
                    xdefaultPrice = info.get('defaultPrice')
                    if xdefaultPrice:
                        defaultPrice=xdefaultPrice
                    else:
                        defaultPrice=info['price']

                    if defaultPrice is not None:
                        Final_list.append([Resname, name,totalratings,defaultPrice,Locality])
                    else:
                            priceless_jsons.append(json_file)
        
        if Final_list:
            menu_df = pd.DataFrame(
                Final_list,
                columns=[
                    "restaurantName",
                    "itemName",
                    "rating",
                    "price",
                    "locality",
                ],
            )
            
            
            
            output_filename = "swiggy/data/menus/output/topres/{}.csv".format(json_file)
            output_dir = os.path.dirname(output_filename)
            os.makedirs(output_dir, exist_ok=True)
            menu_df.to_csv(output_filename,index=False)
            print("New file created and saved: {}".format(json_file))
        else:
            print("Skipped {}: No valid data found.".format(json_file))
        
    except Exception as e:
        print("Error processing {}: {}".format(json_file, str(e)))
        # Delete the output file if an error occurs
        if os.path.exists(output_csv_file):
            os.remove(output_csv_file)
            print("Deleted the output CSV file for {}: {}".format(json_file, output_csv_file))
