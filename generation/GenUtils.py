from NameGenerator import *

#Interest flags
I_ACTIVE = "active"


class Event:
    def get_name():
        pass

    def interest_flags():
        pass

    def roles():
        pass

    def start():
        pass

    def end():
        pass

class Role:
    def __init__(self, c):
        self.character = c

    def can_assign(character):
        pass

    def name():
        pass

class Goal:
    def eval(population):
        pass

class Character:
    def __init__(self):
        self.name = name_gen()
        self.surname = name_gen()
        self.age = 0

        self.interests = {} #interest to weight map
        self.interests[I_ACTIVE] = 1

        self.goals = [] #set of goal operators

        self.history = []

        self.location = None

    def age(self):
        self.age += 1

    def pick_event(self):
        options = self.location.events

        event = None
        value = 0

        for e in options:
            v = 0
            for I_FLAG in e.interest_flags():
                v += self.interests[I_FLAG]
            if v > value:
                value = v
                event = e
        return event


class Location:
    def __init__(self):
        self.parent_location = None
        self.members = []
        self.events = []

        self.population = []

    def add_character(self, character):
        self.population.append(character)

    def add_member(self, member):
        self.members.append(member)

    def get_name():
        pass

    def get_available_events():
        pass
