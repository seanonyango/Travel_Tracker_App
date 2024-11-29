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
        for place in self.placecollection.places:
            output = f"{place.name} in {place.country},priority {place.priority} {"(visited)" if not place.is_visited else ""}"
            button = Button(text=output)
            self.root.ids.places.add_widget(button)

    def display_number_of_unvisited(self):
        return f"Places to visit: {self.placecollection.get_number_of_unvisited()}"


if __name__ == '__main__':
    TravelTrackerApp().run()
