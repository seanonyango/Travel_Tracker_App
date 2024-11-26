from place import Place
from operator import attrgetter
import json

EXTERNAL_FILE = "places.json"


class PlaceCollection:

    def __init__(self):
        self.places = []


    def load_places(self):
        """Load places from external file"""
        with open(EXTERNAL_FILE, "r") as in_file:
            places_data = json.load(in_file)
            self.places = [Place(place['name'], place['country'], place['priority'], place['is_visited']) for place in places_data]

    def save_places(self):
        """Save places to external file"""
        places_data = [place.__dict__ for place in self.places]
        with open(EXTERNAL_FILE, 'w') as out_file:
            json.dump(places_data, out_file)

    def add_place(self,place):
        """Add new place to collection"""
        self.places.append(place)

    def get_number_of_unvisited(self):
        """Count number of unvisited places"""
        return sum(1 for place in self.places if not place.is_visited)

    def sort(self,key, reverse= False):
        """Count number of sorted places"""
        self.places.sort(key=attrgetter(key, 'priority'), reverse = reverse)



