from sympy import *

## define symbolic generalization matrix and associated symbols
def define_g(i,j):
    g = globals()
    (i, j) = sorted( [i, j] )
    gStr = 'g' + g['S'][i] + '_' + g['S'][j]
    if gStr not in g:
        g[ gStr ] = symbols( gStr )
    return g[ gStr ]

def cleanup():
    g = globals()
    if 'S' not in g: return
    if 'R0' not in g: return
    del g[ 'R0' ]
    phase = 1
    while 'R' + str(phase) in g:
        del g[ 'R' + str(phase) ]
        for s in g[ 'S' + str(phase) ]:
            c = 'c' + g['S'][s] + str(phase)
            if c in g: del g[ c ]
        del g[ 'S' + str(phase) ]
    for gf in set( flatten(G) ):
        del g[ str(gf) ]
    del g['G']
    del g['S']

## define stimuli and symbolic generalization matrix 
def define_stimuli( S ):
    g = globals()
    g['S'] = S
    n = len(S)
    for i in range( 0, n ):
        g[ S[i] ] = i
    g[ 'G' ] = Matrix( n, n, define_g )
    g[ 'R0' ] = Matrix( n, 1, n*[0] )

## define response function
def respond( Z, phase ):
    g = globals()
    if phase == 0:
        return g[ 'R0' ][ Z ]
    myS = g[ 'S' + str(phase) ]
    rZ = respond( Z, phase - 1 );
    for i in myS:
        c = 'c' + str( g['S'][i] ) + str(phase)
        rZ += g[ c ] * G[i,Z]
    return rZ.simplify()

def calculate_phase( phase, myS, myR ):
    n = len( myS )
    g = globals()
    g[ 'S' + str(phase) ] = myS
    myR = Matrix( n, 1, myR )
    g[ 'R' + str(phase) ] = myR
    R0 = g[ 'R' + str(phase-1) ]
    myR0 = Matrix( n, 1, n*[0] )
    for s in range(0, n):
        myR0[ s ] = respond( myS[s], phase-1 )
    myG = G[ myS, myS ]
    myC = []
    for s in myS:
        name = g[ 'S' ][s]
        c = 'c' + str(name) + str(phase)
        myC.append( symbols( c ) )
    myC = Matrix( n, 1, myC )
    sol = solve( Eq( myR0 + myG*myC, myR ), myC )
    for c in myC:
        g[ str(c) ] = sol[ c ]
        print( str(c) + ":\t" )
        pretty_print( sol[ c ] )
        print( "" )

## bind a result to a model 
def G_rem():
    g = globals()
    r = symbols('r')
    n = len( g['S'] )
    G = Matrix( n, n, n**2 * [0] )
    for i in range(0,n):
        si = g['S'][ i ]
        ni = len(si)
        G[i,i] = ni
        for j in range(i+1,n):
            sj = g['S'][ j ]
            nj = len(sj)
            k = len( set(si) & set(sj) )
            if k == 0:
                gij= 0
            else:
                m = max( ni, nj ) - 1
                gij = k * (1-r) ** m + (k-1)*r
            G[i,j] = G[j,i] = gij
    return G

## bind a result to a model 
def bind_model( inexpr, G ):
    g = globals()
    n = len( g['S'] )
    outexpr = inexpr
    for i in range(0,n):
        si = g['S'][ i ]
        for j in range(i,n):
            sj = g['S'][ j ]
            outexpr = outexpr.subs( 'g'+si+'_'+sj, G[i,j] )
    return outexpr.simplify()

define_stimuli( ['A', 'B', 'AB'] )

## model generalization factors
rem = G_rem()
c = symbols('c')
pearce94 = Matrix( [ [1, c, 1/sqrt(2-c)],
                  [c, 1, 1/sqrt(2-c)],
                  [1/sqrt(2-c), 1/sqrt(2-c), 1] ] )
pearce87 = Matrix( 3, 3, map( lambda x: x**2, pearce94 ) )

## example: element reversal
(rA1, rA2, rAB2) = symbols('rA1 rA2 rAB2')
calculate_phase( 1, [A], [rA1] )
calculate_phase( 2, [A, AB], [rA2, rAB2] )
rB2 = respond( B, 2 )
fr_rem = bind_model( rB2, rem )
fr_p87 = bind_model( rB2, pearce87 )
fr_p94 = bind_model( rB2, pearce94 )

## example: external inhibition
cleanup()
calculate_phase( 1, [A], [1] )
rB1 = respond( AB, 1 )
ei_rem = bind_model( rB1, rem )
ei_p87 = bind_model( rB1, pearce87 )
ei_p94 = bind_model( rB1, pearce94 )

## example: summation
cleanup()
define_stimuli( ['A', 'B', 'AB'] )
calculate_phase( 1, [A, B], [1, 1] )
rAB1 = respond( AB, 1 )
sm_rem = bind_model( rAB1, rem )
sm_p87 = bind_model( rAB1, pearce87 )
sm_p94 = bind_model( rAB1, pearce94 )

