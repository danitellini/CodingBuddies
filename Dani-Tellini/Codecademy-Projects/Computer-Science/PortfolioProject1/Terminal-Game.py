import random
import time

class Human:
  # methods:
  def __init__(self, input_fname, input_lname, input_age = 0, input_animalpref = None, input_yard = False, input_pets = 0, input_typeofpet = None, input_kids = False):
    self.fname = input_fname
    self.lname = input_lname
    self.age = input_age
    self.pref = input_animalpref
    self.yard = input_yard
    self.pets = input_pets
    self.pet_type = input_typeofpet if input_typeofpet else []
    self.kids = input_kids

  def __repr__(self):
    description = f"Full Name: {self.fname} {self.lname}\n"
    description += f"Age: {self.age}\n"
    description += f"Animal Preference: {self.pref}\n"
        
    if self.yard:
        description += "Yard: Yes\n"
    else:
        description += "Yard: No\n"
        
    if self.pets == 1:
        description += f"Number of Other Pets: 1 ({self.pet_type[0]})\n"
    elif self.pets > 1:
        description += f"Number of Other Pets: {self.pets}\n"
        description += "Pet Types: " + ", ".join(f"{pet}" for pet in self.pet_type) + "\n"
    else:
        description += "Number of Other Pets: 0\n"
        
    if self.kids:
        description += "Has Children: Yes\n"
    else:
        description += "Has Children: No\n"
        
    return description

  def choose_furry_friend(self, dogs, cats):
    print("\nWe found a few that we think will be a perfect match!\n")
    potential_pets = []
    pet_count = 1

    # Check for dog preference or both
    if self.pref in ['Dog', 'Both']:
      for dog in dogs:
        compatible_with_existing_pets = True

        if 'Cat' in self.pet_type and not dog.cats:
          compatible_with_existing_pets = False
        if 'Dog' in self.pet_type and not dog.dogs:
          compatible_with_existing_pets = False

        if (compatible_with_existing_pets and \
          (not dog.highenergy or self.yard) and \
          (not self.kids or dog.kids) and \
          dog.isfriendly):
          potential_pets.append((pet_count, dog))
          pet_count += 1

    # Check for cat preference or both
    if self.pref in ['Cat', 'Both']:
      for cat in cats:
        compatible_with_existing_pets = True

        if 'Dog' in self.pet_type and not cat.dogs:
          compatible_with_existing_pets = False
        if 'Cat' in self.pet_type and not cat.cats:
          compatible_with_existing_pets = False

        if (compatible_with_existing_pets and \
          (not self.kids or cat.kids) and \
          cat.isfriendly):
          potential_pets.append((pet_count, cat))
          pet_count += 1

    # Display potential pets
    if not potential_pets:
      print("No pets match your preferences.")
      return None
    
    print("Here are the possible pets that match your preferences:\n")
    for number, pet in potential_pets:
      print(f"{number}: {pet}\n")

    # User selection
    try:
      choice = int(input("\nType the number of the pet you'd like to adopt: "))
      chosen_pet = next((pet for number, pet in potential_pets if number == choice), None)

      if chosen_pet:
        print(f"\nYou have chosen: {chosen_pet.name}\n")
      else:
        print("Invalid choice.")
    
    except ValueError:
      print("Invalid input. Please enter a number. ")

    return chosen_pet

class Dog:
  # methods:
  def __init__(self, input_name,  input_age = 0, input_breed = None, input_goodwithkids = True, input_highenergy = False, input_goodwithdogs = True, input_goodwithcats = True, input_friendly = True):
    self.name = input_name
    self.age = input_age
    self.breed = input_breed
    self.kids = input_goodwithkids
    self.highenergy = input_highenergy # for Human yard question
    self.dogs = input_goodwithdogs
    self.cats = input_goodwithcats
    self.isfriendly = input_friendly

  def __repr__(self):
    description = "{name} is a {age}-year-old {breed}.".format(name = self.name, age = self.age, breed = self.breed)

    if self.kids:
      description += " They are good with kids."
    else:
      description += " They are not good with kids."

    if self.dogs:
      description += " They are good with other dogs."
    else:
      description += " They are not good with other dogs."

    if self.cats:
      description += " They are good with cats."
    else:
      description += " They are not good with cats."

    if self.highenergy:
      description += " They are very high energy and will need a yard."
    else:
      description += " They are relatively calm."

    if self.isfriendly:
      description += " {name} is friendly with people.".format(name = self.name)
    else:
      description += " {name} is not very friendly with other people.".format(name = self.name)

    return description

  def have_birthday(self):
    self.age += 1

    return (f"{self.name} had a birthday! They are now {self.age}-years-old.")

  def training_program(self):
    commands = {1: 'Sit', 2: 'Stay', 3: 'Leave it', 4: 'Lay down', 5: 'Roll over', 6: 'Shake'}

    if self.isfriendly:
      print(f"{self.name} is already friendly and well-behaved!\n")
      return
    
    required_commands = random.randint(1, 6)
    learned_commands = set()
    print(f"{self.name} needs to learn {required_commands} command(s) to become friendly.\n")

    while len(learned_commands) < required_commands:
      print(f"Which command would you like them to learn next?\n")
      time.sleep(2)
      
      for number, command in commands.items():
        print(f"{number}, {command}")
        

      try:
        choice = int(input("\nType the number of the command you'd like to teach: "))
        if choice in commands:
          print(f"\nTeaching {self.name} to '{commands[choice]}'...\n")
          time.sleep(2)
          print(f"Great! {self.name} has learned to '{commands[choice]}.\n")
          learned_commands.add(choice)
          if len(learned_commands) == required_commands:
            self.isfriendly = True
            print(f"{self.name} has learned {required_commands} command(s) and is now friendly and ready for adoption!\n")
        else:
          print("Invalid choice or command already learned. Please select another. ")
      except ValueError:
        print("Invalid input. Please enter a number. ")

  def lick(self, Human):
    print(f"You go to pet {self.name} on the head. They lick you on the hand.")

    return

