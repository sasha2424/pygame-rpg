import numpy as np

class TileType:
    """
    Each function takes tile types, constructs a corresponding tile object, and returns it
    """
    def get_surface(adj_types, adj_heights_relative):
        # Order of up right down left
        pass

    def get_side():
        pass

    def get_side_bottom(type_left, type_right, type_bottom):
        pass

    def get_side_top():
        pass

    def get_side_single(type_left, type_right, type_bottom):
        pass


def get_tile_type_from_id(id):
    if id == 0:
        return GrassTile
    return GrassTile

class Tile:
    def __init__(self, texture_id):
        self.texture_id = texture_id
        self.original_y = None

    def get_texture_id(self):
        return self.texture_id

class GrassTile:
    def get_surface(adj_types, adj_heights_relative):
        # Order of up right down left
        c = sum((adj_heights_relative < 0)*np.array([1,2,4,8]))
        id_dict = [11,10,21,20,12,23,22,24,1,0,3,13,2,4,15,14]
        if not id_dict[c] == 11:
            print(id_dict[c])
        return Tile(id_dict[c])

    def get_side():
        return Tile(42)

    def get_side_bottom(type_left, type_right, type_bottom):
        return Tile(42)

    def get_side_top():
        return Tile(42)

    def get_side_single(type_left, type_right, type_bottom):
        return Tile(42)
