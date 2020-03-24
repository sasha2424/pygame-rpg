from entities.Entity import Entity
from spritesheet.SpriteSheet import SpriteSheet
from spritesheet.Animation import Animation
from Utils import *
import pygame

class Rock(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        self.spritesheet = SpriteSheet("rock", (50*8, 50*8))
        self.animation = Animation(self.spritesheet)
        self.animation.add_animation_from_sheet("none", (0,0,50,50), 8, (255,255,255))
        self.image = self.animation.get_image()
        self.sprite_shift_x = 25
        self.sprite_shift_y = 50

        self.add_collision_box(-15,-20,30,20)

        self.canMove = False


class LittleRock(Entity):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        self.spritesheet = SpriteSheet("rock", (25*8, 25*8))
        self.animation = Animation(self.spritesheet)
        self.animation.add_animation_from_sheet("none", (0,0,25,25), 8, (255,255,255))
        self.image = self.animation.get_image()
        self.sprite_shift_x = 12.5
        self.sprite_shift_y = 25

        self.add_collision_box(-7.5,-10,15,10)

        self.canMove = False

class Building(Entity):

    class Room:
        def __init__(self, x, y, width, height):
            pass

    def __init__(self, x, y, z):
        super().__init__(x, y, z)

        # set of rooms
        # each room has floor texture and wall texture
        # each room has doors / windows

    def draw(self, screen, dx, dy):
        super().draw(screen, dx, dy)
