__author__ = 'elmariachi'

from Game import Game
from Game_backup import Game2
import os, sys, pygame
from pygame.locals import *
from Globals import Globals


#pygame.init() #pretty much do this before any pygame stuff
#
#game_screen = pygame.display.set_mode((640, 480))
#pygame.display.set_caption('PyTetris by JGNation')
#
##this is always necessary to create a filled background
#background = pygame.Surface((Globals.screen_width, Globals.screen_height))
#background = background.convert()
#background.fill((255,255,255))
#game_screen.blit(background, (100,0)) #why is this necessary here?
#pygame.display.update() #this must be called before any changes can be made!
#
#pygame.time.delay(3000)
#
#
##this works                            #the coordinates here are relative to the SURFACE
#pygame.draw.rect(background, (0,0,0), (0, 100, 20, 20), 0)
#game_screen.blit(background, (100,0))
#pygame.display.update() #update must be called after drawing, otherwise we will never see it
#
##this works
##pygame.draw.rect(game_screen, (0,0,0), (150, 100, 20, 20), 0)
##pygame.display.update()
#
##this doesn't work
##pygame.draw.rect(background, (0,0,0), (150, 100, 20, 20), 0)
##pygame.display.update()


#pygame.time.delay(3000)

game = Game()
game.start_game()


