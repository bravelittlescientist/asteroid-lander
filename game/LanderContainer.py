import sys
import math
import pygame

from pgu import gui

from GameDataPanels import LeaderboardPanel, MineralPanel, PlotsPanel
from LanderCanvas import LanderSprite

class LanderContainer(gui.Container):
    """
    This container is the main GUI for the Lander Game.
    
    """
    def __init__(self):
        """
        Game initialization: 800x800 screen for now
        """
        gui.Container.__init__(self, width=1024, height=800)

        # Initialize screen components: Title Menu
        self.title_menu = gui.Button("Asteroid Miner", width=152, height=36)
        self.base_station_button = gui.Button("Base Station", width=152, height=36)
        self.fuel_button = gui.Button("Buy Fuel", width=152, height=36)
        self.quit_button = gui.Button("Quit", width=96, height=36)   

        # Initialize screen components: Gameplay Canvas
        self.lander = LanderSprite(0, 36, 1024, 524)

        # Initialize screen components: Lander Readouts
        self.altitude_readout = gui.Button("Altitude = 800 m", width=256, height=36)
        self.horizontal_speed_readout = gui.Button("Horizontal Speed: 0.0 m/s", width=256, height=36)
        self.vertical_speed_readout = gui.Button("Vertical Speed: 0.0 m/s", width=256, height=36)

        # Initialize screen components: Mining Dashboard
        self.spaceship_points_leaderboard = gui.Button("[LEADERBOARD]",
                width=336, height=164)
        self.mineral_score_goal_box = gui.Button("[MINERAL SCORES]",
                width=336, height=164)
        self.mining_plots_availability_indicator = gui.Button("[PLOTS]",
                width=336, height=164)
        self.fuel_level_readout = gui.Button("Fuel: 1000 L", width=256,
                height=36)
        self.weight_readout = gui.Button("Weight: 500 tons", width=256,
                height=36) 

        # Position top menu
        self.add(self.title_menu, 0, 0)
        self.add(self.base_station_button, 360, 0)
        self.add(self.fuel_button, 512, 0)
        self.add(self.quit_button, 928, 0)

        # Position canvas and game readouts
        self.add(self.altitude_readout, 0, 560)
        self.add(self.horizontal_speed_readout, 256, 560)
        self.add(self.vertical_speed_readout, 512, 560)

        # Position Gameplay info panels
        self.leaderboardPanel = LeaderboardPanel(0, 596)
        self.mineralPanel = MineralPanel(336, 596)
        self.plotsPanel = PlotsPanel(672, 596)

        self.add(self.fuel_level_readout, 0, 764)
        self.add(self.weight_readout, 256, 764)

    def key_event_handler(self, event):
        self.lander.on_key_event(event)

    def draw_game(self, screen):
        # Update game panels
        self.leaderboardPanel.draw(screen)
        self.mineralPanel.draw(screen)
        self.plotsPanel.draw(screen)
        self.lander.draw(screen)
        
        # Update game       

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024,800))
    app = gui.App()
    c = LanderContainer()
    app.init(c)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0)) 

    running = True

    while running:
        # Key event handling        
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                c.key_event_handler(e)
        
        screen.blit(background, (0, 0))
        c.draw_game(screen)
        app.paint(screen)
        pygame.display.flip()

    # Exit gracefully
    pygame.quit()
