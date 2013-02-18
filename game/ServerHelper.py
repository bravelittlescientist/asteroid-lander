''' contains helper functions for server'''
from collections import namedtuple

def getLeaderboard(self):
    leaderboard =[]
    PlayerInfo = namedtuple('PlayerInfo','name score')
    
    for p in self.players:
        row = PlayerInfo(name=p.id, score=p.score)
        leaderboard.append(row)
    leaderboard.sort(key=self.getPlayerScore,reverse=True)
    print (self.leaderboardToString(leaderboard))
    data = self.leaderboardToString(leaderboard)
    return data
    
    
    
    
def playerInfoToString(self, pInfo):
    return str(pInfo.name) +"  :  " + str(pInfo.score)

def leaderboardToString(self, leaderboard):
    returnString = "player  :   score"
    returnString += "*"*10
    for pInfo in leaderboard:
        returnString += "\n" + self.playerInfoToString(pInfo)
    returnString += "\n"+ "*"*10
    return returnString