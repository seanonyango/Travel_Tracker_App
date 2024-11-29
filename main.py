"""
Name:
Date:
Brief Project Description:
GitHub URL:
"""
# Create your main program in this file, using the TravelTrackerApp class

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from placecollection import PlaceCollection


class TravelTrackerApp(App):

    def __init__(self):
        super().__init__()
        self.placecollection = PlaceCollection()
        self.placecollection.load_places()
        self.placecollection.sort("is_visited")

    def build(self):
        self.title = 'Travel Tracker App'
        self.root = Builder.load_file('app.kv')
        self.display_places()
        return self.root

    def display_places(self):
        self.root.ids.places.clear_widgets()
        self.placecollection.sort("is_visited")

        for place in self.placecollection.places:
            output = self.get_button_text(place)
            button = Button(text=output)
            button.bind(on_press=lambda instance, p=place, btn=button: self.toggle_visited_status(p, btn))
            button.background_color = self.determine_button_background(place)
            self.root.ids.places.add_widget(button)

        self.display_number_of_unvisited()

    def display_number_of_unvisited(self):
        self.root.ids.number_of_unvisited_display.text = f"Places to visit: {self.placecollection.get_number_of_unvisited()}"
        return f"Places to visit: {self.placecollection.get_number_of_unvisited()}"

    @staticmethod
    def determine_button_background(place):
        if place.is_visited:
            return 1, 1, 1, 1
        else:
            return (0, 0.8, 0, 1)

    def toggle_visited_status(self, place, button):
        place.is_visited = not place.is_visited
        button.background_color = self.determine_button_background(place)
        button.text = self.get_button_text(place)
        message = self.determine_toggle_message(place)
        self.display_places()
        self.update_welcome_message(message)

    def update_welcome_message(self, message):
        self.root.ids.welcome_message.text = message

    @staticmethod
    def determine_toggle_message(place):
        if place.is_visited:
            return f"You visited {place.name}. Good travelling!"
        else:
            return f"You need to visit {place.name}. Get going!"
    @staticmethod
    def get_button_text(place):
        return f"{place.name} in {place.country}, priority {place.priority} {'(visited)' if place.is_visited else ''}"


if __name__ == '__main__':
    TravelTrackerApp().run()