dog_one = Dog('Khaleesi', 7, 'American Staffordshire Terrier', True, False, True, True)
dog_two = Dog('Kira', 2, 'Argentine Dogo', True, True, True, True)
dog_three = Dog('Buddy', 5, 'Golden Retriever', True, True, True, False,False)
dog_four = Dog('Max', 3, 'German Shepherd', True, False, False, True)
dog_five = Dog('Bella', 4, 'Labrador Retriever', True, True, True, True)
dogs = [dog_one, dog_two, dog_three, dog_four, dog_five]


class Cat:
  # methods: purr(self, Human)
  def __init__(self, input_name, input_age = 0, input_breed = None, input_goodwithkids = False, input_goodwithdogs = False, input_goodwithcats = False, input_friendly = True):
    self.name = input_name
    self.age = input_age
    self.breed = input_breed
    self.kids = input_goodwithkids
    self.dogs = input_goodwithdogs
    self.cats = input_goodwithcats
    self.isfriendly = input_friendly

  def __repr__(self):
    description = "{name} is a {age}-year-old {breed}.".format(name = self.name, age = self.age, breed = self.breed)

    if self.kids:
      description += " They are good with kids."
    else:
      description += " They are not good with kids."

    if self.dogs:
      description += " They are good with dogs."
    else:
      description += " They are not good with dogs."

    if self.cats:
      description += " They are good with other cats."
    else:
      description += " Other cats should be avoided."

    if self.isfriendly:
      description += " {name} is friendly towards people.".format(name = self.name)
    else:
      description += " {name} will pick their forever human and will be hesitant around other people.".format(name = self.name)

    return description

  def have_birthday(self):
    self.age += 1

    return (f"{self.name} had a birthday! They are now {self.age}-years-old.")

  def purr(self, Human):
    print(f"You scratch {self.name} under the chin. {self.name} starts to purr.")

    return

cat_one = Cat('Emma', 10, 'Orange Tabby', True, True, False)
cat_two = Cat('Medusa', 4, 'Unknown', False, False, False, False)
cat_three = Cat('Whiskers', 3, 'Siamese', True, False, True, True)
cat_four = Cat('Mittens', 4, 'Persian', True, True, True, True)
cat_five = Cat('Luna', 2, 'Maine Coon', False, True, True, False)
cat_six = Cat('Oliver', 5, 'British Shorthair', True, True, False, True)
cats = [cat_one, cat_two, cat_three, cat_four, cat_five, cat_six]

# Start adoption process
start_variable = input("Welcome to Rafaela Pet Adoption Agency! Are you here to fill out an adoption application? Type 'Yes' or 'No' and hit enter: ")

while start_variable != 'Yes' and start_variable != 'No':
  start_variable = input("Whoops, it looks like you didn't choose 'Yes' or 'No'. Try selecting one again: ")

if start_variable == 'No':
  print("Come back when you're ready to adopt!")
  exit()
else:
  human_fname = input("What is your first name? Type your name and hit enter: ")
  human_lname = input("What is your last name? Type your last name and hit enter: ")
  human_age = int(input("What is your age? Type the number and hit enter: "))
  human_animalpref = input("Which animal would you prefer? 'Dog', or 'Cat'? If both, type 'Both' and hit enter: ")

  # Confirm animal preference input
  while human_animalpref not in ['Dog' , 'Cat', 'Both']:
    human_animalpref = (input("We only have dogs and cats at this agency. Please select 'Dog', 'Cat', or 'Both' and hit enter: "))

  human_yard = input("Do you have a yard? 'Yes' or 'No'? Hit enter: ")
  human_yard = True if human_yard == 'Yes' else False

  # Do you have pets
  human_petcount = 0
  human_pettype = []
  holding_variable = input("Do you have any pets? 'Yes' or 'No'. Hit enter: ")

  if holding_variable == 'Yes':
    human_petcount = int(input("How many pets do you have? "))
    for i in range(human_petcount):
      pet_type = input(f"What type of pet is pet {i + 1}? 'Dog', 'Cat', or 'Other'? Hit enter: ")
      while pet_type not in ['Dog', 'Cat', 'Other']:
        pet_type = input(f"Whoops! Please choose 'Dog', 'Cat', or 'Other' for pet {i + 1}: ")
      human_pettype.append(pet_type)

  # Do you have kids
  kids_variable = input("Do you have any kids? 'Yes' or 'No'. Hit enter: ")
  human_kids = True if kids_variable == 'Yes' else False

# Human instance
human = Human(human_fname, human_lname, human_age, human_animalpref, human_yard, human_petcount, human_pettype, human_kids)

# Summary
print("\nSummary of your application:\n")
print(human)

# Application Confirmation
confirm_submission = input("Is this information correct? Type 'Yes' to submit or 'No' to cancel: ")

while confirm_submission != 'Yes' and confirm_submission != 'No':
  confirm_submission = input("Please type 'Yes' to submit or 'No' to cancel: ")

if confirm_submission == 'Yes':
  print("\nSubmitting your applicaiton, please wait...")
  #Delay for submission
  time.sleep(3)

  print("Loading...")
  time.sleep(3)

  print("Handpicking the right matches for you...")
  time.sleep(3)

  print("Please wait while we process your request!")
  time.sleep(3)

else:
  print("\nYour application has been cancelled.")
  exit()

human.choose_furry_friend(dogs, cats)
dog_one.have_birthday()
dog_three.training_program()
dog_one.lick(human)
cat_five.have_birthday()
cat_six.purr(human)