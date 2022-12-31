import cv2
import numpy as np

def printTileMap(tileMap, path):

    global tileWidth
    print(path)
    tile = cv2.imread(path + "\img1.png")
    tw = tile.shape[0]
    number = 0
    h = len(tileMap)
    w = len(tileMap[0])


    img = np.zeros((h*tw,w*tw,3), np.uint8)

    for i in range(w):
        for j in range(h):
            field = tileMap[j][i]
            
            try:
                id = field.get_id()
                rotation = field.get_rotation()
                tile = cv2.imread(path + "\img" + str(id) + ".png")
            except:
                rotation = 0
                tile = cv2.imread(path + "\empty.png")
            
            if(rotation == 1):
                tile = cv2.rotate(tile, cv2.ROTATE_90_CLOCKWISE)
            if(rotation == 2):
                tile = cv2.rotate(tile, cv2.ROTATE_180)
            if(rotation == 3):
                tile = cv2.rotate(tile, cv2.ROTATE_90_COUNTERCLOCKWISE)
            if(not field.isCollapsed):
                tile = cv2.imread(path + "\empty.png")
            xOff = i * tw
            yOff = j * tw
            img[yOff:yOff+tw, xOff:xOff+tw] = tile[0:tw, 0:tw]
    
    file = "output/output" + str(number) + ".png"
    cv2.imwrite(file, img)
    number = number + 1
    #cv2.imshow("yay", img)
    #cv2.waitKey()