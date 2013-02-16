'''
Created on 16/02/2013

@author: Christian Adriano
'''

class TCPConnector(object):
    '''
    handles all the communication between client and server
    '''
    
    eventName=""

    def __init__(self, selfparams):
        '''
        Constructor
        '''
        
        
    def hasEvent(self):
        ''' TODO implement it by checking the event buffer for event'''
        return False
    
    def getEventName(self):
        return self.eventName;
    
    def getEventType(self):
        ''' TODO implement it by mapping events to numbers 
        0==gameFinished
        1==gameStarted
        2==fuelLevelChanged,
        3==gameScoreChanged
        4==mineGridChanged
        '''
        return 0
    
    def getEventValue(self, eventType):
        ''' TODO implement it by checking the event buffer for the type of event'''
        return 1

    def getEventValueAt(self, eventType, index):
        ''' TODO implement by returning  by checking the buffer for the type of event 
            and a value at the specified position
        '''
        return 1

    