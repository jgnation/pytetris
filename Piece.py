__author__ = 'elmariachi'

import os, sys, pygame
from Globals import Globals
from pygame.locals import *

class Piece(object):
    width = Globals.block_width                     #width of individual block within piece
    height = Globals.block_height                   #height of individual block within piece
    total_width = 0                                 #total width of piece in given orientation
    x_start_pos = (Globals.screen_width / 2) - 40   #this may need to be adjusted if screen/block size changes
    y_start_pos = -Globals.block_height*2      #update will be called before this is drawn, which will increment to 0
    block_coordinates = ()
    orientation = 1
    def __init__(self):
        pass
#        width=20
#        height=20
#        x_start_pos = 0
#        y_start_pos = 0
    def update(self):
        self.y_start_pos += self.height
    def move_left(self):
        if self.x_start_pos > 0:
            self.x_start_pos -= self.width
            for pair in self.block_coordinates:
                pair['x'] -= self.width
    def move_right(self):
        if self.x_start_pos + self.total_width < Globals.screen_width:
            self.x_start_pos += self.width
            for pair in self.block_coordinates:
                pair['x'] += self.width
    def draw(self, screen):
        for pair in self.block_coordinates:
            Globals.drawBlock(screen, self.color, pair)
        pygame.display.update()
    def getBlockCoordinates(self):
        return self.block_coordinates
    def getBlockCoordinatesAndColors(self):
        for coord in self.block_coordinates:
            coord['color'] = self.color
        return self.block_coordinates
    def getNextCoordinates(self): #get coordinates of block after next drop
        next_coordinates = []
        for pair in self.block_coordinates:
            next_coordinates.append({'x': pair['x'], 'y': pair['y'] + self.height})
        return next_coordinates
    def getCurrentCoordinates(self):
        current_coordinates = []
        for pair in self.block_coordinates:
            current_coordinates.append({'x': pair['x'], 'y': pair['y']})
        return current_coordinates
    def setCoordinates(self, coordinates):
        self.block_coordinates = coordinates
    def getOrientation(self):
        return self.orientation
    def setOrientation(self, orientation):
        self.orientation = orientation

