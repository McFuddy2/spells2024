import re
import csv

def main(file):
    spells = {}
    spell_list = ""
    spell_level = None

    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace

        # Skip empty lines
        if not line:
            continue

        # Detect spell list category (e.g., Bard Spells, Cleric Spells, Wizard Spells)
        if "Spells" in line:
            spell_list = line.split()[0]  # Extract class name (e.g., Bard, Cleric, Wizard)
            if spell_list not in spells:
                spells[spell_list] = {}  # Initialize the class key
            continue
        
        # Detect spell level (Cantrips are level 0, then levels 1-9)
        if "Cantrips" in line:
            spell_level = 0
            if spell_list and spell_level is not None:
                if spell_level not in spells[spell_list]:
                    spells[spell_list][spell_level] = []
            continue
        elif "Level" in line:
            match = re.search(r'(\d+)', line)
            if match:
                spell_level = int(match.group(1))  # Get the numeric level (e.g., 1, 2, 3)
                if spell_list and spell_level is not None:
                    if spell_level not in spells[spell_list]:
                        spells[spell_list][spell_level] = []
            continue
        
        # Add the spell to the appropriate spell list and level
        if spell_list and spell_level is not None and line:
            spells[spell_list][spell_level].append(line)

    return spells

def write_to_csv(spells):
    # Open the CSV file in write mode
    with open('spells.csv', 'w', newline='') as csvfile:
        # Define CSV headers
        fieldnames = ['Spell', 'Description', 'Level', 'Damage', 'Type', 'Save', 'Range', 
                      'Cast Time', 'Area', 'Duration', 'Concentration', 'Component', 
                      'Ritual', 'School', 'Source', 'Artificer', 'Bard', 'Cleric', 
                      'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']
        
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        # Create a set to hold unique spell names
        unique_spells = {}

        # Loop through each class and level in the spells data
        for spell_class, levels in spells.items():
            for level, spell_names in levels.items():
                for spell_name in spell_names:
                    if spell_name not in unique_spells:
                        # Initialize a dictionary for each spell with empty fields for all attributes
                        unique_spells[spell_name] = {
                            'Spell': spell_name,
                            'Description': '',
                            'Level': level,
                            'Damage': '',
                            'Type': '',
                            'Save': '',
                            'Range': '',
                            'Cast Time': '',
                            'Area': '',
                            'Duration': '',
                            'Concentration': '',
                            'Component': '',
                            'Ritual': '',
                            'School': '',
                            'Source': '',
                            'Artificer': '',
                            'Bard': '',
                            'Cleric': '',
                            'Druid': '',
                            'Paladin': '',
                            'Ranger': '',
                            'Sorcerer': '',
                            'Warlock': '',
                            'Wizard': ''
                        }

                    # Mark the corresponding class with "X"
                    unique_spells[spell_name][spell_class] = 'X'

        # Sort spells alphabetically by name
        sorted_spells = sorted(unique_spells.values(), key=lambda x: x['Spell'])

        # Write each unique spell to the CSV
        for spell_data in sorted_spells:
            writer.writerow(spell_data)

if __name__ == "__main__":
    # Open the spells.md file in read mode
    with open("spells.md", "r") as file:
        spell_data = main(file)
    
    # Write the parsed spell data to a CSV file
    write_to_csv(spell_data)

    print("CSV file 'spells.csv' has been created.")
