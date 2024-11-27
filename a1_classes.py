import random
from place import Place
from placecollection import PlaceCollection

"""
This is the revision of assignment number 1 to include classes.
Only minor changes have been include the class object instead of a list.
The general working of the code remains the same and any functional hiccups from
assignment 1 were maintained such as the ability to mark an already visited place as visited.
"""
"""
"""

EXTERNAL_FILE = "places.json"
DEVELOPER = "Sean Onyango"
MAIN_MENU = """Menu:
D - Display all places
R - Recommend a random place
A - Add a new place
M - Mark a place as visited
Q - Quit"""


def main():
    print(f"Travel tracker 1.0 - by {DEVELOPER}")
    # Initiate places_and_travel_info as object
    places_and_travel_info = PlaceCollection()
    places_and_travel_info.load_places()
    menu_choice = None
    while menu_choice != "Q":
        menu_choice = call_main_menu()
        if menu_choice == "D":
            print(places_and_travel_info)
        elif menu_choice == "R":
            generate_random_city_and_country(places_and_travel_info)
        elif menu_choice == "A":
            places_and_travel_info = add_new_place(places_and_travel_info)
        elif menu_choice == "M":
            places_and_travel_info = mark_place_as_visited(places_and_travel_info)
        else:
            print("Invalid Menu Choice.")
    places_and_travel_info.save_places()
    print(f"{len(places_and_travel_info.places)} places added to {EXTERNAL_FILE}")
    print("Have a nice day!")


def mark_place_as_visited(places_and_travel_info):
    """Mark a place as visited"""
    for i, place in enumerate(places_and_travel_info.places):
        print(f"{i+1}. {place}")
    print("Enter the number of the place to mark as visited")
    index_to_mark = get_valid_integer(1, len(places_and_travel_info.places), ">>>")
    place_to_mark = places_and_travel_info.places[index_to_mark-1]
    place_to_mark.mark_as_visited()
    print(f"{place_to_mark.name} has been marked as visited")
    return places_and_travel_info


def display_marked_place_as_visited(choice, places_and_travel_info):
    """Display marked place as visited"""
    marked_city, marked_country = derive_city_and_country(places_and_travel_info[choice - 1])
    print(f"{marked_city} in {marked_country} visited!")


def update_external_file(places_and_travel_info):
    """Write list to external file"""
    print(places_and_travel_info)
    with open(EXTERNAL_FILE, "w") as output_file:
        for place in places_and_travel_info:
            place_string = ",".join(place)
            output_file.write(f"{place_string}\n")


def mark_new_place_as_visited(places_and_travel_info):
    """Mark a place as visited"""
    choice = get_valid_integer(1, len(places_and_travel_info), ">>> ")
    # Match up the list in memory to the one on display by sorting into unvisited then visited
    places_and_travel_info = sort_unvisited_then_visited(places_and_travel_info)
    places_and_travel_info[choice - 1][3] = "v"
    return choice, places_and_travel_info


def call_main_menu():
    """Display main menu to get choice"""
    print(MAIN_MENU)
    menu_choice = input(">>> ").upper()
    return menu_choice


def add_new_place(places_and_travel_info):
    """Add new place to list"""
    name = get_valid_text_input("Name: ").title()
    country = get_valid_text_input("Country: ").title()
    priority = str(get_valid_numerical_input("Priority: "))
    # Set all new places to unvisited
    new_place = Place(name, country, priority)
    print(f"{new_place.name} in {new_place.country} (priority {new_place.priority}) added to Travel Tracker.")
    places_and_travel_info.add_place(new_place)
    return places_and_travel_info


def display_full_list_of_places(places_and_travel_info):
    """Display formatted list of places"""
    total_places = len(places_and_travel_info)
    total_unvisited = 0
    next_serial = 1
    # Display unvisited places first
    next_serial, total_unvisited = process_unvisited_places(next_serial, total_unvisited, places_and_travel_info)
    # Display visited places next
    process_visited_places(next_serial, places_and_travel_info)
    print(f"{total_places} places tracked. You still want to visit {total_unvisited} places.")


def process_visited_places(first_serial, places_and_travel_info):
    """Sort out visited places from list"""
    for place in places_and_travel_info:
        city, country = derive_city_and_country(place)
        priority = (place[2])
        if is_visited(place):
            print(f"{first_serial:>2} {city:<8} in {country:<11}  {priority:>2}")
            first_serial += 1


def process_unvisited_places(first_serial, total_unvisited, places_and_travel_info):
    """Sort out unvisited places from list"""
    for place in places_and_travel_info:
        city, country = derive_city_and_country(place)
        number = (place[2])
        if not is_visited(place):
            print(f"*{first_serial:} {city:<8} in {country:<11}  {number:>2}")
            total_unvisited += 1
            first_serial += 1
    return first_serial, total_unvisited


def derive_city_and_country(place):
    """Get city and country from list"""
    city = (place[0])
    country = (place[1])
    return city, country


def load_external_file_into_list(file):
    """Creates a list of lines in csv file"""
    with open(file, "r") as in_file:
        return [line.strip().split(",") for line in in_file.readlines()]


def generate_random_city_and_country(places_and_travel_info):
    """Generates a random unvisited city and country pair"""
    try:
        random_city = random.choice([place for place in places_and_travel_info.places if not place.is_visited])
        print(f"Not sure where to visit next?\nHow about... {random_city.name} in {random_city.country}?")
    except IndexError:
        print("No unvisited places")


def get_valid_text_input(prompt):
    """Get a non-empty string"""
    text = input(prompt)
    while text == "":
        print("Input cannot be blank.")
        text = input(prompt)
    return text


def get_valid_numerical_input(prompt):
    """Get a non-empty integer"""
    try:
        number = int(input(prompt))
    except ValueError:
        print("Invalid input; Enter a valid number.")
        number = get_valid_numerical_input(prompt)
    return number


def get_valid_integer(minimum, maximum, prompt):
    """Get valid integer within a given range"""
    number = get_valid_numerical_input(prompt)
    while number < minimum or number > maximum:
        print("Invalid place number.")
        number = get_valid_numerical_input(prompt)
    return number


def is_visited(place):
    """Determines if a place is visited"""
    if place[3] == "n":
        return False
    else:
        return True


def sort_unvisited_then_visited(places_and_travel_info):
    """Sorts list into unvisited and visited places"""
    sorted_places = []
    for place in places_and_travel_info:
        if not is_visited(place):
            sorted_places.append(place)
    for place in places_and_travel_info:
        if is_visited(place):
            sorted_places.append(place)
    return sorted_places


if __name__ == '__main__':
    main()
