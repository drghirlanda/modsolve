import modsolve
from sympy import plot

# feature-positive discrimination
m = modsolve.model()
m.train( {'A':0, 'AB':1} )
VB1 = m.V( 'B', 1 )
VB1rem = m.bind( VB1, 'rem' )
VB1p87 = m.bind( VB1, 'p87' )
VB1p94 = m.bind( VB1, 'p94' )
(r, c) = (m.symbols['r'], m.symbols['c'])
plot( (VB1rem, (r,0,1)), (VB1p87, (c,0,1)), (VB1p94, (c,0,1)) )

# external inhibition
m = modsolve.model()
m.train( {'A':1} )
VAB1 = m.V( 'AB', 1 )
VAB1rem = m.bind( VAB1, 'rem' )
VAB1p87 = m.bind( VAB1, 'p87' )
VAB1p94 = m.bind( VAB1, 'p94' )
(r, c) = (m.symbols['r'], m.symbols['c'])
plot( (VAB1rem, (r,0,1)), (VAB1p87, (c,0,1)), (VAB1p94, (c,0,1)) )

# summation
m = modsolve.model()
m.train( {'A':1, 'B':1} )
VAB1 = m.V( 'AB', 1 )
VAB1rem = m.bind( VAB1, 'rem' )
VAB1p87 = m.bind( VAB1, 'p87' )
VAB1p94 = m.bind( VAB1, 'p94' )
(r, c) = (m.symbols['r'], m.symbols['c'])
plot( (VAB1rem, (r,0,1)), (VAB1p87, (c,0,1)), (VAB1p94, (c,0,1)) )

# compound extinction
m = modsolve.model()
m.train( {'A':1, 'B':1} )
m.train( {'AB':0} )
VA2 = m.V( 'A', 2 )
VA2rem = m.bind( VA2, 'rem' )
VA2p87 = m.bind( VA2, 'p87' )
VA2p94 = m.bind( VA2, 'p94' )
(r, c) = (m.symbols['r'], m.symbols['c'])
plot( (VA2rem, (r,0,1)), (VA2p87, (c,0,1)), (VA2p94, (c,0,1)) )




