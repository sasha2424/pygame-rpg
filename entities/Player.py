from entities.Entity import Entity
from spritesheet.SpriteSheet import SpriteSheet
from spritesheet.Animation import Animation
from Utils import *

import pygame

from enum import Enum

class State(Enum):
    STANDING = 0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Player(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        self.add_collision_sphere(32,60,20,20)

        colorkey = (255, 255, 255)
        self.spritesheet = SpriteSheet("player")
        self.animation = Animation(self.spritesheet)
        self.animation.add_animation_from_sheet("up", (0,0,64,64), 9, colorkey)
        self.animation.add_animation_from_sheet("left", (0,64,64,64), 9, colorkey)
        self.animation.add_animation_from_sheet("down", (0,128,64,64), 9, colorkey)
        self.animation.add_animation_from_sheet("right", (0,192,64,64), 9, colorkey)

        self.animation.add_animation_from_sheet("stand_up", (0,0,64,64), 1, colorkey)
        self.animation.add_animation_from_sheet("stand_left", (0,64,64,64), 1, colorkey)
        self.animation.add_animation_from_sheet("stand_down", (0,128,64,64), 1, colorkey)
        self.animation.add_animation_from_sheet("stand_right", (0,192,64,64), 1, colorkey)

        self.animation.set("stand_down")
        self.image = self.animation.get_image()

        self.action = State.STANDING

        self.interact_range = 100

    def update(self, local_entities, player):
        self.animation.update()
        self.image = self.animation.get_image()

        speed = 5

        animation_state = self.animation.get_state()
        if animation_state == "up":
            self.y -= speed
        if animation_state == "left":
            self.x -= speed
        if animation_state == "down":
            self.y += speed
        if animation_state == "right":
            self.x += speed


    def do_action(self, action):
        if action == "standing":
            animation_state = self.animation.get_state()
            if animation_state == "up":
                self.animation.set("stand_up")
            if animation_state == "left":
                self.animation.set("stand_left")
            if animation_state == "down":
                self.animation.set("stand_down")
            if animation_state == "right":
                self.animation.set("stand_right")
            return
        self.animation.set(action)

    def __getstate__(self):
        return (self.x,self.y,self.action)

    def __setstate__(self, state):
        super().__setstate__((state[0],state[1]))
        self.action = state[2]
