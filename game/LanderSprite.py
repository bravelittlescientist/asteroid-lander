"""
LanderSprite - A Sprite to represent the LunarLander ship
"""
import sys, pygame
from pygame.sprite import Sprite

class LanderSprite(Sprite):
    """ The LunarLander spaceship sprit """
    image = pygame.image.load("images/spaceship-96.png")
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = LanderSprite.image
        self.rect = self.image.get_rect()
        self.rect.midtop = (400, 400)
        self.velocityx = 0
        self.velocityy = 0

    def update(self):
        #pos = pygame.mouse.get_pos()
        #self.rect.midtop = pos
        self.rect.centerx += self.velocityx
        self.rect.centery += self.velocityy
    
    def set_x_velocity(self, xv):
        self.velocityx += xv

    def set_y_velocity(self, yv):
        self.velocityy += yv

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.mouse.set_visible(0)
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

    lander.update()
    screen.blit(background, (0, 0))
    screen.blit(lander.image, lander.rect)
    pygame.display.flip()
