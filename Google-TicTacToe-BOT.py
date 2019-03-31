from pyautogui import *
from random import *
import pyscreenshot as ImageGrab
import numpy as np
import cv2
from time import *

class theToughChoice:
    # The bot can choose between X or O (the game screen chords for that written below)
    playerChoose = [[416,340],[619,339]]

    ranChoice = randint(0,1)
    # A random choice between X or O
    playerChoosed = playerChoose[ranChoice]

    if ranChoice == 0:
        print('You chose: X')
        click(playerChoose[ranChoice])
    else:
        print('You chose: O')
        click(playerChoose[ranChoice])

class playableArea:
    # The playable area, where the game interaction can be done ie. placing a X or O
    
    playHere = [
        [460, 444], [533, 444], [600, 444],
        [460, 514], [532, 515], [600 , 514],
        [460, 589], [530, 585], [600, 589],
    ]

class boxChords:
    # The game screen
    box =[405,402,645,616]
    # OpenCV stuffs - getting the screen, and converting it into Grayscale img for processing
    gameScreenRGB = np.array(ImageGrab.grab(bbox=box))
    gameScreenBGR = cv2.cvtColor(gameScreenRGB, cv2.COLOR_RGB2BGR)
    gameScreenGRAY = cv2.cvtColor(gameScreenBGR, cv2.COLOR_BGR2GRAY)



class CheckXorO(boxChords, playableArea):

    o = cv2.imread('o.jpg', 0)
    x = cv2.imread('x.jpg', 0)
    wO, hO = o.shape[::-1]
    wX, hX = x.shape[::-1]

    # Matching the game screen to O.jpg
    resO = cv2.matchTemplate(boxChords.gameScreenGRAY, o, cv2.TM_CCOEFF_NORMED)
    # Matching the game screen to X.jpg
    resX = cv2.matchTemplate(boxChords.gameScreenGRAY, x, cv2.TM_CCOEFF_NORMED)

    threshold = 0.5

    # Finding the loc and drawing of O
    locO = np.where(resO >= threshold)
    # Drawing a rectangle, where there is O
    for pt in zip(*locO[::-1]):
        # [ OPTIONAL ]cv2.rectangle(boxChords.gameScreenRGB, pt,(pt[0] + wO, pt[1] + hO), (0, 0, 255), 2)
        
        # Getting Centre of O img on the screen
        new_W_O = pt[0] + wO - 25
        new_H_O = pt[1] + hO - 25
        
        # [OPTIONAL ] cv2.circle(boxChords.gameScreenRGB, (new_W_O, new_H_O), 2, (255, 0, 0))
        
        # checking if the cords lies in the playable area so that we can remove it from the list
        clickXcord, clickYcord = boxChords.box[0] + new_W_O, boxChords.box[1] + new_H_O
                
        if [clickXcord, clickYcord] in playableArea.playHere:
            print(clickXcord, clickYcord, ' is here!')
            playableArea.playHere.remove([clickXcord, clickYcord])


    # Finding the loc and drawing of X
    locX = np.where(resX >= threshold)
    for pt in zip(*locX[::-1]):
        # [OPTIONAL]cv2.rectangle(boxChords.gameScreenRGB, pt,(pt[0] + wX, pt[1] + hX), (0, 255, 255), 2)
        new_W_X = pt[0] + wX - 25
        new_H_X = pt[1] + hX - 25

        # [OPTIONAL]cv2.circle(boxChords.gameScreenRGB, (new_W_X, new_H_X), 2, (255, 0, 0))
        # checking if the cords lies in the playable area so that we can remove it from the list

        clickXcord, clickYcord = boxChords.box[0] + new_W_X, boxChords.box[1] + new_H_X

        if [clickXcord, clickYcord] in playableArea.playHere:
            print(clickXcord, clickYcord, ' is here!')
            playableArea.playHere.remove([clickXcord, clickYcord])


class GameOver(boxChords):

    winner = cv2.imread('winner.png', 0)
    w, h = winner.shape[::-1]

    res = cv2.matchTemplate(boxChords.gameScreenGRAY,
                            winner, cv2.TM_CCOEFF_NORMED)

    threshold = 0.5

    loc = np.where(res >= threshold)

    

class plays(theToughChoice, CheckXorO, GameOver):
    
    i = 7

    while i != 0:
        # Randomly click on any box on the grid
        clickable = choice(playableArea.playHere)
        sleep(2)
        
        click(clickable[0], clickable[1], 1)
        # then removing the recently cords from the list, so we can always try the new ones 
        playableArea.playHere.remove(clickable)
        
        i -= 1


playys = plays()

'''
The cords will be depending on the resolution of screen!
'''
