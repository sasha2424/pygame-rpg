from spritesheet.SpriteSheet import SpriteSheet
from spritesheet.Animation import Animation
from Utils import *
import pygame

import numpy as np
import math

import pickle
import os


CHUNK_SIZE = 32*1000
TILE_SIZE = 32
TILES_PER_CHUNK = CHUNK_SIZE//TILE_SIZE

class TileHandler:
    def __init__(self):
        self.tiles = []
        sheet = SpriteSheet("terrain")

        for x in range(74,568,33):
            for y in range(0,329,33):
                self.tiles.append(sheet.image_at((x,y,32,32)))


    def render(self, screen, player, chunkHandler):
        center_x = screen.get_width() / 2
        center_y = screen.get_height() / 2
        dx = player.x - center_x
        dy = player.y - center_y

        for chunk in chunkHandler.active_chunks.values():
            chunk_world_x = chunk.chunk_x * CHUNK_SIZE
            chunk_world_y = chunk.chunk_y * CHUNK_SIZE

            start_x = math.floor((player.x - center_x - chunk_world_x)/TILE_SIZE)
            start_x = max(start_x,0)
            end_x = math.floor((player.x + center_x - chunk_world_x)/TILE_SIZE) + 1
            end_x = min(end_x,chunk.tile_map.shape[0])

            start_y = math.floor((player.y - center_y - chunk_world_y)/TILE_SIZE)
            start_y = max(start_y,0)
            end_y = math.floor((player.y + center_y - chunk_world_y)/TILE_SIZE) + 1
            end_y = min(end_y,chunk.tile_map.shape[1])

            for x in range(start_x,end_x):
                for y in range(start_y,end_y):
                    tile_x = chunk_world_x + x * TILE_SIZE
                    tile_y = chunk_world_y + y * TILE_SIZE

                    tile_texture = self.id_to_tile(chunk.tile_map[x,y])
                    screen.blit(tile_texture,(tile_x - dx, tile_y - dy))

    def id_to_tile(self, id):
        return self.tiles[int(id)]



class ChunkHandler:
    def __init__(self):
        self.active_chunks = {}
        self.passive_chunks = {}
        self.hold_range = 3
        self.save_path = "./chunks"

    def update(self, player_x, player_y, view_width, view_height, entityHandler):
        x_1, y_1 = self.get_chunk_from_coord(player_x - view_width / 2, player_y - view_height / 2)
        x_2, y_2 = self.get_chunk_from_coord(player_x + view_width / 2 + CHUNK_SIZE, player_y + view_height / 2 + CHUNK_SIZE)
        player_chunk_x, player_chunk_y = self.get_chunk_from_coord(player_x, player_y)

        visible_chunks = set()
        for i in range(x_1,x_2):
            for j in range(y_1, y_2):
                visible_chunks.add((i,j))

        #make not visible chunks passive
        for chunk_coord in list(self.active_chunks.keys()):
            if chunk_coord in visible_chunks:
                visible_chunks.remove(chunk_coord)
                continue
            self.make_chunk_passive(chunk_coord)

        #make passive chunks visible
        for chunk_coord in list(self.passive_chunks.keys()):
            if chunk_coord in visible_chunks:
                visible_chunks.remove(chunk_coord)
                self.make_chunk_active(chunk_coord)
                continue

        #any chunks in visible list need to be loaded
        for chunk_coord in visible_chunks:
            chunk = self.load_chunk(chunk_coord)
            entityHandler.add_entities_from_chunk(chunk)
            chunk.clear_entities()
            self.active_chunks[chunk_coord] = chunk

        #save chunks outside of hold_range
        for chunk_coord in list(self.passive_chunks.keys()):
            if abs(chunk_coord[0] - player_chunk_x) > self.hold_range:
                self.save_chunk(self.passive_chunks.pop(chunk_coord), entityHandler)
                continue
            if abs(chunk_coord[1] - player_chunk_y) > self.hold_range:
                self.save_chunk(self.passive_chunks.pop(chunk_coord), entityHandler)
                continue

    def save_chunk(self, chunk, entityHandler):
        chunk.clear_entities()
        entityHandler.store_entities_in_chunk(chunk)
        print("SAVE",chunk.chunk_x,chunk.chunk_y,len(chunk.entities))
        name = "chunk_" + str(chunk.chunk_x) + "_" + str(chunk.chunk_y)
        with open(os.path.join(self.save_path, name), 'wb') as file:
            pickle.dump(chunk, file)

    def load_chunk(self, coord):
        try:
            name = "chunk_" + str(coord[0]) + "_" + str(coord[1])
            with open(os.path.join(self.save_path, name), 'rb') as file:
                chunk = pickle.load(file)
            print("LOAD",chunk.chunk_x,chunk.chunk_y,len(chunk.entities))
        except:
            chunk = Chunk(coord[0],coord[1])
        return chunk

    def make_chunk_active(self, coord):
        chunk = self.passive_chunks.pop(coord)
        self.active_chunks[(chunk.chunk_x,chunk.chunk_y)] = chunk

    def make_chunk_passive(self, coord):
        chunk = self.active_chunks.pop(coord)
        self.passive_chunks[(chunk.chunk_x,chunk.chunk_y)] = chunk

    def get_chunk_from_coord(sefl, world_x, world_y):
        return math.floor(world_x/CHUNK_SIZE), math.floor(world_y/CHUNK_SIZE)

class Chunk:
    def __init__(self, chunk_x, chunk_y):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.tile_map = np.zeros((TILES_PER_CHUNK,TILES_PER_CHUNK))
        self.entities = []

        self.tile_map[0:10,0:10] = 11

        self.tile_map[5,5] = 33
        self.tile_map[6,5] = 43
        self.tile_map[7,5] = 134
        self.tile_map[8,5] = 53

        self.tile_map[5,4] = 2
        self.tile_map[6,4] = 12
        self.tile_map[7,4] = 12
        self.tile_map[8,4] = 22

        self.tile_map[5,3] = 0
        self.tile_map[6,3] = 10
        self.tile_map[7,3] = 10
        self.tile_map[8,3] = 20

    def entity_in_chunk(self, entity):
        if self.chunk_x * CHUNK_SIZE <= entity.x and entity.x < (self.chunk_x + 1) * CHUNK_SIZE:
            if self.chunk_y * CHUNK_SIZE <= entity.y and entity.y < (self.chunk_y + 1) * CHUNK_SIZE:
                return True

    def clear_entities(self):
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)
