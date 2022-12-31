import copy
from field import Field

def get_deepcopy(arr):
    new_grid = [[field for field in row] for row in arr]
    return new_grid

def get_deepcopy2(arr):
    return copy.deepcopy(arr)

def getEmptyTileArray(w, h):
    tiles = []
    row = []
    for j in range(h):
        row = []
        for i in range(w):
            row.append(Field([[1,0], [1,1]]))
        tiles.append(row.copy())
    return tiles

tileMap = getEmptyTileArray(2,2)
map = get_deepcopy(tileMap)
map[0][0].possibleStates[0][0] = 2
print(tileMap[0][0].possibleStates[0][0])