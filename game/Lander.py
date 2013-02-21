from game.Constants import *
from os import environ
from sys import exit
import pygame

SCREENSIZE = (640, 480)

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)

pygame.font.init()
fnt = pygame.font.SysFont("Arial", 14)
txtpos = (100, 90)

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
                    print "L is pressed"
                    self.LandedSafely(12)
                elif event.key == pygame.K_c:
                    self.CrashLanded()
                elif event.key == pygame.K_b:
                    self.BuyFuel();
                elif event.key == pygame.K_r:
                    self.RequestPlot(GOLD);
                elif event.key == pygame.K_e:
                    self.ReturnToEarth();
                elif event.key == pygame.K_q:
                    self.QuitGame();
                else:
                    pass
            else:
                pass

    def Hey(self):
        #print "itna to chal"
        self.HelloWorld()

    def Draw(self, linesets):
        screen.fill([255, 255, 255])
        txt = fnt.render(self.statusLabel, 1, (0, 0, 0))
        screen.blit(fnt.render(self.statusLabel, 1, (0, 0, 0)), [10, 10])
        txt = fnt.render(self.playersLabel, 1, (0, 0, 0))
        screen.blit(fnt.render(self.playersLabel, 1, (0, 0, 0)), [10, 20])
        [[pygame.draw.aalines(screen, c, False, l) for l in lines if len(l) > 1] for c, lines in linesets]
        pygame.display.flip()
        self.frame += 1
