usernames = ['admin',
             'brock',
             'blaise',
             'maddog',
             'BEAR']

new_users = ['mom', 'dad', 'bear', 'gigi']

for user in new_users : 
    if user.lower() in map(str.lower, usernames) : 
        print('Geez, that username is already taken man')
    else : 
        print('Geez, that usernames free man')
        

nos = list(range(1, 10))

for no in nos : 
    if no == 1 : 
        print('1st')
    elif no == 2 : 
        print('2nd')
    elif no == 3 : 
        print('3rd')
    else : 
        print(str(no) + 'th')
        
def describe_pet(animal_type, pet_name='luke'):
    """Display information about a pet."""
    print("\nI have a " + animal_type + ".")
    print("My " + animal_type + "'s name is " + pet_name.title() + ".")
    
def make_shirt(shirt_size = 'L', saying = 'I Love Python'):
    """Display message about shirt and size """
    print("We are making a shirt in size " + shirt_size + " and it says " + 
          saying + '.')
    
def city_describe(state, city = 'Sinajana') :
    print(city + ' is in ' + state)