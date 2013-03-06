from game.Constants import *
from os import environ
from sys import exit

import pygame
from pygame.locals import *
from LanderContainer import LanderContainer
from pgu import gui

pygame.init()

def global_stop_pygame():
    print "Stopping pygame"
    pygame.quit()

class SpaceshipViewer:

    def __init__(self):
        self.statusLabel = "connecting"
        self.playersLabel = "0 players"
        self.frame = 0
        self.down = False

        self.init_gui()

    def init_gui(self):
        self.screen = pygame.display.set_mode((1024,800), SWSURFACE)
        self.app = gui.App()

        self.c = LanderContainer()
        self.lc = gui.Container(align=-1,valign=-1)    
        self.lc.add(self.c, 0, 0)

        self.app.init(self.lc)

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0)) 

    def stop_pygame(self):
        global_stop_pygame()

    def GameLoop(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                self.c.key_event_handler(e)
                self.Events(e)
            elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:         
                self.c.mouse_event_handler(e)
        
        self.screen.blit(self.background, (0, 0))
        self.c.draw_game(self.screen)
        self.app.paint(self.screen)
        pygame.display.flip()
     
    def Events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                print event.key, "is pressed"
                self.LandedSafely(12) #this is the landing points.We have to obtain it from the PhysicsEngine
            elif event.key == pygame.K_c:
                print event.key, "is pressed"
                self.CrashLanded()
            elif event.key == pygame.K_b:
                print event.key, "is pressed"
                self.BuyFuel();
            elif event.key == pygame.K_r:
                print event.key, "is pressed"
                self.RequestPlot(GOLD);
            elif event.key == pygame.K_e:
                print event.key, "is pressed"
                self.ReturnToEarth(100); #this is fuel level. We have to obtain it from the GUI
            elif event.key == pygame.K_q:
                print event.key, "is pressed"
                self.QuitGame();
            else:
                pass
        else:
            pass        
