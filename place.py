class Place:

    def __init__(self,name,country,priority,is_visited):
        self.name = name
        self.country = country
        self.priority = priority
        if is_visited == "v":
            self.is_visited = True
        else:
            self.is_visited = False

    def __str__(self):
        return f"{self.name:<8} in {self.country:<11}  {self.priority:>2}"

    def mark_as_visited(self):
        """Mark place as visited"""
        self.is_visited = True

    def mark_as_unvisited(self):
        """Mark place as unvisited"""
        self.is_visited = False



