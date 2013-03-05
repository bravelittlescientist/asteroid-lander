import sys
import math

import pygame
from pygame.sprite import Sprite

class LanderSprite(Sprite):
    """ The LunarLander spaceship sprit """
    image = pygame.image.load("images/spaceship-96.png")
    
    def __init__(self, game_left_limit, game_top_limit, game_width, game_height):
        pygame.sprite.Sprite.__init__(self)

        self.image = LanderSprite.image
        self.rect = self.image.get_rect()

        self.position_x = game_left_limit + game_width/2
        self.position_y = game_top_limit + 96
        self.rect.midbottom = (self.position_x, self.position_y)

        self.landed = False
        self.crashed = False

        self.gravity = 0.02
        self.velocity_slowing = 0.01  
        self.velocity_x = 0
        self.velocity_y = 0
    
        self.moving_left = False;
        self.moving_right = False;
        self.thrusters = False;
    
        self.left_limit = game_left_limit
        self.top_limit = game_top_limit
        self.right_limit = self.left_limit + game_width
        self.bottom_limit = self.top_limit + game_height

    def update_velocity(self):
        """ Update velocities depending on which direction ship is moving """
        # Set thruster (up/down) movement
        if self.thrusters:
            self.velocity_y -= self.gravity
        else:
            self.velocity_y += self.velocity_slowing

        # Set left movement
        if self.moving_left:
            self.velocity_x -= self.gravity
        else:
            if self.velocity_x < 0:
                self.velocity_x += self.velocity_slowing
        
        # Set right movement
        if self.moving_right:
            self.velocity_x += self.gravity
        else:
            if self.velocity_x > 0:
                self.velocity_x -= self.velocity_slowing

    def update(self):
        """ Update the position of the lunar lander sprite based on current velocities """
        # Update velocity based on movement state setting        
        self.update_velocity()

        # Update position due to velocity
        if (self.position_x + self.velocity_x) < (self.left_limit + 48) or (self.position_x + self.velocity_x) > (self.right_limit - 48):
            self.velocity_x = 0
        self.position_x += self.velocity_x

        if self.position_y + self.velocity_y < self.top_limit + 96 or self.position_y + self.velocity_y > self.bottom_limit:
            self.velocity_y = 0
        self.position_y += self.velocity_y
        self.rect.midbottom = (self.position_x, self.position_y)

    def draw(self, screen):
        """ Draw lander sprite to existing game canvas """
        screen.blit(self.image, self.rect)

    def set_thrusters(self, thrusters_on):
        """ Up-arrow: Player uses thrusters to propel lander up """
        self.thrusters = thrusters_on

    def set_left_movement(self, left):
        """ Left-arrow: Moving left or stopping left movement """
        self.moving_left = left 

    def set_right_movement(self, right):
        """ Right-arrow: Moving right or stopping right movement """
        self.moving_right = right        

    def get_vertical_velocity(self):
        return self.velocity_y

    def get_horizontal_velocity(self):
        return self.velocity_x

# Initialize game
pygame.init()
screen = pygame.display.set_mode((640, 640))
#pygame.mouse.set_visible(0)

lander = LanderSprite(40, 100, 560, 400)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        # On Keypress, set movement state
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lander.set_left_movement(True)
            elif event.key == pygame.K_RIGHT:
                lander.set_right_movement(True)
            elif event.key == pygame.K_UP:
                lander.set_thrusters(True)
            
        # On Keyrelease, release movement state setting
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                lander.set_left_movement(False)
            elif event.key == pygame.K_RIGHT:
                lander.set_right_movement(False)
            elif event.key == pygame.K_UP:
                lander.set_thrusters(False)

    # Clear game canvas background
    screen.blit(background, (0, 0))

    # Update lander speed/position
    lander.update()
    lander.draw(screen)

    # Update entire display
    pygame.display.flip()

pygame.quit()
