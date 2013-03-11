from game.Constants import IRON, GOLD, COPPER
from game.libs import jsonpickle
from game.libs.pgu import gui
from game.model.Leaderboard import *
from game.model.LeaderboardEntry import *
import pygame
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
    def addHeader(self):
        self.tr()
        self.td(gui.Label("Spaceship        ", color=self.fg), colspan=2)
        self.td(gui.Label("Points", color=self.fg), colspan=1)
    
    def addRow(self, ship, score):
        self.tr()
        self.td(gui.Label(ship, color=self.fg), colspan=2)
        self.td(gui.Label(str(score), color=self.fg), colspan=1)
    
    def delRows(self):
        while self.getRows()>0:
            self.remove_row(0)
    #def updateLeaderboard(self, player_score_list):
    def refreshLeaderboard(self,data):
        self.delRows()
        self.addHeader()
        print "data", data ," type", type(data)
        obj = jsonpickle.decode(data)
        for entry in obj.entries:
            self.addRow(entry['player'], entry['score'])
        #self.addRow(ship, score)
        

class MineralPanel(GamePanel):
    def __init__(self, x, y, goal):
        GamePanel.__init__(self, x, y)

        self.goal = goal
        self.score = {IRON: 0, GOLD: 0, COPPER: 0}

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
        self.ironScoreLabel = gui.Label(str(self.score[IRON]),  color=self.fg)
        self.goldScoreLabel = gui.Label(str(self.score[GOLD]),  color=self.fg)
        self.copperScoreLabel = gui.Label(str(self.score[COPPER]),  color=self.fg)
        self.td(gui.Label("Score   ",               color=self.fg), colspan=1)
        self.td(self.ironScoreLabel, colspan=1)
        self.td(self.goldScoreLabel, colspan=1)
        self.td(self.copperScoreLabel, colspan=1)

        self.tr()
        self.td(gui.Label("Goal   ",                color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal[IRON]),   color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal[GOLD]),   color=self.fg), colspan=1)
        self.td(gui.Label(str(self.goal[COPPER]), color=self.fg), colspan=1)

    def update_score(self, score):
        self.score = score
        print "inside update_score: score", score
        self.ironScoreLabel.value = str(self.score[IRON])
        self.goldScoreLabel.value = str(self.score[GOLD])
        self.copperScoreLabel.value = str(self.score[COPPER])
#        self.setValue(gui.Label(str(self.score[IRON]), color=self.fg), 1, 2)
#        self.setValue(gui.Label(str(self.score[GOLD]), color=self.fg), 2, 2)
#        self.setValue(gui.Label(str(self.score[COPPER]), color=self.fg), 3, 2)  

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
        
        self.goldButton = gui.Button(str(self.plots[GOLD]), width=36, height=36)
        self.ironButton = gui.Button(str(self.plots[IRON]), width=36, height=36)
        self.copperButton = gui.Button(str(self.plots[COPPER]), width=36, height=36)
        self.tr()
        self.td(self.ironButton, colspan=1)
        self.td(self.goldButton, colspan=1)
        self.td(self.copperButton, colspan=1)

        self.tr()  
        self.td(gui.Label("   Iron   ", color=self.fg), colspan=1)
        self.td(gui.Label("   Gold   ", color=self.fg), colspan=1)
        self.td(gui.Label("   Copper   ", color=self.fg), colspan=1)

    def update_plots(self, plots):
        self.plots = plots
        print "plots", self.plots
        self.goldButton.value = str(self.plots[GOLD])
        self.ironButton.value = str(self.plots[IRON])
        self.copperButton.value = str(self.plots[COPPER])