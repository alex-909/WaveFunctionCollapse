class Tile:
    def __init__(self, id, northTiles, eastTiles, southTiles, westTiles):
        self.id = id

        self.northTiles = northTiles
        self.eastTiles = eastTiles
        self.southTiles = southTiles
        self.westTiles = westTiles

        self.allTiles = []
        self.allTiles.append(northTiles)
        self.allTiles.append(eastTiles)
        self.allTiles.append(southTiles)
        self.allTiles.append(westTiles)

        self.rotation = 0
    