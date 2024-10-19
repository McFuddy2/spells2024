import requests
from bs4 import BeautifulSoup
import csv
import logging
import re

# Set up logging for easier debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

spells = []

# Read spell names from spellslist.csv
with open('spellslist.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    spellslist = csv.reader(csvfile)
    
    # Skip header row if there is one
    next(spellslist, None)  # Leave this line if your CSV has a header
    
    # Populate the spells list with the first column (spell names)
    for row in spellslist:
        if row and row[0]:  # Ensure the row and the first column are not empty
            spells.append(row[0].strip())  # Strip any surrounding whitespace


def clean_segment(segment):
    # Remove single quotes from within parentheses
 
    open = False
    x = 0
    seg_to_merge = []
    for line in segment:
        if '(' in line:
            open = True
        if open:
            seg_to_merge.append(x)
        if ")" in line:
            open = False
        x += 1
    new_seg = [segment[0]]
    if 1 in seg_to_merge:
        if 2 in seg_to_merge:
            new_seg.append(segment[1]+", " + segment[2])
        else:
            return segment
        if 3 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[3]
        else:
            new_seg.append(segment[3:])
            return new_seg
        if 4 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[4]
        else:
            new_seg.append(segment[4:])
            return new_seg
        if 5 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[5]
        else:
            new_seg.append(segment[5:])
            return new_seg
        if 6 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[6]
        else:
            new_seg.append(segment[6:])
            return new_seg
        if 7 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[7]
        else:
            new_seg.append(segment[7:])
            return new_seg
        if 8 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[8]
        else:
            new_seg.append(segment[8:])
            return new_seg
        if 9 in seg_to_merge:
            new_seg[1] = new_seg[1]+", " + segment[9]
        else:
            new_seg.append(segment[9:])
            return new_seg

    return new_seg

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

    # FOR TESTING!
    # if spell_name == "Aid" or spell_name == "Acid Splash":
    print("Spell", spell_name)


    if not page_content:
        logging.error(f"Spell details not found for {spell_name}")
        return None
    
    # Initialize the variables with defaults
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
            level_info = source_and_level[2]

            
            # Extract level, school, and classes from level_info
            level_part_and_class = level_info.split(" (")
      
            if len(level_part_and_class) > 1:
                level_parts = level_part_and_class[0].split(" ")
                if "Cantrip" in level_parts:
                    level = 0
                    school = level_parts[0]

                else:
                    level = level_parts[1].strip()
                    school = level_parts[2]

                classes = (level_part_and_class[1].replace(")", ""))

        else:
            new_paragraphs = []

            for p in paragraphs:
                cleaned_text = str(p).replace("<p>", "").replace("</p>", "").replace("<em>", "").replace("</em>", "").replace("<br/>", "").replace("<strong>", "").replace("</strong>", "")
                new_paragraphs.append(cleaned_text)

            # Join the list into a single string with commas separating the elements
            new_paragraphs = ",".join(new_paragraphs)
            new_paragraphs = [p2.strip() for p2 in new_paragraphs.replace("\n", ",").split(",")]

            
            level_part_and_class = clean_segment(new_paragraphs)[1].split(" (")

            if len(level_part_and_class) > 1:
                level_parts = level_part_and_class[0].split(" ")
                if "Cantrip" in level_parts:
                    level = 0
                    school = level_parts[0]

                else:
                    level = level_parts[1].strip()
                    school = level_parts[2]

                classes = (level_part_and_class[1].replace(")", ""))
            

        
        # Extract additional details from other paragraphs
        for p in paragraphs:
 
            p_text = p.get_text(separator=' ').strip()

            # Check for multiple attributes in a single paragraph using regex
            casting_time_match = re.search(r"Casting Time:\s*([^\n]+)", p_text)
            range_match = re.search(r"Range:\s*([^\n]+)", p_text)
            components_match = re.search(r"Components:\s*([^\n]+)", p_text)
            duration_match = re.search(r"Duration:\s*([^\n]+)", p_text)

            if casting_time_match:
                casting_time = casting_time_match.group(1).strip()
            if range_match:
                range_info = range_match.group(1).strip()
            if components_match:
                components = components_match.group(1).strip()
            if duration_match:
                duration = duration_match.group(1).strip()
            
            # If no matches are found, treat it as part of the description
            if not (casting_time_match or range_match or components_match or duration_match):
                description += " " + p_text
                description = description.replace("Source: Player's Handbook ", "")

    else:
        print(spell_name, "ERROR NO PARAGRAPH")

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
        "Damage": "", # Always empty
        "Type": "",  # Always empty
        "Save": "",  # Always empty
        "Range": range_info,
        "Cast Time": casting_time.replace("or Ritual", "") if "Ritual" in casting_time else casting_time,
        "Area": "",  # Always empty
        "Duration": duration.replace("Concentration, ", "") if "Concentration, " in duration else duration,
        "Concentration": "Yes" if "Concentration" in duration else "No",
        "Component": components,
        "Ritual": "Yes" if "Ritual" in casting_time else "No",  
        "School": school,
        "Source": "PHB24",
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