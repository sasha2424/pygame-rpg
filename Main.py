import sys
import time

import pygame
from pygame.locals import *

from entities.Entity import EntityHandler
from entities.Player import Player
from entities.Stationary import *
from entities.NPC import *

from Rendering import Render_Queue, queue_render
from operator import itemgetter

from KeyHandler import KeyHandler
from InteractionHandler import InteractionHandler

from terrain.Terrain import *

from Utils import *

"""
Testing Assets:

"""


pygame.init()
screen = pygame.display.set_mode((600,600),RESIZABLE)
pygame.display.set_caption("Game")


player = Player(0,0,0)

interactionHandler = InteractionHandler(player)
keyHandler = KeyHandler(player)

entityHandler = EntityHandler(player)
entityHandler.add_entity(Rock(100,100,0))
entityHandler.add_entity(LittleRock(100,200,0))
entityHandler.add_entity(Rick(100,0,0))

tileHandler = TileHandler()
chunkHandler = ChunkHandler()



def tick():
    # interaction handler for player interaction
    # chunk handler for terrain collision
    entityHandler.update(interactionHandler, chunkHandler)

def render():
    chunkHandler.update(player.x, player.y, screen.get_width(), screen.get_height(), entityHandler)
    screen.fill((0,100,0))

    center_x = screen.get_width()/ 2
    center_y = screen.get_height() / 2
    tileHandler.render(player, center_x, center_y, chunkHandler)
    entityHandler.render(center_x, center_y)

    render_list = sorted(Render_Queue.render_list,key=itemgetter(0))
    for _,args in render_list:
        screen.blit(*args)
    Render_Queue.render_list = []

    #pygame.display.update()
    pygame.display.flip()

fps = 60
frame_start = time.time()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            keyHandler.add_input(event.key, True)
            interactionHandler.handle_input(event.key, True)
        if event.type == pygame.KEYUP:
            keyHandler.add_input(event.key, False)
            interactionHandler.handle_input(event.key, False)
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    keyHandler.handle_inputs()

    if time.time() - frame_start > 1 / fps:
        tick()
        render()
        frame_start = time.time()
