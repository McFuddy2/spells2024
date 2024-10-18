import csv

def main(file):
    spells = set()  # Use a set to automatically handle duplicates
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Skip empty lines and lines starting with "Spell" or "Level"
        if not line or line.startswith('Spell') or line.startswith('Level'):
            continue
        
        # Handle spell levels (e.g., "Cantrips (Level 0 Bard Spells)", "Level 1 Bard Spells")
        if "Spells" in line:
            continue

        # Split the line by tab characters
        parts = line.split("\t")
        if len(parts) > 0:
            spell_name = parts[0].strip()
            spells.add(spell_name)  # Add spell to set (automatically handles duplicates)

    return sorted(spells)  # Sort the spell names alphabetically

def write_to_csv(spells):
    # Open the CSV file in write mode
    with open('spellslist.csv', 'w', newline='') as csvfile:
        # Define the CSV headers
        fieldnames = ['Spell']
        
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()

        # Write each spell to the CSV
        for spell_name in spells:
            writer.writerow({'Spell': spell_name})

if __name__ == "__main__":
    # Open the spells.md file in read mode
    with open("spells.md", "r") as file:
        spell_data = main(file)
    
    # Write the parsed spell data to a CSV file
    write_to_csv(spell_data)

    print("CSV file 'spellslist.csv' has been created.")
