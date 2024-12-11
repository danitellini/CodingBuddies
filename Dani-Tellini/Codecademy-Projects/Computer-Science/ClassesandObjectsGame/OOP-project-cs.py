# You can start with the
# Cat class or erase this
# and use your own!
class Turtle:
  def __init__(self, input_name, input_species, input_gender, input_age = 0, input_foster = False, input_mated = False):
    self.name = input_name
    self.species = input_species
    self.gender = input_gender
    self.age = input_age
    self.is_foster = input_foster
    self.mated = input_mated
    self.mate_name = []

  def have_birthday(self):
    self.age = self.age + 1
    print('{name} had a birthday! {name} is now {age} years old.'.format(name = self.name, age = self.age))

  def become_mates(self, other_turtle):
    if other_turtle.mated == False and self.mated == False and other_turtle.gender == 'female' and self.gender == 'male':
      self.mated = True
      other_turtle.mated = True
      self.mate_name.append(other_turtle)
      other_turtle.mate_name.append(self)
      print('{selfname} and {matename} are compatible and have become mated!'.format(selfname = self.name, matename = other_turtle.name))
    else:
      print('{selfname} and {othername} are not compatible and did not become mated.'.format(selfname = self.name, othername = other_turtle.name))

  # Create a __repr__ method
  def __repr__(self):
    if self.mated == True:
      mate = self.mate_name[0]
      mate_info = 'is mated to the ' + mate.species + ' ' + mate.name
    else:
      mate_info = 'is not mated'
    description = 'This {species} named {name} is {age} years old and {selfmate}.'.format(species = self.species, name = self.name, age = self.age, selfmate = mate_info)
    return description

# Create two pets.
turtle_one = Turtle('Oscar', 'Painted Turtle', 'male', 15, True)
turtle_two = Turtle('Luna', 'Painted Turtle', 'female', 12, True)

# Print out your pet below!
turtle_one.have_birthday
turtle_one.become_mates(turtle_two)
print(turtle_one)