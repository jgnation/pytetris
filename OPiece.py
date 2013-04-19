__author__ = 'elmariachi'

import os, sys, pygame
from pygame.locals import *
from Globals import Globals
from Piece import Piece

class OPiece(Piece):
    def __init__(self):
        self.orientation = 1
        self.color = (200, 200, 100)
    def rotate(self):
        self.y_start_pos -= Globals.block_height  #todo
        self.update()
    def update(self):
        super(OPiece, self).update()
        x = self.x_start_pos
        y = self.y_start_pos
        width = self.width
        height = self.height
        self.block_coordinates = ({'x': x, 'y': y+height},
                                      {'x': x+width, 'y': y+height},
                                      {'x': x, 'y': y+height*2},
                                      {'x': x+width, 'y': y+height*2})
        self.total_width = width*2