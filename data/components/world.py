from .tiles import Tile


class World(object):
    def __init__(self):
        self.grid = {}
        for x in prepare.tile_map:
            i, j = x[0]
            grid[i, j] = Tile((i*64, j*64), x[1])
        self.obstacles = [obst[0](obst[1]) for obst in prepare.obstacles]
            
            
    def draw(self, surface):
        for tile in self.grid.values():
            tile.draw(surface)

    def move(self, offset):
        for tile in self.grid.values():
            tile.move(offset)
    
        