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
        
        Resname = data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['name']
        
        cuisines = data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['cuisines']
        
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
                        category=info['category']
                        id = info['id']
                        image=info.get("imageId")
                        if image:
                            img_url=f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_208,h_208,c_fit/{image}"
                        else:
                            img_url=None
                            
                        
                        rating = (info["ratings"]["aggregatedRating"].get('rating'))
                        if rating:
                            rating=float(rating)
                        else:
                            rating=None
                        xratingcount = info["ratings"]["aggregatedRating"].get("ratingCount")
                        if xratingcount:
                            if "ratings" in xratingcount:
                                ratingcount = (xratingcount[:xratingcount.index("r")])
                        else:
                            ratingcount=None
                        xdefaultPrice = info.get('defaultPrice')
                        if xdefaultPrice:
                            defaultPrice=xdefaultPrice
                        else:
                            defaultPrice=info['price']

                            
                        Final_list.append([restaurantId,Resname,cuisines,category,id, name, rating, ratingcount, defaultPrice, latitude,longitude,Locality,img_url])
                        
                            

            else:
                chaser = category.get('itemCards', "")
                for card in chaser:
                    data = card.get('card')
                    info = data['info']
                    name = info['name']
                    id = info['id']
                    category=info['category']
                    image=info.get("imageId")
                    if image:
                        img_url=f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_208,h_208,c_fit/{image}"
                    else:
                        img_url=None
                        
                    rating = (info["ratings"]["aggregatedRating"].get('rating',None))
                    if rating:
                            rating=float(rating)
                    else:
                            rating=None
                    xratingcount = info["ratings"]["aggregatedRating"].get("ratingCount",None)
                    if xratingcount:
                        if "ratings" in xratingcount:
                            ratingcount = (xratingcount[:xratingcount.index("r")])
                    else:
                        ratingcount=None
                    xdefaultPrice = info.get('defaultPrice')
                    if xdefaultPrice:
                        defaultPrice=xdefaultPrice
                    else:
                        defaultPrice=info['price']

                    if defaultPrice is not None:
                        Final_list.append([restaurantId,Resname,cuisines,category,id, name, rating, ratingcount, defaultPrice, latitude,longitude,Locality,img_url])
                    else:
                            priceless_jsons.append(json_file)
        print(type(ratingcount))
        # if Final_list:
        #     menu_df = pd.DataFrame(
        #         Final_list,
        #         columns=[
        #             "restaurantId",
        #             "restaurantName",
        #             "cuisines",
        #             "subMenu",
        #             "itemId",
        #             "itemName",
        #             "rating",
        #             "ratingCount",
        #             "price",
        #             "latitude",
        #             "longitude",
        #             "locality",
        #             "imgUrl",
        #         ],
        #     )
            
            
            
        #     output_filename = "swiggy/data/menus/output/newresitem/{}.csv".format(json_file)
        #     output_dir = os.path.dirname(output_filename)
        #     os.makedirs(output_dir, exist_ok=True)
        #     menu_df.to_csv(output_filename,index=False)
        #     print("New file created and saved: {}".format(json_file))
        # else:
        #     print("Skipped {}: No valid data found.".format(json_file))
        
    except Exception as e:
        print("Error processing {}: {}".format(json_file, str(e)))
        # Delete the output file if an error occurs
        if os.path.exists(output_csv_file):
            os.remove(output_csv_file)
            print("Deleted the output CSV file for {}: {}".format(json_file, output_csv_file))
if priceless_jsons:
    priceless_df = pd.DataFrame(priceless_jsons, columns=["Pricelessjsons"])
    # priceless_csv = os.path.join("swiggy/data/menus/output/pricelessjsons.csv")
    priceless_df.to_csv("swiggy/data/menus/output/pricelessjsons.csv", index=False)
    print("Priceless data")