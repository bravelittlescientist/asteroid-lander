'''
Created on Mar 7, 2013

@author: vaibhavsaini
'''

class LeaderboardEntry():
    '''
    classdocs
    '''


    def __init__(self, player, score):
        '''
        Constructor
        '''
        self.player = player
        self.score = score
    
    def getSelfStateObj(self):
        return vars(self)
    
