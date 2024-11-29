"""
Name: Sean Onyango
Date: 29/11/2024
Brief Project Description: This is a travel tracker application which allows the user to load a
file with their wishlist of destinations and constantly update whether they are visited or not.
It also allows the user to add new entries through the GUI. It is heavily based on the use of class objects.

GitHub URL: https://github.com/cp1404-students/a2-seanonyango
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from placecollection import PlaceCollection
from place import Place

WHITE = 0, 0.8, 0, 1  # Color for not visited places
GREEN = 1, 1, 1, 1  # Color for visited places


class TravelTrackerApp(App):
    """Main application class for the Travel Tracker App"""

    def __init__(self):
        """Initialize the application and load existing places"""
        super().__init__()
        self.placecollection = PlaceCollection()  # Create a PlaceCollection instance
        self.placecollection.load_places()  # Load places from storage

    def build(self):
        """Build the GUI using the kivy library"""
        self.title = 'Travel Tracker App'
        self.root = Builder.load_file('app.kv')
        self.display_places()  # Display the initial list of places
        return self.root

    def display_places(self, key="is_visited"):
        """Load places and create dynamic widgets for each place."""
        self.root.ids.places.clear_widgets()  # Reset places before each reload to avoid duplicates
        if key == 'Visited':
            key = 'is_visited'  # Adjust key for sorting

        self.placecollection.sort(key.lower())

        for place in self.placecollection.places:
            output = self.get_button_text(place)  # Format place string properly for display
            button = Button(text=output)
            # Enable toggle status on each button for visited status
            button.bind(on_press=lambda instance, p=place, btn=button: self.toggle_visited_status(p, btn))
            button.background_color = self.determine_button_background(place)
            self.root.ids.places.add_widget(button)

        self.display_number_of_unvisited()  # Update the display of unvisited places

    def display_number_of_unvisited(self):
        """Display the number of unvisited places in the GUI."""
        self.root.ids.number_of_unvisited_display.text = f"Places to visit: {self.placecollection.get_number_of_unvisited()}"

    @staticmethod
    def determine_button_background(place):
        """Return the background color for a button based on the visited status"""
        if place.is_visited:
            return GREEN
        else:
            return WHITE

    def toggle_visited_status(self, place, button):
        """Toggle the visited status of a place"""
        place.is_visited = not place.is_visited
        button.background_color = self.determine_button_background(place)
        button.text = self.get_button_text(place)
        message = self.determine_toggle_message(place)  # Get message based on the new status
        self.display_places()
        self.update_welcome_message(message)  # Add message to status label

    def update_welcome_message(self, message=""):
        """Update the welcome message displayed in the GUI."""
        self.root.ids.welcome_message.text = message  # Set the welcome message text

    def add_new_place(self):
        """Add a new place based on user input from the text fields."""
        name = self.root.ids.name_input.text.title()
        country = self.root.ids.country_input.text.title()
        priority = self.root.ids.priority_input.text
        message = self.validate_new_place(country, name, priority)  # Get validation message or error message
        self.update_welcome_message(message)
        self.display_places()

    def validate_new_place(self, country, name, priority):
        """Validate the new place input"""
        if name and country and priority:  # Check that all fields are filled
            if priority.isdigit():  # Ensure priority is a number
                if int(priority) < 1:
                    message = "Priority must be > 0"  # Check priority is greater than 0
                else:
                    new_place = Place(name=name, country=country, priority=int(priority))
                    self.placecollection.add_place(new_place)
                    message = f"{name} in {country}, priority {priority} added"  # Success message
            else:
                message = "Please enter a valid number"  # Invalid priority message
        else:
            message = "All fields must be completed"  # Missing fields message
        return message

    def handle_clear(self):
        """Clear all input fields in the GUI."""
        ids_to_clear = ['name_input', 'country_input', 'priority_input', 'welcome_message']
        for input_id in ids_to_clear:
            self.root.ids[input_id].text = ""

    @staticmethod
    def determine_toggle_message(place):
        """Determine the message to display based on the visited status of the place."""
        if place.is_visited:
            return f"You visited {place.name}. Good travelling!"  # Message for visited places
        else:
            return f"You need to visit {place.name}. Get going!"  # Message for unvisited places

    @staticmethod
    def get_button_text(place):
        """Determine the text of the button for the given place."""
        return f"{place.name} in {place.country}, priority {place.priority} {'(visited)' if place.is_visited else ''}"

    def on_stop(self):
        """Save places when the application is closed."""
        self.placecollection.save_places()


if __name__ == '__main__':
    TravelTrackerApp().run()
