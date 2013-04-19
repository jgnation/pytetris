__author__ = 'elmariachi'

import os, sys, pygame
from pygame.locals import *
from Globals import Globals
from Piece import Piece

class ZPiece(Piece):
    def __init__(self):
        self.orientation = 1
        self.color = (255, 0, 5)
    def rotate(self):
        if self.orientation == 1:
            self.orientation = 2
        elif self.orientation == 2:
            self.orientation = 1
        self.y_start_pos -= Globals.block_height  #todo
        self.update()
    def update(self):
        super(ZPiece, self).update()
        x = self.x_start_pos
        y = self.y_start_pos
        width = self.width
        height = self.height
        if self.orientation == 1:
            self.block_coordinates = ({'x': x, 'y': y+height},
                                          {'x': x+width, 'y': y+height},
                                          {'x': x+width, 'y': y+height*2},
                                          {'x': x+width*2, 'y': y+height*2})
            self.total_width = width*3
        if self.orientation == 2:
            self.block_coordinates = ({'x': x, 'y': y+height*2},
                                          {'x': x+width, 'y': y},
                                          {'x': x+width, 'y': y+height},
                                          {'x': x, 'y': y+height})
            self.total_width = width*2