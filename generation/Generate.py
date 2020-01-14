
from GenUtils import *

world = Location()
population = []

for i in range(10):
    population.append(Character())

for C in population:
    world.add_character(c)



for year in range(10):
    events = []
    for C in population:
        event = c.pick_event()
    for event in events:
        event.start()
        event.end()
