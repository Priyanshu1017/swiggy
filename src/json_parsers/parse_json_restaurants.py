import os
import json
import pandas as pd

city="bangalore"
folder_path =f"swiggy/data/menus/intermidiate/{city}/"
json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]

for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)
    
    output_csv_file = "swiggy/data/menus/output/{}.csv".format(json_file)
    if os.path.exists(output_csv_file):
        print("CSV file already exists for {}: {}".format(json_file, output_csv_file))
        continue
        
    with open(file_path, 'r') as file:
        data = json.load(file)
        try:
            xcards = data["menu"]["pl"]["data"]["data"]["cards"][2]["cards"]
            
            restaurantId = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['id']
        
            Resname = data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['name']
            
            Locality=data["menu"]["pl"]["data"]["data"]["cards"][0]['info']['areaName']
                    
            xlatLong = data["menu"]["pl"]["data"]["data"]["cards"][0]["info"]['latLong']
            latlong=xlatLong.split(",")
            latitude=(latlong[0])
            longitude=(latlong[1])
            
            if xcards:
                cards=xcards
            else:
                print("json_file")
            Final_list=[]
            # Loop through the cards and extract information
            for category in cards:
                chase=category.get('categories',"")
                if chase:
                    chaser=category.get('categories',"")
                    for itemcards in chaser:
                        item=itemcards.get("itemCards")
                        for card in item:
                            data=card.get('card')
                            info=data['info']
                            name=info['name']
                            image=info.get("imageId")
                            if image:
                                img_url=f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_208,h_208,c_fit/{image}"
                            else:
                                img_url=None
                                
                            category=info['category']
                            
                            xdefaultPrice = info.get('defaultPrice')
                            if xdefaultPrice:
                                defaultPrice=xdefaultPrice
                            else:
                                defaultPrice=info['price']

                            description=info.get("description",None)
                            itemid=info['id']
                            ribbon = info["ribbon"].get("text", "Common")
                            vegClassifier = info["itemAttribute"].get("vegClassifier", "Not Available")
                            rating = info["ratings"]["aggregatedRating"].get('rating',None)
                            ratingcount = info["ratings"]["aggregatedRating"].get("ratingCount",None)
                            
                            addons = info.get("addons")
                            variants = info["variantsV2"].get("variantGroups")
                            result_info = []  # To store combined addon and variant information
                            
                            if addons is not None:
                                addon_choices_names = []
                                for addon in addons:
                                    choices = addon.get("choices","")
                                    for choice in choices:
                                        choice_name = choice.get("name", "")
                                        choice_price = choice.get("price", "")
                                        result_info.append([choice_name,choice_price])
                            
                            if variants:
                                for variant_group in variants:
                                    group_name = variant_group.get("name", "No Variant Group Name")
                                    variations = variant_group.get("variations","")
                                    for variation in variations:
                                        choice_name = variation.get("name", "No Variation Name")
                                        choice_price = variation.get("price", "Not Available")
                                        result_info.append([choice_name,choice_price])
                            
                            
                            Final_list.append([restaurantId,Resname,itemid,category,ribbon,vegClassifier,name,rating,ratingcount,defaultPrice,description,result_info,img_url,latitude,longitude,Locality])

                else:
                    chaser=category.get('itemCards',"")
                    for card in chaser:
                            data=card.get('card')
                            info=data['info']
                            name=info['name']
                            category=info['category']
                            
                            xdefaultPrice = info.get('defaultPrice')
                            if xdefaultPrice:
                                defaultPrice=xdefaultPrice
                            else:
                                defaultPrice=info['price']
                            
                            description=info.get("description","N/A")
                            itemid=info['id']
                            
                            if "itemAttribute" in info:
                                vegClassifier = info["itemAttribute"].get("vegClassifier", "Not Available")
                            else:
                                vegClassifier = "Not Available"
                                
                            ribbon = info["ribbon"].get("text", "Regular")
                            rating = info["ratings"]["aggregatedRating"].get('rating',None)
                            ratingcount = info["ratings"]["aggregatedRating"].get("ratingCount",None)

                            image=info.get("imageId",None)
                            if image:
                                img_url=f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_208,h_208,c_fit/{image}"
                            else:
                                img_url="N/A"
                            addons = info.get("addons")
                            variants = info["variantsV2"].get("variantGroups")
                            result_info = []  # To store combined addon and variant information
                            
                            if addons is not None:
                                addon_choices_names = []
                                for addon in addons:
                                    choices = addon.get("choices","")
                                    for choice in choices:
                                        choice_name = choice.get("name", "")
                                        choice_price = choice.get("price", "")
                                        result_info.append([choice_name,choice_price])
                            
                            if variants:
                                for variant_group in variants:
                                    group_name = variant_group.get("name", "No Variant Group Name")
                                    variations = variant_group.get("variations","")
                                    for variation in variations:
                                        choice_name = variation.get("name", "No Variation Name")
                                        choice_price = variation.get("price", "Not Available")
                                        result_info.append([choice_name,choice_price])
                            
                            Final_list.append([restaurantId,Resname,itemid,category,ribbon,vegClassifier,name,rating,ratingcount,defaultPrice,description,result_info,img_url,latitude,longitude,Locality])

                        
                menu_df = pd.DataFrame(
                    Final_list,
                    columns=[
                        "restaurantId",
                        "restaurantName",
                        "itemId",
                        "category",
                        "ribbon",
                        "vegClassifier",
                        "itemName",
                        "rating",
                        "ratingCount",
                        "price",
                        "discription",
                        "variations",
                        "imgUrl",
                        "latitude",
                        "longitude",
                        "locality",
                    ],
                )
            
            
            output_filename="swiggy/data/menus/output/{}/{}.csv".format(city,json_file)
            output_dir = os.path.dirname(output_filename)
            os.makedirs(output_dir, exist_ok=True)
            menu_df.to_csv(output_filename,index=False)
            print("New file created and saved: {}".format(json_file))
        except :
            print(json_file, " not processed")                    
                    