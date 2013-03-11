from GameDataPanels import LeaderboardPanel, MineralPanel, PlotsPanel
from PhysicsEngine import PhysicsEngine
from game.Constants import IRON, GOLD, COPPER, IRON_PLOT_TOTAL, GOLD_PLOT_TOTAL, \
    COPPER_PLOT_TOTAL, GAME_GOAL_IRON, GAME_GOAL_GOLD, GAME_GOAL_COPPER
from game.libs.pgu import gui
from pygame.locals import *
import math
import pygame
import sys



class LanderContainer(gui.Container):
    """
    This container is the main GUI for the Lander Game.
    
    """
    def __init__(self, controller):
        """
        Game initialization: 1024x768 screen for now
        """
        self.controller = controller
        gui.Container.__init__(self, width=1024, height=704)

        # Initialize screen components: Title Menu
        self.title_menu = gui.TextArea(value="Asteroid Miner", width=152, height=36, focusable=False)
        
        self.base_station_button = gui.Button("Returning to Base Station", width=152, height=36)#, background=(208, 208, 208))
        self.notify_value = "NOTIFY"
        self.notification_zone = gui.TextArea(value=self.notify_value, width=256, height=36, focusable=False)
        self.fuel_button = gui.Button("Buying Fuel", width=152, height=36)

        self.quit_button = gui.Button("Quit", width=96, height=36)   

        # Initialize screen components: Gameplay Canvas
        self.lander = PhysicsEngine(0, 36, 1024, 524)

        # Initialize screen components: Lander Readouts
        self.altitude_readout = gui.TextArea(value="Altitude = 800 m", width=256, height=20, focusable=False)
        self.horizontal_speed_readout = gui.TextArea(value="Horizontal Speed: 0.0 km/s", width=256, height=20, focusable=False)#, color=(255, 0, 0))
        self.vertical_speed_readout = gui.TextArea(value="Vertical Speed: 0.0 km/s", width=256, height=20, focusable=False)
        self.fuel_level_readout = gui.TextArea(value="Fuel: 1000.00 L", width=256, height=20, focusable=False) # TODO From Message
        self.fuel_level = 1000.00

        # Position top menu
        self.add(self.title_menu, 0, 0)
        self.add(self.base_station_button, 360, 0)
        self.add(self.fuel_button, 512, 0)
        self.add(self.quit_button, 928, 0)

        # Position canvas and game readouts
        self.add(self.notification_zone, 768, 36)
        self.add(self.altitude_readout, 0, 562)
        self.add(self.horizontal_speed_readout, 256, 562)
        self.add(self.vertical_speed_readout, 512, 562)
        self.add(self.fuel_level_readout, 768, 562)

        # Position Gameplay info panels
        self.leaderboardPanel = LeaderboardPanel(24, 616)
        self.mineralPanel = MineralPanel(320, 616, {IRON: GAME_GOAL_IRON, GOLD: GAME_GOAL_GOLD, COPPER: GAME_GOAL_COPPER})
        self.plotsPanel = PlotsPanel(744, 616, {IRON : IRON_PLOT_TOTAL, GOLD: GOLD_PLOT_TOTAL, COPPER: COPPER_PLOT_TOTAL}) # TODO From Message
        self.add(self.plotsPanel, 744, 616)
        self.add(self.mineralPanel, 320, 616)
        self.add(self.leaderboardPanel, 24, 616)

    def clicked_in_button(self, button, position):
        return button.collidepoint(position)

    def mouse_event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Purchasing / Traveling Buttons
            if self.clicked_in_button(self.base_station_button.rect, pos): self.triggerBaseStation()
            elif self.clicked_in_button(self.fuel_button.rect, pos): self.triggerBuyFuel()
            elif self.clicked_in_button(self.quit_button.rect, pos): self.quit()

            # Mining Plots Selection
            elif self.clicked_in_button(self.plotsPanel.rectIron, pos): self.triggerMiningPlotIron()
            elif self.clicked_in_button(self.plotsPanel.rectGold, pos): self.triggerMiningPlotGold()
            elif self.clicked_in_button(self.plotsPanel.rectCopper, pos): self.triggerMiningPlotCopper()
            #else: self.updateNotify(str(pos[0]) + " " + str(pos[1]))

        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    def key_event_handler(self, event):
        if event.key == pygame.K_b:
            self.triggerBaseStation()
        elif event.key == pygame.K_f:
            self.triggerBuyFuel()       
        else:     
            self.lander.on_key_event(event)
    
    def game_ready(self):
        self.lander.set_ready()

    def draw_game(self, screen):
        # Update game
        self.lander.draw(screen)
        status = self.lander.get_status()
        if status == "CRASHED":
            self.updateNotify(status)
            self.triggerCrashedLanded();
            self.lander.set_status(self.lander.STATUS_PAUSED);
        elif status == "LANDED":
            self.triggerLandedSafely(10);
            self.lander.set_status(self.lander.STATUS_PAUSED);
            #send this signal to server
             
        
        # Update Readouts
        self.altitude_readout.value = "Altitude: " + str(self.lander.get_vertical_position()) + " m"
       
        self.horizontal_speed_readout.value = "Horizontal Speed: " + str(self.lander.get_horizontal_velocity()) + " km/s"
        self.vertical_speed_readout.value = "Vertical Speed: " + str(self.lander.get_vertical_velocity()) + " km/s"
        if abs(self.lander.get_horizontal_velocity()) > 4 or self.lander.get_vertical_velocity() > 4:
            pygame.draw.rect(screen, (255, 0, 0), (0,560,1024,2), 0)
        self.notification_zone.value = self.notify_value
        if (status == "RUNNING"):       
            self.fuel_level -= 1
        self.fuel_level_readout.value = "Fuel: " + str(self.fuel_level) + " L"

    def triggerMiningPlotIron(self):
        self.updateNotify("Mining: Iron")
        self.controller.RequestPlot(IRON)

    def triggerMiningPlotGold(self):
        self.updateNotify("Mining: Gold")
        self.controller.RequestPlot(GOLD)

    def triggerMiningPlotCopper(self):
        self.updateNotify("Mining: Copper")
        self.controller.RequestPlot(COPPER)

    def triggerBaseStation(self):
        self.fuel_level = 1000.00
        self.updateNotify("Returning to Base Station")
        self.controller.ReturnToEarth()
    
    def triggerBuyFuel(self):
        self.updateNotify("Buying Fuel")
        self.controller.BuyFuel()

    def triggerUpdateMineralScore(self, score_dict):
        self.mineralPanel.update_score(score_dict)

    def updateNotify(self, notif):
        print notif
        self.notify_value = notif
    
    def triggerCrashedLanded(self):
        self.controller.CrashLanded()
    def triggerLandedSafely(self,score):
        self.controller.LandedSafely(score)
        
    def refreshLeaderboard(self,data):
        self.leaderboardPanel.refreshLeaderboard(data)

    def updatePlots(self,data):
        self.plotsPanel.update_plots(data)
    
    def quit(self):
        # TODO Send player quitting message here        
        sys.exit(0)     
