'''
Created on Mar 7, 2013

@author: vaibhavsaini
'''

class Leaderboard():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.entries = []
    def addEntry(self, entry):
        self.entries.append(entry)

    def getSelfStateObj(self):
        return vars(self)
