import numpy as np


"""
Depricated

"""

class Tile:
    def get_tile(id):
        if id == 1:
            return Grass_Tile
        return Grass_Tile

    def get_texture_ids(tile, adjacent_relative_heights):
        edges = np.abs(adjacent_relative_heights < 0)
        num = edges[0]
        for b in edges[1:]:
            num = 2*num + b
        return tile.textures[num], tile.side


class Grass_Tile:
    textures = [11,1,12,2,21,3,22,15,10,0,23,4,20,13,24,14]
    side = 42
