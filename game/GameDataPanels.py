import pygame
from pgu import gui

class GamePanel(gui.Table):
    """
    Base class for dashboard info panels
    """
    def __init__(self, x, y):
        gui.Table.__init__(self)
        self.x = x
        self.y = y
        self.width = 256
        self.height = 164
        self.fg = (255,255,255)

    def setValue(self, w, cr, rr, cs=1, rs=1):
        self.td(w, cr, rr, cs, rs);  
  
class LeaderboardPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)

        self.tr()
        self.td(gui.Label("Spaceship        ", color=self.fg), colspan=2)
        self.td(gui.Label("Points", color=self.fg), colspan=1)

        self.addRow("Enterprise", 10)
        self.addRow("Constellation", 8)
        self.addRow("DeepSpace", 6)

        #[] {}

    def addRow(self, ship, score):
        self.tr()
        self.td(gui.Label(ship, color=self.fg), colspan=2)
        self.td(gui.Label(str(score), color=self.fg), colspan=1)

    #def updateLeaderboard(self, player_score_list):
        

class MineralPanel(GamePanel):
    def __init__(self, x, y, goal):
        GamePanel.__init__(self, x, y)

        self.goal = goal
        self.score = {"Iron" : 0, "Gold": 0, "Copper": 0}

        self.tr()
        self.td(gui.Label(" ", color=self.fg), colspan=1)
        self.td(gui.Image("images/iron.png", width=64, height=64), colspan=1)
        self.td(gui.Image("images/gold.png", width=64, height=64), colspan=1)
        self.td(gui.Image("images/copper.png", width=64, height=64), colspan=1)

        self.tr()
        self.td(gui.Label(" ", color=self.fg), colspan=1)
        self.td(gui.Label("Iron", color=self.fg), colspan=1)
        self.td(gui.Label("Gold", color=self.fg), colspan=1)
        self.td(gui.Label("Copper", color=self.fg), colspan=1)

        self.tr()
        self.td(gui.Label("Score   ",               color=self.fg), colspan=1)
        self.td(gui.Label(str(self.score["Iron"]),  color=self.fg), colspan=1)
        self.td(gui.Label(str(self.score["Gold"]),  color=self.fg), colspan=1)
        self.td(gui.Label(str(self.score["Copper"]),color=self.fg), colspan=1)

        self.tr()
        self.td(gui.Label("Goal   ",                color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal["Iron"]),   color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal["Gold"]),   color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal["Copper"]), color=self.fg), colspan=1)

    def update_score(self, score):
        self.score = score
        self.setValue(gui.Label(str(self.score["Iron"]), color=self.fg), 1, 2)
        self.setValue(gui.Label(str(self.score["Gold"]), color=self.fg), 2, 2)
        self.setValue(gui.Label(str(self.score["Copper"]), color=self.fg), 3, 2)  

class PlotsPanel(GamePanel):
    def __init__(self, x, y, plots):
        GamePanel.__init__(self, x, y)

        self.plots = plots 
        # e.g., {"Iron" : 4, "Gold": 6, "Copper": 1}, a mapping of minerals to quantities

        self.rectIron = pygame.Rect((752, 620), (36, 36))
        self.rectGold = pygame.Rect((814, 620), (36, 36))
        self.rectCopper = pygame.Rect((892, 620), (36, 36))

        self.tr()
        self.td(gui.Label("Mining Plots", color=self.fg), colspan=3)
        
        self.tr()
        self.td(gui.Button(str(self.plots["Iron"]), width=36, height=36), colspan=1)
        self.td(gui.Button(str(self.plots["Gold"]), width=36, height=36), colspan=1)
        self.td(gui.Button(str(self.plots["Copper"]), width=36, height=36), colspan=1)

        self.tr()  
        self.td(gui.Label("   Iron   ", color=self.fg), colspan=1)
        self.td(gui.Label("   Gold   ", color=self.fg), colspan=1)
        self.td(gui.Label("   Copper   ", color=self.fg), colspan=1)

    def update_plots(self, plots):
        self.plots = plots
        self.setValue(gui.Button(str(self.plots["Iron"]), width=36, height=36), 0, 2)
        self.setValue(gui.Button(str(self.plots["Gold"]), width=36, height=36), 1, 2)
        self.setValue(gui.Button(str(self.plots["Copper"]), width=36, height=36), 2, 2)
        

