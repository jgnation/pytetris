__author__ = 'elmariachi'

import os, sys, pygame
from pygame.locals import *

class Globals(object):
    window_width = 640
    window_height = 480
    screen_width = 200
    screen_height = 480
    block_width = block_height = 20

    @staticmethod
    def drawBlock(screen, color, coord_pair):
        #draw a filled in, colored rectangle.  Draw over it with another rectangle with a small border
        pygame.draw.rect(screen, color, (coord_pair['x'], coord_pair['y'], Globals.block_width, Globals.block_height), 0)
        pygame.draw.rect(screen, (0,0,0), (coord_pair['x'], coord_pair['y'], Globals.block_width, Globals.block_height), 2)