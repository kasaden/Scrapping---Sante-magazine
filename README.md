# SCRAPPING - SANTÉ MAGAZINE

## Description

This repository contains a Python script designed to scrape nutritional data for a variety of foods from Santé Magazine. The goal of this project is to create a database of nutritional values that can be used for another ongoing project. This script fetches data from multiple pages, processes it into a structured format, and saves it as both JSON and CSV files.

---

## Features

- **Category Scraping**: Fetches all food categories and their respective links from the main page.
- **Nutritional Data Retrieval**: Extracts detailed nutritional values for each food item in the categories.
- **Progress Feedback**: Displays progress in the console during scraping operations.
- **Data Export**:
  - **JSON**: Structured data for easy programmatic access.
  - **CSV**: Tabular format for data analysis.

---

## Workflow Overview

1. **`main()`**  
   Orchestrates the entire process:
   - Fetches food categories using `get_all_types_aliments`.
   - Scrapes food item details for each category with `get_all_links`.
   - Saves the data in JSON and CSV formats.

2. **Key Functions**:
   - **`get_all_types_aliments(main_url)`**  
     Retrieves food categories from the main page. Returns a list of dictionaries containing:
     - `category`: The category name.
     - `link`: The link to the category's page.
   - **`get_all_links(data)`**  
     Iterates through all categories to fetch food items and their nutritional values using:
       - **`get_valeurs_nutritionnelles(aliment_url)`**  
         Scrapes nutritional data from a food item's page. Normalizes and processes data into a dictionary.
   - **`save_to_json(aliments_dict, filename)`**  
     Saves the collected data to a JSON file.
   - **`save_to_csv(aliments_dict, filename)`**  
     Exports the data to a CSV file with predefined headers.

---

## How It Works

1. **Scrape Categories**  
   The `get_all_types_aliments()` function retrieves all food categories and their respective URLs from the main page.

2. **Extract Food Item Data**  
   - For each category, `get_all_links()` fetches all food items and their links.  
   - For each food item, `get_valeurs_nutritionnelles()` retrieves nutritional information, such as protein, lipids, and vitamins.

3. **Save the Results**  
   - Data is saved in both JSON and CSV formats with timestamped filenames (e.g., `Data_23-11-15-12-30.json`).

---

## Usage

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run the script**
   ```bash
   python main.py
4. **Check output files**
  - JSON and CSV files are saved in the project directory.

---

## CSV Output Headers
The CSV file includes the following columns:
- Types d'aliments: Food category.
- aliment: Food item name.
- link: URL of the food item.
- Nutritional values (e.g., Protéines, Glucides, Lipides, Vitamines, Calcium, etc.).

---

## Dependencies
- `requests`: For HTTP requests.
- `BeautifulSoup4`: HTML parsing.
- `unidecode`: Text normalization.
- `csv`, `json`: For data export.
Install dependencies with:
   ```bash
   pip install requests beautifulsoup4 unidecode
---

## Improvements in this Version
- Streamlined Functions: Simplified workflow with fewer redundant operations.
- Enhanced Output: CSV and JSON files now include all essential nutritional data.
- Progress Tracking: Detailed progress tracking for categories and food items.

---

## Future Enhancements
- Add retry logic for failed HTTP requests.
- Implement multithreading for faster scraping.
- Support additional output formats (e.g., SQL database, Excel).
