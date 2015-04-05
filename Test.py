#module is for testing propose
#no required in program
import design
import modsolve
d = design.design()
d.append({'A':1, 'AB':0})

print(d.printDesign())
kernel = modsolve.kernelMachine()
print d.allStimuli()
kernel.train(d)

