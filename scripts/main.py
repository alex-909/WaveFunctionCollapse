from tile import Tile
from field import Field
from changehistory import ChangeHistory
import imagecreator
import jsonloader

import random
import shutil
import os
import math 
import copy
from collections import deque

tileSet = []
tileWidth = 0


def getEmptyTileArray(w, h, n):
    tiles = []
    row = []
    for j in range(h):
        row = []
        for i in range(w):
            arr = []
            for a in range(n):
                arr.append([a+1,0])
                arr.append([a+1,1])
                arr.append([a+1,2])
                arr.append([a+1,3])
            row.append(Field(arr))
        tiles.append(row.copy())
 
    return tiles


def collapseSingle(tileMap, x, y):
    field = tileMap[y][x]
    field.isCollapsed = True
    #print("possible States")
    #print("x: {0} y: {1}".format(x,y))
    #print(field.possibleStates)

    if(field.number_of_states() == 1):
        return tileMap

    state = random.choice(field.possibleStates)
    field.collapse(state)

    tileMap[y][x] = field
    return tileMap


def update_single_neighbor(tileStates, tileMap, x:int, y:int):
    neighbor = tileMap[y][x]

    if(neighbor.isCollapsed):
        return tileMap

    updatedStates = []
    for state in neighbor.possibleStates:
        if(state in tileStates):
            updatedStates.append(state)

    neighbor.set_states(updatedStates)
    #print(neighbor.possibleStates)
    tileMap[y][x] = neighbor
    return tileMap

def get_tile_states(id, rotation):
    global tileSet
    _tileSet = copy.deepcopy(tileSet)
    tiles = []
    index = [0,1,2,3]
    r = rotation
    for i in index:
        dir = _tileSet[id-1].allTiles[(i-r)%4]
        tiles.append(dir)

    #print(" ")
    #print("test1:")
    #print(tileSet[1].allTiles[0])
    
    for dir in tiles:
        for tile in dir:
            tile[1] = (tile[1]+r)%4

    #print("test2:")
    #print(tileSet[1].allTiles[0])

    return tiles

def updateNeighbors(tileMap, x, y):
    field = tileMap[y][x]
    id = field.get_id()
    rotation = field.get_rotation()
    
    tiles = get_tile_states(id, rotation)
    #print("origin: x:{0} y:{1} r:{2}".format(x,y, rotation))

    if(y > 0): #north
        tileMap = update_single_neighbor(tiles[0], tileMap, x, y-1)

    if(x < len(tileMap[0])-1): #east
        tileMap = update_single_neighbor(tiles[1], tileMap, x+1, y)

    if(y < len(tileMap)-1):   
        tileMap = update_single_neighbor(tiles[2], tileMap, x, y+1)

    if(x > 0):
        tileMap = update_single_neighbor(tiles[3], tileMap, x-1, y)

    #number_of_collapsed(tileMap)
    #show_collapsed(tileMap)

    return tileMap

def nearest_to_collapse(indexes, collapsed):
    #pick first to collapse
    r = 0
    x = indexes[r][1]
    y = indexes[r][0]
    
    
    return x,y

    #find nearest to collapse
    x_sum = 0
    y_sum = 0
    l = len(collapsed)
    for pos in collapsed:
        x_sum += float(pos[1])
        y_sum += float(pos[0])
    x_m = x_sum / l
    y_m = y_sum / l

    min_dist = 100000

    for pos in indexes:
        a_squared = (x_m - pos[1])*(x_m - pos[1])
        b_squared = (y_m - pos[0])*(y_m - pos[0])
        dist = math.sqrt(a_squared + b_squared)
        if dist < min_dist:
            min_dist = dist
            x = pos[1]
            y = pos[0]
    return x,y

def collapseFull(tileMap):

    stack = deque()
    done = False
    w = len(tileMap[0])
    h = len(tileMap)
    changes = ChangeHistory(0, 0, w, h)

    stuck_iteration = 0
    current_iteration = 0
    reset_amount = 0

    while(not done):
        n = 0
        done = True
        lowestEntrophy = 1000000
        collapsed = []
        #print("new loop")
        for i in range(w):
            for j in range(h):
                field = tileMap[j][i]
                t = "i: {0}, j: {1}".format(i,j)
                entrophy = field.number_of_states()
                if(not field.isCollapsed):
                    done = False
                    if(entrophy < lowestEntrophy):
                        lowestEntrophy = entrophy
                else:
                    collapsed.append([j,i])

        if done:
            break

        print(number_of_collapsed(tileMap))
        indexes = []
        for i in range(w):
            for j in range(h):
                field = tileMap[j][i]
                if(not field.isCollapsed and lowestEntrophy == field.number_of_states()):
                    indexes.append([j,i])
        

        x,y = nearest_to_collapse(indexes, collapsed)

        # see we are stuck:
        # at lower than thresh:
            # set thresh to current
            # counter to 1
            # reset 1 step

        # at higher than current:
            # set thresh to thresh
            # counter to 1
            # reset 1 step
        
        # at thresh again
            # set counter++
            # reset counter steps


        current_iteration = len(collapsed)
        
        if(tileMap[y][x].number_of_states() == 0):
            if(current_iteration < stuck_iteration):
                stuck_iteration = current_iteration
                reset_amount = 1

            elif(current_iteration > stuck_iteration):
                stuck_iteration = current_iteration
                reset_amount = 1

            elif(current_iteration == stuck_iteration):
                stuck_iteration = current_iteration
                reset_amount += 1

            for i in range(reset_amount):
                changes = stack.pop()
                changes.revert_tileMap(tileMap)
                n += 1

            continue
        
        changes = ChangeHistory(x, y, w, h)
        changes.save_tileMap(tileMap)
        stack.append(changes)

        tileMap = collapseSingle(tileMap, x, y)
        tileMap = updateNeighbors(tileMap, x, y)
        #printTileMap(tileMap)

    print(n)
    return tileMap

def number_of_collapsed(tileMap):
    w = len(tileMap[0])
    h = len(tileMap)
    n = 0
    for i in range(w):
            for j in range(h):
                field = tileMap[j][i]
                if(field.isCollapsed):
                    n = n+1
    print("collapsed: {0}/{1}".format(n, w*h))


def show_collapsed(tileMap):
    w = len(tileMap[0])
    h = len(tileMap)
    for j in range(h):
        s = ""
        for i in range(w):
            field = tileMap[j][i]
            if(field.isCollapsed):
                s += "1"
            else:
                s+= "."
        print(s)

def clear_output():
    # location
    path = "D:\Projects\WaveFunctionCollapse\output"
 
    # removing directory
    shutil.rmtree(path)
    os.mkdir(path)

#main method:

clear_output()

path = r"D:\Projects\WaveFunctionCollapse"
folder = r"\sourceTiles2"

json_file = path + folder + "\info.json"

tileSet = jsonloader.json_to_tile_array(json_file)
n = jsonloader.number_of_tiles(json_file)

w = 10
h = 10

tileWidth = 8

tileMap = "failed"
while(tileMap == "failed"):
    print("again")
    tileMap = getEmptyTileArray(w, h, n)    
    tileMap = collapseFull(tileMap)

print("done") 
imagecreator.printTileMap(tileMap, path + folder)