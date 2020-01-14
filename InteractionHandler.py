from entities.NPC import NPC

from pygame.locals import *

class InteractionHandler:
    def __init__(self, player):
        self.player = player
        self.nearest_entity = None

        self.INTERACTION = False
        self.SELECT_UP = False
        self.SELECT_DOWN = False


    def handle_input(self, key, pressed):
        if self.nearest_entity == None:
            return
        if key == K_e or key == K_RETURN:
            if not self.INTERACTION and pressed:
                self.nearest_entity.interact("e")
            self.INTERACTION = pressed
        if key == K_UP or key == K_LEFT:
            if not self.SELECT_UP and pressed:
                self.nearest_entity.interact("up_arrow")
            self.SELECT_UP = pressed
        if key == K_DOWN or key == K_RIGHT:
            if not self.SELECT_DOWN and pressed:
                self.nearest_entity.interact("down_arrow")
            self.SELECT_DOWN = pressed
