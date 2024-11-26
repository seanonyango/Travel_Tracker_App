import random

"""
CP1404 Assignment 1 - Travel Tracker
Name:Sean Onyango
Date started:21/10/2024
GitHub URL: https://github.com/cp1404-students/a1-seanonyango
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
    places_and_travel_info = load_external_file_into_list("places.json")
    menu_choice = None
    while menu_choice != "Q":
        menu_choice = call_main_menu()
        if menu_choice == "D":
            display_full_list_of_places(places_and_travel_info)
        elif menu_choice == "R":
            generate_random_city_and_country(places_and_travel_info)
        elif menu_choice == "A":
            places_and_travel_info = add_new_place(places_and_travel_info)
        elif menu_choice == "M":
            display_full_list_of_places(places_and_travel_info)
            print("Enter the number of place to mark as visited")
            choice, places_and_travel_info = mark_new_place_as_visited(places_and_travel_info)
            display_marked_place_as_visited(choice, places_and_travel_info)
        else:
            print("Invalid Menu Choice.")
    update_external_file(places_and_travel_info)
    print(f"{len(places_and_travel_info)} places added to {EXTERNAL_FILE}")
    print("Have a nice day!")


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
    new_place = [name, country, priority, "n"]
    print(f"{name} in {country} (priority {priority}) added to Travel Tracker.")
    places_and_travel_info.append(new_place)
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
    unvisited_places = [place for place in places_and_travel_info if place[3] == "n"]

    try:
        random_city, random_country = derive_city_and_country(random.choice(unvisited_places))
        print(f"Not sure where to visit next?\nHow about... {random_city.title()} in {random_country.title()}?")
    # Exception for when there are no unvisited places
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

