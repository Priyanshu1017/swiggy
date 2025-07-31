import os
import pandas as pd

city="bangalore"
folder_path = output_filename="swiggy/data/menus/output/{}/".format(city)
csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

merged_data = pd.DataFrame()

# Loop through each CSV file and merge its contents
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, df], ignore_index=True)

# Path to the output merged CSV file
output_file_path = "swiggy/data/menus/output/Merged_list.csv"

# Save the merged data to a new CSV file
merged_data.to_csv(output_file_path, index=False)

print(f"Merged CSV saved to {output_file_path}")
        
    