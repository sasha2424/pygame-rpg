from generation.GenUtils import *

class World(Location):
    def __init__(self, name):
        super().__init__()
        self.members = []

    def get_name():
        return "World"

    def get_available_events():
        pass

class City(Location):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_name():
        return "City " + self.name

    def get_available_events():
        pass

class House(Location):
    def __init__(self):
        super().__init__()

    def get_name():
        return "House"

    def get_available_events():
        pass

class Camp(Location):
    def __init__(self):
        super().__init__()

    def get_name():
        return "Hunting Camp"

    def get_available_events():
        pass
