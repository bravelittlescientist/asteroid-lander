import sys
import math
from random import randint

import pygame
from pygame.sprite import Sprite

class PhysicsEngine(Sprite):
    """ The LunarLander spaceship sprit """
   
    def __init__(self, game_left_limit, game_top_limit, game_width, game_height):
        pygame.sprite.Sprite.__init__(self)
        
        # Properties that persist through multiple landings        
        self.left_limit = game_left_limit
        self.top_limit = game_top_limit
        self.right_limit = self.left_limit + game_width
        self.bottom_limit = self.top_limit + game_height
        self.background_rect = pygame.Rect(self.left_limit, self.top_limit, game_width, game_height)
  
        self.shipslow = pygame.image.load("images/shipslow.png")
        self.shipmed = pygame.image.load("images/shipmed.png")
        self.shipfast = pygame.image.load("images/shipfast.png")
        self.image = self.shipslow        
        self.rect = self.image.get_rect()
        self.platform = pygame.image.load("images/platform.png")

        self.STATUS_PAUSED = 10
        self.STATUS_RUNNING = 20
        self.STATUS_LANDED = 30
        self.STATUS_CRASHED = 40
        self.STATUS_READY = 50

        self.gravity = 0.08
        self.velocity_slowing = 0.06 
        self.max_landing_velocity = 4

        self.copperbg = [
            pygame.image.load("images/Terrains/copper1.bmp"),
            pygame.image.load("images/Terrains/copper2.bmp")
        ]
        self.ironbg = [
            pygame.image.load("images/Terrains/iron1.bmp"),
            pygame.image.load("images/Terrains/iron2.bmp")
        ]
        self.goldbg = [
            pygame.image.load("images/Terrains/gold1.bmp"),
            pygame.image.load("images/Terrains/gold2.bmp")
        ]

        self.reset_game()   

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
        if self.position_y + self.velocity_y < self.top_limit + self.rect.height:
            self.velocity_y = 0
        elif self.position_y + self.velocity_y > self.bottom_limit:
            self.position_y = self.bottom_limit - 1
            if self.velocity_y > self.max_landing_velocity or abs(self.velocity_x) > self.max_landing_velocity: 
                self.set_status(self.STATUS_CRASHED)
            else: 
                self.set_status(self.STATUS_LANDED)
        else:
            self.position_y += self.velocity_y

        if (self.position_x + self.velocity_x) < (self.left_limit + self.rect.height/2):
            if self.status == self.STATUS_RUNNING: self.velocity_x = 0
        elif (self.position_x + self.velocity_x) > (self.right_limit - self.rect.height/2):
            if self.status == self.STATUS_RUNNING: self.velocity_x = 0
        
        if self.status == self.STATUS_RUNNING: self.position_x += self.velocity_x

        # Check for bounds
        if self.status == self.STATUS_LANDED and \
            (self.left_landing_bounds > self.position_x - self.rect.width/2 or \
                self.right_landing_bounds < self.position_x + self.rect.width/2):
            self.status = self.STATUS_CRASHED

        self.rect.midbottom = (self.position_x, self.position_y)

    def draw(self, screen):
        """ Draw lander sprite to existing game canvas """
        if self.status == self.STATUS_RUNNING:        
            self.update()

        screen.blit(pygame.transform.scale(self.background_img, (self.background_rect.width,self.background_rect.height)), self.background_rect)
        screen.blit(self.platform, pygame.Rect((self.left_landing_bounds, self.bottom_limit - 48), (128, 48)))
        
        if abs(self.velocity_x) > 4 or self.velocity_y > 4: 
            screen.blit(self.shipfast, self.rect)
        else:
            screen.blit(self.shipmed, self.rect)

    def get_background(self, mineral_string="Iron"):
        if mineral_string == "Copper":
            return self.copperbg[randint(0,1)]
        elif mineral_string == "Gold":
            return self.goldbg[randint(0,1)]
        elif mineral_string == "Iron":
            return self.ironbg[randint(0,1)]

    # Management movement
    def set_thrusters(self, thrusters_on):
        """ Up-arrow: Player uses thrusters to propel lander up """
        self.thrusters = thrusters_on

    def set_left_movement(self, left):
        """ Left-arrow: Moving left or stopping left movement """
        self.moving_left = left 

    def set_right_movement(self, right):
        """ Right-arrow: Moving right or stopping right movement """
        self.moving_right = right        

    def set_status(self, stat):
        self.status = stat

    def get_vertical_velocity(self):
        return self.velocity_y

    def get_horizontal_velocity(self):
        return self.velocity_x

    def get_vertical_position(self):
        return self.bottom_limit - self.rect.midbottom[1] - 1

    def set_ready(self):
        self.status = self.STATUS_READY

    def get_status(self):
        if self.status == self.STATUS_LANDED:
            return "LANDED"
        elif self.status == self.STATUS_CRASHED:
            return "CRASHED"
        elif self.status == self.STATUS_RUNNING:
            return "RUNNING"
        elif self.status == self.STATUS_PAUSED:
            return "PAUSED"

    def start_game(self):
        if self.status != self.STATUS_RUNNING:
            self.set_status(self.STATUS_RUNNING)

    def reset_game(self):
        self.position_x = self.left_limit + (self.right_limit - self.left_limit)/2
        self.position_y = self.top_limit + self.rect.height
        self.rect.midbottom = (self.position_x, self.position_y)  
        self.status = self.STATUS_PAUSED

        self.velocity_x = 0
        self.velocity_y = 0

        self.moving_left = False;
        self.moving_right = False;
        self.thrusters = False;

        self.left_landing_bounds = randint(128, self.right_limit - 256)
        self.right_landing_bounds = self.left_landing_bounds + 128

        self.background_img = self.get_background()

    def on_key_event(self, event):
        # Handle key up/down events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.set_left_movement(True)
            elif event.key == pygame.K_RIGHT:
                self.set_right_movement(True)
            elif event.key == pygame.K_UP:
                self.set_thrusters(True) 
            elif event.key == pygame.K_SPACE:
                if self.status == self.STATUS_READY: self.start_game()
            #elif event.key == pygame.K_r:
            #    self.reset_game()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.set_left_movement(False)
            elif event.key == pygame.K_RIGHT:
                self.set_right_movement(False)
            elif event.key == pygame.K_UP:
                self.set_thrusters(False)   
