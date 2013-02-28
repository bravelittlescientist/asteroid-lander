import sys
import math

import pygame
from pygame.sprite import Sprite

class LanderSprite(Sprite):
    """ The LunarLander spaceship sprit """
    image = pygame.image.load("images/spaceship-96.png")
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = LanderSprite.image
        self.rect = self.image.get_rect()
        self.rect.midtop = (320, 100)
        self.velocityx = 0
        self.velocityy = 0 
        self.g = 1.622 # m/s^2, gravity on the moon

    def update(self, ms):
        # Update position due to gravity

        # Update position due to movement 
        self.rect.centerx += 10 * self.velocityx
        self.rect.centery += 10 * self.velocityy
        self.rect.centery += (self.g/10 * math.pow(float(ms/1000), 2)) * .5

        # Avoid going outside of bounds
        self.rect.centerx = min(self.rect.centerx, 640 - 48)
        self.rect.centerx = max(self.rect.centerx, 48)
        self.rect.centery = min(self.rect.centery, 640 - 48)
        self.rect.centery = max(self.rect.centery, 48)

    def set_x_velocity(self, xv):
        self.velocityx += xv

    def set_y_velocity(self, yv):
        self.velocityy += yv

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.mouse.set_visible(0)

app = gui.App()

lander = LanderSprite()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        # On Keypress, set movement speed.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lander.set_x_velocity(-1)
            elif event.key == pygame.K_RIGHT:
                lander.set_x_velocity(1)
            elif event.key == pygame.K_UP:
                lander.set_y_velocity(-1)
            elif event.key == pygame.K_DOWN:
                lander.set_y_velocity(1)

        # On Keyrelease, set movement speed opposite
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                lander.set_x_velocity(1)
            elif event.key == pygame.K_RIGHT:
                lander.set_x_velocity(-1)
            elif event.key == pygame.K_UP:
                lander.set_y_velocity(1)
            elif event.key == pygame.K_DOWN:
                lander.set_y_velocity(-1)

    lander.update(pygame.time.get_ticks())
    screen.blit(background, (0, 0))
    screen.blit(lander.image, lander.rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Y: " + str(lander.rect.centery) + "m  T: " + str(pygame.time.get_ticks()) + " ms", 1, (250, 250, 250))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)

    pygame.display.flip()

pygame.quit()
