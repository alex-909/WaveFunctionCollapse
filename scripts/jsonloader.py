import json
from tile import Tile

def json_to_tile_array(json_file):
    print(json_file)
    f = open(json_file)
    data = json.load(f)

    tiles = []
    count = data["count"]
    for i in range(count):
        dict = data["tiles"][i]
        tile = Tile(dict["id"], dict["north"], dict["east"], dict["south"], dict["west"])
        tiles.append(tile)
    return tiles

def number_of_tiles(json_file):
    print(json_file)
    f = open(json_file)
    data = json.load(f)
    return data["count"]