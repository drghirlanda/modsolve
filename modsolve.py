from sympy import *
import Design
#from math import copysign
# keep in mind these variable naming conventions to navigate the code:
# - X represents a stimulus
# - V represents an associative strength
# - V0 is the initial value of an associative strength
# - w is the weight of a stimulus in the kernel machine
# - postfix 's' stands for plural; e.g., ws is a list of weights
# - prefix 'i' stands for 'index'; e.g., iXs is a list of stimulus indices
# - the self.symbols dictionary is often aliased to s for brevity
class model:
    '''A generic associative learning model (kernel machine).'''
    def __init__( self ):
        self.design = Design.Design() # phase 0 is empty by default
        self.symbols = {} # all symbols for this model
        self.stimuli = [] # all stimuli, in order of addition
        self.info = 1 # set to 1 to get some messages
        
    def train( self, XVs ):
        '''Add a training phase. For example: XVs = {'A':1, 'AB':0}
         trains a response of 1 to A and of 0 to AB.'''
        s = self.symbols # shortcut
        design = self.design
        design.addDesign( XVs )
        self._info( "training phases: " + design.printDesignList() )
        p = design.numberOfDesigns() - 1 # number of the phase performed
        self._add_stimuli( XVs.keys() )
        ws = [] # symbols for stimulus weights
        for X in XVs:
            wXp = 'w' + str(X) + str(p) # weight symbol name
            if wXp not in s:
                s[ wXp ] = symbols( wXp ) # create symbol
            ws.append( s[ wXp ] ) # append to weights list
        ws = Matrix( ws ) # turn list into vector
        iXs = [ self.stimuli.index(X) for X in XVs ] # stimulus indices
        G = self.G[ iXs, iXs ] # generalization submatrix
        Vs0 = Matrix([self.V(X, p-1) for X in XVs]) # initial Vs
        Vs = Matrix( XVs.values() ) # target Vs
        solution = solve( Eq( Vs0 + G * ws, Vs ), ws ) # SOLUTION!
        print(solution)
        for w in ws:
            self._info( str(w) + " = " + str( solution[w] ) )
            s[ str(w) ] = solution[ w ] # add ws to symbols
        
    def bind( self, inexpr, model ):
        '''Compute the value of a generic expression for a particular
        model.
        '''
        # the way we do this is to create a copy of the input
        # expression, substitute all the gX_Y coefficients with the
        # model values, and then simplify. the result is returned and
        # NOT stored in the model's symbols dictionary.
        s = self.symbols
        self._make_G( model ) # create model's generalization matrix
        G = s[ 'G' + model ] # shortcut
        outexpr = inexpr
        n = len( self.stimuli )
        for i in range(0, n):
            si = self.stimuli[ i ]
            for j in range(i, n):
                sj = self.stimuli[ j ]
        outexpr = outexpr.subs( 'g'+si+'_'+sj, G[i,j] )
        outexpr = outexpr.simplify()
        pretty_print( outexpr )
        return outexpr

    def _make_G( self, model ):
        '''Create a generalization matrix for a given model.'''
        s = self.symbols
        if model == 'rem' and 'r' not in s:
            s[ 'r' ] = symbols('r')
        elif model in ['p87', 'p94'] and 'c' not in s:
            s[ 'c' ] = symbols('c')
        n = self.G.rows
        G = s[ 'G'+model ] = Matrix( n, n, n**2 * [0] )
        for i in range(0, G.rows):
            s[ 'c' ] = symbols('c')
            for j in range(i, G.rows ):
                (si, sj) = str( self.G[i,j] )[ 1: ].split('_')
                G[j,i] = G[i,j] = self._make_g( si, sj, model )
            
    def _make_g( self, s1, s2, model ):
        '''Create a single generalization factor for a given model.'''
        s = self.symbols
        n1 = len( s1 )
        n2 = len( s2 )
        k = len( set(s1) & set(s2) )
        if model == 'rem':
            if k == 0:
                return 0
            elif s1 == s2:
                return k
            else:
                m = max( n1, n2 ) - 1
                g = k * ( 1 - s['r'] )**m + (k-1) * s['r']
        elif model in ['p87', 'p94']:
            if s1 == s2:
                return 1
            elif (n1==1 and n2==2 or n1==2 and n2==1) and k==1:
                g = 1 / sqrt( 2 - s['c'] )
            elif n1==1 and n2==1:
                g = s['c']
            else:
                Exception( 'model "'+model+'" not implemented for '+ str(s1)+' and '+str(s2) )
            if model == 'p87':
                g = g**2
        else:
            raise Exception('model "' + model + '" not known')
        return g.simplify()

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
        self.G = Matrix( n, n, n**2 * [0] ) #create matrix n by n and fill it with 0's

        #don't like this loop. Extra unnessary statements, maybe redundancy
        #futher tracing and testing required
        for i in range(0, n):
            stri = str( Xs[i] ) #redundancy?
            self.G[i,i] = symbols( 'g' + stri + '_' + stri ) #redundancy here?
            for j in range(i,n):
                self.G[i,j] = symbols( 'g' + stri + '_' + str(Xs[j]) )
                self.G[j,i]= self.G[i,j]#?
            
    def _info( self, msg ):
        '''An internal method to print informational messages.'''
        if self.info:
            print msg
