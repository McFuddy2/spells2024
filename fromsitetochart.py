import requests
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging for easier debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

spells = []

# Read spell names from spellslist.csv
with open('spellslist.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    spellslist = csv.reader(csvfile)
    
    # Skip header row if there is one
    next(spellslist, None)  # Comment this line if your CSV does not have a header
    
    # Populate the spells list with the first column (spell names)
    for row in spellslist:
        if row:  # Ensure the row is not empty
            spells.append(row[0])


# Function to convert spell name to the URL format
def spell_to_url(spell_name):
    return spell_name.lower().replace(" ", "-").replace("'", "-")

# Function to scrape spell data
def clean_spell_name(spell_name):
    # Replace spaces, slashes, and apostrophes with dashes, and convert to lowercase
    cleaned_name = spell_name.replace(" ", "-").replace("/", "-").replace("’", "-").replace("'", "-").lower()
    return cleaned_name

def get_spell_data(spell_name):
    # Clean the spell name before constructing the URL
    cleaned_name = clean_spell_name(spell_name)
    url = f"http://dnd2024.wikidot.com/spell:{cleaned_name}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        logging.error(f"Failed to retrieve data for {spell_name}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    page_content = soup.find('div', id='page-content')

    if not page_content:
        logging.error(f"Spell details not found for {spell_name}")
        return None
    
    # Initialize the variables with defaults
    source = ""
    level = ""
    school = ""
    classes = []
    casting_time = ""
    range_info = ""
    components = ""
    duration = ""
    description = ""

    # Extract source and details from paragraphs
    paragraphs = page_content.find_all('p')
    
    # Process the first paragraph for source and level information
    if paragraphs:
        first_paragraph = paragraphs[0].get_text(separator='|').strip()
        source_and_level = first_paragraph.split('|')
        
        if len(source_and_level) > 1:
            source = source_and_level[0].replace("Source: ", "").strip()
            level_info = source_and_level[1]
            
            # Extract level, school, and classes from level_info
            level_parts = level_info.split(" (")
            if len(level_parts) > 1:
                level = level_parts[0].strip()
                school_classes = level_parts[1].replace(")", "").split(",")
                classes = [cls.strip() for cls in school_classes]

                if classes:
                    school = classes[0].strip()
                    classes = classes[1:]  # Remaining items are classes
                else:
                    logging.error(f"No classes found in level info for {spell_name}")

        # Extract additional details from other paragraphs
        for p in paragraphs[1:]:
            p_text = p.get_text(separator=' ').strip()
            if "Casting Time:" in p_text:
                casting_time = p_text.split("Casting Time:")[1].strip().split()[0]
            elif "Range:" in p_text:
                range_info = p_text.split("Range:")[1].strip().split()[0]
            elif "Components:" in p_text:
                components = p_text.split("Components:")[1].strip().split()[0]
            elif "Duration:" in p_text:
                duration = p_text.split("Duration:")[1].strip().split()[0]
            else:
                # Assume it's part of the description if it doesn't match above
                description += " " + p_text

    # Prepare class indicators
    classes_info = {
        "Artificer": "X" if "Artificer" in classes else "",
        "Bard": "X" if "Bard" in classes else "",
        "Cleric": "X" if "Cleric" in classes else "",
        "Druid": "X" if "Druid" in classes else "",
        "Paladin": "X" if "Paladin" in classes else "",
        "Ranger": "X" if "Ranger" in classes else "",
        "Sorcerer": "X" if "Sorcerer" in classes else "",
        "Warlock": "X" if "Warlock" in classes else "",
        "Wizard": "X" if "Wizard" in classes else ""      
    }

    return {
        "Spell": spell_name,
        "Description": description.strip(),
        "Level": level,
        "Damage": "",
        "Type": "",  # Always empty
        "Save": "",  # Always empty
        "Range": range_info,
        "Cast Time": casting_time.replace("or Ritual", "") if "Ritual" in casting_time else casting_time,
        "Area": "",  # Not available in this example
        "Duration": duration,
        "Concentration": "Yes" if "Concentration" in duration else "No",
        "Component": components,
        "Ritual": "Yes" if "Ritual" in casting_time else "No",  # Not available in this example
        "School": school,
        "Source": source,
        "Artificer": classes_info["Artificer"],
        "Bard": classes_info["Bard"],
        "Cleric": classes_info["Cleric"],
        "Druid": classes_info["Druid"],
        "Paladin": classes_info["Paladin"],
        "Ranger": classes_info["Ranger"],
        "Sorcerer": classes_info["Sorcerer"],
        "Warlock": classes_info["Warlock"],
        "Wizard": classes_info["Wizard"]
    }


# Function to save data to a CSV file
def save_to_csv(spell_data_list, filename="spells.csv"):
    headers = [
        "Spell", "Description", "Level", "Damage", "Type", "Save", "Range", "Cast Time", 
        "Area", "Duration", "Concentration", "Component", "Ritual", "School", "Source",
        "Artificer", "Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"
    ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for spell_data in spell_data_list:
            writer.writerow(spell_data)

# Main script to fetch all spells and save to CSV
def main():
    spell_data_list = []
    
    for spell in spells:
        data = get_spell_data(spell)
        if data:
            spell_data_list.append(data)
    
    save_to_csv(spell_data_list)

# Run the script
if __name__ == "__main__":
    main()