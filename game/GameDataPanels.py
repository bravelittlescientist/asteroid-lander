import pygame
from pgu import gui

class GamePanel:
    """
    Base class for dashboard info panels
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 164
        self.placeholder = pygame.image.load("images/spaceship-96.png")

    def draw(self, screen):
        screen.blit(self.image, (x, y))

class LeaderboardPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)

class MineralPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)

class PlotsPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)
    
