import pygame
import os

class SpriteSheet(object):
    def __init__(self, name, size = None):
        self.sheet = pygame.image.load(os.path.join("./assets", name + ".bmp")).convert()
        self.size = size
        if not self.size == None:
            self.sheet = pygame.transform.scale(self.sheet, self.size)

    def full_image(self):
        "Return full spritesheet"
        return self.sheet

    def image_at(self, rectangle, colorkey=(255,255,255), scale=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image.set_alpha(255)
        if scale == None:
            return image
        return pygame.transform.scale(image,scale)

    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
