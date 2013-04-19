__author__ = 'elmariachi'

#http://stackoverflow.com/questions/6318814/how-can-i-tell-pycharm-what-type-a-parameter-is-expected-to-be
#http://www.pygame.org/docs/
#http://youtrack.jetbrains.com/issue/PY-2197?query=8
#http://en.wikipedia.org/wiki/Tetris
#inheritance: http://www.daniweb.com/software-development/python/code/216596/a-simple-class-inheritance-example-python

import os, sys, pygame
from pygame.locals import *

#some tutorials had the following two lines.  I'm not sure if it is common for font/mixer to be unavailable?
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from random import randint
from IPiece import IPiece
from JPiece import JPiece
from LPiece import LPiece
from OPiece import OPiece
from SPiece import SPiece
from TPiece import TPiece
from ZPiece import ZPiece
from Globals import Globals

def getNewPiece():
    #store reference to piece classes
    pieces = (IPiece, JPiece, LPiece, OPiece, SPiece, TPiece, ZPiece)
    index = randint(0, len(pieces) - 1)
    return pieces[index]()      #execute piece constructor

#check to see if piece hit bottom of the screen
def checkBottom(next_coordinates):
    bottom = False
    for coord in next_coordinates:
        if coord['y'] >= Globals.screen_height:
            bottom = True
    return bottom

def gameOver(occupied_blocks, current_coordinates):
    gameOver = False
    for block in occupied_blocks:
        for coord in current_coordinates:
            if block['x'] == coord['x'] and block['y'] == coord['y']:
                gameOver = True
                break                   #Game Over!
        if gameOver == True:
            break
    return gameOver

#based on the next_coordinates of a piece (i.e., if one more update occurred),
#check to see if it would result in overlapping another piece
def checkOverlap(occupied_blocks, next_coordinates):
    overlap = False
    for block in occupied_blocks:
        for coord in next_coordinates:
            if block['x'] == coord['x'] and block['y'] == coord['y']:
                overlap = True
    return overlap

#todo: change references to 20 in here to use Global values
def checkForFullRow(background, occupied_blocks, screen, piece):
    #check occupied_blocks for full row
    block_positions = piece.getCurrentCoordinates()
    #min_position is the top of the highest sub_block in the piece that was just placed
    min_position = min([x['y'] for x in block_positions])

    for y in range(Globals.screen_height, min_position, -20): #start at bottom of screen and move up
        if len([x for x in occupied_blocks if x['y'] == y]) == 10:
            #at this point a row has been filled and I need to delete it
            occupied_blocks[:] = [x for x in occupied_blocks if x['y'] != y] #using a slice to modify list in place
            #now move the blocks ABOVE the deleted row down a notch
            for block in occupied_blocks: #look for more elegant way to do this
                if block['y'] < y:
                    block['y'] += 20

            #the items have been deleted from occupied_blocks....now redraw everything
            background.fill((255,255,255))
            screen.blit(background, (0,0))
            for block in occupied_blocks:
                #draw a filled in, colored rectangle.  Draw over it with another rectangle with a small border
                pygame.draw.rect(screen, block['color'], (block['x'], block['y'], Globals.block_width, Globals.block_height), 0)
                pygame.draw.rect(screen, (0,0,0), (block['x'], block['y'], Globals.block_width, Globals.block_height), 2)
            pygame.display.update()
            background = screen.copy()
            #every row above the deleted row has now been moved down.  Now, y needs to be reset
            y += 20
            pygame.time.delay(4000)
    return background

def start_game():
    pygame.init() #pretty much do this before any pygame stuff

    screen = pygame.display.set_mode((Globals.screen_width, Globals.screen_height))
    pygame.display.set_caption('PyTetris by JGNation')

    #this is always necessary to create a filled background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))
    screen.blit(background, (0,0)) #why is this necessary here?
    pygame.display.update() #this must be called before any changes can be made!

    occupied_blocks = []
    timeDelay = 500
    piece = getNewPiece()

    #game loop start
    while True:

        for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)):
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    timeDelay = 50
                elif event.key == pygame.K_LEFT:
                    piece.move_left()
                elif event.key == pygame.K_RIGHT:
                    piece.move_right()
                elif event.key == pygame.K_SPACE:
                    piece.rotate()
            elif event.type == pygame.KEYUP:
                timeDelay = 500

        #check to see if piece is going to be drawn on another piece, resulting in Game Over
        current_coordinates = piece.getCurrentCoordinates()
        if gameOver(occupied_blocks, current_coordinates):
            break

        #check to see if piece is sitting on top of another piece
        next_coordinates = piece.getNextCoordinates()
        overlap = checkOverlap(occupied_blocks, next_coordinates)

        #check to see if piece is touching the bottom of the screen
        bottom = checkBottom(next_coordinates)

        if overlap == True or bottom == True:
            block_coordinates = piece.getBlockCoordinatesAndColors()
            for coord in block_coordinates:
                occupied_blocks.append(coord)   #add the piece to the occupied_blocks list
            background = screen.copy()          #update the state of the background

            #occupied_blocks may be changed in the following method
            background = checkForFullRow(background, occupied_blocks, screen, piece)
            #why did background have to be explicitly returned from the method instead of modified through the reference?

            piece = getNewPiece()
        else:
            screen.blit(background, (0,0)) #this reloads the original background - basically erases it
            piece.draw(screen)
            piece.update() #update the piece's position internally

        pygame.time.delay(timeDelay)

    pygame.time.delay(3000) #executed at end of game

start_game() #game is started here




#todo: major!
#make sure rotate is legal (make sure it won't overlap another piece OR go off the screen)
#gravity!
#cleanup the deleting row code
#row deletion only works for a single row
#note, I dropped in a piece that should have deleted two rows.  On the next piece, which didn't create a new deletions,
#the old row that should have been previously deleted was deleted

#todo: minor!
#cleanup end of game handling
#make points, count rows eliminated, make cleaner gui


#i am removing buffers on left side of pieces.....buffers can be added in piece's rotate method

#to check legal rotate:
#I can probably move the updating of self.coordinates in each piece from the draw() method to rotate()



