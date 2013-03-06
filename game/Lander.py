from game.Constants import *
from os import environ
from sys import exit

import pygame
from pygame.locals import *
from LanderContainer import LanderContainer
from pgu import gui

pygame.init()
screen = pygame.display.set_mode((1024,800), SWSURFACE)
app = gui.App()

c = LanderContainer()
lc = gui.Container(align=-1,valign=-1)    
lc.add(c, 0, 0)

app.init(lc)
done = False

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0)) 

while not done:
    # Key event handling        
    #for e in pygame.event.get():
    #    if e.type is pygame.QUIT:
    #        done = True
    #    elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
    #        c.key_event_handler(e)
    #    elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:         
    #        c.mouse_event_handler(e)
        
    screen.blit(background, (0, 0))
    c.draw_game(screen)
    app.paint(screen)
    pygame.display.flip()

# Exit gracefully
pygame.quit()

class Lander:

    def __init__(self):
        self.statusLabel = "connecting"
        self.playersLabel = "0 players"
        self.frame = 0
        self.down = False

    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
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
