from sympy import *
from math import copysign
from abstractModel import model
from design import design

# keep in mind these variable naming conventions to navigate the code:
# - X represents a stimulus
# - V represents an associative strength
# - V0 is the initial value of an associative strength
# - w is the weight of a stimulus in the kernel machine
# - postfix 's' stands for plural; e.g., ws is a list of weights 
# - prefix 'i' stands for 'index'; e.g., iXs is a list of stimulus indices
# - the self.symbols dictionary is often aliased to s for brevity

class kernelMachine(model):
    '''A generic associative learning model (kernel machine).'''

    def __init__( self ):
        self.design = design()
        self.symbols = {}    # all symbols for this model
        self.stimuli = []    # all stimuli, in order of addition
        self.info = 1        # 0: no message; 1: messages

    def train( self, design ):
        '''Add a training phase. For example: XVs = {'A':1, 'AB':0} 
        trains a response of 1 to A and of 0 to AB.'''
        s = self.symbols # shortcut
        #self.design.append( dict( XVs ) )
        self._info( "training phases: " + design.printDesign())
        p = design.len() - 1     # this phase
        self._add_stimuli(design.allStimuli())
        ws = []# symbols for stimulus weights
        
        #this for loop creats weight symbols and store them in symbols
        for i in design:
            for X in i:
                wXp = 'w' + str(X) + str(p)   # weight symbol name
                if wXp not in s: 
                    s[ wXp ] = symbols( wXp ) # create symbol
                ws.append( s[ wXp ] )         # append to weights list
        #print ws
        ws = Matrix( ws )# turn list into vector
        iXs = []
        for i in design:
            for X in i:
                iXs.append(self.stimuli.index(X)) # stimulus indices 
        G = self.G[ iXs, iXs ]            # generalization submatrix
        
        
        Vs0 = Matrix([self.V(X, p-1) for i in design for X in i])    # initial Vs
        Vs = Matrix( design.values() )                   # target Vs
        solution = solve( Eq( Vs0 + G * ws, Vs ), ws ) # SOLUTION
        for w in ws:
            self._info( str(w) + " = " + str( solution[w] ) )
            s[ str(w) ] = solution[ w ]   # add ws to symbols
    def V( self, X, p ):
        '''Return the associative strength of X at the end of phase p.'''
        self._add_stimuli( [X] )
        s = self.symbols
        VXp = 'V' + X + str(p)
        if p==0:
            if VXp not in s:
                self._info( 'assuming ' + VXp +' = 0' )
                s[ VXp ] = 0
            return s[ VXp ]
        VX = self.V( X, p-1 )
        iX = self.stimuli.index( X )
        for i in range(0, len(self.stimuli) ):
            w = 'w' + self.stimuli[i] + str(p)
            if w in s:
                VX += s[w] * self.G[i,iX]
        s[ VXp ] = simplify( VX )
        return s[ VXp ]
 	
    def _add_stimuli( self, newXs ):
        '''An internal method to add stimuli to the list of known
        stimuli, and expand the generalization matrix as needed.'''
        Xs = self.stimuli
        for x in newXs:
            if x not in Xs:
                Xs.append( x )
        n = len( Xs )
        self.G = Matrix( n, n, n**2 * [0] )
        for i in range(0, n):
            stri = str( Xs[i] )
            self.G[i,i] = symbols( 'g' + stri + '_' + stri )
            for j in range(i,n):
                self.G[i,j] = symbols( 'g' + stri + '_' + str(Xs[j]) )
                self.G[j,i]= self.G[i,j]

    def _info( self, msg ):
        '''An internal method to print informational messages.'''
        if self.info:
            print msg
