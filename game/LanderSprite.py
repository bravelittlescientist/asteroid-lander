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

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.mouse.set_visible(0)
lander = LanderSprite()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    lander.update()
    screen.blit(background, (0, 0))
    screen.blit(lander.image, lander.rect)
    pygame.display.flip()
