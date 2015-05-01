from sympy import *
from modsolve import kernelMachine

class rem(kernelMachine):
    
    def __init__(self, kernel):
        '''constructor accepts kernelMachine object'''
        '''REM model object can only be created if kernelMachine model exists and it is trained'''
        self.symbols = kernel.symbols
        self.stimuli = kernel.stimuli
        self.G = kernel.G
        self.model = 'rem'
    
    def bind( self, inexpr):
        '''Compute the value of a generic expression for a rem
        model.'''
        # the way we do this is to create a copy of the input
        # expression, substitute all the gX_Y coefficients with the
        # model values, and then simplify. the result is returned and
        # NOT stored in the model's symbols dictionary.
        s = self.symbols
        model = self.model
        self._make_G() # create model's generalization matrix
        G = s[ 'G' + model ]  # shortcut 
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

    def _make_G(self):
        '''Create a generalization matrix for a given model.'''
        s = self.symbols
        model = self.model
        if 'r' not in s:
            s[ 'r' ] = symbols('r')
        n = self.G.rows
        G = s[ 'G'+model ] = Matrix( n, n, n**2 * [0] )
        for i in range(0, G.rows):
            s[ 'c' ] = symbols('c')
            for j in range(i, G.rows ):
                (si, sj) = str( self.G[i,j] )[ 1: ].split('_')
                G[j,i] = G[i,j] = self._make_g( si, sj)

    def _make_g( self, s1, s2):
        '''Create a single generalization factor for a given model.''' 
        s = self.symbols
        n1 = len( s1 )
        n2 = len( s2 )
        k = len( set(s1) & set(s2) )
        if k == 0:
            return 0
        elif s1 == s2:
            return k
        else:
            m = max( n1, n2 ) - 1
            g = k * ( 1 - s['r'] )**m + (k-1) * s['r']
            #else:
            #    raise Exception('model "' + self.model + '" not known')
        return g.simplify()
