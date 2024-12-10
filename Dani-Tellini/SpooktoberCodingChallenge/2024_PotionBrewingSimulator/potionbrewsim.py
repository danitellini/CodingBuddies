import json
import time
from datetime import datetime

# - Ingredients Dictionary -
ingredients = {
    "Bat Wing": {"effect": "Invisibility", "power_level": 2, "negates": ["Night Vision"]},
    "Spider Venom": {"effect": "Poison", "power_level": 3, "negates": ["Healing"]},
    "Dragon Scale": {"effect": "Fire Resistance", "power_level": 5, "negates": ["Strength Enhancement"]},
    "Mandrake Root": {"effect": "Healing", "power_level": 4, "negates": ["Poison"]},
    "Phoenix Feather": {"effect": "Revitalization", "power_level": 5, "negates": ["Paralysis"]},
    "Witch's Hair": {"effect": "Transformation", "power_level": 3, "negates": ["Protection"]},
    "Troll Slime": {"effect": "Strength Enhancement", "power_level": 4, "negates": ["Fire Resistance"]},
    "Ghostly Mist": {"effect": "Evasion", "power_level": 3, "negates": ["Enhanced Agility"]},
    "Zombie Toenail": {"effect": "Paralysis", "power_level": 2, "negates": ["Revitalization"]},
    "Unicorn Horn Dust": {"effect": "Purification", "power_level": 5, "negates": ["Poison"]},
    "Goblin Earwax": {"effect": "Night Vision", "power_level": 1, "negates": ["Invisibility"]},
    "Mummy Bandage": {"effect": "Protection", "power_level": 4, "negates": ["Transformation"]},
    "Black Widow Silk": {"effect": "Trapping", "power_level": 3, "negates": []},
    "Vampire Blood": {"effect": "Lifesteal", "power_level": 4, "negates": []},
    "Werewolf Claw": {"effect": "Enhanced Agility", "power_level": 3, "negates": ["Evasion"]},
}

# - ASCII Art for Potion Effects -
ascii_art = {
    "Invisibility": """
        ______
       /      \\
      |        |
      |   🌀   |
       \\______/
       """,
       "Poison": """
        ______
       /      \\
      |  ☠️    |
      |         |
       \\______/
       """,
       "Fire Resistance": """
        ______
       /      \\
      |  🔥🔥  |
      |         |
       \\______/
       """,
       "Healing": """
        ______
       /      \\
      |  💧    |
      |        |
       \\______/
       """,
       "Revitalization": """
        ______
       /      \\
      |  🌟🌟  |
      |         |
       \\______/
       """,
       "Transformation": """
        ______
       /      \\
      |  🦋🦋  |
      |         |
       \\______/
    """,
    "Strength Enhancement": """
        ______
       /      \\
      |  💪    |
      |        |
       \\______/
    """,
    "Evasion": """
        ______
       /      \\
      |  🌫️    |
      |        |
       \\______/
    """,
    "Paralysis": """
        ______
       /      \\
      |  ⚡️    |
      |        |
       \\______/
    """,
    "Purification": """
        ______
       /      \\
      |  ✨✨  |
      |         |
       \\______/
    """,
    "Night Vision": """
        ______
       /      \\
      |  🦉👁️  |
      |         |
       \\______/
    """,
    "Protection": """
        ______
       /      \\
      |  🛡️    |
      |        |
       \\______/
    """,
    "Trapping": """
        ______
       /      \\
      |  🕸️🕸️  |
      |         |
       \\______/
    """,
    "Lifesteal": """
        ______
       /      \\
      |  🩸🩸  |
      |         |
       \\______/
    """,
    "Enhanced Agility": """
        ______
       /      \\
      |  🏃‍♂️    |
      |        |
       \\______/
    """
}

# - Potion Log to Save Brewed Potions -
potion_log = []

# - Function to Determine Final Potion Effects Considering Negations and Power Levels -
def determine_effects(ingredient_list):
    effects = {}
    for ingredient_name in ingredient_list:
        ingredient = ingredients[ingredient_name]
        effect = ingredient["effect"]
        power_level = ingredient["power_level"]
        for existing_effect, existing_power in effects.items():
            if existing_effect in ingredient["negates"] and power_level > existing_power:
                print(f"{ingredient_name} negates the effect of a weaker {existing_effect}")
                time.sleep(1)
                effects.pop(existing_effect)
            elif effect in ingredients[ingredient_name]["negates"] and existing_power > power_level:
                print(f"{effect} effect of {ingredient_name} is negated by a stronger {existing_effect}.")
                time.sleep(1)
                break
        else:
            effects[effect] = power_level
    return effects

# - Function to Save a Potion to the Log with Timestamp -
def save_potion(name, ingredients, effects, outcome="Success"):
    potion = {
        "name": name,
        "ingredients": ingredients,
        "effects": effects,
        "outcome": outcome,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    potion_log.append(potion)
    print(f"Potion '{name}' saved to the log!")

# - Function to Save the Potion Log to a File -
def save_log_to_file(filename="potion_log.json"):
    try:
        with open(filename, "r") as file:
            existing_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_log = []
    existing_log.extend(potion_log)
    with open(filename, "w") as file:
        json.dump(existing_log, file, indent=4)
    print("Potion log saved to file!")

# - Function to Display ASCII Art for Each Effect -
def display_ascii_art(effects):
    for effect in effects:
        if effect in ascii_art:
            print(f"\nEffect: {effect}")
            print(ascii_art[effect])
            time.sleep(1)

# - Function to Display the Potion Log -
def view_potion_log():
    if not potion_log:
        print("The potion log is empty.")
    else:
        print("\nPotion Log:")
        for potion in potion_log:
            print(f"Name: {potion['name']}")
            print(f"Ingredients: {', '.join(potion['ingredients'])}")
            print(f"Effects: {', '.join(potion['effects'])}")
            print(f"Outcome: {potion['outcome']}")
            print(f"Timestamp: {potion['timestamp']}\n")
        time.sleep(1)

# -- Custom Title-Case Function (Witch's Hair test problem solution) --
def custom_title_case(word):
    return ' '.join([word[0].upper() + word[1:].lower() if word else ' ' for word in word.split()])

# - Function to Brew a Potion -
def brew_potion():
    print("Enter a name for your potion: ")
    name = input()
    print("\nAvailable Ingredients:")
    for ingredient_name, details in ingredients.items():
        print(f"- {ingredient_name}: {details['effect']}")
    ingredient_list = []
    while True:
        ingredient = custom_title_case(input("Add an ingredient (or type 'done' to finish): ").strip())
        if ingredient == "Done":
            break
        elif ingredient in ingredients:
            ingredient_list.append(ingredient)
            print(f"Added {ingredient} to the potion.")
        else:
            print("Invalid ingredient. Please select from the available list.")
        time.sleep(0.5)
    print("\nBrewing your potion...")
    time.sleep(2)
    effects = determine_effects(ingredient_list)
    outcome = "Success" if effects else "Failure"
    save_potion(name, ingredient_list, list(effects.keys()), outcome)
    print(f"\nFinal Potion Effects for {name}:")
    display_ascii_art(effects.keys())

# - Main Menu Function -
def main_menu():
    while True:
        print("\n--- Potion Brewing Simulator ---")
        print("1. Brew a Potion")
        print("2. View Potion Log")
        print("3. Save Log to File")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            brew_potion()
        elif choice == "2":
            view_potion_log()
        elif choice == "3":
            save_log_to_file()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# -Run the Main Menu -
main_menu()
