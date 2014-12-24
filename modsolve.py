from sympy import *

init_printing()

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
def r( Z, phase ):
    g = globals()
    if phase == 0:
        return g[ 'R0' ][ Z ]
    myS = g[ 'S' + str(phase) ]
    rZ = r( Z, phase - 1 );
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
        myR0[ s ] = r( myS[s], phase-1 )
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

## define stimuli and associated objects
define_stimuli( ['A', 'B', 'X', 'AB'] )

## phase 1: compound conditioning
calculate_phase( 1, [AB, X], [1, 0] )

## phase 2: revaluation
rA2 = symbols( 'rA2' )
calculate_phase( 2, [A, X], [rA2, 0] )

rev = r( B, 2 ) - r( B, 1 )
rev = rev.subs( [ (gB_X, gA_X), (gB_AB, gA_AB), (gX_X, 0) ] )

