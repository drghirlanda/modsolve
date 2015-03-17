# Class will represent the design of particular experiment
#the initial state of the design is empy design
class Design:
    
    def __init__(self):
        '''constructor creat empty list of dictionaries for the design class
        new designs will be appended to the list by seperate function'''
        self.designs = [{}]
        
    def addDesign(self, newDesign):
        '''function append new design to the list of already existed designs'''
        self.designs.append(dict(newDesign))
        
    def numberOfDesigns(self):
        '''Function return the number of designs which are currently in the list'''
        return len(self.designs)
    
    # currently doesn't work will be corrected later
    #def delDesign(self,position):
     #   '''Function delete design from the list at specific position'''
      #  self.designs.pop([position])
        
    def printDesign(self,position):
        '''Function print design by given position in the list'''
        return str(self.designs[position])
        
    def printDesignList(self):
        '''Prints list of all designs'''
        return str(self.designs)
        
