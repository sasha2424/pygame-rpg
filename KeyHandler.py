from pygame.locals import *

class KeyHandler:
    def __init__(self, player):
        self.player = player

        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False
        self.TURN_RIGHT = False
        self.TURN_LEFT = False

    def add_input(self, key, pressed):
        if key == K_d:
            self.RIGHT = pressed
        if key == K_a:
            self.LEFT = pressed
        if key == K_s:
            self.DOWN = pressed
        if key == K_w:
            self.UP = pressed
        if key == K_e:
            self.TURN_RIGHT = pressed
        if key == K_q:
            self.TURN_LEFT = pressed



    def handle_inputs(self):
        if self.RIGHT:
            self.player.do_action("right")
        if self.LEFT:
            self.player.do_action("left")
        if self.DOWN:
            self.player.do_action("down")
        if self.UP:
            self.player.do_action("up")
        if not (self.UP or self.DOWN or self.RIGHT or self.LEFT):
            self.player.do_action("standing")
        if self.UP:
            self.player.do_action("up")
