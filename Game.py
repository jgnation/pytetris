__author__ = 'elmariachi'

import os, sys, pygame
from pygame.locals import *
import pygame.font

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

class Game(object):
    def __init__(self):
        pygame.init() #pretty much do this before any pygame stuff
        self.font = pygame.font.SysFont("Comic Sans MS", 25)

        self.display_splash()

        self.game_screen_color = (200,200,255)
        self.game_screen_start_x = (Globals.window_width - Globals.screen_width) / 2
        self.rows_eliminated = 0
        self.to_next_level = 0
        self.level = 1
        self.level_label = self.font.render("Level: " + str(self.level), 1, (255,255,255))
        self.rows_eliminated_label = self.font.render("Rows Eliminated: " + str(self.rows_eliminated), 1, (255,255,255))
        self.time_delay = 400
        self.current_time_delay = self.time_delay
        self.backup_delay = 0

    def start_game(self):

        game_screen = pygame.Surface((Globals.screen_width, Globals.screen_height))
        game_screen = game_screen.convert()

        pygame.display.set_caption('PyTetris by JGNation')

        #this is always necessary to create a filled background
        background = pygame.Surface(game_screen.get_size())
        background = background.convert()
        background.fill(self.game_screen_color)
        game_screen.blit(background, (0,0)) #why is this necessary here?
        self.window_screen.blit(game_screen, (self.game_screen_start_x,0))

        # put the label object on the screen at point x=100, y=100
        self.window_screen.blit(self.level_label, (450, 80))
        self.window_screen.blit(self.rows_eliminated_label, (450, 100))

        pygame.display.update() #this must be called before any changes can be made!

        occupied_blocks = []
        piece = self.getNewPiece()

        #game loop start
        while True:

            for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)):
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.current_time_delay = 50
                    elif event.key == pygame.K_LEFT:
                        piece.move_left()
                        current_coordinates = piece.getCurrentCoordinates()
                        overlap = self.checkOverlap(occupied_blocks, current_coordinates)
                        if overlap: piece.move_right()
                        game_screen.blit(background, (0,0))
                        piece.draw(game_screen)
                        self.window_screen.blit(game_screen, (self.game_screen_start_x,0))
                        continue
                    elif event.key == pygame.K_RIGHT:
                        piece.move_right()
                        current_coordinates = piece.getCurrentCoordinates()
                        overlap = self.checkOverlap(occupied_blocks, current_coordinates)
                        if overlap: piece.move_left()
                        game_screen.blit(background, (0,0))
                        piece.draw(game_screen)
                        self.window_screen.blit(game_screen, (self.game_screen_start_x,0))
                        continue
                    elif event.key == pygame.K_UP:
                        backup_coordinates = piece.getCurrentCoordinates()
                        backup_orientation = piece.getOrientation()
                        piece.rotate()
                        current_coordinates = piece.getCurrentCoordinates()
                        overlap = self.checkOverlap(occupied_blocks, current_coordinates)
                        if overlap:
                            piece.setCoordinates(backup_coordinates)
                            piece.setOrientation(backup_orientation)
                        else:
                            game_screen.blit(background, (0,0))
                            piece.draw(game_screen)
                            self.window_screen.blit(game_screen, (self.game_screen_start_x,0))
                elif event.type == pygame.KEYUP:
                    self.current_time_delay = self.time_delay

            #check to see if piece is going to be drawn on another piece, resulting in Game Over
            current_coordinates = piece.getCurrentCoordinates()
            if self.gameOver(occupied_blocks, current_coordinates):
                break

            #check to see if piece is sitting on top of another piece
            next_coordinates = piece.getNextCoordinates()
            overlap = self.checkOverlap(occupied_blocks, next_coordinates)

            #check to see if piece is touching the bottom of the screen
            bottom = self.checkBottom(next_coordinates)

            if overlap == True or bottom == True:
                block_coordinates = piece.getBlockCoordinatesAndColors()
                for coord in block_coordinates:
                    occupied_blocks.append(coord)       #add the piece to the occupied_blocks list
                background = game_screen.copy()              #update the state of the background

                #occupied_blocks may be modified in the following method #why did background have to be returned instead of modifying the reference?
                background = self.checkForFullRow(background, occupied_blocks, game_screen, piece)
                piece = self.getNewPiece()
                self.current_time_delay = self.time_delay    #rest time delay so holding down DOWN will not affect new Piece
            game_screen.blit(background, (0,0)) #this reloads the original background - basically erases it
            piece.update() #update the piece's position internally
            piece.draw(game_screen)
            self.window_screen.blit(game_screen, (self.game_screen_start_x,0))
            pygame.time.delay(self.current_time_delay)

    def getNewPiece(self):
        #store reference to piece classes
        pieces = (IPiece, JPiece, LPiece, OPiece, SPiece, TPiece, ZPiece)
        index = randint(0, len(pieces) - 1)
        return pieces[index]()      #execute piece constructor

    #check to see if piece hit bottom of the screen
    def checkBottom(self, next_coordinates):
        bottom = False
        for coord in next_coordinates:
            if coord['y'] >= Globals.screen_height:
                bottom = True
        return bottom

    def gameOver(self, occupied_blocks, current_coordinates):
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
    def checkOverlap(self, occupied_blocks, next_coordinates):
        overlap = False
        for block in occupied_blocks:
            for coord in next_coordinates:
                if block['x'] == coord['x'] and block['y'] == coord['y']:
                    overlap = True
        return overlap

    def checkForFullRow(self, background, occupied_blocks, screen, piece):
        #check occupied_blocks for full row
        block_positions = piece.getCurrentCoordinates()
        #min_position is the top of the highest sub_block in the piece that was just placed
        min_position = min([x['y'] for x in block_positions])

        y = Globals.screen_height
        while y >= min_position: #todo: >= here?

            if len([x for x in occupied_blocks if x['y'] == y]) == 10:
                self.rows_eliminated += 1
                self.to_next_level += 1
                if self.to_next_level >= 10:
                    self.time_delay -= 20
                    self.to_next_level = 0
                    self.level += 1
                #at this point a row has been filled and I need to delete it
                occupied_blocks[:] = [x for x in occupied_blocks if x['y'] != y] #using a slice to modify list in place
                #now move the blocks ABOVE the deleted row down a notch
                for block in occupied_blocks:
                    if block['y'] < y: block['y'] += Globals.block_height

                #the items have been deleted from occupied_blocks....now redraw everything
                background.fill(self.game_screen_color)
                screen.blit(background, (0,0))
                for block in occupied_blocks:
                    Globals.drawBlock(screen, block['color'], block)
                self.level_label = self.font.render("Level: " + str(self.level), 1, (255,255,255))
                self.rows_eliminated_label = self.font.render("Rows Eliminated: " + str(self.rows_eliminated), 1, (255,255,255))
                self.window_screen.fill((0,0,0))
                self.window_screen.blit(self.level_label, (450, 80))
                self.window_screen.blit(self.rows_eliminated_label, (450, 100))
                self.window_screen.blit(screen, (self.game_screen_start_x,0))
                pygame.display.update() #update this during the loop to give the effect of removing rows one at a time
                background = screen.copy()
                pygame.time.delay(250)
            else: y -= Globals.block_height
        return background

    def display_splash(self):
        self.window_screen = pygame.display.set_mode((Globals.window_width, Globals.window_height))
        self.window_screen.fill((0,0,0))
        splash_image = pygame.image.load('PyTetrisSplash.jpg').convert()
        self.window_screen.blit(splash_image, (0, 0))
        self.splash_label1 = self.font.render("Use the left and right arrows to move the piece left and right.", 1, (255,255,255))
        self.splash_label2 = self.font.render("Hold down to drop the piece quickly.  Press up to rotate the piece.", 1, (255,255,255))
        self.window_screen.blit(self.splash_label1, (75, 300))
        self.window_screen.blit(self.splash_label2, (60, 325))
        self.splash_label3 = self.font.render("Press ENTER to continue.", 1, (255,255,255))
        self.window_screen.blit(self.splash_label3, (200, 375))
        pygame.display.update()

        while True:
            continue_game = False
            for event in pygame.event.get((pygame.KEYDOWN, pygame.QUIT)):
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        continue_game = True
                        break
            if continue_game == True:
                break

        self.window_screen.fill((0,0,0))
        pygame.display.update()

