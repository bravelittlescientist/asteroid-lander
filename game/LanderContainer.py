import sys
import math
import pygame
from pygame.locals import *

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
        self.title_menu = gui.TextArea(value="Asteroid Miner", width=152, height=36, focusable=False)
        
        self.base_station_button = gui.Button("Returning to Base Station", width=152, height=36)#, background=(208, 208, 208))
        self.notify_value = "NOTIFY"
        self.notification_zone = gui.TextArea(value=self.notify_value, width=256, height=36, focusable=False)
        self.fuel_button = gui.Button("Buying Fuel", width=152, height=36)

        self.quit_button = gui.Button("Quit", width=96, height=36)   
        #self.quit_button.connect(gui.CLICK, self.exit, None)

        # Initialize screen components: Gameplay Canvas
        self.lander = LanderSprite(0, 36, 1024, 524)

        # Initialize screen components: Lander Readouts
        self.altitude_readout = gui.TextArea(value="Altitude = 800 m", width=256, height=20, focusable=False)
        self.horizontal_speed_readout = gui.TextArea(value="Horizontal Speed: 0.0 m/s", width=256, height=20, focusable=False)#, color=(255, 0, 0))
        self.vertical_speed_readout = gui.TextArea(value="Vertical Speed: 0.0 m/s", width=256, height=20, focusable=False)

        # Initialize screen components: Ship Readouts
        self.fuel_level_readout = gui.TextArea(value="Fuel: ??? L", width=256, height=36, focusable=False)
        self.weight_readout = gui.TextArea(value="Weight: ??? tons", width=256, height=36, focusable=False) 

        # Position top menu
        self.add(self.title_menu, 0, 0)
        self.add(self.base_station_button, 360, 0)
        self.add(self.fuel_button, 512, 0)
        self.add(self.quit_button, 928, 0)

        # Position canvas and game readouts
        self.add(self.notification_zone, 768, 36)
        self.add(self.altitude_readout, 0, 560)
        self.add(self.horizontal_speed_readout, 360, 560)
        self.add(self.vertical_speed_readout, 720, 560)

        # Position Gameplay info panels
        self.leaderboardPanel = LeaderboardPanel(24, 596)
        self.mineralPanel = MineralPanel(360, 596)
        self.plotsPanel = PlotsPanel(696, 596)
        self.add(self.plotsPanel, 696, 596)
        self.add(self.mineralPanel, 360, 596)
        self.add(self.leaderboardPanel, 24, 596)

        self.add(self.fuel_level_readout, 0, 764)
        self.add(self.weight_readout, 256, 764)

    def clicked_in_button(self, button, position):
        return button.rect.collidepoint(position)

    def mouse_event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.clicked_in_button(self.base_station_button, pos): self.triggerBaseStation()
            elif self.clicked_in_button(self.fuel_button, pos): self.triggerBuyFuel()
            elif self.clicked_in_button(self.quit_button, pos): self.quit()

        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    def key_event_handler(self, event):
        if event.key == pygame.K_b:
            c.triggerBaseStation()
        elif event.key == pygame.K_f:
            c.triggerBuyFuel()       
        else:     
            self.lander.on_key_event(event)
      
    def draw_game(self, screen):
        # Update game
        self.lander.draw(screen)
        status = self.lander.get_status()
        if status == "CRASHED" or status == "LANDED":
            self.updateNotify(status) 
        
        # Update Readouts
        self.altitude_readout.value = "Altitude: " + str(self.lander.get_vertical_position()) + " m"
       
        self.horizontal_speed_readout.value = "Horizontal Speed: " + str(self.lander.get_horizontal_velocity()) + " m/s"
        if abs(self.lander.get_horizontal_velocity()) > 4: self.horizontal_speed_readout.color = (255, 0, 0)
        else: self.horizontal_speed_readout.color = (255, 255, 255)
        self.vertical_speed_readout.value = "Vertical Speed: " + str(self.lander.get_vertical_velocity()) + " m/s"
        #if self.lander.get_vertical_velocity() > 4: self.horizontal_speed_readout.color = (255, 0, 0)
        #else: self.horizontal_speed_readout.color = (255, 255, 255)
       
        self.notification_zone.value = self.notify_value

    def triggerBaseStation(self):
        self.updateNotify("Go to Base Station")
    
    def triggerBuyFuel(self):
        self.updateNotify("Buying Fuel")

    def updateNotify(self, notif):
        self.notify_value = notif

    def quit(self):
        # TODO Send player quitting message here        
        sys.exit(0)     
      
def running_offline():
    pygame.init()
    screen = pygame.display.set_mode((1024,800), SWSURFACE)
    app = gui.App()

    c = LanderContainer()
    lc = gui.Container(align=-1,valign=-1)    
    lc.add(c, 0, 0)
    
    app.init(lc)
    done = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0)) 

    while not done:
        # Key event handling        
        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                done = True
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                c.key_event_handler(e)
            elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:         
                c.mouse_event_handler(e)

        screen.blit(background, (0, 0))
        c.draw_game(screen)
        app.paint(screen)
        pygame.display.flip()

    # Exit gracefully
    pygame.quit()
  
if __name__ == "__main__":
    pass
    #running_offline()
