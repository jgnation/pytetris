__author__ = 'elmariachi'

import os, sys, pygame


from Piece import Piece
from Globals import Globals

class SPiece(Piece):
    def __init__(self):
        #super(SBlock, self).__init__()
        self.orientation = 1
        self.color = (153, 255, 0)
    def rotate(self):
        if self.orientation == 1:
            self.orientation = 2
        elif self.orientation == 2:
            self.orientation = 1
        self.y_start_pos -= Globals.block_height  #todo
        self.update()
    def update(self):
        super(SPiece, self).update()
        x = self.x_start_pos
        y = self.y_start_pos
        width = self.width
        height = self.height
        if self.orientation == 1:
            self.block_coordinates = ({'x': x+width, 'y': y+height},
                                          {'x': x+width*2, 'y': y+height},
                                          {'x': x, 'y': y+height*2},
                                          {'x': x+width, 'y': y+height*2})
            self.total_width = width*3
        if self.orientation == 2:
            self.block_coordinates = ({'x': x, 'y': y+height},
                                          {'x': x+width, 'y': y+height},
                                          {'x': x+width, 'y': y+height*2},
                                          {'x': x, 'y': y})
            self.total_width = width*2
#    def draw(self, screen):
#        #self.width, self.height, etc. are defined in Piece
#        x = self.x_start_pos
#        y = self.y_start_pos
#        width = self.width
#        height = self.height
#        if self.orientation == 1:
#            self.block_coordinates = ({'x': x+width, 'y': y+height},
#                                      {'x': x+width*2, 'y': y+height},
#                                      {'x': x, 'y': y+height*2},
#                                      {'x': x+width, 'y': y+height*2})
#            self.total_width = width*3
#        if self.orientation == 2:
#            self.block_coordinates = ({'x': x, 'y': y+height},
#                                      {'x': x+width, 'y': y+height},
#                                      {'x': x+width, 'y': y+height*2},
#                                      {'x': x, 'y': y})
#            self.total_width = width*2
#        self._drawPiece(screen)
#        pygame.display.update()

