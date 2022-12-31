import copy

class ChangeHistory:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y

    def save_tileMap(self, tileMap):
        x = self.x
        y = self.y

        self.prevCenter = copy.deepcopy(tileMap[y][x])

        if(y > 0):
            self.prevNorth = copy.deepcopy(tileMap[y-1][x])

        if(x < len(tileMap[0])-1):
            self.prevEast = copy.deepcopy(tileMap[y][x+1])

        if(y < len(tileMap)-1):   
            self.prevSouth = copy.deepcopy(tileMap[y+1][x])

        if(x > 0):
            self.prevWest = copy.deepcopy(tileMap[y][x-1])

    def revert_tileMap(self, tileMap):
        x = self.x
        y = self.y

        tileMap[y][x] = self.prevCenter

        if(y > 0):
            tileMap[y-1][x] = self.prevNorth

        if(x < len(tileMap[0])-1):
            tileMap[y][x+1] = self.prevEast

        if(y < len(tileMap)-1):   
            tileMap[y+1][x] = self.prevSouth

        if(x > 0):
            tileMap[y][x-1] = self.prevWest

