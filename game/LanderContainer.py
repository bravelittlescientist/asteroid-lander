import sys
import pygame
from pgu import gui

class LanderContainer(gui.Container):
    """
    This container is the main GUI for the Lander Game.
    
    """
    def __init__(self):
        """
        Game initialization: 800x600 screen for now
        """
        gui.Container.__init__(self, width=800, height=600)

        # Initialize screen components: Title Menu
        self.base_station_button = gui.Button("Base Station", width=150, height=36)
        self.fuel_button = gui.Button("Buy Fuel", width=150, height=36)
        self.quit_button = gui.Button("Quit", width=100, height=36)
        self.title_menu = gui.Button("Asteroid Miner", width=150, height=36)

        # Initialize screen components: Gameplay Canvas
        self.gameplay_canvas = gui.Button("[CANVAS]", width=800, height=324,
                border=0)

        # Initialize screen components: Lander Readouts
        self.altitude_readout = gui.Button("Altitude=800m", width=200, height=36)
        self.horizontal_speed_readout = gui.Button("HSpeed: 0.0 m/s", width=200, height=36)
        self.vertical_speed_readout = gui.Button("VSpeed: 0.0 m/s", width=200, height=36)

        # Initialize screen components: Mining Dashboard
        self.spaceship_points_leaderboard = gui.Button("[LEADERBOARD]",
                width=200, height=164)
        self.mineral_score_goal_box = gui.Button("[MINERAL SCORES]",
                width=200, height=164)
        self.mining_plots_availability_indicator = gui.Button("[PLOTS]",
                width=200, height=164)
        self.fuel_level_readout = gui.Button("Fuel: 1000 L", width=150,
                height=36)
        self.weight_readout = gui.Button("Weight: 500 tons", width=150,
                height=36) 

        self.add(self.title_menu, 0, 0)
        self.add(self.base_station_button, 250, 0)
        self.add(self.fuel_button, 400, 0)
        self.add(self.quit_button, 700, 0)

        self.add(self.gameplay_canvas, 0, 36)

        self.add(self.altitude_readout, 0, 360)
        self.add(self.horizontal_speed_readout, 400, 360)
        self.add(self.vertical_speed_readout, 600, 360)

        self.add(self.spaceship_points_leaderboard, 36, 400)
        self.add(self.mineral_score_goal_box, 300, 400)
        self.add(self.mining_plots_availability_indicator, 564, 400)

        self.add(self.fuel_level_readout, 0, 564)
        self.add(self.weight_readout, 150, 564)

    def draw_game(self, screen):
        #self.add(self.base_station_button, 100, 100)
        pass        

        #self.base_station_button = gui.Button("Base Station", width=100, height=36)
        #self.fuel_button = gui.Button("Buy Fuel", width=100, height=36)
        #self.quit_button = gui.Button("Quit", width=100, height=36)
        #self.title_menu = gui.Button("Asteroid Miner", width=200, height=36)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    app = gui.App()
    c = LanderContainer()
    app.init(c)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0)) 

    running = True

    while running:
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        c.draw_game(screen)
        app.paint(screen)
        pygame.display.flip()
