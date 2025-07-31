import os
import pandas as pd


def Merged_local_restaurants(city):
    print("Merging local restaurants for city '{}'".format(city))
    folder_path = f"swiggy/data/restaurants/output/{city}/local/"

    try:
        # csv_files = [
        #     obj["Key"]
        #     for obj in s3.list_objects_v2(Bucket=bucket, Prefix=f"{folder_path}")[
        #         "Contents"
        #     ]
        #     if obj["Key"].endswith(".csv")
        # ]

        csv_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith(".csv")
        ]

        merged_data = pd.DataFrame()
        for csv_file in csv_files:
            try:
                # Read CSV directly from S3
                # csv_object = s3.get_object(Bucket=bucket, Key=csv_file)
                # df = pd.read_csv(pd.io.common.BytesIO(csv_object["Body"].read()))
                df = pd.read_csv(csv_file)
                merged_data = pd.concat([merged_data, df], ignore_index=True)

            except Exception as e:
                print("Error reading CSV file {}: {}".format(csv_file, str(e)))
                continue

        # Debugging: Print duplicates based on "link" column
        duplicates = merged_data[merged_data.duplicated(subset=["link"], keep=False)]
        print("Duplicates based on link column:")
        print(duplicates)

        # Remove duplicate rows based on "link" column
        merged_data.drop_duplicates(subset=["link"], inplace=True)

        # After removing duplicates, reset the index
        merged_data.reset_index(drop=True, inplace=True)

        # Path to the output merged CSV file
        output_file_path = f"swiggy/data/restaurants/output/{city}/Merged_list.csv"
        # Save the merged and de-duplicated data to a new CSV file
        merged_data.to_csv(output_file_path, index=False)
        # s3.upload_file(output_file_path, bucket, output_file_path)

        print(f"Merged and de-duplicated CSV saved to {output_file_path}")

    except Exception as e:
        print("Error merging local restaurants: {}".format(str(e)))


if __name__ == "__main__":
    city="Jabalpur"
    # s3 = boto3.client(
    #         "s3",
    #         region_name="ap-south-1",
    #         aws_access_key_id="AKIATWA3UBH1rNVNiCq",
    #     )

    # bucket = "swiggy-zomato-scraper"
    city = city.capitalize()
    Merged_local_restaurants()
