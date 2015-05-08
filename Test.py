#module is for testing propose
#not required in program
import design
import modsolve
import rem
import p87
import p94
d = design.design()
d.append({'A':1, 'AB':0})
#kernel = modsolve.kernelMachine()
#kernel.train(d)
rem = rem.rem(d)
rem.V('AB1', 1)
#p87 = p87.p87(kernel)
#p94 = p94.p94(kernel)
print

#p87.bind(kernel.symbols['wA1'])
print
#rem.bind(kernel.symbols['wA1'])
print
#p94.bind(kernel.symbols['wA1'])


