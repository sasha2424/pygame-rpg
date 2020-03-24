import pygame
from pygame.locals import *
import math

from spritesheet.SpriteSheet import SpriteSheet
from Utils import *

class EntityHandler():
    def __init__(self, player):
        self.player = player
        self.entities = [player]

    def add_entity(self, e):
        self.entities.append(e)

    def add_entities_from_chunk(self,chunk):
        for e in chunk.entities:
            self.entities.append(e)

    def store_entities_in_chunk(self, chunk):
        i = 0
        while i < len(self.entities):
            e = self.entities[i]
            if chunk.entity_in_chunk(e):
                chunk.add_entity(e)
                self.entities.remove(e)
                continue
            i += 1

    def render(self, screen, center_x, center_y):
        for entity in self.entities:
            entity.draw(screen, self.player.x - center_x, self.player.y - center_y)

    def update(self, interactionHandler):
        for e in self.entities:
            #TODO should be local entities
            e.update(self.entities, self.player)

        #get nearest entity to player in interaction range
        nearest = None
        dist_nearest = self.player.interact_range
        for e in self.entities: #TODO should be local entities to player
            if e == self.player:
                continue
            d = dist(e.x,e.y,self.player.x,self.player.y)
            if d < dist_nearest:
                nearest = e
                dist_nearest = d
        interactionHandler.nearest_entity = nearest


        num_entities = len(self.entities)
        for i in range(num_entities - 1):
            for j in range(i + 1,num_entities):
                e1 = self.entities[i]
                e2 = self.entities[j]
                EntityHandler.collide(e1, e2)

    @staticmethod
    def collide(e1, e2):
        shift_x = 0
        shift_y = 0
        for cb1 in e1.collisionBox:
            for cb2 in e2.collisionBox:
                x, y = Box.collide(cb1,cb2)
                #print(x,y)
                if abs(x) > abs(shift_x):
                    shift_x = x
                if abs(y) > abs(shift_y):
                    shift_y = y

        if e1.canMove and e2.canMove:
            e1.x -= shift_x/2.0
            e1.y -= shift_y/2.0

            e2.x += shift_x/2.0
            e2.y += shift_y/2.0
        elif e1.canMove:
            e1.x -= shift_x
            e1.y -= shift_y
        elif e2.canMove:
            e2.x += shift_x
            e2.y += shift_y
        else:
            pass #neither should move

class Entity:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.sprite_shift_x = 0
        self.sprite_shift_y = 0

        self.spritesheet = None
        self.animation = None
        self.collisionBox = []
        self.canMove = True

        self.can_interact = False
        self.interact_range = 0

    def add_collision_box(self, x, y, w, h):
        self.collisionBox.append(Box(self, x, y, w, h, True))

    def add_collision_sphere(self, x, y, w, h):
        self.collisionBox.append(Box(self, x, y, w, h, False))

    def update(self, local_entities, player):
        pass

    def draw(self, screen, dx, dy):
        screen.blit(self.image,(self.x - dx - self.sprite_shift_x, self.y - dy - self.sprite_shift_y))
        # for b in self.collisionBox:
        #     if b.is_rect:
        #         pygame.draw.rect(self.image, (255,0,0,100), (b.x,b.y,b.w,b.h),1)
        #     else:
        #         pygame.draw.circle(self.image, (255,0,0,100), (b.x,b.y),b.w//2,1)


    def interact(self, player):
        pass

    def __getstate__(self):
        return (self.x,self.y)

    def __setstate__(self, state):
        print(self.__class__)
        self.__init__(state[0],state[1])


class Box:
    def __init__(self, parent, x, y, w, h, is_rect):
        self.parent = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_rect = is_rect
        if not is_rect:
            self.h = self.w

    @staticmethod
    def collide(A, B):
        if A.is_rect and B.is_rect:
            return Box.collide_box_box(A,B)
        elif A.is_rect and not B.is_rect:
            return Box.collide_box_sphere(A,B)
        elif not A.is_rect and B.is_rect:
            shift_x, shift_y = Box.collide_box_sphere(B,A)
            return -shift_x, -shift_y
        else:
            return Box.collide_sphere_sphere(A,B)

    @staticmethod
    def collide_box_box(box1, box2):
        dx = box1.parent.x - box2.parent.x
        dy = box1.parent.y - box2.parent.y

        overlap_x = interval_overlap(box1.x + dx,box1.w, box2.x, box2.w)
        overlap_y = interval_overlap(box1.y + dy, box1.h, box2.y, box2.h)
        if abs(overlap_x) > abs(overlap_y):
            return 0, overlap_y
        return overlap_x, 0

    @staticmethod
    def collide_box_sphere(box, sphere):
        box_x = box.x + box.parent.x - sphere.parent.x
        box_y = box.y + box.parent.y - sphere.parent.y

        if box_x < sphere.x and sphere.x < box_x + box.w or \
            box_y < sphere.y and sphere.y < box_y + box.h:
            overlap_x = interval_overlap(box_x, box.w, sphere.x - sphere.w/2, sphere.w)
            overlap_y = interval_overlap(box_y, box.h, sphere.y - sphere.w/2, sphere.w)
            if abs(overlap_x) > abs(overlap_y):
                return 0, overlap_y
            return overlap_x, 0
        else:
            corn_x = box_x if sphere.x < box_x else box_x + box.w
            corn_y = box_y if sphere.y < box_y else box_y + box.h

            dx = sphere.x - corn_x
            dy = sphere.y - corn_y
            D = math.sqrt(dx*dx + dy*dy)
            if D > sphere.w/2:
                return 0,0
            r = (sphere.w/2 - D)/D #ratio
            return dx*r,dy*r


    @staticmethod
    def collide_sphere_sphere(sphere1, sphere2):
        sphere1_x = sphere1.x + sphere1.parent.x - sphere2.parent.x
        sphere1_y = sphere1.y + sphere1.parent.y - sphere2.parent.y
        dx = sphere2.x - sphere1_x
        dy = sphere2.y - sphere1_y
        D = math.sqrt(dx*dx + dy*dy)
        if D > sphere1.w/2 + sphere2.w/2:
            return 0,0
        r = (sphere1.w/2 + sphere2.w/2 - D)/D
        return dx*r,dy*r
