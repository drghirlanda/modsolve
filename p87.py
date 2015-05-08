from sympy import *
from modsolve import kernelMachine

class p87(kernelMachine):
    
    def __init__(self, kernel):
        '''constructor accepts kernelMachine object'''
        '''p87 model object can only be created if kernelMachine model exists and it is trained'''
        self.kernel = kernelMachine()
        self.kernel.train(design)
        self.symbols = self.kernel.symbols
        self.stimuli = self.kernel.stimuli
        self.G = self.kernel.G
        self.model = 'p87'
        
    def bind( self, inexpr):
        '''Compute the value of a generic expression for a particular
        model.

        '''
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

    def _make_G( self):
        '''Create a generalization matrix for p87 model.'''
        s = self.symbols
        model = self.model
        if 'c' not in s:
            s[ 'c' ] = symbols('c')
        n = self.G.rows
        G = s[ 'G'+model ] = Matrix( n, n, n**2 * [0] )
        for i in range(0, G.rows):
            s[ 'c' ] = symbols('c')
            for j in range(i, G.rows ):
                (si, sj) = str( self.G[i,j] )[ 1: ].split('_')
                G[j,i] = G[i,j] = self._make_g( si, sj)

    def _make_g( self, s1, s2):
        '''Create a single generalization factor for p87 model.''' 
        s = self.symbols
        n1 = len( s1 )
        n2 = len( s2 )
        k = len( set(s1) & set(s2) )
        if s1 == s2:
            return 1
        elif (n1==1 and n2==2 or n1==2 and n2==1) and k==1:
            g = 1 / sqrt( 2 - s['c'] )
        elif n1==1 and n2==1:
            g = s['c']
        else:
            Exception( 'model "'+model+'" not implemented for '+str(s1)+' and '+str(s2) )
        g = g**2
        #else:
        #    raise Exception('model "' + model + '" not known')
        return g.simplify()
    
    def V(self, X, p):
        expression = self.kernel.V(X,p)
        self.symbols = self.kernel.symbols
        self.stimuli = self.kernel.stimuli
        self.G = self.kernel.G
        self.bind(expression)