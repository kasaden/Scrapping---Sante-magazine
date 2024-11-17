import csv
import json
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from datetime import datetime

# Main function to orchestrate the data retrieval and saving
def main():
    main_url = 'https://www.santemagazine.fr/alimentation/nutriments/guide-des-calories/'
    data = get_all_food_types(main_url)
    if data:
        food_dict = get_all_links(data)
        current_time = datetime.now().strftime("%y-%m-%d-%H-%M")
        json_filename = f"Data_{current_time}.json"
        csv_filename = f"Data_{current_time}.csv"
        save_to_json(food_dict, json_filename)
        save_to_csv(food_dict, csv_filename)
    else:    
        print("No data to save")

# Get all types of aliments from the main URL
def get_all_food_types(main_url):
    response = requests.get(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('a', href=lambda href: href and '/alimentation/nutriments/guide-des-calories/' in href)
        data = []
        for item in items:
            types = unidecode(item.get_text(strip=True)).replace(" ", "-").lower().replace(",", ".")
            link_type = 'https://www.santemagazine.fr' + item['href']
            data.append({'category': types, 'link': link_type})
        return data
    else:
        print("Failed to retrieve the main page")
        return []

# Get nutritional values for a specific aliment
def get_nutritional_values(food_url):
    response = requests.get(food_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_list = soup.find_all('ul', class_='lg:mb-6 mb-4 ciqual-widget')
        nutritional_values = {}
        for ul in ul_list:
            for li in ul.find_all('li'):
                p_tags = li.find_all('p')
                if len(p_tags) >= 2:
                    nutrient = p_tags[0].get_text(strip=True).replace(",", ".")
                    value = p_tags[1].get_text(strip=True).replace(",", ".")

                    if value == "-":
                        nutritional_values[nutrient] = None
                    else:
                        match = re.search(r'(\d+(\.\d+)?)(\s*µg|\s*mg|\s*g)?', value)
                        if match:
                            numeric_value = float(match.group(1))
                            unit = match.group(3) 

                            if unit and "µg" in unit:
                                nutritional_values[nutrient] = numeric_value * 1  
                            elif unit and "mg" in unit:
                                nutritional_values[nutrient] = numeric_value * 1_000    
                            elif unit and "g" in unit:
                                nutritional_values[nutrient] = numeric_value * 1_000_000  
                            else:
                                nutritional_values[nutrient] = numeric_value  
                        else:
                            nutritional_values[nutrient] = None  

        return nutritional_values
    else:
        print(f"Failed to retrieve the page for {food_url}")

# Get all links for each type of aliment
def get_all_links(data):
    food_dict = {}
    total_categories = len(data)  # Nombre total de catégories
    for index, entry in enumerate(data, start=1):
        response = requests.get(entry['link'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            food_list = soup.find_all(
                'a',
                class_='paragraph-primary text-black hover:text-primary-main t-decoration-n',
                href=lambda href: href and f'/alimentation/nutriments/guide-des-calories/{entry["category"]}/' in href
            )
            food_dict[entry['category']] = []
            count = 0  # Nombre d'aliments traités
            total_foods = len(food_list)

            print(f"{index}/{total_categories} START: {entry['category']} ({total_foods} foods)")
            
            # Process each food item
            for i, food in enumerate(food_list, start=1):
                food_name = food.get_text(strip=True)
                food_link = 'https://www.santemagazine.fr' + food['href']
                nutritional_values = get_nutritional_values(food_link)
                food_dict[entry['category']].append({
                    'aliment': food_name,
                    'link': food_link,
                    'nutritional_values': nutritional_values
                })
                count += 1
                
                # Update progress bar
                print_progress_bar(i, total_foods, length=40)

            print(f"{index}/{total_categories} DONE: {entry['category']} with {count} foods")
        else:
            print(f"{index}/{total_categories} FAILED: {entry['category']} failed!")
    return food_dict

# Function to print a progress bar
def print_progress_bar(iteration, total, length=50):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r[{bar}] {percent}%', end='\r')
    if iteration == total:
        print()

# Save the data to a JSON file
def save_to_json(food_dict, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(food_dict, jsonfile, ensure_ascii=False, indent=4)

# Save the data to a CSV file
def save_to_csv(food_dict, filename):
    headers = [
        "Types d'aliments", "aliment", "link", "Quantité", "Eau", "Protéines", 
        "Alcool", "Glucides", "Lipides", "Vitamine A(rétinol)", "Bêta-carotène(provitamine A)", 
        "Vitamine D(cholécalciférol)", "Vitamine E(tocophérol)", "Vitamine K1", "Vitamine K2", 
        "Vitamine C", "Vitamine B1(thiamine)", "Vitamine B2(riboflavine)", "Vitamine B3(niacine)", 
        "Vitamine B5(acide panthonéique)", "Vitamine B6", "Vitamine B9(acide folique)", 
        "Vitamine B12(cobolamine)", "Calcium", "Cuivre"
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)

        for category, aliments in food_dict.items():
            for aliment in aliments:
                row = [
                    category,
                    aliment.get("aliment", ""),
                    aliment.get("link", ""),
                    aliment["nutritional_values"].get("Quantité", 0) if "Quantité" in aliment["nutritional_values"] else aliment["nutritional_values"].get("Nutriments", 0),
                    aliment["nutritional_values"].get("Eau", 0),
                    aliment["nutritional_values"].get("Protéines", 0),
                    aliment["nutritional_values"].get("Alcool", 0),
                    aliment["nutritional_values"].get("Glucides", 0),
                    aliment["nutritional_values"].get("Lipides", 0),
                    aliment["nutritional_values"].get("Vitamine A(rétinol)", 0),
                    aliment["nutritional_values"].get("Bêta-carotène(provitamine A)", 0),
                    aliment["nutritional_values"].get("Vitamine D(cholécalciférol)", 0),
                    aliment["nutritional_values"].get("Vitamine E(tocophérol)", 0),
                    aliment["nutritional_values"].get("Vitamine K1", 0),
                    aliment["nutritional_values"].get("Vitamine K2", 0),
                    aliment["nutritional_values"].get("Vitamine C", 0),
                    aliment["nutritional_values"].get("Vitamine B1(thiamine)", 0),
                    aliment["nutritional_values"].get("Vitamine B2(riboflavine)", 0),
                    aliment["nutritional_values"].get("Vitamine B3(niacine)", 0),
                    aliment["nutritional_values"].get("Vitamine B5(acide panthonéique)", 0),
                    aliment["nutritional_values"].get("Vitamine B6", 0),
                    aliment["nutritional_values"].get("Vitamine B9(acide folique)", 0),
                    aliment["nutritional_values"].get("Vitamine B12(cobolamine)", 0),
                    aliment["nutritional_values"].get("Calcium", 0),
                    aliment["nutritional_values"].get("Cuivre", 0)
                ]
                csv_writer.writerow(row)

if __name__ == "__main__":
    main()