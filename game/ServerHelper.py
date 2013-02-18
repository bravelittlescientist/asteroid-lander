''' contains helper functions for server'''
from collections import namedtuple


    
    
def getPlayerScore(self, pInfo):
    return pInfo.score
    
def playerInfoToString(self, pInfo):
    return str(pInfo.name) +"  :  " + str(pInfo.score)

def leaderboardToString(self, leaderboard):
    returnString = "player  :   score"
    returnString += "*"*10
    for pInfo in leaderboard:
        returnString += "\n" + self.playerInfoToString(pInfo)
    returnString += "\n"+ "*"*10
    return returnString