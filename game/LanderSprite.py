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
        pass
    
    def move_left(self):
        self.rect.centerx -= 20

    def move_right(self):
        self.rect.centerx += 20
    
    def move_up(self):
        self.rect.centery -= 20

    def move_down(self):
        self.rect.centery += 20

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lander.move_left()
            elif event.key == pygame.K_RIGHT:
                lander.move_right()
            elif event.key == pygame.K_UP:
                lander.move_up()
            elif event.key == pygame.K_DOWN:
                lander.move_down()
    
    screen.blit(background, (0, 0))
    screen.blit(lander.image, lander.rect)
    pygame.display.flip()
