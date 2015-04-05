from abc import *

class model(object):
    '''abstract class for all models'''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def train(self,design):
        '''abstract train function'''
    
    @abstractmethod
    def V(self,assocStrength, phase):
        '''Return the associative strength of X at the end of phase p.'''