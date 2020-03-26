from spritesheet.SpriteSheet import SpriteSheet
from spritesheet.Animation import Animation
from Utils import *
import pygame

import numpy as np
import math

import pickle
import os

from terrain.Tiles import *
from entities.Entity import Box #used for terrain collision

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
                    tile_texture = self.texture_from_id(chunk.tile_map[x,y])

                    screen.blit(tile_texture,(tile_x - dx, tile_y - dy))

    def texture_from_id(self,id):
        return self.tiles[id]


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
        chunk.wipe_cache()
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
            chunk.reset_cache()
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

    def get_chunk(self, world_x, world_y):
        chunk_loc = self.get_chunk_from_coord(world_x, world_y)
        if chunk_loc in self.active_chunks:
            return self.active_chunks[chunk_loc]
        return None

class Chunk:
    def __init__(self, chunk_x, chunk_y):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.tile_map = np.zeros((TILES_PER_CHUNK,TILES_PER_CHUNK), dtype='int')
        self.height_map = np.zeros((TILES_PER_CHUNK,TILES_PER_CHUNK), dtype='int')

        self.tile_map.fill(11)

        self.tile_map[5,5] = 14
        self.tile_map[5,6] = 42

        self.height_map[5,5] = 1
        self.height_map[5,6] = 1

        self.entities = []

        self.collision_cache = {}


    def get_collision_box_for_height(self, z):
        z = int(z)
        if z in self.collision_cache.keys():
            return self.collision_cache[z]

        world_x = self.chunk_x * CHUNK_SIZE
        world_y = self.chunk_y * CHUNK_SIZE

        collisionBox = []

        for x in range(self.height_map.shape[0]):
            for y in range(self.height_map.shape[1]):
                #don't need a collision box for terrain at same height
                if self.height_map[x,y] == z:
                    continue

                # check if this tile needs a collision box
                # if it is at the edge of a chunk it needs a box
                # if it has a neighbor of a different height needs a box
                need_collision_box = True
                for loc in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if loc[0] < 0 or x >= self.height_map.shape[0]:
                        need_collision_box = False
                        break
                    if y < 0 or y  >= self.height_map.shape[1]:
                        need_collision_box = False
                        break
                    if not self.height_map[x,y] == self.height_map[loc[0],loc[1]]:
                        need_collision_box = False
                        break

                b = Box(None, world_x + x * TILE_SIZE, world_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE, True)
                collisionBox.append(b)
        self.collision_cache[z] = collisionBox
        return collisionBox



    def wipe_cache(self):
        self.collision_cache = None

    def reset_cache(self):
        self.collision_cache = {}

    def get_adjacent_relative_heights(self, x, y, active_chunks):
        # get all adjacent heights
        ret = [self.get_adjacent_tile_height(*t,active_chunks) for t in [(x,y-1), (x+1,y), (x,y+1), (x-1,y)]]
        #if array has None values then we are at a chunk border that has not
        #been loaded. We assume the default height and toggle the no_cache flag.
        #This way we will try again at the next tick. It is likely that the chunk
        #will be loaded in

        no_cache = None in ret
        ret = [self.height_map[x,y] if v is None else v for v in ret]
        ret = np.array(ret)

        #convert to -1, 0, 1 based
        ret = (ret - self.height_map[x,y]).astype(int)
        return np.array(ret), no_cache

    """
    Here we are assuming that the adjacent tiles are all loaded
    """
    def get_adjacent_heights(self, x, y, active_chunks):
        # get all adjacent heights
        ret = [self.get_tile_height(*t,active_chunks) for t in [(x,y-1), (x+1,y), (x,y+1), (x-1,y)]]
        return np.array(ret)

    def get_tile_height(self, x, y, active_chunks):
        if 0 <= x and x < TILES_PER_CHUNK:
            if 0 <= y and y < TILES_PER_CHUNK:
                return self.height_map[x,y]

        fetch_chunk_x = self.chunk_x + x // TILES_PER_CHUNK
        fetch_chunk_y = self.chunk_y + y // TILES_PER_CHUNK
        fetch_x = x % TILES_PER_CHUNK
        fetch_y = y % TILES_PER_CHUNK
        for chunk in active_chunks:
            if chunk.chunk_x == fetch_chunk_x and chunk.chunk_y == fetch_chunk_y:
                return chunk.height_map[fetch_x,fetch_y]

        return None

    def entity_in_chunk(self, entity):
        if self.chunk_x * CHUNK_SIZE <= entity.x and entity.x < (self.chunk_x + 1) * CHUNK_SIZE:
            if self.chunk_y * CHUNK_SIZE <= entity.y and entity.y < (self.chunk_y + 1) * CHUNK_SIZE:
                return True

    def clear_entities(self):
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)
