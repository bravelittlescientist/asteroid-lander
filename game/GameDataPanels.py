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
        self.width = 200
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

    def addRow(self, ship, score):
        self.tr()
        self.td(gui.Label(ship, color=self.fg), colspan=2)
        self.td(gui.Label(str(score), color=self.fg), colspan=1)

class MineralPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)

        self.tr()
        self.td(gui.Label(" ", color=self.fg), colspan=1)
        self.td(gui.Label("[IMG Indio]", color=self.fg), colspan=1)
        self.td(gui.Label("[IMG Gold]", color=self.fg), colspan=1)
        self.td(gui.Label("[IMG Copper]", color=self.fg), colspan=1)

        self.tr()
        self.td(gui.Label(" ", color=self.fg), colspan=1)
        self.td(gui.Label("Indio", color=self.fg), colspan=1)
        self.td(gui.Label("Gold", color=self.fg), colspan=1)
        self.td(gui.Label("Copper", color=self.fg), colspan=1)

        self.tr()
        self.td(gui.Label("Score   ", color=self.fg), colspan=1)
        self.td(gui.Label(str(4), color=self.fg), colspan=1)
        self.td(gui.Label(str(3), color=self.fg), colspan=1)
        self.td(gui.Label(str(5), color=self.fg), colspan=1)

        self.tr()
        self.td(gui.Label("Goal   ", color=self.fg), colspan=1)
        self.td(gui.Label(str(6), color=self.fg), colspan=1)
        self.td(gui.Label(str(8), color=self.fg), colspan=1)
        self.td(gui.Label(str(10), color=self.fg), colspan=1)  

        self.setValue(gui.Label("test", color=self.fg), 0, 0)

class PlotsPanel(GamePanel):
    def __init__(self, x, y):
        GamePanel.__init__(self, x, y)

        self.tr()
        self.td(gui.Label("Mining Plots", color=self.fg), colspan=3)
        
        self.tr()
        self.td(gui.Label(str(4), color=self.fg), colspan=1)
        self.td(gui.Label(str(6), color=self.fg), colspan=1)
        self.td(gui.Label(str(1), color=self.fg), colspan=1)

        self.tr()  
        self.td(gui.Label("Indio", color=self.fg), colspan=1)
        self.td(gui.Label("Gold", color=self.fg), colspan=1)
        self.td(gui.Label("Copper", color=self.fg), colspan=1)

