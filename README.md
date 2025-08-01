# swiggy
Swiggy Restaurant & Menu Scraper
This project automates the process of extracting restaurant and menu data from Swiggy for a given city. It supports a step-by-step pipeline that scrapes HTML pages, parses data, downloads menu JSONs, processes them, and compiles all data in CSV format for easy analysis.

# Table of Contents
1. **Features**
2. **Project Structure**
3. **Environment Setup**
4. **Usage Guide**
5. **Pipeline Details :**

    Step 1: Scrape Initial HTML

    Step 2: Parse Restaurant Menus

    Step 3: Parse Localities HTML

    Step 4: Extract Localities Restaurant Links

    Step 5: Parse Locality-wise Restaurant Data

    Step 6: Merge Local Restaurant Data

    Step 7: Scrape Restaurant Menu JSONs

    Step 8: Parse Restaurant JSONs

6. **Output Structure**
7. **Error Handling**
8. **Troubleshooting**
9. **License**

## Features
Automated browser-based scraping (Selenium/BeautifulSoup)

Multiple ETL steps for robust data processing

Easy extension for other cities or endpoints

CSV outputs for convenient data consumption

## Project Structure
```bash
.
├── main.py                           # Entrypoint for orchestrating the pipeline
├── src/
│   └── restaurants/
│       ├── site_scraper.py           # Step 1: Download initial city HTML
│       ├── parse_restaurants.py      # Step 2: Parse HTML for restaurant data
│       ├── localities_html.py        # Step 3: Download localities HTML
│       ├── localities.py             # Step 4: Extract locality restaurant links
│       ├── parse_local_items.py      # Step 5: Parse local restaurant HTMLs
│       └── Merged_local_restaurants.py # Step 6: Merge locality restaurant data
│   └── menu/
│       ├── site_scraper_requests.py  # Step 7: Download restaurant menu JSONs
│       └── restaurant_json_parser.py # Step 8: Parse and compile menu JSONs
├── swiggy/
│   └── data/
│       └── ...                       # Contains all intermediate and final datasets

```
## Environment Setup
You must have Python 3.7+ installed.

Install dependencies:

text
pip install selenium beautifulsoup4 pandas requests
ChromeDriver Setup:

Download chromedriver and place it in your PATH.

Make sure your chrome browser and chromedriver versions are compatible.

Directory Permissions:

Run the script from a location with write permissions, as the pipeline saves data to nested directories.

## Usage Guide
Run the pipeline by specifying a city:

text
```bash
python swiggy/main.py city_name 
     
python main.py <city>
```
Example for Bengaluru:

text
python main.py bengaluru or python swiggy/main.py bengaluru 
The city name is NOT case-sensitive (e.g., bengaluru or Bengaluru).

All intermediate and output files are saved inside the swiggy/data/ folder relative to the project root.

## Pipeline Details
The pipeline is coordinated by the Scrape class in main.py, which executes steps in priority_order.

Step 1: Scrape Initial HTML
File: src/restaurants/site_scraper.py

Scrapes the main Swiggy restaurant listing HTML for the specified city.

Handles "Show more" button to scroll and fully load restaurants.

Output:

swiggy/data/restaurants/intermediate/{city}/swiggy_{city}.html

Skips scraping if the HTML file already exists.

Step 2: Parse Restaurant Menus
File: src/restaurants/parse_restaurants.py

Parses the main HTML for basic restaurant info (name, link, rating, cuisine, etc.) using BeautifulSoup.

Outputs two CSVs for redundancy:

swiggy/data/restaurants/output/{city}/local/swiggy_{city}.csv

swiggy/data/restaurants/output/{city}/swiggy_{city}.csv

Step 3: Extract Localities Restaurant Links
File: src/restaurants/localities.py

Reads the city HTML and extracts a list of localities and links.

Saves:

swiggy/data/restaurants/output/{city}/swiggy_locality_{city}.csv

Step 4: Parse Localities HTML
File: src/restaurants/localities_html.py

Reads the locality links CSV.

For each locality, navigates to the webpage and saves the full HTML (scrolling and "Show more" enabled) for each locality.

Output:

swiggy/data/restaurants/intermediate/{city}/localities/{locality}/{city}_{locality}.html

Skips locality if HTML already exists.

Step 5: Parse Locality-wise Restaurant Data
File: src/restaurants/parse_local_items.py

Parses each locality's HTML for restaurants (name/link/image/cuisine etc.).

Saves output as:

swiggy/data/restaurants/output/{city}/local/{restaurant_name}.csv

Step 6: Merge Local Restaurant Data
File: src/restaurants/Merged_local_restaurants.py

Reads all above locality restaurant CSVs.

Deduplicates by restaurant link.

Saves resulting merged list:

swiggy/data/restaurants/output/{city}/Merged_list.csv

Step 7: Scrape Restaurant Menu JSONs
File: src/menu/site_scraper_requests.py

For every restaurant in the merged list, formulates the Swiggy API url and fetches the menu as JSON.

Uses an API proxy (scrape.do); you must specify your token if you use your own proxy.

Output:

swiggy/data/menus/intermediate/{city}/{restaurant_id}.json

Skips download if JSON already exists, or deletes file if empty.

Step 8: Parse Restaurant Menu JSONs
File: src/menu/restaurant_json_parser.py

Parses all JSON menu files.

For each restaurant, extracts both restaurant and item detail into a tabular (CSV) format.

Output:

swiggy/data/menus/output/{city}/{restaurant_id}.csv

## Output Structure
After a run, you’ll typically get:

text
```bash
swiggy/
├── data/
│   └── restaurants/
│       ├── intermediate/
│       │   └── {city}/
│       │       ├── swiggy_{city}.html
│       │       └── localities/
│       ├── output/
│       │   └── {city}/
│       │       ├── local/
│       │       ├── swiggy_{city}.csv
│       │       ├── swiggy_locality_{city}.csv
│       │       └── Merged_list.csv
│   └── menus/
│       ├── intermediate/
│       │   └── {city}/
│       │       └── *.json
│       └── output/
│           └── {city}/
│               └── *.csv
Each row in the final menu CSV contains restaurant metadata and menu item details.

```
## Error Handling
Most scripts are robust to missing/invalid files; errors are reported, but processing continues.

Files with no content or wrong structure are deleted/skipped.

If a step is already completed (file exists), it is skipped for performance.

## Troubleshooting
Selenium Issues: Make sure you have a compatible Chrome/ChromeDriver.

Encoding Issues: All I/O is done in UTF-8.

Proxy API (scrape.do):

If requests fail, check your API token and internet connectivity.

KeyError/Parsing: If Swiggy changes their HTML/JSON structure, parsing scripts may need updating.

## Credits
Developed for educational / research / data collection purposes only.
Not affiliated with Swiggy.

## Customizing:
You can modify the priority_order in main.py if you want to run only a subset of steps.

For questions or contributions, open an issue or PR.